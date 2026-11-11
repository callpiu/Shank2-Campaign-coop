from pathlib import Path
import importlib.util,json,sys,struct
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
p=m.Process(int(sys.argv[1]));diag=0x7ff000;params=p.u32(diag+28)
def string(a):
 cap=p.u32(a+0x18);where=p.u32(a+4) if cap>=16 else a+4
 return p.read(where,100).split(b'\0')[0].decode(errors='replace')
out={'stage':p.u32(diag+4),'recalls':p.u32(diag+40),'steps':p.u32(diag+44),'screen':hex(p.u32(diag+200) or 0),'p2_hud':hex(p.u32(diag+204) or 0),'hud_updates':p.u32(diag+208)}
if params:
 out['descriptors']=[{'name':string(params+o+4),'character':string(params+o+0x20),'tail':{hex(x):hex(p.u32(params+o+x)) for x in range(0x3c,0x70,4)}} for o in [8,0x78]]
print(json.dumps(out,indent=2));p.close()
