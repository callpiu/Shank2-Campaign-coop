from pathlib import Path
import sys,struct,re
sys.path.insert(0,str(Path('work/pydeps').resolve()))
import pefile
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
p=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin\shank2.exe'); b=p.read_bytes(); pe=pefile.PE(data=b); base=pe.OPTIONAL_HEADER.ImageBase
md=Cs(CS_ARCH_X86,CS_MODE_32)
def va(o): return base+pe.get_rva_from_offset(o)
def dis(addr,size=400):
 off=pe.get_offset_from_rva(addr-base)
 for i in md.disasm(b[off:off+size],addr): print(f'{i.address:08x}  {i.bytes.hex():20} {i.mnemonic:8} {i.op_str}')
if len(sys.argv)>1:
 dis(int(sys.argv[1],16),int(sys.argv[2],0) if len(sys.argv)>2 else 400)
else:
 print('BASE',hex(base),'SECTIONS',[(s.Name,hex(s.VirtualAddress),hex(s.PointerToRawData),hex(s.SizeOfRawData)) for s in pe.sections])
 for s in [b'cCampaignGameMode::Init()',b'multiplayer=%i',b'Campaigngamemode',b'survivalgamemode',b'Command-line:',b'SpawnLocation%d',b'playercontroller',b'setcontroller',b'windowed']:
  o=b.find(s); v=va(o); refs=[va(m.start()) for m in re.finditer(re.escape(struct.pack('<I',v)),b)]
  print('\nSTRING',s,hex(v),'XREFS',[hex(x) for x in refs])
  for r in refs[:6]: dis(r-20,100)
