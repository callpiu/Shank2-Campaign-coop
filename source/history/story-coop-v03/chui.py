"""Strict reader for the Shank 2 UI definitions observed in the native loader."""
from pathlib import Path
import struct,sys,json

class Reader:
 def __init__(self,data):self.data=data;self.pos=0;self.nodes=[]
 def take(self,n):
  assert 0<=n<=len(self.data)-self.pos,(hex(self.pos),n)
  b=self.data[self.pos:self.pos+n];self.pos+=n;return b
 def u32(self):return struct.unpack('<I',self.take(4))[0]
 def vint(self):
  v=0
  for shift in range(0,35,7):
   x=self.take(1)[0];v|=(x&127)<<shift
   if x<128:return v
  raise ValueError('Invalid varint')
 def string(self):return self.take(self.vint()).decode('utf-8')
 def image(self):
  self.take(1)
  for _ in range(self.u32()):self.string();self.string();self.take(4)
 def font(self):self.take(16);self.string();self.take(4)
 def node(self):
  start=self.pos;t=self.u32();name=self.string();common=self.pos
  fields=self.take(25);kids=[];extra=self.pos
  print('  '*getattr(self,'depth',0),hex(start),t,name) if '--trace' in sys.argv else None
  if t==14:
   count=self.u32();self.depth=getattr(self,'depth',0)+1
   kids=[self.node() for _ in range(count)];self.depth-=1
  elif t in [13,16]:self.string()
  elif t in [8,10]:self.image()
  elif t==4:self.string();self.font()
  elif t==15:self.take(4);self.string()
  elif t==3:
   for _ in range(self.u32()):self.string();self.take(16)
   self.string()
   for _ in range(5):self.string()
  else:raise ValueError(f'Unknown node type {t} {name} at {start:x}, extra at {extra:x}')
  node={'start':start,'end':self.pos,'type':t,'name':name,'common':common,'extra':extra,'children':kids}
  self.nodes.append(node);return node

if __name__=='__main__':
 p=Path(sys.argv[1]);r=Reader(p.read_bytes())
 if len(sys.argv)>2 and not sys.argv[2].startswith('--'):
  r.pos=int(sys.argv[2],16);root=r.node();print(json.dumps(root,indent=2));print('Next',hex(r.pos),r.data[r.pos:r.pos+20].hex())
 else:
  print('VERSION',r.u32());count=r.u32();print('TEMPLATES',count)
  templates=[r.node() for _ in range(count)]
  print('ROOTS at',hex(r.pos));count=r.u32();print('ROOT COUNT',count)
  roots=[r.node() for _ in range(count)]
  print('END',hex(r.pos),'SIZE',hex(len(r.data)))
  assert r.pos==len(r.data)
