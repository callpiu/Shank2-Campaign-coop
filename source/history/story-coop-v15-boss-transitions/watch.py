"""Read-only position/health/graph evidence during the two manual boss regressions."""
import argparse
import datetime
import json
import math
from pathlib import Path
import struct
import sys
import time
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent/'story-coop-v14-transitions'),str(HERE.parent/'story-coop-v10-cyclops')]
from observe import sample as equipment
from score_probe import memory
NAMES=json.loads((HERE.parent/'story-coop-v04/state-names.json').read_text())

def component(p,actor,offset):
    flag=p.u32(actor+0x134);value=p.u32(actor+0x134+offset)
    if not value:return None
    if flag and p.read(flag,1) not in (b'',b'\0'):return p.u32(value+12)
    return value

def number(p,address):
    b=p.read(address,4)
    if len(b)!=4:return None
    n=struct.unpack('<f',b)[0]
    return round(n,3) if math.isfinite(n) else None

def snapshot(p):
    header=p.read(0x7ff000,40)
    row=equipment(p)
    if not row or row['stage']!=5:return row
    for player in row['players']:
        actor=int(player['actor'],16)
        body=component(p,actor,4);state=p.u32(body+0x30) if body else None
        hp=component(p,actor,0x14);graph=component(p,actor,0x18)
        value=p.u32(graph+0x34) if graph else None
        player.update(hp=number(p,hp+0xa0) if hp else None,
                      position=[number(p,state+0x70),number(p,state+0x74)] if state else None,
                      graph_state=NAMES.get(str(value),hex(value or 0)))
    if p.read(0x7ff000,40)!=header:return None
    return row

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('pid',type=int)
    ap.add_argument('--seconds',type=int,default=1800);ap.add_argument('--watch',type=Path)
    args=ap.parse_args();p=memory.Process(args.pid)
    try:
        if not args.watch:print(json.dumps(snapshot(p),indent=2));raise SystemExit
        assert p.read(0x75ae04,4)==struct.pack('<I',0x7fc900)
        assert p.read(0x511460,6)==bytes.fromhex('e99bb72e0090')
        previous=None;end=time.monotonic()+args.seconds
        with args.watch.open('x',encoding='utf-8') as out:
            while time.monotonic()<end and p.read(0x400000,2):
                row=snapshot(p)
                if row is not None and row!=previous:
                    out.write(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(),**row))+'\n');out.flush();previous=row
                time.sleep(.1)
    finally:p.close()
