from pathlib import Path
import json,hashlib,numpy as np
from prepare_samples import HERE,RATE,enhance,limit,save,stats
source=np.fromfile(HERE/'intro-original.f32',dtype='<f4').reshape(-1,2).astype(float)
trial=json.loads((HERE/'samples.json').read_text());start=int(trial['start_seconds']*RATE);n=int(trial['duration_seconds']*RATE)
x=source[start:start+n]*10**(trial['common_reference_gain_db']/20)
out=HERE/'samples';report={'voice_band_max_boost_db':7,'duration_seconds':n/RATE,'method':'dynamic mid/side and non-speech-band ducking; not isolated voice/music stems','profiles':{}}
for name,duck in [('reference',0),('background-gentle',4),('background-strong',7)]:
    y=enhance(x,7,background_duck_db=duck);y,limiter=limit(y)
    path=out/('strong.wav' if name=='reference' else name+'.wav')
    if name=='reference':
        # Refactor must preserve the already-approved trial exactly.
        temporary=out/'reference-check.wav';save(temporary,y)
        assert temporary.read_bytes()==path.read_bytes();temporary.unlink()
    else:save(path,y)
    report['profiles'][name]={'maximum_wide_background_duck_db':duck,'mid_outside_band_duck_db':duck*.5,**stats(y),'limiter':limiter,'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(HERE/'background-samples.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
