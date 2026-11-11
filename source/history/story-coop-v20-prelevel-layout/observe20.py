import importlib.util
import json
import sys
from flow20 import HERE

path=HERE.parent/'story-coop-v18-prelevel-duo/observe.py'
spec=importlib.util.spec_from_file_location('native_prelevel_observer',path)
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
p=previous.memory.Process(int(sys.argv[1]))
try:
    row=previous.sample(p)
    pointer=p.read(0x7ff400,32).split(b'\0')[0].decode('ascii')
    if row:row['campaign_ui']=pointer
    assert pointer=='campaigncoopv20chs.chui'
    print(json.dumps(row,indent=2))
    (HERE/f'latest-{sys.argv[1]}.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
finally:p.close()
