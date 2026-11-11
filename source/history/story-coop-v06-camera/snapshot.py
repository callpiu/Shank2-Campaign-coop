"""Read-only live camera evidence; never moves a player or writes game memory."""
from pathlib import Path
import sys,json,struct,importlib.util
HERE=Path(__file__).resolve().parent
probe=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('probe',probe);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
metadata=json.loads((HERE/'build.json').read_text());data=int(metadata['data'],16)
p=m.Process(int(sys.argv[1]))
def floats(address,n):
 raw=p.read(address,n*4)
 return list(struct.unpack('<'+'f'*n,raw)) if len(raw)==n*4 else None
def ptr(value):return hex(value) if value else None
try:
 result={'pid':int(sys.argv[1]),'stage':p.u32(0x7ff004),'world':ptr(p.u32(0x7ff024)),
         'enabled':p.u32(data+4),'toggles':p.u32(data+12),'fitter_updates':p.u32(data+16),'cameras':{}}
 for i,name in enumerate(['Follow','Rail','Positional']):
  slot=data+0x40+i*0x40
  entry={'updates':p.u32(slot),'object':ptr(p.u32(slot+4)),'sim':ptr(p.u32(slot+8)),
         'native_center_and_zoom':floats(slot+12,3),'final_zoom':floats(slot+24,1),'eligible':p.u32(slot+28)}
  if i<2:
   state=data+0x200+i*0x80
   entry.update(framing_input=floats(state,8),previous_zoom=floats(state+32,1),history_valid=p.u32(state+36),
                output_target_floor=floats(state+40,3))
  result['cameras'][name]=entry
 print(json.dumps(result,indent=2))
 if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(result,indent=2))
finally:p.close()
