from pathlib import Path
import sys,struct,re
exec(Path('work/shank2-story-coop/analyze.py').read_text().split('if len(sys.argv)>1:')[0])
for a in [0x6a8b40,0x6a5ac0]:
 print('CALLS',hex(a))
 for m in re.finditer(b'\xe8....',b[:0x32c800],re.S):
  if va(m.start())+5+struct.unpack('<i',m.group()[1:])[0]==a:
   o=m.start();s=b.rfind(b'\x55\x8b\xec',max(0,o-3000),o);print('FUNC',hex(va(s)));dis(va(s),o-s+90)
