from pathlib import Path
import re,hashlib,struct,zipfile,json
root=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
exe=root/'bin/shank2.exe'
b=exe.read_bytes()
out=Path('work/shank2-story-coop')
strings=[(m.start(),m.group().decode('ascii')) for m in re.finditer(rb'[\x20-\x7e]{4,}',b)]
(out/'exe-strings.txt').write_text('\n'.join(f'{o:08x} {s}' for o,s in strings),encoding='utf-8')
print('SHA256',hashlib.sha256(b).hexdigest(),'MACHINE',hex(struct.unpack_from('<H',b,struct.unpack_from('<I',b,0x3c)[0]+4)[0]))
for o,s in strings:
 if re.search(r'player|campaign|survival|gamemode|commandline|profile|\.pdb|lua',s,re.I):
  print(f'{o:08x} {s}')
for name in ['shank2_campaign_01_dark_road','shank2_multiplayer_test_small_v4']:
 p=root/'data-pc/levels'/name
 for zname in ['data.zip','palettes.zip']:
  with zipfile.ZipFile(p/zname) as z:
   print(name,zname,z.namelist()[:25])
   for n in z.namelist():
    if n.endswith('.lua') and re.search(r'main|level|script',n,re.I): print(n,z.read(n)[:300])
