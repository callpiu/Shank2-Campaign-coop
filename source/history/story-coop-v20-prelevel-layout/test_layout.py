import os
from pathlib import Path
import runpy
import struct
import subprocess
import tempfile
from flow20 import HERE,BASE,routines
from capstone import Cs,CS_ARCH_X86,CS_MODE_32

prior=runpy.run_path(str(BASE/'test_order.py'))
B,D,Q,CFG,CAT,SCREEN=(prior[k] for k in ('B','D','Q','CFG','CAT','SCREEN'))
asm=prior['asm'];old=bytearray(prior['buf']);new=bytearray(old)
targets=prior['targets']
for a,raw in routines(asm,B,D,diag=Q,config=CFG,catalog=CAT).items():
    blob=bytearray(raw)
    for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(raw,a):
        if i.mnemonic in ('call','jmp') and i.op_str.startswith('0x'):
            dest=int(i.op_str,16)
            if dest in targets:
                fix=asm(f'{i.mnemonic} {targets[dest]}',i.address);assert len(fix)==i.size
                pos=i.address-a;blob[pos:pos+len(fix)]=fix
    for before,after in ((0x800c00,D+0xc00),(0x800c04,D+0xc04)):
        blob=blob.replace(struct.pack('<I',before),struct.pack('<I',after))
    new[a-B:a-B+len(blob)]=blob
def put(b,o,s):
    raw=asm(s,B+o);b[o:o+len(raw)]=raw
for b in (old,new):
    put(b,0x2000,f'''push ebx;push esi
        mov ebx,ecx;inc dword ptr [{D+0xe00}]
        mov byte ptr [ebx+0x24],0;mov dword ptr [ebx+0x20],4
        mov dword ptr [{D+0xf24}],0
        xor edx,edx;mov esi,{CAT+0x140};mov eax,[ebx+0x1e8]
        find:cmp eax,[esi];je found;inc edx;add esi,0x90;cmp edx,17;jb find;xor edx,edx
        found:mov [{D+0xf00}],edx
        push 0;mov ecx,ebx;call {B+0x1700}
        mov dword ptr [{D+0xf20}],0
        pop esi;pop ebx;ret''')
    put(b,0x2580,f'''mov eax,[ebp+8];mov [ecx+0x20],eax
        cmp eax,3;jne weapon
        mov dword ptr [{D+0xf20}],1;jmp done
        weapon:cmp eax,2;ja done
        push ecx;mov ecx,eax;mov eax,1;shl eax,cl;or [{D+0xf24}],eax;pop ecx
        done:mov esp,ebp;pop ebp;ret 4''')
with tempfile.TemporaryDirectory(dir=HERE,prefix='layout-') as folder:
    oldfile=Path(folder)/'old.bin';oldfile.write_bytes(old)
    newfile=Path(folder)/'new.bin';newfile.write_bytes(new)
    ids=Path(folder)/'ids.json';ids.write_text(prior['json'].dumps(prior['fixture']['CATALOG']))
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_layout.ps1'),
        str(oldfile),str(newfile),str(ids),str(HERE/'layout-validation.json')],check=True)
