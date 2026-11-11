"""Read-only v16 build identity, lifetime counters, and current player state."""
import json
import struct
import sys
from pose3 import HERE
from build_teleport import Ks,KS_ARCH_X86,KS_MODE_32
sys.path[:0]=[str(HERE.parent/'story-coop-v15-boss-transitions')]
from watch import snapshot
from score_probe import memory

def sample(pid):
    p=memory.Process(pid)
    try:
        ks=Ks(KS_ARCH_X86,KS_MODE_32)
        assert p.read(0x511460,6)==bytes(ks.asm('jmp 0x7fcc00;nop',0x511460)[0])
        assert p.read(0x75ae04,4)==struct.pack('<I',0x7fc900)
        return dict(pid=pid,adapted_draws=p.u32(0x7ffa00),retained_queue_entries=p.u32(0x7ffa04),
            state=snapshot(p))
    finally:p.close()

if __name__=='__main__':
    row=sample(int(sys.argv[1]))
    print(json.dumps(row,indent=2))
    (HERE/f'latest-{sys.argv[1]}.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
