from pathlib import Path
import sys,struct,re
sys.path.insert(0,r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps')
import pefile
b=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin\shank2.exe').read_bytes();p=pefile.PE(data=b);base=p.OPTIONAL_HEADER.ImageBase
va=lambda o:base+p.get_rva_from_offset(o)
for s in sys.argv[1:]:
 if s.startswith('0x'):
  off=p.get_offset_from_rva(int(s,16)-base);print(s,b[off:b.index(b'\0',off)].decode('ascii',errors='replace'));continue
 for sm in re.finditer(re.escape(s.encode()+b'\0'),b):
  o=sm.start()
  if o and b[o-1] not in [0,0xcc]:continue
  a=va(o);refs=[]
  for m in re.finditer(re.escape(struct.pack('<I',a)),b):
   if m.start()>0x32c800:continue
   pro=b.rfind(b'\x55\x8b\xec',max(0,m.start()-5000),m.start())
   refs.append((hex(va(m.start())),hex(va(pro)) if pro>=0 else '?'))
  print(s,hex(a),refs)
