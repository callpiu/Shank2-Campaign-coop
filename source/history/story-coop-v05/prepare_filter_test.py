"""Run generated x86 row filtering with deterministic native service stubs."""
from pathlib import Path
import struct,sys
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parent/'story-coop-v04')]
from native import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from loadout_code import hash_name
b=(HERE/'shank2-coop-v05-menu-test.exe').read_bytes();pe=pefile.PE(data=b)
v=0x20000000;old=0x802000;data=0x803000
src=bytearray(b[pe.get_offset_from_rva(old-0x400000):pe.get_offset_from_rva(old-0x400000)+4096])
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
targets={0x6bfb30:v+0xe00,0x46fea0:v+0xe20,0x697680:v+0xe40,0x68cda5:v+0xe60,0x68cd74:v+0xe80,0x6bfa80:v+0xea0}
for start,end in [(0x900,0x980),(0x980,0xa40),(0xa40,0xb00)]:
 for ins in Cs(CS_ARCH_X86,CS_MODE_32).disasm(bytes(src[start:end]),old+start):
  if ins.mnemonic=='int3':break
  offset=ins.address-old
  if ins.mnemonic in ['call','jmp'] and ins.op_str.startswith('0x'):
   target=int(ins.op_str,16)
   if target in targets:
    new=asm(f'{ins.mnemonic} {targets[target]}',v+offset);assert len(new)==ins.size
    src[offset:offset+len(new)]=new
for delta in range(0x1000):
 if delta+4<=len(src):
  value=struct.unpack_from('<I',src,delta)[0]
  if data<=value<data+4096:struct.pack_into('<I',src,delta,v+4096+value-data)
  elif value==0x7ff004:struct.pack_into('<I',src,delta,v+0x1800)
buf=src+bytes(4096)
struct.pack_into('<I',buf,0x1800,5)
def put(offset,code):
 raw=asm(code,v+offset);assert len(raw)<0x100
 buf[offset:offset+len(raw)]=raw
put(0xd00,f'''push ebp;mov ebp,esp;sub esp,0x240
mov dword ptr [ebp-0x22c],{v+0x1500}
mov eax,dword ptr [ebp+8];mov dword ptr [ebp-0x230],eax
mov dword ptr [{v+0x1520}],3
mov eax,dword ptr [ebp+12];mov dword ptr [{v+0x1658}],eax
mov eax,dword ptr [ebp+16];mov dword ptr [{v+0x165c}],eax
mov dword ptr [ebp-0x80],{v+0x1600}
call {v+0x980}
mov esp,ebp;pop ebp;ret''')
put(0xe00,'mov eax,0x12345678;ret 8')
put(0xe20,'mov eax,dword ptr [ecx];ret')
put(0xe40,'mov eax,dword ptr [esp+4];mov eax,dword ptr [eax+0x5c];ret 4')
put(0xe60,'mov eax,1;ret')
put(0xe80,'xor eax,eax;ret')
put(0xea0,'mov eax,dword ptr [esp+12];ret 12')
put(0xec0,f'''push dword ptr [esp+4];push 0;call {v+0x900};ret''')
put(0xf00,f'''push ebp;mov ebp,esp;push dword ptr [ebp+12];push dword ptr [ebp+8];push 0
call {v+0xa40};pop ebp;ret''')
(HERE/'filter-test.bin').write_bytes(buf)
(HERE/'filter-test-hashes.json').write_text(__import__('json').dumps([hash_name(s) for s in ['melee','ranged','consumable']]))
