from pathlib import Path
import sys,struct,json
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
b=(HERE/'shank2-coop-v07-background-test.exe').read_bytes();pe=pefile.PE(data=b);meta=json.loads((HERE/'audio-build.json').read_text());code=int(meta['code'],16);data=int(meta['data'],16)
off=lambda a:pe.get_offset_from_rva(a-0x400000)
v=0x20000000;buf=bytearray(16384);buf[:1024]=b[off(code):off(code)+1024];buf[4096:6144]=b[off(data):off(data)+2048]
for pos in range(1021):
 value=struct.unpack_from('<I',buf,pos)[0]
 if data<=value<data+2048:struct.pack_into('<I',buf,pos,v+4096+value-data)
 elif value==0x72e2d8:struct.pack_into('<I',buf,pos,v+0x1f00)
ks=Ks(KS_ARCH_X86,KS_MODE_32)
stub=bytes(ks.asm(f'''mov eax,dword ptr [esp+8];mov dword ptr [{v+0x1f20}],eax
inc dword ptr [{v+0x1f24}]
mov ecx,dword ptr [esp+4]
cmp dword ptr [{v+0x1f28}],0
je copy
cmp byte ptr [ecx],71
jne copy
xor eax,eax;ret 8
copy:
mov edx,{v+0x2400}
loop:
mov al,byte ptr [ecx];mov byte ptr [edx],al;inc ecx;inc edx;test al,al;jnz loop
mov eax,{v+0x2400};ret 8''',v+0x2000)[0])
struct.pack_into('<I',buf,0x1f00,v+0x2000);buf[0x2000:0x2000+len(stub)]=stub
(HERE/'audio-test.bin').write_bytes(buf)
