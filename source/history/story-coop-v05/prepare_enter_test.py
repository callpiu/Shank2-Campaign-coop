from pathlib import Path
import struct,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
here=Path(__file__).resolve().parent
b=(here/'shank2-coop-v05-menu-test.exe').read_bytes();pe=pefile.PE(data=b)
v=0x20000000;code=bytearray(8192)
src=b[pe.get_offset_from_rva(0x802c00-0x400000):pe.get_offset_from_rva(0x802d00-0x400000)]
for delta in [0x160,0x164,0x168,0x16c,0x170]:src=src.replace(struct.pack('<I',0x803000+delta),struct.pack('<I',v+4096+delta))
src=src.replace(struct.pack('<I',0x72e224),struct.pack('<I',v+0xe00))
code[0xc00:0xd00]=src
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
wrapper=asm(f'''push esi
mov eax, dword ptr [esp+8]
mov dword ptr [{v+0x1100}], eax
mov eax, dword ptr [esp+12]
mov dword ptr [{v+0x1160}], eax
mov eax, dword ptr [esp+16]
mov dword ptr [{v+0x1170}], eax
mov esi, {v+0x1200}
mov dword ptr [esi+4], 0
push 13
call {v+0xc00}
movzx eax, word ptr [esi+4]
pop esi
ret''',v+0xd00)
code[0xd00:0xd00+len(wrapper)]=wrapper
struct.pack_into('<I',code,0xe00,v+0xe20)
stub=asm(f'mov eax, dword ptr [{v+0x1100}]; ret 4',v+0xe20);code[0xe20:0xe20+len(stub)]=stub
(here/'enter-test.bin').write_bytes(code)
