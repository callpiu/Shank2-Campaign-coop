from pathlib import Path
import importlib.util,json,sys,struct,time,datetime
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
p=m.Process(int(sys.argv[1]));end=time.monotonic()+360;out=Path(sys.argv[2]);count=0
def string(a):
 cap=p.u32(a+0x18)
 if cap is None:return None
 where=p.u32(a+4) if cap>=16 else a+4
 return p.read(where,100).split(b'\0')[0].decode(errors='replace')
with out.open('w',encoding='utf-8') as f:
 while time.monotonic()<end:
  raw=p.read(0x7ff000,212)
  if len(raw)!=212:break
  w=struct.unpack('<53I',raw);params=w[7]
  row={'time':datetime.datetime.now().isoformat(),'stage':w[1],'recalls':w[10],'steps':w[11],'hud_updates':w[52],'screen':hex(w[50]),'hud2':hex(w[51])}
  if w[50] and w[51]:
   states=[]
   for hud in [w[50]+0x638,w[51]]:
    entry={'wrappers':{}}
    for off in [0,0x30,0x48,0x87c]:
     ptr=p.u32(hud+off+4)
     entry['wrappers'][hex(off)]={'widget':hex(ptr or 0),'visible':list(p.read(ptr+0x31,1)) if ptr else None}
    states.append(entry)
   row['hud_states']=states
  if params:
   row['descriptors']=[{'name':string(params+o+4),'character':string(params+o+0x20),'tail':{hex(x):hex(p.u32(params+o+x) or 0) for x in range(0x3c,0x70,4)}} for o in [8,0x78]]
  f.write(json.dumps(row)+'\n');f.flush();count+=1;time.sleep(.5)
p.close();print(json.dumps({'samples':count,'file':str(out)}))
