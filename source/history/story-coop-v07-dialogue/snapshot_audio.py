from pathlib import Path
import sys,json,importlib.util,hashlib
HERE=Path(__file__).resolve().parent
probe=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('probe',probe);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
meta=json.loads((HERE/'audio-build.json').read_text());data=int(meta['data'],16);p=m.Process(int(sys.argv[1]))
try:
 out={'pid':int(sys.argv[1]),'stage':p.u32(0x7ff004),'enabled':p.u32(data+28),'redirect_attempts':p.u32(data+4),'passthrough_opens':p.u32(data+8),'fallbacks':p.u32(data+24),'last_return_handle':hex(p.u32(data+16) or 0),
      'last_original':p.read(data+64,256).split(b'\0')[0].decode(errors='replace'),'last_redirect':p.read(data+0x500,512).split(b'\0')[0].decode(errors='replace'),
      'movie_attempts':{name:p.u32(data+0x740+i*4) for i,name in enumerate(meta['files'])}}
 if out['last_redirect']:
  path=Path(out['last_redirect']);out['resource_sha256']=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
 print(json.dumps(out,indent=2))
 if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2))
finally:p.close()
