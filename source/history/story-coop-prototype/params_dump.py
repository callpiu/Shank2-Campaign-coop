from pathlib import Path
import sys,struct
sys.path.insert(0,str(Path('work/pydeps').resolve()))
from lua_chunk import Chunk
from lupa.lua51 import LuaRuntime
root=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
lua=LuaRuntime(encoding=None)
for f in [root/'data/gamemodeparams/normal.lua']:
 lua.execute(Chunk(f.read_bytes()).convert());p=lua.globals()[b'Params']
 def summary(t,dep=0):
  for k,v in t.items():
   print(' '*dep,k, 'TABLE' if hasattr(v,'items') else v)
   if hasattr(v,'items') and dep<1:summary(v,dep+1)
 summary(p)
