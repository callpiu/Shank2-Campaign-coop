"""Read-only input, graph-state and independent inventory sampling."""
from pathlib import Path
import importlib.util,struct,json,sys,time,datetime,argparse
from loadout_code import hash_name
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
ap=argparse.ArgumentParser();ap.add_argument('pid',type=int);ap.add_argument('--watch',type=Path);ap.add_argument('--seconds',type=int,default=240);args=ap.parse_args()
names=json.loads((Path(__file__).parent/'state-names.json').read_text())
catalog=json.loads((Path(__file__).parent/'catalog.json').read_text());weapons={w['hash']:w['id'] for slots in catalog['weapons'].values() for items in slots.values() for w in items}
p=m.Process(args.pid)
def resolve(handle):
    flag=p.u32(handle);value=p.u32(handle+4)
    return p.u32(value+12) if value and flag and p.read(flag,1)!=b'\0' else value
def inventory(actor):
    head=p.u32(actor+0x160);node=p.u32(head+4);key=p.u32(0x7db2d4)
    for _ in range(64):
        if not node or node==head:return None
        val=p.u32(node+12)
        if val==key:return resolve(p.u32(node+16))
        node=p.u32(node+(0 if key<val else 8))
    raise RuntimeError('Extension tree traversal exceeded bound')
def sample():
    out={'time':datetime.datetime.now().isoformat(),'players':[]}
    for i in range(2):
        actor=p.u32(0x7ff00c+i*4)
        if not actor:continue
        flag=p.u32(actor+0x134);graph=p.u32(actor+0x14c)
        if graph and flag and p.read(flag,1)!=b'\0':graph=p.u32(graph+12)
        inv=inventory(actor);state=p.u32(graph+0x34)
        entry={'player':i+1,'actor':hex(actor),'input':hex(p.u32(0x7ff08c+4*i) or 0),'state':names.get(str(state),hex(state or 0)),'substate':p.u32(graph+0x3c),'inventory':hex(inv or 0)}
        if inv:
            entry['weapons']={slot:weapons.get(p.u32(inv+offset),hex(p.u32(inv+offset) or 0)) for slot,offset in [('melee',0x2c),('ranged',0x30),('consumable',0x48)]}
            entry['consumable_count']=p.u32(inv+0x4c)
        out['players'].append(entry)
    return out
try:
    if args.watch:
        deadline=time.monotonic()+args.seconds;previous=None
        with args.watch.open('w',encoding='utf-8') as f:
            while time.monotonic()<deadline:
                row=sample();key=row['players']
                if key!=previous:f.write(json.dumps(row)+'\n');f.flush();previous=key
                time.sleep(.04)
    else:print(json.dumps(sample(),indent=2))
finally:p.close()
