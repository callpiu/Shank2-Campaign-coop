"""Native x86 regression: original trigger moves one player; scoped fix moves both."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from build_teleport import routine,TARGET,Ks,KS_ARCH_X86,KS_MODE_32,HERE
B=0x20000000
ks=Ks(KS_ARCH_X86,KS_MODE_32)
asm=lambda s,a:bytes(ks.asm(s,a)[0])
buf=bytearray(0x10000)
def put(o,data):
    assert buf[o:o+len(data)]==bytes(len(data))
    buf[o:o+len(data)]=data
put(0,routine(asm,B,B+0x3000,B+0x1000))
native=asm(f'''push ebx
    mov eax,[esp+8]
    mov eax,[eax+8]
    mov edx,[{B+0x9000}]
    mov [{B+0x9100}+edx*4],eax
    inc dword ptr [{B+0x9000}]
    mov ebx,[ecx+8]
    mov [eax+0x70],ebx
    mov ebx,[ecx+12]
    mov [eax+0x74],ebx
    mov eax,[{B+0x9000}]
    pop ebx
    ret 4''',B+0x1000)
put(0x1000,native)
for offset,target in ((0x1800,B),(0x1840,B+0x1000)):
    put(offset,asm(f'push {B+0x6000};mov ecx,{B+0x2000};call {target};ret',B+offset))
for o,v in ((0x2008,TARGET[0]),(0x200c,TARGET[1]),(0x3004,5),(0x300c,B+0x4000),
            (0x3010,B+0x5000),(0x3024,B+0x7000),(0x4020,B+0x7000),(0x5020,B+0x7000),
            (0x6000,B+0x7000),(0x6004,0x1234),(0x6008,B+0x4000),(0x600c,0x5678)):
    struct.pack_into('<I',buf,o,v)
with tempfile.TemporaryDirectory(prefix='teleport-',dir=HERE) as temp:
    path=Path(temp)/'fixture.bin';path.write_bytes(buf)
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_teleport.ps1'),
        str(path),str(HERE/'teleport-validation.json')],check=True)
