"""Offline center-band dialogue trials; immutable movie sources, no game writes."""
from pathlib import Path
import numpy as np,json,wave,hashlib
HERE=Path(__file__).resolve().parent
RATE=48000

def enhance(samples,boost_db=4.,rate=RATE,background_duck_db=0.):
    x=np.asarray(samples,dtype=np.float64)
    mid=(x[:,0]+x[:,1])*.5;side=(x[:,0]-x[:,1])*.5
    size=2048;hop=512;window=np.sqrt(np.hanning(size));pad=size
    def spectrum(signal):
        framed=np.lib.stride_tricks.sliding_window_view(np.pad(signal,(pad,pad),mode='reflect'),size)[::hop]
        return np.fft.rfft(framed*window,axis=1)
    m=spectrum(mid);s=spectrum(side);freq=np.fft.rfftfreq(size,1/rate)
    band=np.zeros_like(freq)
    lo=(freq>=120)&(freq<220);band[lo]=.5-.5*np.cos(np.pi*(freq[lo]-120)/100)
    band[(freq>=220)&(freq<=4300)]=1
    hi=(freq>4300)&(freq<6000);band[hi]=.5+.5*np.cos(np.pi*(freq[hi]-4300)/1700)
    energy_mid=(np.abs(m)**2*band).sum(axis=1)
    energy_side=(np.abs(s)**2*band).sum(axis=1)
    confidence=np.clip((energy_mid/(energy_mid+energy_side+1e-20)-.5)/.4,0,1)
    # Smooth a frame-level weight rather than bin-wise phase-sensitive masks.
    alpha=hop/(rate*.08)
    for i in range(1,len(confidence)):confidence[i]=alpha*confidence[i]+(1-alpha)*confidence[i-1]
    for i in range(len(confidence)-2,-1,-1):confidence[i]=alpha*confidence[i]+(1-alpha)*confidence[i+1]
    gain=1+(10**(boost_db/20)-1)*confidence[:,None]*band[None,:]
    if background_duck_db:
        # Single-track approximation: retain speech-band mid enhancement,
        # gently duck out-of-band mid, and duck the wide stereo bed more.
        other_gain=10**(-background_duck_db*.5/20)
        gain+=(other_gain-1)*confidence[:,None]*(1-band[None,:])
    def reconstruct(spec):
        frames=np.fft.irfft(spec,n=size,axis=1)*window
        acc=np.zeros((len(frames)-1)*hop+size);denom=np.zeros_like(acc)
        for i,frame in enumerate(frames):
            start=i*hop;acc[start:start+size]+=frame;denom[start:start+size]+=window*window
        return (acc/np.maximum(denom,1e-20))[pad:pad+len(mid)]
    enhanced_mid=reconstruct(m*gain)
    if background_duck_db:
        side_gain=1+(10**(-background_duck_db/20)-1)*confidence[:,None]
        side=reconstruct(s*side_gain)
    return np.column_stack((enhanced_mid+side,enhanced_mid-side))

def limit(samples,rate=RATE,ceiling=.95):
    x=np.asarray(samples,dtype=np.float64);block=240
    padded=np.pad(np.max(np.abs(x),axis=1),(0,(-len(x))%block))
    peak=padded.reshape(-1,block).max(axis=1)
    raw=np.minimum(1,ceiling/np.maximum(peak,1e-20))
    future=np.minimum(raw,np.r_[raw[1:],raw[-1]])
    gain=future.copy();release=1-np.exp(-block/(rate*.18))
    for i in range(1,len(gain)):gain[i]=min(future[i],gain[i-1]+release*(1-gain[i-1]))
    # Lookahead keeps both interpolation endpoints under the current block cap.
    envelope=np.interp(np.arange(len(x)),np.r_[0,(np.arange(len(gain))+1)*block],np.r_[gain[0],gain])
    out=x*envelope[:,None]
    assert np.max(np.abs(out))<=ceiling+1e-10
    return out,{'minimum_gain_db':float(20*np.log10(max(float(gain.min()),1e-20))),'limited_blocks':int((gain<.99999).sum())}

def stats(x):
    peak=float(np.max(np.abs(x)));rms=float(np.sqrt(np.mean(x*x)))
    return {'peak_dbfs':float(20*np.log10(max(peak,1e-20))),'rms_dbfs':float(20*np.log10(max(rms,1e-20))),'sample_peak':peak}

def save(path,samples):
    assert np.isfinite(samples).all() and np.max(np.abs(samples))<1
    pcm=np.rint(samples*32767).astype('<i2')
    with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(pcm.tobytes())
    with wave.open(str(path),'rb') as w:assert w.getnframes()==len(samples) and w.getframerate()==RATE

def main():
    raw=np.fromfile(HERE/'intro-original.f32',dtype='<f4').reshape(-1,2).astype(np.float64)
    start=12.;seconds=16.;x=raw[int(start*RATE):int((start+seconds)*RATE)]
    common_gain=.95/max(1,float(np.abs(x).max()));x*=common_gain
    samples=HERE/'samples';samples.mkdir(exist_ok=True)
    report={'source_movie':'01_INT_003.bik','source_audio':'one mixed stereo 48kHz Bink DCT track','start_seconds':start,'duration_seconds':seconds,'common_reference_gain_db':float(20*np.log10(common_gain)),'method':'center-weighted speech-band boost; not isolated voice stems','profiles':{}}
    for name,db in [('original',0),('gentle',4),('strong',7)]:
        y=x.copy() if db==0 else enhance(x,db)
        y,limiter=limit(y);path=samples/(name+'.wav');save(path,y)
        report['profiles'][name]={'requested_mid_band_gain_db':db,**stats(y),'limiter':limiter,'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (HERE/'samples.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':main()
