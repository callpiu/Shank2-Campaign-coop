from pathlib import Path
import sys,struct,re
exec(Path('work/shank2-story-coop/analyze.py').read_text().split('if len(sys.argv)>1:')[0])
u=lambda o:struct.unpack_from('<I',b,o)[0]
for name in ['cCampaignGameMode','cGameMode','cSurvivalGameMode','cSimulation','GameSimStartParams','cCampaignGameScreen','cSurvivalGameScreen']:
 pat=('.?AV'+name).encode();o=b.find(pat)
 if o<0:pat=('.?AU'+name).encode();o=b.find(pat)
 if o<0:continue
 td=va(o-8);print('\nTYPE',name,hex(td))
 for m in re.finditer(re.escape(struct.pack('<I',td)),b):
  col=m.start()-12
  if col<0 or u(col)!=0 or u(col+4)>100:continue
  print('COL',hex(va(col)))
  for n in re.finditer(re.escape(struct.pack('<I',va(col))),b):
   print('VTABLE',hex(va(n.start()+4)))
   for i in range(30):
    a=u(n.start()+4+i*4)
    if not 0x401000<=a<0x72e000:break
    print(hex(i*4),hex(a))
for a in [0x6a7ee0,0x6a9290]:
 print('CALLS',hex(a))
 for m in re.finditer(b'\xe8....',b[:0x32c800],re.S):
  if va(m.start())+5+struct.unpack('<i',m.group()[1:])[0]==a:print(hex(va(m.start())))
