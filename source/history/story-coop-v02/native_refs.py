from pathlib import Path
import sys,struct,re
sys.path.insert(0,r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps')
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
b=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin\shank2.exe').read_bytes();p=pefile.PE(data=b);base=p.OPTIONAL_HEADER.ImageBase
md=Cs(CS_ARCH_X86,CS_MODE_32)
def dis(addr,size):
 o=p.get_offset_from_rva(addr-base)
 for i in md.disasm(b[o:o+size],addr):print(f'{i.address:08x} {i.mnemonic:8} {i.op_str}')
for arg in sys.argv[1:]:
 addr=int(arg,16); print('TARGET',hex(addr))
 if len(sys.argv)>2 and sys.argv[1]=='dis':break
 for s in p.sections:
  if not s.Characteristics&0x20000000:continue
  data=s.get_data();start=base+s.VirtualAddress
  # Decode only direct CALL candidates, verifying the rel32 destination.
  for m in re.finditer(b'\xe8',data):
   o=m.start()
   if o+5<=len(data) and start+o+5+struct.unpack_from('<i',data,o+1)[0]==addr:
    call=start+o;print('CALL',hex(call));dis(call-32,90)
