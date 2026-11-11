"""Read-only player/HUD samples; never changes game memory."""
from pathlib import Path
import importlib.util,json,sys,struct,time,datetime,argparse
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
ap=argparse.ArgumentParser();ap.add_argument('pid',type=int);ap.add_argument('--watch',type=Path);ap.add_argument('--seconds',type=int,default=180);a=ap.parse_args()
p=m.Process(a.pid)
def f32(addr):
 b=p.read(addr,4);return round(struct.unpack('<f',b)[0],5) if len(b)==4 else None
def component(actor,off):
 flag=p.u32(actor+0x134);ptr=p.u32(actor+0x134+off)
 return p.u32(ptr+12) if ptr and flag and p.read(flag,1)!=b'\0' else ptr
def sample():
 d=0x7ff000;screen=p.u32(d+200);hud2=p.u32(d+204)
 if screen is None:return None
 out={'time':datetime.datetime.now().isoformat(),'stage':p.u32(d+4),'recalls':p.u32(d+40),'preload_count':p.u32(d+212),'players':[]}
 out['death_probe']={'gameover_calls':p.u32(d+220),'desired_result':p.u32(d+224),'caller':hex(p.u32(d+232) or 0),'sim_result':p.u32(d+240),'isolated_death_actions':p.u32(d+244),'screen_state':hex(p.u32(screen+0x11a0) or 0) if screen else None}
 out['partner_multiplayer_graph_checks']=p.u32(d+248)
 out['partner_context_checks']=p.u32(d+252)
 out['suppressed_living_tints']=p.u32(d+256)
 out['primary_down_checks']=p.u32(d+260)
 out['primary_down_partner_alive']=p.u32(d+264)
 out['both_players_down']=p.u32(d+268)
 for i in range(2):
  actor=p.u32(d+12+4*i);hud=screen+0x638 if i==0 and screen else hud2
  entry={'actor':hex(actor or 0),'hud':hex(hud or 0)}
  if actor:
   health=component(actor,0x14) # writable component contains current HP
   body=component(actor,4);state=p.u32(body+0x30) if body else 0
   entry.update(health_component=hex(health or 0),hp=f32(health+0xa0) if health else None,position=[f32(state+0x70),f32(state+0x74)] if state else None)
  if hud:
   progress=p.u32(hud+0x60)
   entry['bar_percent']=f32(progress+0xe4) if progress else None
   entry['grenade_slots']=[{'visible':list(p.read((p.u32(hud+0x30+0x6c+n*0x1c+4) or 0)+0x31,1))} for n in range(5)]
  out['players'].append(entry)
 return out
try:
 if a.watch:
  end=time.monotonic()+a.seconds
  with a.watch.open('w',encoding='utf-8') as f:
   while time.monotonic()<end:
    row=sample()
    if row is None:break
    f.write(json.dumps(row)+'\n');f.flush();time.sleep(.25)
 else:print(json.dumps(sample(),indent=2))
finally:p.close()
