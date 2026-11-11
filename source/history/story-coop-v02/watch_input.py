from pathlib import Path
import importlib.util,json,sys,struct,time,datetime
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
spec=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=m.Process(int(sys.argv[1]));output=Path(sys.argv[2]);last=None;count=0;end=time.monotonic()+180
with output.open('w',encoding='utf-8') as f:
 while time.monotonic()<end:
  raw=p.read(0x7ff000,184)
  if len(raw)!=184:break
  w=struct.unpack('<46I',raw)
  event={'stage':w[1],'follow_count':w[10],'follow_ticks':w[11],'pads_buttons':w[35:37],'pads_axes':w[38:40],'native_flags':w[40:44],'polls':w[37],'native_calls':w[44:46]}
  if w[1]==5:
   app=p.u32(0x7dcccc);ui=p.u32(app+0x8c) if app else 0
   uv=p.u32(ui) if ui else 0;sv=p.u32(w[9])
   event['meta']={'app':hex(app or 0),'ui':hex(ui or 0),'ui_vtable':hex(uv or 0),'ui_methods':[hex(p.u32(uv+x) or 0) for x in [0x14,0x18]] if uv else [],'sim_vtable':hex(sv or 0),'count_method':hex(p.u32(sv+0x20) or 0) if sv else '','params_mode':p.u32(w[7]+0x164)}
   actors=[]
   for actor in w[3:5]:
    try:
     flag=p.u32(actor+0x134);body=p.u32(actor+0x138)
     if flag and p.read(flag,1)!=b'\0' and body:body=p.u32(body+12)
     state=p.u32(body+0x30) if body else None
     pos=p.read(state+0x70,8) if state else b''
     actors.append([round(x,3) for x in struct.unpack('<2f',pos)] if len(pos)==8 else None)
    except (TypeError,ValueError,struct.error):actors.append(None)
   event['positions']=actors
  signature={k:v for k,v in event.items() if k not in ('polls','native_calls')}
  if signature!=last:
   event['time']=datetime.datetime.now().isoformat();f.write(json.dumps(event)+'\n');f.flush();last=signature;count+=1
  time.sleep(.05)
p.close();print(json.dumps({'events':count,'path':str(output)}))
