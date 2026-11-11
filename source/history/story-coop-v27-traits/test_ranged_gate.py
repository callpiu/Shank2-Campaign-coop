"""Execute the original projectile gate and its scoped replacement in x86.

The failing baseline uses the exact seven original bytes. Both continuations
invoke the same multiplier stub; the test changes only the upstream gate.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

from build_traits import HERE, routines, Ks, KS_ARCH_X86, KS_MODE_32

B=0x20000000
C=B+0x4000
D=B+0x7000
DIAG=B+0x7800
P1=B+0x8000
P2=B+0x8100
OTHER=B+0x8200
CTX=B+0x8300
CONTROL=B+0x8400
SIM=B+0x8500
fixture=bytearray(0x10000)
ks=Ks(KS_ARCH_X86,KS_MODE_32)

def asm(a,source):
    blob=bytes(ks.asm(source,a)[0])
    fixture[a-B:a-B+len(blob)]=blob

def put(a,kind,*values):
    struct.pack_into(kind,fixture,a-B,*values)

blocks=routines(C,D,diag=DIAG,ranged_yes=B+0x1207,ranged_no=B+0x1220)
for name in ('scope','ranged_gate'):
    a,blob=blocks[name]
    fixture[a-B:a-B+len(blob)]=blob
put(D+4,'<I',1)
put(DIAG+4,'<I',5)
put(DIAG+12,'<2I',P1,P2)
put(DIAG+36,'<I',SIM)
for p,factor in ((P1,0.7),(P2,1.3),(OTHER,9.0)):
    put(p+0x20,'<I',SIM)
    put(p+0x40,'<f',factor)
put(CTX+8,'<I',P2)
put(CONTROL+4,'<f',10.0)
original=bytes.fromhex('84c0741c8b4b08')
fixture[0x1000:0x1007]=original
asm(B+0x1200,f'jmp {blocks["ranged_gate"][0]};nop;nop')
for gate,wrapper in ((B+0x1000,B+0x900),(B+0x1200,B+0xa00)):
    asm(wrapper,f'''push ebx;push esi;push edi;push ebp
        mov ebx,{CTX};mov esi,0x12345678;mov edi,0x34567812;mov ebp,0x56781234
        mov edx,0x11223344;mov eax,[{CONTROL}];jmp {gate}''')
    asm(gate+7,f'''call {B+0x1800};jmp {B+0x1900}''')
    asm(gate+0x20,f'''mov eax,0x41200000;jmp {B+0x1900}''')
asm(B+0x1800,f'''cmp ecx,[ebx+8];jne bad
    cmp edx,0x11223344;jne bad
    inc dword ptr [{CONTROL+8}]
    fld dword ptr [ecx+0x40];fmul dword ptr [{CONTROL+4}]
    fstp dword ptr [{CONTROL+12}];mov eax,[{CONTROL+12}];ret
    bad:mov eax,-1;ret''')
asm(B+0x1900,'''cmp esi,0x12345678;jne bad
    cmp edi,0x34567812;jne bad
    cmp ebp,0x56781234;jne bad
    jmp done
    bad:mov eax,-2
    done:pop ebp;pop edi;pop esi;pop ebx;ret''')
ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
with tempfile.TemporaryDirectory(prefix='ranged-gate-',dir=HERE) as folder:
    path=Path(folder)/'fixture.bin'
    path.write_bytes(fixture)
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_ranged_gate.ps1'),str(path)],check=True)
(HERE/'ranged-validation.json').write_text(json.dumps({
    'passed':True,'original_gate_reproduces_missing_campaign_bonus':True,
    'p2_ranged':{'base':10,'factor':1.3,'result':13},
    'p1_independent_factor':0.7,'original_survival_preserved':True,
    'reject':['solo','invalid stage','foreign actor','wrong simulation','null actor'],
    'context_actor_unchanged':True,'registers_preserved':True,
    'runtime_verified':False},indent=2)+'\n')
