"""Inspect the actually observed first Boss rather than the earlier Magnus assumption."""
import json
import sys
from read_dump import HERE
sys.path.insert(0,str(HERE.parent/'story-coop-v15-boss-transitions'))
from investigate import decode,walk

for category in ('stategraphs','attributes'):
    obj=decode(f'data/{category}/boss_militia.lua')
    (HERE/f'{category}-boss_militia.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
    if category=='stategraphs':
        g=obj['StateGraph']
        relevant=[]
        for key,s in g['States'].items():
            if any(term in s.get('name','') for term in ('grab','grapple','atk')):
                relevant.append(dict(index=key,data=s))
        (HERE/'militia-grabs.json').write_text(json.dumps(relevant,indent=2)+'\n',encoding='utf-8')
        print('states',[(r['index'],r['data']['name'],r['data'].get('anim')) for r in relevant])
        print('Corina branches',[(p,v) for p,v in walk(g) if any('corina' in str(x).lower() for x in v.values() if isinstance(x,str))])
    else:
        for p,v in walk(obj):
            if v.get('componenttype')=='viz':print('viz sources',v.get('sources'),v.get('noloadsources'))
