from pathlib import Path
import importlib.util,json,sys,struct,datetime
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
spec=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=m.Process(int(sys.argv[1]));diag=int(sys.argv[2],16) if len(sys.argv)>2 else 0x7ff000
raw=p.read(diag,160)
if len(raw)!=160:raise RuntimeError('Game diagnostics unavailable')
words=struct.unpack('<40I',raw)
out={'time':datetime.datetime.now().isoformat(),'stage':words[1],'mode':hex(words[2]),'p1':hex(words[3]),'p2':hex(words[4]),'ids':words[5:7],'params':hex(words[7]),'initializations':words[8],'sim':hex(words[9]),'follow_count':words[10],'ticks':words[11],'p1_position':struct.unpack_from('<2f',raw,48),'p2_position':struct.unpack_from('<2f',raw,56),'keyboard_polls':words[37],'keybuttons':words[35:37]}
params=words[7]
if params:
    out['player_configs']=[{'valid':list(p.read(params+o,1)),'controller_id':p.u32(params+o+0x60),'input_device_id':p.u32(params+o+0x64)} for o in [8,0x78]]
    sim=words[9]
    actors=[]
    for actor in words[3:5]:
        flag=p.u32(actor+0x134);body=p.u32(actor+0x138)
        if flag and p.read(flag,1)!=b'\0' and body:body=p.u32(body+12)
        state=p.u32(body+0x30) if body else None
        charflag=p.u32(actor+0x24);component=actor+0x28
        if charflag and p.read(charflag,1)!=b'\0' and component:component=p.u32(component+0xc8)
        pos=p.read(state+0x70,8) if state else b''
        actors.append({'position':struct.unpack('<2f',pos) if len(pos)==8 else None,'controller':p.u32(component+0xbc) if component else None,'index':p.u32(component+0xc4) if component else None})
    out['actors']=actors
p.close();print(json.dumps(out,indent=2))
