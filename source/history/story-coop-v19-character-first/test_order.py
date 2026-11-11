"""Real x86 regression of role-first routing and two-player commit."""
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import tempfile
from flow19 import HERE,BASE,routines
from capstone import Cs,CS_ARCH_X86,CS_MODE_32

fixture=runpy.run_path(str(BASE/'test_flow.py'))
B,D,Q,CFG,CAT,SCREEN=(fixture[k] for k in ('B','D','Q','CFG','CAT','SCREEN'))
asm=fixture['asm'];buf=bytearray(fixture['buf']);targets=dict(fixture['targets'])
targets[0x68d1c5]=B+0x2580
targets[0x46fea0]=B+0x2600
targets[0x697160]=B+0x2640
buf[:0x1800]=bytes(0x1800)
for a,raw in routines(asm,B,D,Q,CFG,CAT).items():
    blob=bytearray(raw)
    for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw,a):
        if i.mnemonic in ('call','jmp') and i.op_str.startswith('0x'):
            dest=int(i.op_str,16)
            if dest in targets:
                new=asm(f'{i.mnemonic} {targets[dest]}',i.address);assert len(new)==i.size
                pos=i.address-a;blob[pos:pos+len(new)]=new
    for old,new in ((0x800c00,D+0xc00),(0x800c04,D+0xc04)):
        blob=blob.replace(struct.pack('<I',old),struct.pack('<I',new))
    buf[a-B:a-B+len(blob)]=blob
def put(o,s):
    raw=asm(s,B+o);buf[o:o+len(raw)]=raw
put(0x1800,f'''push ebp;mov ebp,esp
    mov ecx,{SCREEN};mov eax,[ebp+8]
    cmp eax,0;je show;cmp eax,1;je confirm;cmp eax,2;je tick
    cmp eax,3;je hide;cmp eax,4;je sync;cmp eax,5;je back
    cmp eax,8;je equipment_done
    xor eax,eax;jmp done
    show:call {B+0x180};jmp done
    confirm:mov eax,ecx;call {B+0x600};jmp done
    tick:push 0;call {B+0xb00};jmp done
    hide:call {B+0x400};jmp done
    sync:call {B+0xf00};jmp done
    back:push 0;call {B+0x1200};jmp done
    equipment_done:push 3;call {B+0x1700}
    done:mov esp,ebp;pop ebp;ret''')
# The real OnShow populates the spinner from the selected skin and asks
# Page(0) from sentinel4. Model those inputs so the actual routing runs.
put(0x2000,f'''push ebx;push esi
    mov ebx,ecx;inc dword ptr [{D+0xe00}]
    mov byte ptr [ebx+0x24],0;mov dword ptr [ebx+0x20],4
    xor edx,edx;mov esi,{CAT+0x140};mov eax,[ebx+0x1e8]
    find:cmp eax,[esi];je found;inc edx;add esi,0x90;cmp edx,17;jb find;xor edx,edx
    found:mov [{D+0xf00}],edx
    push 0;mov ecx,ebx;call {B+0x1700}
    pop esi;pop ebx;ret''')
put(0x2580,'''mov eax,[ebp+8];mov [ecx+0x20],eax
    mov esp,ebp;pop ebp;ret 4''')
put(0x2600,f'mov eax,{B+0x8800};ret')
put(0x2640,f'mov eax,[esp+8];mov [{D+0xf14}],eax;ret 8')
with tempfile.TemporaryDirectory(dir=HERE,prefix='order-') as folder:
    f=Path(folder)/'order.bin';f.write_bytes(buf)
    ids=Path(folder)/'ids.json';ids.write_text(json.dumps(fixture['CATALOG']))
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_order.ps1'),
        str(f),str(ids),str(HERE/'order-validation.json')],check=True)
