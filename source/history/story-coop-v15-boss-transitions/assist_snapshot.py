"""Inspect only the temporary assist's own counters and current player state."""
import json
import struct
import sys
from watch import HERE,memory,snapshot
pid=int(sys.argv[1]);report=json.loads((HERE/f'assist-{pid}.json').read_text())
p=memory.Process(pid)
try:
    raw=p.read(int(report['counters'],16),12)
    assert len(raw)==12
    counts=struct.unpack('<3I',raw)
    row=dict(pid=pid,prevented_player_damage=counts[0],boosted_ordinary_enemy_hits=counts[1],
             other_receiver_hits_native_damage=counts[2],current=snapshot(p))
    (HERE/f'assist-observed-{pid}.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(row,indent=2))
finally:p.close()
