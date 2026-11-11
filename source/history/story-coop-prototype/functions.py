from pathlib import Path
import sys
exec(Path('work/shank2-story-coop/analyze.py').read_text().split('if len(sys.argv)>1:')[0])
for addr in [0x6a94e8,0x6a8017]:
 off=pe.get_offset_from_rva(addr-base)
 start=b.rfind(b'\x55\x8b\xec',max(0,off-6000),off)
 print('FUNCTION',hex(va(start)))
 dis(va(start),off-start+1000)
