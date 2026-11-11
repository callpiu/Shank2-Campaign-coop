from pathlib import Path
import json,numpy as np
from prepare_samples import HERE,RATE,enhance,limit,save,stats
raw=np.fromfile(HERE/'intro-original.f32',dtype='<f4').reshape(-1,2).astype(np.float64)
trial=json.loads((HERE/'samples.json').read_text())
gain=10**(trial['common_reference_gain_db']/20)
processed=enhance(raw*gain,7)
processed,limiter=limit(processed)
save(HERE/'intro-strong-full.wav',processed)
(HERE/'full-intro-processing.json').write_text(json.dumps({'samples':len(raw),'sample_rate':RATE,'seconds':len(raw)/RATE,'profile_db':7,'reference_gain_db':trial['common_reference_gain_db'],'processing':stats(processed),'limiter':limiter,'source_unchanged':True},indent=2))
print(json.dumps({'seconds':len(raw)/RATE,'profile':'user-selected strong','output':'intro-strong-full.wav','stats':stats(processed)}))
