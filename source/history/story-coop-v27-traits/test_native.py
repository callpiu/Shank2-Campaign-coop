"""Execute the generated x86 scope gates, spawn wrapper, and native tag replay."""
import json
from pathlib import Path
import os
import struct
import subprocess
import tempfile
from build_traits import HERE, Ks, KS_ARCH_X86, KS_MODE_32, routines

base=0x20000000
c=base
d=base+0x2000
diag=base+0x2600
actor1=base+0x2800
actor2=base+0x2880
sim=base+0x2900
hp=base+0x2a00
weapon1=base+0x2c00
weapon2=base+0x2c40
weapon3=base+0x2c80
x=base+0x1000
ks=Ks(KS_ARCH_X86,KS_MODE_32)
fixture=bytearray(0x4000)
def asm(a,s):
    b=bytes(ks.asm(s,a)[0])
    fixture[a-base:a-base+len(b)]=b
def write(a,kind,*items):struct.pack_into(kind,fixture,a-base,*items)
addrs=dict(diag=diag,max_hp=x+0x500,fill=x+0x540,combat=x+0x580,appearance=x+0x5c0,
           health_yes=x+0x410,health_no=x+0x430,attack_yes=x+0x410,attack_no=x+0x430,
           tag_continue=x+0x450)
blocks=routines(c,d,**addrs)
for a,blob in blocks.values():fixture[a-base:a-base+len(blob)]=blob
write(d+4,'<I',1)
write(diag+4,'<I',5)
write(diag+12,'<2I',actor1,actor2)
write(diag+36,'<I',sim)
for p in (actor1,actor2):write(p+0x20,'<I',sim)
for weapon,actor in ((weapon1,actor1),(weapon2,actor2),(weapon3,actor2)):
    write(weapon+8,'<I',actor)
write(x+0x600,'<If',0x214eea,1.5)

# Copy the native stack shape at the branch and test the result and callee-saved regs.
for ofs,p,native,gate in [(0,actor1,0,'health_gate'),(0x40,actor2,0,'attack_gate'),
                         (0x80,actor2,1,'attack_gate'),(0xc0,0,0,'attack_gate')]:
    asm(x+ofs,f'''push {p};call {x+ofs+0x18};add esp,4;ret
                  nop;nop;nop;nop;nop;nop;nop;nop;nop;nop;nop;nop
                  push ebp;mov ebp,esp;push esi;mov eax,{native};jmp {blocks[gate][0]}''')
    # The synthetic caller must jump to the beginning of the inner frame.
    asm(x+ofs+0x18,f'push ebp;mov ebp,esp;push esi;mov eax,{native};jmp {blocks[gate][0]}')
for ofs,p in [(0x300,weapon1),(0x340,weapon2),(0x380,weapon3)]:
    asm(x+ofs,f'''push {p};call {x+ofs+0x18};add esp,4;ret
                  nop;nop;nop;nop;nop;nop;nop;nop;nop;nop;nop;nop
                  push ebp;mov ebp,esp;push esi;mov eax,0;jmp {blocks["attack_gate"][0]}''')
    asm(x+ofs+0x18,f'push ebp;mov ebp,esp;push esi;mov eax,0;jmp {blocks["attack_gate"][0]}')
asm(x+0x410,'mov eax,1;pop esi;pop ebp;ret')
asm(x+0x430,'xor eax,eax;pop esi;pop ebp;ret')
for ofs,p in [(0x100,actor1),(0x140,actor2)]:
    asm(x+ofs,f'push {p};call {blocks["spawn"][0]};ret')
asm(x+0x500,f'mov eax,[esp+4];mov dword ptr [eax+0x200],0x42c80000;ret 4')
asm(x+0x540,'mov eax,[esi+0x200];mov [esi+0xa0],eax;ret 4')
asm(x+0x580,f'mov eax,{hp};ret')
asm(x+0x5c0,'mov eax,1234;ret 4')
for ofs,p in [(0x200,actor1),(0x280,actor2)]:
    asm(x+ofs,f'''push {p};call {x+ofs+0x18};add esp,4;ret''')
    asm(x+ofs+0x18,f'''push ebp;mov ebp,esp;push esi;sub esp,0x1c
                       mov dword ptr [esp+0x18],0x41200000;mov esi,{x+0x600}
                       jmp {blocks["observe_tag"][0]}''')
asm(x+0x450,'mov eax,[esp+0x18];add esp,0x1c;pop esi;pop ebp;ret')
ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
with tempfile.TemporaryDirectory(prefix='trait-test-',dir=HERE) as folder:
    path=Path(folder)/'fixture.bin'
    path.write_bytes(fixture)
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_native.ps1'),str(path)],check=True)
(HERE/'native-validation.json').write_text(json.dumps({'passed':True,'scope':'native / P1 / P2 / direct actors only / component impostors rejected / disabled / wrong owner / invalid stage / null',
    'tag':{'native_result_preserved':True,'base':10,'factor':1.5,'result':15},
    'spawn':{'two_independent_slots':True,'full_health':True,'original_callback':True}},indent=2)+'\n')
