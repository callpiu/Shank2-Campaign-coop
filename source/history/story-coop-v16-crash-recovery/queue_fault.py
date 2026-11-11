import json
import struct
from read_dump import Dump,HERE
d=Dump()
result={}
for a,n in ((0x19edb0,32),(0x19f894,0x220),(0x19f29c,32)):
    raw=d.read(a,n)
    result[hex(a)]=[hex(x) for x in struct.unpack('<'+str(len(raw)//4)+'I',raw)]
print(json.dumps(result,indent=2))
