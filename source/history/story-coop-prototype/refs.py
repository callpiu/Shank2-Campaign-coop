from pathlib import Path
import sys,struct,re
exec(Path('work/shank2-story-coop/analyze.py').read_text().split('if len(sys.argv)>1:')[0])
for arg in sys.argv[1:]:
 data=arg.encode()+b'\0';o=b.find(data);v=va(o)
 print('STRING',arg,hex(v))
 for m in re.finditer(re.escape(struct.pack('<I',v)),b):
  r=va(m.start());print('REF',hex(r));off=m.start();s=b.rfind(b'\x55\x8b\xec',max(0,off-5000),off);print('FUNCTION',hex(va(s)))
  dis(va(s),min(off-s+600,1500))
