import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from test_assist import HERE,ENEMIES,TABLE,routine,Ks,KS_ARCH_X86,KS_MODE_32
B=0x20000000;ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
buf=bytearray(0x8000)
blocks={0:routine(asm,B,B+0x3000,B+0x400,B+0x300,False),
0x300:asm(f'mov edx,[esp+8];mov [{B+0x1810}],edx;inc dword ptr [{B+0x180c}];mov eax,7;ret 16',B+0x300),
0x400:asm('lea eax,[ecx+0x100];ret',B+0x400),
0x500:asm(f'''mov edx,[esp+4]
    push 4;push 3;push dword ptr [{B+0x3080}];push edx
    mov eax,123;stc;call {B};adc eax,0;ret 4''',B+0x500),
0x1000:struct.pack('<'+str(len(ENEMIES))+'I',*ENEMIES)}
for o,b in blocks.items():buf[o:o+len(b)]=b
for o,v in ((0x3004,5),(0x300c,B+0x4100),(0x3010,B+0x4200),(0x3024,B+0x3200),
            (0x4120,B+0x3200),(0x4220,B+0x3200),(0x4320,B+0x3200),
            (0x6008,B+0x4100),(0x6108,B+0x4200),(0x6208,B+0x4300),(0x3080,0x40a00000)):
    struct.pack_into('<I',buf,o,v)
bosses=[r['hash'] for r in TABLE['enemies'] if r['boss']]
assert len(bosses)==15 and not set(bosses)&set(ENEMIES)
with tempfile.TemporaryDirectory(prefix='assist-',dir=HERE) as temp:
    t=Path(temp);(t/'fixture.bin').write_bytes(buf)
    (t/'ids.json').write_text(json.dumps(dict(enemies=ENEMIES,bosses=bosses)),encoding='utf-8')
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_assist_native.ps1'),
        str(t/'fixture.bin'),str(t/'ids.json'),str(HERE/'assist-validation.json')],check=True)
