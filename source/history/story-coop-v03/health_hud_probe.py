"""A/B the health sub-widget against the full second PlayerUI update."""
from pathlib import Path
import sys,hashlib
import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
b=bytearray((Path(__file__).parent/'final/shank2-coop-v03-keyboard.exe').read_bytes());p=pefile.PE(data=b)
off=p.get_offset_from_rva(0x7fe300-0x400000)
ks=Ks(KS_ARCH_X86,KS_MODE_32)
code=bytes(ks.asm('''
push ebp
mov ebp, esp
push esi
push edi
mov esi, ecx
push dword ptr [ebp+12]
push dword ptr [ebp+8]
call 0x6966a0
mov ecx, esi
call 0x6936e0
test eax, eax
jz done
mov ecx, eax
mov edx, dword ptr [eax]
push 1
call dword ptr [edx+0x2c]
test eax, eax
jz done
mov edi, eax
push dword ptr [ebp+12]
push edi
push dword ptr [ebp+8]
lea ecx, [esi+0x1420]
call 0x6735a0
inc dword ptr [0x7ff0d0]
done:
pop edi
pop esi
pop ebp
ret 8
''',0x7fe300)[0]);assert len(code)<256
b[off:off+256]=code+b'\xcc'*(256-len(code))
Path(sys.argv[1]).write_bytes(b);print(hashlib.sha256(b).hexdigest())
