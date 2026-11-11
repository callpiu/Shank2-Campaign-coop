from pathlib import Path
import sys,struct
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from build_fixes import routines
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
v=0x20000000;ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0]);buf=bytearray(16384)
blobs=routines(asm,v,v+0x1000,v+0x1800,v+0x700,v+0x800,v+0x900,v+0xa00)
blobs[0x400]=asm(f'mov ecx,dword ptr [esp+4];push dword ptr [esp+8];call {v};ret 8',v+0x400)
blobs[0x440]=asm(f'push ebx;mov ebx,dword ptr [esp+8];mov ecx,dword ptr [esp+12];call {v+0xc0};pop ebx;ret 8',v+0x440)
blobs[0x480]=asm(f'mov eax,dword ptr [esp+4];push 0;push dword ptr [esp+12];call {v+0x100};ret 8',v+0x480)
blobs[0x700]=asm('mov eax,1;ret',v+0x700)
blobs[0x800]=asm(f'''push ebx
mov eax,dword ptr [{v+0x1004}];mov dword ptr [{v+0x1020}],eax
mov eax,dword ptr [esp+8];mov ebx,dword ptr [eax+8]
mov ecx,dword ptr [{v+0x1824}]
call {v+0xc0}
mov dword ptr [{v+0x1024}],eax
mov eax,0x12345678;pop ebx;ret 4''',v+0x800)
blobs[0x900]=asm(f'mov eax,dword ptr [{v+0x1028}];ret',v+0x900)
blobs[0xa00]=asm(f'''mov dword ptr [{v+0x102c}],ecx
mov dword ptr [{v+0x1030}],edx
mov eax,dword ptr [esp+4];mov dword ptr [{v+0x1034}],eax
mov eax,dword ptr [esp+8];mov dword ptr [{v+0x1038}],eax
ret 8''',v+0xa00)
for o,b in blobs.items():buf[o:o+len(b)]=b
(HERE/'native-test.bin').write_bytes(buf)
