from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads((HERE/p).read_text(encoding='utf-8-sig'))
a=load('before-retry-final.json');b=load('after-retry-final.json')
old=load('before-retry-weapons.json')['players'];new=load('after-retry-weapons.json')['players']
assert a['pid']==b['pid'] and b['initializations']>a['initializations']
players=[]
for x,y in zip(old,new):
    assert x['player']==y['player'] and x['weapons']==y['weapons']
    assert x['actor']!=y['actor']
    players.append({'player':x['player'],'new_actor':True,'weapons_retained':True,'weapons':y['weapons']})
result={'same_process':True,'initializations_before':a['initializations'],'initializations_after':b['initializations'],'players':players,'scope':'both-down retry, not a natural transition into another story level'}
(HERE/'retry-comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
