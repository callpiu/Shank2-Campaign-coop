"""Read-only fix counters; distinguish native evidence from user gameplay."""
from pathlib import Path
import sys,json,importlib.util,struct
HERE=Path(__file__).resolve().parent
probe=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
spec=importlib.util.spec_from_file_location('probe',probe);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
meta=json.loads((HERE/'shank2-coop-v09-fixes-test.fixes.json').read_text());d=int(meta['data'],16)
p=m.Process(int(sys.argv[1]))
try:
 out={'pid':int(sys.argv[1]),'stage':p.u32(0x7ff004),'magic':hex(p.u32(d) or 0),'active_cleanup_actor':hex(p.u32(d+4) or 0),'cleanup_scopes':p.u32(d+8),'scoped_singleplayer_checks':p.u32(d+12),'physics_only_recalls':p.u32(d+16),'manual_recalls_total':p.u32(0x7ff028),'players':[]}
 for i in range(2):
  actor=p.u32(0x7ff00c+i*4);out['players'].append({'actor':hex(actor or 0)})
 print(json.dumps(out,indent=2))
 if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2))
finally:p.close()
