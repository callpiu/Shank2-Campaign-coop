"""Instrument a separate local test executable without changing death behavior."""
from pathlib import Path
import struct,sys,hashlib
import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
source=Path(__file__).parent/'final/shank2-coop-v03-keyboard.exe'
target=Path(sys.argv[1]);data=bytearray(source.read_bytes());pe=pefile.PE(data=data)
off=lambda va:pe.get_offset_from_rva(va-0x400000)
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
assert data[off(0x6a7150):off(0x6a7150)+5]==bytes.fromhex('558bec6aff')
blob=asm('''
push eax
inc dword ptr [0x7ff0dc]
mov dword ptr [0x7ff0e4], ecx
mov eax, dword ptr [esp+8]
mov dword ptr [0x7ff0e0], eax
mov eax, dword ptr [esp+4]
mov dword ptr [0x7ff0e8], eax
pop eax
push ebp
mov ebp, esp
push -1
jmp 0x6a7155
''',0x7feb00)
data[off(0x7feb00):off(0x7feb00)+len(blob)]=blob
data[off(0x6a7150):off(0x6a7150)+5]=asm('jmp 0x7feb00',0x6a7150)
step=asm('''
push ebp
mov ebp, esp
push esi
mov esi, ecx
push dword ptr [ebp+8]
call 0x4ac550
mov ecx, esi
call 0x40bae0
mov ecx, eax
call 0x4502f0
mov dword ptr [0x7ff0f0], eax
pop esi
pop ebp
ret 4
''',0x7fec00)
data[off(0x7fec00):off(0x7fec00)+len(step)]=step
md=Cs(CS_ARCH_X86,CS_MODE_32)
calls=[i for i in md.disasm(data[off(0x7fc500):off(0x7fc500)+256],0x7fc500) if i.mnemonic=='call' and i.op_str=='0x4ac550']
assert len(calls)==1
a=calls[0].address;data[off(a):off(a)+5]=asm('call 0x7fec00',a)
if '--isolate-death-actions' in sys.argv:
 assert struct.unpack_from('<I',data,off(0x75b5b4))[0]==0x566db0
 guard=asm('''
cmp dword ptr [0x7ff004], 5
jne original
mov eax, dword ptr [esp+4]
test eax, eax
jz original
mov eax, dword ptr [eax+8]
cmp eax, dword ptr [0x7ff010]
jne original
inc dword ptr [0x7ff0f4]
ret 4
original:
jmp 0x566db0
''',0x7fed00)
 data[off(0x7fed00):off(0x7fed00)+len(guard)]=guard
 struct.pack_into('<I',data,off(0x75b5b4),0x7fed00)
target.write_bytes(data);print(hashlib.sha256(data).hexdigest())
