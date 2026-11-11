"""Read-only inventory of the partner's native game-object post effects."""
from pathlib import Path
import importlib.util,struct,json,sys,datetime,argparse
from loadout_code import hash_name
src=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-story-coop\memory_probe.py')
sp=importlib.util.spec_from_file_location('memory_probe',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
ap=argparse.ArgumentParser();ap.add_argument('pid',type=int);ap.add_argument('output',nargs='?',type=Path);ap.add_argument('--player',type=int,choices=[1,2],default=2);args=ap.parse_args()
p=m.Process(args.pid)
try:
    actor=p.u32(0x7ff00c+(args.player-1)*4);assert actor
    char=actor+0x28;flag=p.u32(actor+0x24)
    if flag and p.read(flag,1)!=b'\0':char=p.u32(char+0xc8)
    actorid=p.u32(char+0xac)
    flag=p.u32(actor+0x134);graph=p.u32(actor+0x14c)
    if flag and p.read(flag,1)!=b'\0':graph=p.u32(graph+12)
    handle=p.u32(graph+0x58);assert handle and p.read(handle+0x1c,1)!=b'\0'
    iface=p.u32(handle+0x18);manager=p.u32(iface+0x1c)
    head=p.u32(manager+2*12+4);node=p.u32(head+4);entries=[]
    names=['blue_glow.peg','blue_glow_loop.peg','red_glow.peg','red_glow_loop.peg','redflashloop.peg']
    names={hash_name(n):n for n in names}
    for _ in range(128):
        if not node or node==head:break
        key=p.u32(node+12)
        if key==actorid:
            start,end=struct.unpack('<2I',p.read(node+20,8))
            assert start<=end and (end-start)%16==0 and end-start<=16384
            for at in range(start,end,16):
                age,h,tag,_=struct.unpack('<f3I',p.read(at,16))
                entries.append({'name':names.get(h,hex(h)),'age':age,'tag':hex(tag)})
            break
        node=p.u32(node+(0 if actorid<key else 8))
    else:raise RuntimeError('Native effect tree exceeded traversal limit')
    out={'time':datetime.datetime.now().isoformat(),'actor':hex(actor),'native_id':hex(actorid),'effects':entries}
    text=json.dumps(out,indent=2);print(text)
    if args.output:args.output.write_text(text,encoding='utf-8')
finally:p.close()
