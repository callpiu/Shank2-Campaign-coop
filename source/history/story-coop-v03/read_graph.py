"""Load declarative game graph tables in an isolated Lua runtime after ABI conversion."""
from pathlib import Path
import struct,sys,json
from lupa.lua51 import LuaRuntime,lua_type
def convert(b):
 pos=12;out=bytearray(b[:12]);out[8]=8
 def take(n):
  nonlocal pos
  v=b[pos:pos+n];assert len(v)==n;pos+=n;out.extend(v);return v
 def u():return struct.unpack('<I',take(4))[0]
 def string():
  n=u();del out[-4:];out.extend(struct.pack('<Q',n));take(n)
 def proto():
  string();take(12);take(u()*4)
  for _ in range(u()):
   t=take(1)[0]
   if t==1:take(1)
   elif t==3:take(8)
   elif t==4:string()
   else:assert t==0
  for _ in range(u()):proto()
  take(u()*4)
  for _ in range(u()):string();take(8)
  for _ in range(u()):string()
 proto();assert pos==len(b);return bytes(out)
def plain(v):
 if lua_type(v)=='table':return {str(k):plain(x) for k,x in v.items()}
 return v if lua_type(v) is None else '<'+lua_type(v)+'>'
if __name__=='__main__':
 p=Path(sys.argv[1]);l=LuaRuntime();before=set(l.globals().keys());r=l.execute(convert(p.read_bytes()))
 result={k:plain(l.globals()[k]) for k in set(l.globals().keys())-before}
 if r is not None:result['return']=plain(r)
 dest=Path(sys.argv[2]);dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(list(result))
