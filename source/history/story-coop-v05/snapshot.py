"""Read-only v0.5 runtime evidence, including live equipment and menu maps."""
from pathlib import Path
import sys,importlib.util,struct,json
HERE=Path(__file__).resolve().parent
probe=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('probe',probe);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
p=m.Process(int(sys.argv[1]))
try:
 # The packaged build appends features before CHS, while early prototypes
 # appended them after CHS. Derive the data VA from the installed Step hook.
 step=p.u32(0x750188);d=step-0x800+0x1000
 assert d in (0x802000,0x803000),hex(d)
 out={'pid':int(sys.argv[1]),'data':hex(d),'stage':p.u32(0x7ff004),'initializations':p.u32(0x7ff020),
      'config':p.read(0x7ff800,128).hex(),'terrain_recalls':[p.u32(d+16),p.u32(d+20)],
      'menu':{hex(o):p.u32(d+o) for o in [0x100,0x104,0x108,0x110,0x114,0x118,0x140,0x148,0x14c,0x150,0x154,0x160,0x164,0x168,0x16c,0x170]},
      'weapon_maps':{name: list(struct.unpack('<16I',p.read(d+offset,64))) for name,offset in [('melee',0x400),('ranged',0x440),('consumable',0x480)]}}
 print(json.dumps(out,indent=2))
 if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2))
finally:p.close()
