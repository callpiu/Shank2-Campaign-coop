from pathlib import Path
import struct,re
for name in ['campaignscreen','survivalscreen']:
 b=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\data-pc\ui',name+'.chui').read_bytes()
 print(name)
 for key in [b'playerui',b'player1',b'player2',b'players',b'PlayerUI']:
  for m in re.finditer(key,b):
   o=m.start();print(key,hex(o))
   if key==b'PlayerUI':continue
   start=max(0,o-72);end=min(len(b),o+104)
   for a in range(start,end,16):
    x=b[a:a+16];print(hex(a),x.hex(' '),''.join(chr(c) if 32<=c<127 else '.' for c in x))
