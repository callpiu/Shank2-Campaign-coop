"""Real x86 regression for the stack packet escape missed in pose2's tests."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from pose3 import HERE, routine
from pose2 import routine as old_routine, BOSS, FEMALE, PACKET_SIZE
from build_teleport import Ks, KS_ARCH_X86, KS_MODE_32
from native import b, off

B = 0x20000000
ks = Ks(KS_ARCH_X86, KS_MODE_32)
asm = lambda s, a: bytes(ks.asm(s, a)[0])
buf = bytearray(0x10000)
def put(o, data): buf[o:o + len(data)] = data

for offset, fn in ((0, routine), (0x800, old_routine)):
    options={'metrics':B+0x3040} if offset==0 else {}
    code = fn(asm, B + offset, B + 0x3000, B + 0x1000, B + 0x1100, **options)
    assert len(code) < 0x800
    put(offset, code)
# Preserve the actual enqueue instructions found at the fault's upstream call.
# They store EBX, EDX and increment count; this is not an immediate packet copy.
native_enqueue = b[off(0x511c15):off(0x511c18)] + b[off(0x511c20):off(0x511c2a)]
assert native_enqueue.hex() == '891cc88954c804ff8000020000'
head = asm(f'''push ebx;push esi;push edi
    mov ebx,[esp+20]
    cmp byte ptr [ebx+0x6c],0
    jne hidden
    mov edx,[{B+0x9000}];imul edx,edx,0x270;add edx,{B+0x9200}
    mov edi,edx;mov esi,ebx;mov ecx,{PACKET_SIZE//4};cld
    rep movsd dword ptr es:[edi],dword ptr ds:[esi]
    inc dword ptr [{B+0x9000}]
    cmp dword ptr [{B+0x9004}],0
    jne hidden
    mov eax,[esp+24];mov ecx,[eax+0x200];mov edx,0x3f292492
    jmp enqueue
    hidden:pop edi;pop esi;pop ebx;mov eax,7;ret
    enqueue:''', B+0x1000)
put(0x1000, head + native_enqueue + asm('pop edi;pop esi;pop ebx;mov eax,7;ret', B+0x1000+len(head)+len(native_enqueue)))
put(0x1100, asm(f'cmp eax,77;jne none;mov eax,{B+0x5000};ret 4;none:xor eax,eax;ret 4', B+0x1100))
for offset, target in ((0x1800, B), (0x1900, B+0x800)):
    put(offset, asm(f'''push ebx;push esi;push edi;push ebp
        mov ebx,0x11223344;mov esi,0x22334455;mov edi,0x33445566;mov ebp,0x44556677
        push {B+0x7000};push {B+0x4000};push {B+0x6000};call {target};add esp,12
        cmp ebx,0x11223344;jne bad;cmp esi,0x22334455;jne bad
        cmp edi,0x33445566;jne bad;cmp ebp,0x44556677;jne bad
        jmp end;bad:mov eax,-99
        end:pop ebp;pop edi;pop esi;pop ebx;ret''', B+offset))
# Re-enter via the queued ORIGINAL pointers in a later pass with enqueue off.
put(0x1a00, asm(f'''push ebx;push esi;push edi
    mov dword ptr [{B+0x9004}],1
    mov esi,{B+0x7000};mov edi,[esi+0x200];xor ebx,ebx
    again:cmp ebx,edi;jae done
    push esi;push dword ptr [esi+ebx*8];push {B+0x6000};call {B};add esp,12
    inc ebx;jmp again
    done:pop edi;pop esi;pop ebx;mov eax,7;ret''', B+0x1a00))
for n in (0x4000, 0x5000): put(n, bytes((i*7+3)%256 for i in range(PACKET_SIZE)))
for o, v in ((0x3004,5),(0x4000,0x759294),(0x4070,77),(0x407c,BOSS),
             (0x5000,0x759294),(0x507c,FEMALE),(0x5070,0xffffffff),(0x6000,B+0x8000)):
    struct.pack_into('<I',buf,o,v)
buf[0x406c]=0;buf[0x506c]=1
with tempfile.TemporaryDirectory(dir=HERE, prefix='deferred-') as t:
    f=Path(t)/'test.bin';f.write_bytes(buf)
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',
                    str(HERE/'test_deferred.ps1'),str(f),str(HERE/'deferred-validation.json')],check=True)
