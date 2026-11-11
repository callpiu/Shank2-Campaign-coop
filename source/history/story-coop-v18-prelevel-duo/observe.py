"""Read-only UI transaction and actual spawned-character evidence."""
import argparse
import datetime
import json
import struct
import sys
import time
from flow import HERE,DATA
from selector import CATALOG
sys.path[:0]=[str(HERE.parent/'story-coop-v15-boss-transitions')]
from watch import snapshot as actors
from score_probe import memory

def sample(p):
    raw=p.read(DATA,0x40)
    if len(raw)!=0x40:return None
    words=struct.unpack('<16I',raw);screen=words[4]
    row=dict(registered=[hex(x) for x in words[:2]],active_screen=hex(screen),player=words[5]+1,
        refresh=words[6],hold_old_inventory=words[7],generation=words[8],shown=words[9],
        p1_confirmed=words[10],p2_confirmed=words[11],committed=words[12],cancelled=words[13],family_changes=words[14],
        state=actors(p))
    row['role_confirmed']=words[15]
    row['current_step']=('equipment' if words[15] else 'character') if screen else None
    if row['state'] and row['state'].get('stage')==5:
        skins={r['hash']:r['id'] for r in CATALOG}
        for player in row['state'].get('players',[]):
            actor=int(player['actor'],16);descriptor=actor+0x28;flag=p.u32(actor+0x24)
            if flag:
                mode=p.read(flag,1)
                if not mode:return None
                if mode!=b'\0':descriptor=p.u32(descriptor+0xc8)
            if descriptor:
                skin=p.u32(descriptor+0x104)
                player['actual_skin']=skins.get(skin,hex(skin or 0))
                player['actual_family_hash']=p.u32(descriptor+0xc0)
    if screen and p.u32(screen)==0x7532b0:
        row['screen']={name:p.u32(screen+offset) for name,offset in (
            ('category',0x20),('melee',0x1dc),('ranged',0x1e0),('throwable',0x1e4),('skin',0x1e8),('profile',0x1ec))}
    cfg=p.read(0x7ff800,128)
    if len(cfg)==128:
        row['committed_config']=[dict(family=cfg[o+4:o+20].split(b'\0')[0].decode('ascii','replace'),
            skin=struct.unpack_from('<I',cfg,o+20)[0],weapons=list(struct.unpack_from('<3I',cfg,o+24))) for o in (0,64)]
    if p.read(DATA,0x40)!=raw:return None
    return row

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('pid',type=int)
    ap.add_argument('--watch');ap.add_argument('--seconds',type=int,default=1800)
    args=ap.parse_args();p=memory.Process(args.pid)
    try:
        assert p.read(0x7532b8,4)==struct.pack('<I',0x806180)
        if not args.watch:
            row=sample(p);print(json.dumps(row,indent=2))
            (HERE/f'latest-{args.pid}.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
        else:
            end=time.monotonic()+args.seconds;previous=None
            with open(args.watch,'x',encoding='utf-8') as log:
                while time.monotonic()<end and p.read(0x400000,2)==b'MZ':
                    row=sample(p)
                    if row is not None and row!=previous:
                        log.write(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(),**row))+'\n')
                        log.flush();previous=row
                    time.sleep(.1)
    finally:p.close()
