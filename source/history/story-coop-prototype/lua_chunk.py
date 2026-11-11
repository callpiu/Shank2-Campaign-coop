from pathlib import Path
import sys,struct
sys.path.insert(0,str(Path('work/pydeps').resolve()))
from lupa.lua51 import LuaRuntime
class Chunk:
 def __init__(self,b): self.b=b;self.p=12
 def get(self,n): v=self.b[self.p:self.p+n];self.p+=n;return v
 def n(self): return struct.unpack('<I',self.get(4))[0]
 def string(self):
  n=self.n();return struct.pack('<Q',n)+self.get(n)
 def fn(self):
  out=self.string()+self.get(12)
  n=self.n();out+=struct.pack('<I',n)+self.get(n*4)
  n=self.n();out+=struct.pack('<I',n)
  for _ in range(n):
   t=self.get(1);out+=t
   if t==b'\x01':out+=self.get(1)
   elif t==b'\x03':out+=self.get(8)
   elif t==b'\x04':out+=self.string()
   elif t!=b'\x00':raise ValueError(t)
  n=self.n();out+=struct.pack('<I',n)
  for _ in range(n):out+=self.fn()
  n=self.n();out+=struct.pack('<I',n)+self.get(n*4)
  n=self.n();out+=struct.pack('<I',n)
  for _ in range(n):out+=self.string()+self.get(8)
  n=self.n();out+=struct.pack('<I',n)
  for _ in range(n):out+=self.string()
  return out
 def convert(self):
  out=self.b[:8]+b'\x08'+self.b[9:12]+self.fn();assert self.p==len(self.b),(self.p,len(self.b));return out
if __name__=='__main__':
 lua=LuaRuntime(encoding=None)
 for f in sys.argv[1:]:
  b=Path(f).read_bytes();lua.execute(Chunk(b).convert() if b.startswith(b'\x1bLua') else b)
  p=lua.globals()[b'Params']
  print(f)
  for k,v in p.items():
   if not hasattr(v,'items'): print(k,v)
