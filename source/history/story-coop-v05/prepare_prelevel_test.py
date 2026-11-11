"""Bounded native x86 regression harness for the shared loadout show/hide path."""
from pathlib import Path
import sys,struct
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from native import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
source=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'final/shank2-coop-v05-keyboard.exe'
b=source.read_bytes();pe=pefile.PE(data=b)
sections={s.Name.rstrip(b'\0'):s for s in pe.sections}
old=0x400000+sections[b'.terrain'].VirtualAddress;olddata=0x400000+sections[b'.terdata'].VirtualAddress
at=pe.get_offset_from_rva(old-0x400000)
v=0x20000000;buf=bytearray(0x4000);buf[:4096]=b[at:at+4096]
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
targets={0x68de70:v+0x2380,0x68c330:v+0x23a0,0x68c420:v+0x2300}
for start,end in [(0xce0,0xd00),(0xd00,0xd80),(0xe00,0xe80),(0xe80,0x1000)]:
 for ins in Cs(CS_ARCH_X86,CS_MODE_32).disasm(bytes(buf[start:end]),old+start):
  if ins.mnemonic=='int3':break
  if ins.mnemonic in ['call','jmp'] and ins.op_str.startswith('0x'):
   target=int(ins.op_str,16)
   if target in targets:
    blob=asm(f'{ins.mnemonic} {targets[target]}',v+ins.address-old);assert len(blob)==ins.size
    buf[ins.address-old:ins.address-old+len(blob)]=blob
# Rewrite absolute mod-data operands; relative calls inside the code retain offsets.
for pos in range(4093):
 value=struct.unpack_from('<I',buf,pos)[0]
 if olddata<=value<olddata+0x1000:struct.pack_into('<I',buf,pos,v+0x1000+value-olddata)
 elif 0x7ff800<=value<0x7ff880:struct.pack_into('<I',buf,pos,v+0x1800+value-0x7ff800)
 elif value==0x7ff004:struct.pack_into('<I',buf,pos,v+0x1900)
def put(offset,src):
 blob=asm(src,v+offset);buf[offset:offset+len(blob)]=blob
put(0x2000,f'''push ebp;mov ebp,esp
mov eax,dword ptr [ebp+16];mov dword ptr [{v+0x1900}],eax
mov ecx,{v+0x3000}
cmp dword ptr [ebp+8],0
jne hide
mov eax,dword ptr [ebp+12];mov dword ptr [{v+0x1144}],eax
call {v+0xce0}
jmp done
hide:
mov eax,dword ptr [ebp+20];mov byte ptr [ecx+0x24],al
call {v+0xd00}
done:
xor eax,eax;pop ebp;ret''')
put(0x2300,f'''inc dword ptr [{v+0x1300}]
mov eax,dword ptr [esp+4];mov dword ptr [ecx+0x1c0],eax
mov eax,dword ptr [esp+8];mov dword ptr [ecx+0x1dc],eax
mov eax,dword ptr [esp+12];mov dword ptr [ecx+0x1e0],eax
mov eax,dword ptr [esp+16];mov dword ptr [ecx+0x1e4],eax
mov eax,dword ptr [esp+20];mov dword ptr [ecx+0x1e8],eax
ret 20''')
put(0x2380,f'inc dword ptr [{v+0x1380}];ret')
put(0x23a0,f'inc dword ptr [{v+0x13a0}];ret')
(HERE/'prelevel-test.bin').write_bytes(buf)
