"""Read-only native replay/render packet inventory for the isolated game."""
import json
import struct
import sys
from investigate import HERE,ROOT
sys.path.insert(0,str(ROOT/'work/story-coop-v10-cyclops'))
from score_probe import memory
sys.path.insert(0,str(ROOT/'work/story-coop-v04'))
from loadout_code import hash_name

p=memory.Process(int(sys.argv[1]))
try:
    players=[]
    for slot in range(2):
        actor=p.u32(0x7ff00c+slot*4);character=actor+0x28;flag=p.u32(actor+0x24)
        if flag and p.read(flag,1)!=b'\0':character=p.u32(character+0xc8)
        players.append(dict(actor=hex(actor),id=p.u32(character+0xac),family=p.u32(character+0xc0)))
    ids={r['id'] for r in players}
    bosses={r['hash']:r['name'] for r in json.loads((HERE/'enemy-whitelist.json').read_text())['enemies'] if r['boss']}
    addresses=p.scan({'packet':struct.pack('<I',0x759294)})['packet']
    known={hash_name(name):name for name in ('corina','shank','boss_magnus','idle','corina_basic','shank_basic','corina_basic_hit','hit_mid1','character')}
    known.update(bosses)
    rows=[]
    for addr in addresses:
        if p.u32(addr+0x78) in ids or p.u32(addr+0x7c) in bosses:
            values={hex(o):p.u32(addr+o) for o in (0x6c,0x70,0x78,0x7c,0x80,0x84,0x88,0x8c,0x90,0x94,0x98,0xa0)}
            rows.append(dict(address=hex(addr),values=values,names={k:known[v] for k,v in values.items() if v in known}))
    out=dict(players=players,packet_count=len(addresses),matching=rows)
    (HERE/'render-snapshot.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(players=players,packet_count=len(addresses),matching=rows[:8]),indent=2))
finally:p.close()
