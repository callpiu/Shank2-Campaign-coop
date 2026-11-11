"""Build a conservative native-attribute whitelist for temporary test damage."""
import json
from investigate import GAME,HERE,decode
from build_pose import hash_name

records=[];errors=[]
for p in sorted((GAME/'data/attributes').glob('*.lua')):
    try:a=decode(p.relative_to(GAME).as_posix()).get('Attributes',{})
    except Exception as error:errors.append(dict(file=p.name,error=str(error)));continue
    if a.get('type')!='ai':continue
    tags=a.get('tags',{})
    tags=list(tags.values()) if isinstance(tags,dict) else str(tags).split()
    name=a.get('name',p.stem)
    boss=any('boss' in str(t).lower() for t in tags) or name.lower().startswith('boss_')
    # Hostages, allies and scenery do not qualify as ordinary combat enemies.
    excluded=any(any(term in str(t).lower() for term in ('hostage','friendly','civilian','npc')) for t in tags)
    records.append(dict(name=name,hash=hash_name(name),tags=tags,boss=boss,
                        one_hit=not boss and not excluded and 'lifeform' in tags))
report=dict(enemies=records,errors=errors)
(HERE/'enemy-whitelist.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(ordinary=sum(r['one_hit'] for r in records),bosses=[r['name'] for r in records if r['boss']],errors=errors),indent=2))
