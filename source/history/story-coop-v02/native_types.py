from pathlib import Path
import sys,struct,re
sys.path.insert(0,r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps')
import pefile
b=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin\shank2.exe').read_bytes();p=pefile.PE(data=b);base=p.OPTIONAL_HEADER.ImageBase
u=lambda o:struct.unpack_from('<I',b,o)[0]
va=lambda o:base+p.get_rva_from_offset(o)
for name in sys.argv[1:]:
 o=b.find(('.?AV'+name).encode())
 if o<0:continue
 td=va(o-8);print('TYPE',name,hex(td))
 for m in re.finditer(re.escape(struct.pack('<I',td)),b):
  col=m.start()-12
  if col<0 or u(col)!=0 or u(col+4)>100:continue
  for n in re.finditer(re.escape(struct.pack('<I',va(col))),b):
   print('VTABLE',hex(va(n.start()+4)))
   for i in range(70):
    a=u(n.start()+4+i*4)
    if not 0x401000<=a<0x72e000:break
    print(hex(i*4),hex(a))
