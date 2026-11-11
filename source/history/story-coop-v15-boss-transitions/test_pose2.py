import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from build_teleport import HERE,Ks,KS_ARCH_X86,KS_MODE_32
from pose2 import routine,BOSS,FEMALE,PACKET_SIZE
B=0x20000000;ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
buf=bytearray(0x10000)
def put(o,b):buf[o:o+len(b)]=b
put(0,routine(asm,B,B+0x3000,B+0x1000,B+0x1100))
put(0x1000,asm(f'''push esi;push edi
    mov edx,[{B+0x9000}];imul edx,edx,0x270;add edx,{B+0x9200}
    mov edi,edx;mov esi,[esp+16];mov ecx,{PACKET_SIZE//4};cld
    rep movsd dword ptr es:[edi],dword ptr ds:[esi]
    inc dword ptr [{B+0x9000}]
    pop edi;pop esi;mov eax,7;ret''',B+0x1000))
put(0x1100,asm(f'cmp eax,77;jne none;mov eax,{B+0x5000};ret 4;none:xor eax,eax;ret 4',B+0x1100))
put(0x1800,asm(f'push 0x44;push {B+0x4000};push {B+0x6000};call {B};add esp,12;ret',B+0x1800))
for n in (0x4000,0x5000):put(n,bytes((i*7+3)%256 for i in range(PACKET_SIZE)))
for o,v in ((0x3004,5),(0x4000,0x759294),(0x4070,77),(0x407c,BOSS),(0x5000,0x759294),(0x507c,FEMALE),(0x5070,0xffffffff),(0x6000,B+0x7000)):
    struct.pack_into('<I',buf,o,v)
buf[0x406c]=0;buf[0x506c]=1
with tempfile.TemporaryDirectory(dir=HERE,prefix='pose2-') as t:
    f=Path(t)/'test.bin';f.write_bytes(buf)
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_pose2.ps1'),str(f),str(HERE/'pose2-validation.json')],check=True)
