"""Read-only identity/counter evidence after the current anchor adjustment."""
import json
import struct
import sys
from anchor import HERE,routine
from build_teleport import Ks,KS_ARCH_X86,KS_MODE_32
from watch import snapshot
from score_probe import memory

pid=int(sys.argv[1]);record=json.loads((HERE/f'live-{pid}.json').read_text())
p=memory.Process(pid)
try:
    remote=int(record['thunk'],16)
    ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
    assert p.read(0x511460,6)==bytes.fromhex(record['entry'])
    code=routine(asm,remote,metrics=0x7ffa00)
    assert p.read(remote,len(code))==code
    now=[p.u32(0x7ffa00),p.u32(0x7ffa04)]
    assist=json.loads((HERE.parent/f'story-coop-v16-crash-recovery/assist-{pid}.json').read_text())
    counts=struct.unpack('<3I',p.read(int(assist['counters'],16),12))
    result=dict(pid=pid,anchor_hook_exact=True,counters=now,
        counters_since_alignment=[a-b for a,b in zip(now,record['old_counts'])],
        test_assist=dict(player_hits_blocked=counts[0],ordinary_enemy_hits_boosted=counts[1],other_hits_unchanged=counts[2]),
        state=snapshot(p))
    (HERE/f'latest-{pid}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
finally:p.close()
