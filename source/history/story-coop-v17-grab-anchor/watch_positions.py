"""Bounded read-only evidence across the pending Slums Boss cinematic."""
import argparse
import datetime
import json
import struct
import time
from anchor import HERE
from watch import snapshot
from score_probe import memory

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pid',type=int);ap.add_argument('--seconds',type=int,default=1800)
    ap.add_argument('--out',required=True)
    args=ap.parse_args();p=memory.Process(args.pid)
    try:
        proof=json.loads((HERE/f'live-{args.pid}.json').read_text())
        assert p.read(0x511460,6)==bytes.fromhex(proof['entry'])
        assert p.read(0x75ae04,4)==struct.pack('<I',0x7fc900)
        end=time.monotonic()+args.seconds;previous=None
        with open(args.out,'x',encoding='utf-8') as out:
            while time.monotonic()<end and p.read(0x400000,2)==b'MZ':
                row=snapshot(p)
                if row is not None and row!=previous:
                    out.write(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(),**row))+'\n')
                    out.flush();previous=row
                time.sleep(.1)
    finally:p.close()
