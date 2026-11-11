import numpy as np,json
from pathlib import Path
from prepare_samples import enhance,limit,RATE
rng=np.random.default_rng(7);n=RATE*2;t=np.arange(n)/RATE;checks=[]
x=rng.normal(0,.02,(n,2))
y=enhance(x,0);assert np.max(np.abs(x-y))<1e-10;checks.append('zero boost preserves stereo phase and timing')
s=.1*np.sin(2*np.pi*1000*t);x=np.column_stack((s,-s))
y=enhance(x,7);assert np.max(np.abs(x-y))<1e-10;checks.append('side-only content preserved before limiter')
x=np.column_stack((s,s));y=enhance(x,4)
gain=20*np.log10(np.sqrt(np.mean(y[4096:-4096]**2))/np.sqrt(np.mean(x[4096:-4096]**2)))
assert 3.8<gain<4.1;checks.append('center 1kHz signal receives intended mild gain')
low=.1*np.sin(2*np.pi*50*t);x=np.column_stack((low,low));y=enhance(x,7)
gain=20*np.log10(np.sqrt(np.mean(y[4096:-4096]**2))/np.sqrt(np.mean(x[4096:-4096]**2)))
assert abs(gain)<.01;checks.append('low bass is not broadly amplified')
x=np.zeros((n,2));assert np.array_equal(enhance(x,7),x);checks.append('silence stays silent')
x=rng.normal(0,.4,(n,2));x[n//2,0]=3.;y,report=limit(x)
assert y.shape==x.shape and np.abs(y).max()<=.95000001 and np.isfinite(y).all();checks.append('transients limited without overflow or duration change')
voice=.1*np.sin(2*np.pi*1000*t);bed=.05*np.sin(2*np.pi*50*t)
x=np.column_stack((voice+bed,voice-bed));y=enhance(x,7,background_duck_db=7)
region=slice(4096,-4096)
mid=(y[:,0]+y[:,1])*.5;side=(y[:,0]-y[:,1])*.5
voice_gain=20*np.log10(np.sqrt(np.mean(mid[region]**2))/np.sqrt(np.mean(voice[region]**2)))
bed_gain=20*np.log10(np.sqrt(np.mean(side[region]**2))/np.sqrt(np.mean(bed[region]**2)))
assert 6.8<voice_gain<7.1 and -7.1<bed_gain<-6.8
checks.append('center speech boosts while a stereo background bed drops')
x=np.column_stack((bed,-bed));y=enhance(x,7,background_duck_db=7)
assert np.max(np.abs(x-y))<1e-10;checks.append('pure stereo bed with no center speech is not constantly ducked')
report={'checks':checks,'passed':len(checks)}
Path(__file__).with_name('processing-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
