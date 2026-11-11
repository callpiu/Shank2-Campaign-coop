from pathlib import Path
import sys,json,importlib.util,hashlib
HERE=Path(__file__).resolve().parent
probe=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('probe',probe);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
build=json.loads((HERE/'preview-build.json').read_text());data=int(build['data'],16)
p=m.Process(int(sys.argv[1]))
try:
 out={'pid':int(sys.argv[1]),'stage':p.u32(0x7ff004),'matched_intro_opens':p.u32(data+4),'other_movie_opens':p.u32(data+8),
      'last_open_returned_handle':hex(p.u32(data+16) or 0),'last_original_filename':p.read(data+64,256).split(b'\0')[0].decode(errors='replace'),
      'redirect_filename':p.read(data+0x200,512).split(b'\0')[0].decode(errors='replace')}
 path=Path(build['new_resource_path']);out['preview_resource_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
 print(json.dumps(out,indent=2))
 if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2))
finally:p.close()
