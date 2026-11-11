"""Bounded, read-only cross-level observations; never inject calls or modify game data."""
import argparse
import datetime
import json
from pathlib import Path
import struct
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v10-cyclops'))
from score_probe import inventory, memory

CATALOG=json.loads((HERE.parent/'story-coop-v04/catalog.json').read_text())
SKINS={item['hash']:item['id'] for item in CATALOG['skins']}
WEAPONS={item['hash']:item['id'] for slots in CATALOG['weapons'].values() for items in slots.values() for item in items}


def name(table,value):return table.get(value,f'0x{value:08x}')


def sample(p):
    raw=p.read(0x7ff000,40)
    if len(raw)!=40:return None
    words=struct.unpack('<10I',raw)
    stage,generation,sim=words[1],words[8],words[9]
    result=dict(stage=stage,generation=generation,simulation=f'0x{sim:08x}',players=[])
    if stage!=5:return result
    config=p.read(0x7ff800,128)
    if len(config)!=128 or not sim or not all(words[3:5]) or words[3]==words[4]:return None
    for slot,actor in enumerate(words[3:5]):
        if p.u32(actor+0x20)!=sim:return None
        inv=inventory(p,actor)
        if not inv or p.u32(inv+8)!=actor:return None
        equipment=p.read(inv+0x2c,0x28)
        if len(equipment)!=0x28:return None
        melee,ranged=struct.unpack_from('<2I',equipment)
        throwable,count,score=struct.unpack_from('<3I',equipment,0x1c)
        offset=slot*64
        skin,qmelee,qranged,qthrowable,qcount=struct.unpack_from('<5I',config,offset+20)
        result['players'].append(dict(slot=slot+1,actor=f'0x{actor:08x}',inventory=f'0x{inv:08x}',
            actual_weapons=dict(melee=name(WEAPONS,melee),ranged=name(WEAPONS,ranged),throwable=name(WEAPONS,throwable)),
            throwable_count=count,score=score,
            next_spawn=dict(family=config[offset+4:offset+20].split(b'\0')[0].decode('ascii','replace'),
                skin=name(SKINS,skin),melee=name(WEAPONS,qmelee),ranged=name(WEAPONS,qranged),
                throwable=name(WEAPONS,qthrowable),throwable_count=qcount)))
    # Discard torn snapshots during a retry, teardown or menu callback.
    if p.read(0x7ff000,40)!=raw or p.read(0x7ff800,128)!=config:return None
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pid',type=int);ap.add_argument('--watch',type=Path)
    ap.add_argument('--seconds',type=int,default=1800)
    args=ap.parse_args()
    p=memory.Process(args.pid)
    try:
        # Released build has no Cyclops/godmode scratch state.
        if p.read(0x7ff900,60)!=bytes(60):raise RuntimeError('Expected a clean release process, not a diagnostic build.')
        if not args.watch:print(json.dumps(sample(p),ensure_ascii=False,indent=2));return
        deadline=time.monotonic()+args.seconds
        previous=None
        with args.watch.open('x',encoding='utf-8') as log:
            while time.monotonic()<deadline:
                if not p.read(0x400000,2):break
                row=sample(p)
                if row is not None and row!=previous:
                    previous=row
                    log.write(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(),**row),ensure_ascii=False)+'\n')
                    log.flush()
                time.sleep(.1)
    finally:p.close()


if __name__=='__main__':main()
