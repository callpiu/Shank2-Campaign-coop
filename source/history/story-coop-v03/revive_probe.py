"""Record native teleport and onrevive boundaries in a separate test EXE."""
from pathlib import Path
import struct,sys,hashlib
import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
b=bytearray((Path(__file__).parent/'final/shank2-coop-v03-keyboard.exe').read_bytes())
p=pefile.PE(data=b);off=lambda a:p.get_offset_from_rva(a-0x400000)
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
def patch(a,old,dest,body):
 old=bytes.fromhex(old);assert b[off(a):off(a)+len(old)]==old
 blob=asm(body,dest);assert len(blob)<=256
 assert b[off(dest):off(dest)+len(blob)]==b'\xcc'*len(blob)
 b[off(dest):off(dest)+len(blob)]=blob
 b[off(a):off(a)+len(old)]=asm(f'jmp {dest:#x}',a)+b'\x90'*(len(old)-5)
patch(0x4d25e0,'51568bf08bce',0x7feb00,'''
pushfd
pushad
cmp dword ptr [0x7ff004], 5
jne done
cmp eax, dword ptr [0x7ff010]
jne done
mov edx, dword ptr [0x7ff100]
and edx, 15
shl edx, 3
mov ecx, dword ptr [esp+36]
mov dword ptr [edx+0x7ff200], ecx
mov dword ptr [edx+0x7ff204], eax
inc dword ptr [0x7ff100]
done:
popad
popfd
push ecx
push esi
mov esi, eax
mov ecx, esi
jmp 0x4d25e6
''')
patch(0x4d9a80,'8d44240450',0x7fec00,'''
pushfd
pushad
cmp dword ptr [0x7ff004], 5
jne done
cmp dword ptr [esp+40], 0x0d720814
jne done
inc dword ptr [0x7ff104]
mov edx, dword ptr [ecx+8]
mov dword ptr [0x7ff108], edx
mov dword ptr [0x7ff10c], ecx
mov edx, dword ptr [esp+36]
mov dword ptr [0x7ff110], edx
done:
popad
popfd
lea eax, [esp+4]
push eax
jmp 0x4d9a85
''')
target=Path(sys.argv[1]);target.write_bytes(b);print(hashlib.sha256(b).hexdigest())
