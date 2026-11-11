import json
from pathlib import Path
from investigate import walk,HERE

for name in ('boss_magnus','corina','shank'):
    graph=json.loads((HERE/f'stategraphs-{name}.json').read_text())['StateGraph']
    if name=='boss_magnus':
        print('BOSS STATES',[(i,s.get('name')) for i,s in graph['States'].items()])
    matches=[]
    for i,s in graph['States'].items():
        text=json.dumps(s)
        if ('magnus' in text.lower() if name!='boss_magnus' else any(w in s.get('name','').lower() for w in ('grab','grapp','throw'))):
            matches.append(dict(index=i,data=s))
    (HERE/f'{name}-focused.json').write_text(json.dumps(matches,indent=2),encoding='utf-8')
    print(name,'MATCH STATES',[(s['index'],s['data'].get('name')) for s in matches])
    if name=='corina':
        print('VICTIM STATES',[(i,s.get('name')) for i,s in graph['States'].items() if any(w in s.get('name','').lower() for w in ('held','grabbed','grappled','hit_grap','attached'))])
print('done')
