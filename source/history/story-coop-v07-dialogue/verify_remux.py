from pathlib import Path
import sys,struct,hashlib,json,subprocess,numpy as np,wave
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE/'tools'))
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
source=HERE.parents[1]/'outputs/Shank2-StoryCoop-v0.5-CHS/patch/payload/data/movies/01_INT_003.bik'
target=HERE/'01_INT_003-strong.bik'
def split(path):
    b=path.read_bytes();assert b[:4]==b'BIKi'
    size,frames=struct.unpack_from('<II',b,4);assert size+8==len(b)
    tracks=struct.unpack_from('<I',b,40)[0];assert tracks==1
    index=struct.unpack_from('<'+'I'*frames,b,44+12*tracks)
    video=[]
    for i,start in enumerate(index):
        start&=~1;end=(index[i+1]&~1) if i+1<frames else len(b)
        cursor=start
        for _ in range(tracks):
            n=struct.unpack_from('<I',b,cursor)[0];cursor+=4+n
        assert cursor<end
        video.append(hashlib.sha256(b[cursor:end]).hexdigest())
    return b,video,[i&1 for i in index]
a,av,ak=split(source);b,bv,bk=split(target)
assert av==bv and ak==bk
assert all(a[o:o+4]==b[o:o+4] for o in [8,20,24,28,32,36])
p=subprocess.run([ff,'-v','error','-i',str(target),'-map','0:a:0','-vn','-ac','2','-ar','48000','-f','f32le','-y',str(HERE/'intro-remixed.f32')],capture_output=True)
assert p.returncode==0,p.stderr
x=np.fromfile(HERE/'intro-remixed.f32',dtype='<f4').reshape(-1,2)
assert np.isfinite(x).all()
with wave.open(str(HERE/'intro-strong-full.wav'),'rb') as w:
    expected=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(float)/32768
# Estimate decoder/remux delay using an interior 8-second window at 12kHz.
start=12*48000;length=8*48000
ea=expected[start:start+length:4].mean(axis=1);eb=x[start:start+length:4].mean(axis=1)
nfft=1<<(len(ea)*2-1).bit_length();corr=np.fft.irfft(np.fft.rfft(eb,nfft)*np.conj(np.fft.rfft(ea,nfft)),nfft)
lags=np.arange(-2400,2401);lag=int(lags[np.argmax(corr[lags%nfft])]);delay=lag*4
assert abs(delay)<=16,delay
assert abs(len(x)-len(expected))<=4096
over=float(np.abs(x).max());assert over<1.0,over
n=min(len(x),len(expected))
snr=float(10*np.log10(np.mean(expected[:n]**2)/np.mean((x[:n]-expected[:n])**2)))
report={'source_sha256':hashlib.sha256(a).hexdigest(),'output_sha256':hashlib.sha256(b).hexdigest(),
        'video_frames_byte_identical':len(av),'keyframe_flags_identical':True,'video_geometry_fps_duration_unchanged':True,
        'source_audio_header':a[44:56].hex(),'output_audio_header':b[44:56].hex(),
        'decoded_sample_peak':over,'clipped_samples':int((np.abs(x)>=1).sum()),'sample_delay':delay,'delay_ms':delay/48,
        'pcm_input_samples':len(expected),'decoded_samples':len(x),'bytes':len(b),'audio_roundtrip_snr_db':snr}
(HERE/'remux-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
