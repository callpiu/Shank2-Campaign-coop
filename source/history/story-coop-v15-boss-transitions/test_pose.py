"""Exercise the actual rendering shim with native packet and caller ABI fixtures."""
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from build_pose import HERE,routine,FEMALE,BOSS,POSE,PACKET_SIZE,Ks,KS_ARCH_X86,KS_MODE_32
B=0x20000000;ks=Ks(KS_ARCH_X86,KS_MODE_32)
asm=lambda s,a:bytes(ks.asm(s,a)[0])
buf=bytearray(0x10000)
def put(o,data):
    assert buf[o:o+len(data)]==bytes(len(data));buf[o:o+len(data)]=data
put(0,routine(asm,B,B+0x3000,B+0x1000,B+0x1100))
put(0x1000,asm(f'''push esi;push edi
    mov eax,[esp+12];mov [{B+0x9000}],eax
    mov esi,[esp+16];mov [{B+0x9004}],esi
    mov eax,[esp+20];mov [{B+0x9008}],eax
    mov edi,{B+0x9200};mov ecx,{PACKET_SIZE//4};cld;rep movsd dword ptr es:[edi],dword ptr ds:[esi]
    pop edi;pop esi;mov eax,0x12345678;ret''',B+0x1000))
put(0x1100,asm(f'''inc dword ptr [{B+0x9010}]
    mov edx,[esp+4];mov [{B+0x9014}],edx
    cmp eax,77;jne missing
    mov eax,{B+0x5000};ret 4
    missing:xor eax,eax;ret 4''',B+0x1100))
put(0x1800,asm(f'push 0x44;push {B+0x4000};push {B+0x6000};call {B};add esp,12;ret',B+0x1800))
put(0x4000,bytes((i*7+3)%256 for i in range(PACKET_SIZE)))
for o,v in ((0x3004,5),(0x4000,0x759294),(0x4070,77),(0x407c,FEMALE),
            (0x5000,0x759294),(0x507c,BOSS),(0x6000,B+0x7000)):
    struct.pack_into('<I',buf,o,v)
buf[0x406c]=1
with tempfile.TemporaryDirectory(prefix='pose-',dir=HERE) as temp:
    path=Path(temp)/'fixture.bin';path.write_bytes(buf)
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_pose.ps1'),
        str(path),str(HERE/'pose-validation.json'),str(POSE)],check=True)
