from pathlib import Path
import re
import zipfile
from investigate import GAME,HERE,walk
import json

for name in ('boss_grappler_attacks_corina.zip','boss_grappler_attacks.zip','boss_magnus_grapple.zip','shank_counter_magnus.zip','corina_build.zip','shank_build_new.zip'):
    path=GAME/'data-pc/canims'/name
    if not path.exists():continue
    with zipfile.ZipFile(path) as z:
        print(name,[(i.filename,i.file_size) for i in z.infolist()])
        for member in z.namelist():
            if member.endswith(('.bin','.xml','.canim')):
                data=z.read(member)
                strings=re.findall(rb'[\x20-\x7e]{4,90}',data)
                print(member,data[:48].hex(),[x.decode() for x in strings[:35]])
g=json.loads((HERE/'stategraphs-boss_magnus.json').read_text())['StateGraph']
for p,v in walk(g):
    if v.get('Type') and any(s in v['Type'].lower() for s in ('anim','grapple','attach')):
        if v.get('Type') not in ('spawnAR','hitgrapplepartner'):print(p,json.dumps(v)[:600])
