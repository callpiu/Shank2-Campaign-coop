"""Execute the actual selection/transaction x86 with bounded native UI stubs."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from flow import HERE,routines,v12
from selector import CATALOG,constants
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32

B=0x20000000;D=B+0x3000;Q=B+0x5000;CFG=B+0x5800;CAT=B+0x6000;SCREEN=B+0x8000
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
buf=bytearray(0x10000)
targets={0x801ce0:B+0x2000,0x7fb680:B+0x2100,0x5e33c0:B+0x2180,0x68c420:B+0x2200,
    0x5e49f0:B+0x2300,0x68c470:B+0x2340,0x801700:B+0x2380,0x5e4540:B+0x23c0,
    0x5e3e00:B+0x2400,0x5e45a0:B+0x2440,0x4604e0:B+0x2480,0x68dd66:B+0x2500,0x68c2e7:B+0x2540}
for a,raw in routines(asm,B,D,Q,CFG,CAT).items():
    blob=bytearray(raw)
    for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw,a):
        if i.mnemonic in ('call','jmp') and i.op_str.startswith('0x'):
            target=int(i.op_str,16)
            if target in targets:
                new=asm(f'{i.mnemonic} {targets[target]}',i.address);assert len(new)==i.size
                pos=i.address-a;blob[pos:pos+len(new)]=new
    for old,new in ((0x800c00,D+0xc00),(0x800c04,D+0xc04)):
        blob=blob.replace(struct.pack('<I',old),struct.pack('<I',new))
    buf[a-B:a-B+len(blob)]=blob
def put(o,source):
    b=asm(source,B+o);buf[o:o+len(b)]=b
put(0x1800,f'''push ebp;mov ebp,esp
    mov ecx,{SCREEN};mov eax,[ebp+8]
    cmp eax,0;je show;cmp eax,1;je confirm;cmp eax,2;je tick
    cmp eax,3;je hide;cmp eax,4;je sync;cmp eax,5;je back
    cmp eax,6;je gate;cmp eax,7;je stage_gate
    xor eax,eax;jmp done
    show:call {B+0x180};jmp done
    confirm:mov eax,ecx;call {B+0x600};jmp done
    tick:push 0;call {B+0xb00};jmp done
    hide:call {B+0x400};jmp done
    sync:call {B+0xf00};jmp done
    back:push 0;call {B+0x1200};jmp done
    gate:call {B+0x500};jmp done
    stage_gate:call {B+0x1680};setz al;movzx eax,al
    done:mov esp,ebp;pop ebp;ret''')
put(0x2000,f'inc dword ptr [{D+0xe00}];mov dword ptr [ecx+0x20],0;mov byte ptr [ecx+0x24],0;ret')
put(0x2100,f'''inc dword ptr [{D+0xe04}]
    cmp byte ptr [ecx+0x24],1;jne no_owner
    push esi;push edi
    lea esi,[ecx+0x1dc];mov edi,{D+0xe40};push ecx;mov ecx,4;cld
    rep movsd dword ptr es:[edi],dword ptr ds:[esi]
    pop ecx;pop edi;pop esi
    inc dword ptr [{D+0xe08}]
    no_owner:ret''')
put(0x2180,f'mov ecx,eax;call {B+0x400};ret')
put(0x2200,'''mov eax,[esp+4];mov [ecx+0x1c0],eax
    mov eax,[esp+8];mov [ecx+0x1dc],eax
    mov eax,[esp+12];mov [ecx+0x1e0],eax
    mov eax,[esp+16];mov [ecx+0x1e4],eax
    mov eax,[esp+20];mov [ecx+0x1e8],eax;ret 20''')
put(0x2300,f'mov eax,[{D+0xf00}];ret')
put(0x2340,f'inc dword ptr [{D+0xe0c}];ret 4')
put(0x2380,f'inc dword ptr [{D+0xe10}];ret')
put(0x23c0,'mov eax,ecx;ret')
put(0x2400,'ret 4')
put(0x2440,f'mov [{D+0xf10}],ecx;ret')
put(0x2480,'ret')
put(0x2500,f'inc dword ptr [{D+0xe14}];mov esp,ebp;pop ebp;ret 4')
put(0x2540,'mov esp,ebp;pop ebp;ret 4')
buf[CAT-B:CAT-B+0xc00]=constants(CAT)
for i,row in enumerate(CATALOG):struct.pack_into('<I',buf,CAT-B+0x140+i*0x90,row['hash'])
struct.pack_into('<I',buf,CAT-B+0x128,CAT+0x140+17*0x90)
for i,family in enumerate(('shank','corina')):
    o=CFG-B+i*64;struct.pack_into('<I',buf,o,1);buf[o+4:o+4+len(family)]=family.encode()
    names=(family,'machete','throwingknives','weapon_grenade') if i==0 else (family,'sword','revolver','weapon_grenade')
    struct.pack_into('<5I',buf,o+20,*map(v12.hash_name,names),3)
struct.pack_into('<I',buf,D-B,SCREEN);struct.pack_into('<I',buf,SCREEN-B,0x7532b0)
struct.pack_into('<I',buf,Q-B+32,7)
with tempfile.TemporaryDirectory(dir=HERE,prefix='flow-') as tmp:
    f=Path(tmp)/'flow.bin';f.write_bytes(buf)
    meta=Path(tmp)/'ids.json';meta.write_text(json.dumps(CATALOG))
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_flow.ps1'),
        str(f),str(meta),str(HERE/'flow-validation.json')],check=True)
