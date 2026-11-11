"""Compare the real packet copies and call arguments at the crash."""
import json
import struct
from read_dump import Dump,HERE
d=Dump();report=json.loads((HERE/'dump-analysis.json').read_text())
rows=[];returns=[]
for start,end,offset in d.ranges:
    data=d.data[offset:offset+end-start]
    key=struct.pack('<I',0x759294);pos=data.find(key)
    while pos>=0:
        addr=start+pos
        if d.u32(addr+0x78) in (10005,10010,10075):
            rows.append(dict(address=hex(addr),fields={hex(o):hex(d.u32(addr+o) or 0) for o in (0x70,0x78,0x7c,0x90,0x94,0x98,0x20c,0x210,0x214,0x268)}))
        pos=data.find(key,pos+1)
    if start<=0x19e7bc<end:
        for addr in range(0x19e7bc,end-4,4):
            value=d.u32(addr)
            if value and (0x9b0000<=value<0x9b1000 or 0x7fcc00<=value<0x7fcf00):
                lo=max(addr-16,0x19e7bc);size=min(64,end-lo)
                returns.append(dict(address=hex(addr),value=hex(value),near=[hex(x) for x in struct.unpack('<'+str(size//4)+'I',d.read(lo,size//4*4))]))
out=dict(packets=rows,shim_returns=returns)
(HERE/'dump-packets.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
