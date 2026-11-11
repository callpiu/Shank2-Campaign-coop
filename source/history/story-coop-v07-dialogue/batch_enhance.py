"""Resumable development-only movie audio enhancement with video packet proof."""
from pathlib import Path
import sys,subprocess,struct,json,hashlib,wave,argparse,gc
import numpy as np
from prepare_samples import HERE,RATE,enhance,limit,save,stats
sys.path.insert(0,str(HERE/'tools'))
import imageio_ffmpeg
ROOT=HERE.parents[1]
SOURCE=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS/patch/payload/data/movies'
OUT=HERE/'enhanced';AUDIT=HERE/'batch-audit';SCRATCH=HERE/'batch-scratch'
PROFILE={'id':'voice7-background7-v1','voice_band_max_boost_db':7,'wide_background_max_duck_db':7,'mid_outside_band_max_duck_db':3.5,'sample_peak_ceiling':.95,'audio_compression':0,'method':'center-weighted frequency enhancement and dynamic stereo-bed ducking; not isolated stems'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
FF=imageio_ffmpeg.get_ffmpeg_exe();RAD=HERE/'tools/rad-portable/radvideo64.exe'

def packets(path):
    b=path.read_bytes();assert b[:4]==b'BIKi'
    size,frames=struct.unpack_from('<II',b,4);assert size+8==len(b)
    tracks=struct.unpack_from('<I',b,40)[0];assert tracks==1
    rate,flags=struct.unpack_from('<HH',b,48);assert rate==RATE and flags&0x2000
    index=struct.unpack_from('<'+'I'*frames,b,56);hashes=[]
    for i,start in enumerate(index):
        start&=~1;end=(index[i+1]&~1) if i+1<frames else len(b)
        n=struct.unpack_from('<I',b,start)[0];cursor=start+4+n;assert cursor<end
        hashes.append(hashlib.sha256(b[cursor:end]).hexdigest())
    fields={str(o):struct.unpack_from('<I',b,o)[0] for o in [8,20,24,28,32,36]}
    return {'frames':frames,'geometry_timing_flags':fields,'video_packets':hashes,'keyframes':[x&1 for x in index],'audio_format':b[48:56].hex()}

def decode(movie,path):
    p=subprocess.run([FF,'-v','error','-i',str(movie),'-map','0:a:0','-vn','-ac','2','-ar',str(RATE),'-f','f32le','-y',str(path)],capture_output=True,timeout=120)
    assert p.returncode==0,p.stderr.decode(errors='replace')
    x=np.fromfile(path,dtype='<f4').reshape(-1,2);assert len(x)>4096 and np.isfinite(x).all()
    return x

def mux(original,pcm,target):
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    p=subprocess.run([str(RAD),'BinkMix',str(original),str(pcm),str(target),'/SoundCompress0','/TrackID0','/Overwrite','/AutoClose'],startupinfo=startup,creationflags=subprocess.CREATE_NO_WINDOW,capture_output=True,timeout=120)
    assert p.returncode==0 and target.exists(),(p.returncode,p.stdout,p.stderr)

def delay_and_snr(reference,decoded):
    n=min(len(reference),len(decoded));ref=reference[:n];actual=decoded[:n]
    energy=float(np.mean(ref*ref));mse=float(np.mean((ref-actual)**2))
    snr=10*np.log10(energy/max(mse,1e-30)) if energy>1e-15 else None
    block=RATE;strength=[float(np.mean(ref[i:i+block]**2)) for i in range(0,n,block)]
    if max(strength)<1e-14:return None,None
    length=min(8*RATE,n);start=max(0,min(int(np.argmax(strength))*RATE-2*RATE,n-length))
    a=ref[start:start+length:4].mean(axis=1);b=actual[start:start+length:4].mean(axis=1)
    nfft=1<<(len(a)*2-1).bit_length();corr=np.fft.irfft(np.fft.rfft(b,nfft)*np.conj(np.fft.rfft(a,nfft)),nfft)
    lags=np.arange(-2400,2401);lag=int(lags[np.argmax(corr[lags%nfft])])*4
    return lag,float(snr) if snr is not None else None

def one(original):
    target=OUT/original.name;audit=AUDIT/(original.stem+'.json');source_hash=sha(original)
    if audit.exists() and target.exists():
        old=json.loads(audit.read_text())
        if old['profile']==PROFILE and old['input_sha256']==source_hash and old['output_sha256']==sha(target):return old
    original_info=packets(original)
    raw_path=SCRATCH/'source.f32';decoded_path=SCRATCH/'result.f32';pcm=SCRATCH/'processed.wav'
    x=decode(original,raw_path).astype(np.float64)
    if original.name=='01_INT_003.bik':
        gain_db=json.loads((HERE/'samples.json').read_text())['common_reference_gain_db'];gain=10**(gain_db/20)
    else:
        gain=.95/max(1,float(np.abs(x).max()));gain_db=float(20*np.log10(gain))
    y=enhance(x*gain,7,background_duck_db=7);y,limiter=limit(y);del x;gc.collect()
    backoff=1.;attempts=0
    for attempts in range(3):
        save(pcm,y*backoff);mux(original,pcm,target);decoded=decode(target,decoded_path)
        peak=float(np.abs(decoded).max())
        if peak<.995:break
        backoff*=.97/peak
    else:raise AssertionError(('Encoded peak remained too high',original.name,peak))
    result_info=packets(target)
    assert original_info==result_info,('Video or format changed',original.name)
    with wave.open(str(pcm),'rb') as w:expected=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(float)/32768
    assert abs(len(decoded)-len(expected))<=4096
    delay,snr=delay_and_snr(expected,decoded)
    assert delay is None or abs(delay)<=16,(original.name,'delay',delay)
    assert snr is None or snr>20,(original.name,'SNR',snr)
    result={'file':original.name,'profile':PROFILE,'input_sha256':source_hash,'output_sha256':sha(target),'bytes':target.stat().st_size,
            'video_frames_byte_identical':original_info['frames'],'keyframes_and_video_format_unchanged':True,'audio_header_unchanged':True,
            'seconds':len(expected)/RATE,'samples_before_encode':len(expected),'decoded_samples':len(decoded),'sample_delay':delay,
            'audio_roundtrip_snr_db':snr,'decoded_sample_peak':peak,'clipped_samples':int((np.abs(decoded)>=1).sum()),
            'reference_gain_db':gain_db,'codec_backoff_db':float(20*np.log10(backoff)),'mux_attempts':attempts+1,'limiter':limiter}
    audit.write_text(json.dumps(result,indent=2));return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int);args=ap.parse_args()
    for p in [OUT,AUDIT,SCRATCH]:p.mkdir(exist_ok=True)
    files=sorted(SOURCE.glob('*.bik'),key=lambda p:(p.name!='01_INT_003.bik',p.name))
    if args.limit:files=files[:args.limit]
    rows=[]
    for i,source in enumerate(files):
        r=one(source);rows.append(r)
        print(json.dumps({'done':i+1,'total':len(files),'file':source.name,'peak':r['decoded_sample_peak'],'sample_delay':r['sample_delay'],'identical_video_frames':r['video_frames_byte_identical']}),flush=True)
        (HERE/'enhanced-manifest.json').write_text(json.dumps({'profile':PROFILE,'files':rows,'complete':len(rows)==27},indent=2))
    print(json.dumps({'completed':len(rows),'movie_count':len(files),'video_frames_preserved':sum(r['video_frames_byte_identical'] for r in rows),'seconds':sum(r['seconds'] for r in rows),'all_clipped_samples':sum(r['clipped_samples'] for r in rows)}),flush=True)

if __name__=='__main__':main()
