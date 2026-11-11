"""Decode original declarative graphs and capture relevant boss transitions."""
from pathlib import Path
import json
import re
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
GAME=ROOT/'work/story-coop-v14-transitions/game'
sys.path[:0]=[str(ROOT/'work/story-coop-v04'),r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps']
from read_graph import convert,plain,LuaRuntime

def decode(relative):
    b=(GAME/relative).read_bytes()
    lua=LuaRuntime(encoding='latin1');before=set(lua.globals().keys())
    value=lua.execute(convert(b) if b.startswith(b'\x1bLua') else b)
    result={k:plain(lua.globals()[k]) for k in set(lua.globals().keys())-before}
    if value is not None:result['return']=plain(value)
    return result

def walk(value,path=''):
    if isinstance(value,dict):
        yield path,value
        for key,child in value.items():yield from walk(child,path+'/'+str(key))

if __name__=='__main__':
    for category,names in [('stategraphs',('corina','shank','boss_magnus')),('attributes',('corina','shank','boss_magnus'))]:
        for name in names:
            result=decode(f'data/{category}/{name}.lua')
            (HERE/f'{category}-{name}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            if category=='stategraphs':
                found=[dict(path=p,data=v) for p,v in walk(result) if isinstance(v.get('name'),str) and re.search('magnus|grapple|grab_boss|hold',v['name'],re.I)]
                (HERE/f'{name}-grab-states.json').write_text(json.dumps(found,indent=2),encoding='utf-8')
                print(name,[(x['path'],x['data']['name']) for x in found if 'magnus' in x['data']['name'] or 'boss_grab' in x['data']['name']])
            else:
                for p,v in walk(result):
                    if v.get('componenttype')=='viz':print(name,'viz',v.get('sources'),v.get('noloadsources'))
    result=decode('data-pc/levels/shank2_campaign_slums/shank2_campaign_slums.lua')
    found=[dict(path=p,data=v) for p,v in walk(result) if v.get('TriggerName')=='Teleport To Boss']
    (HERE/'slums-teleport-trigger.json').write_text(json.dumps(found,indent=2),encoding='utf-8')
