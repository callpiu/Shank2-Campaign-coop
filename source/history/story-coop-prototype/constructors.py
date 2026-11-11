from pathlib import Path
import sys,struct,re
exec(Path('work/shank2-story-coop/analyze.py').read_text().split('if len(sys.argv)>1:')[0])
for a in [0x75023c,0x750ab4]:
 print('VTABLE WRITES',hex(a))
 for m in re.finditer(re.escape(struct.pack('<I',a)),b[:0x32c800]):
  o=m.start();s=b.rfind(b'\x55\x8b\xec',max(0,o-3000),o);print('FUNCTION',hex(va(s)));dis(va(s),o-s+60)
