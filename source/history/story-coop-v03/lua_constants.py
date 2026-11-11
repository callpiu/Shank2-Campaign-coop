"""Read Lua 5.1 constant tables without running the bytecode."""
from pathlib import Path
import struct,sys,json
def read(path):
 b=path.read_bytes();pos=12;found=[]
 assert b[:6]==b'\x1bLua\x51\x00' and b[6:12]==bytes([1,4,4,4,8,0])
 def take(n):
  nonlocal pos
  v=b[pos:pos+n];assert len(v)==n;pos+=n;return v
 def u():return struct.unpack('<I',take(4))[0]
 def string():
  n=u();return take(n)[:-1].decode('utf-8','replace') if n else ''
 def proto():
  start=pos;source=string();take(12);take(u()*4);vals=[]
  for _ in range(u()):
   t=take(1)[0]
   if t==0:v=None
   elif t==1:v=take(1)[0]!=0
   elif t==3:v=struct.unpack('<d',take(8))[0]
   elif t==4:v=string()
   else:raise ValueError(t)
   vals.append(v)
  found.append({'start':start,'constants':vals})
  for _ in range(u()):proto()
  take(u()*4)
  for _ in range(u()):string();take(8)
  for _ in range(u()):string()
 proto();assert pos==len(b)
 return found
if __name__=='__main__':
 for path in map(Path,sys.argv[1:]):
  rows=read(path)
  for r in rows:
   hits=[(i,v) for i,v in enumerate(r['constants']) if isinstance(v,str) and any(s in v.lower() for s in ['death','dark','desatur','dead']) or isinstance(v,(float,int)) and v in [0x4025dbd3,0xce59bf24]]
   if hits:
    print(path.name,'function',r['start'],'hits',hits)
    for i,v in hits:print('near',r['constants'][max(0,i-5):i+6])
