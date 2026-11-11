import json
import zipfile
from investigate import HERE,GAME,walk
g=json.loads((HERE/'stategraphs-boss_magnus.json').read_text())['StateGraph']
for key in ('69','71','72','73','74'):
    s=g['States'][key]
    print('STATE',key,s['name'],json.dumps({k:v for k,v in s.items() if k in ('on_enter','on_exit','at_time','anim','tags')},indent=1))
for filename in ('boss_magnus_grapple.zip','shank_counter_magnus.zip','boss_militia_grappled.zip','corina_basic_hit.zip'):
    path=GAME/'data-pc/canims'/filename
    if path.exists():
        with zipfile.ZipFile(path) as z:print(filename,[(i.filename,i.file_size) for i in z.infolist()])
