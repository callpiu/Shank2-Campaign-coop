"""Locate built-in teleport/animation action registration and code references."""
import json
import re
import struct
import sys
from investigate import HERE,ROOT
sys.path.insert(0,str(ROOT/'work/story-coop-v05'))
from native import b,pe,off,dis
print('TELEPORT VTABLE',[(hex(0x75ae00+i),hex(struct.unpack_from('<I',b,off(0x75ae00+i))[0])) for i in range(0,40,4)])

for match in re.finditer(rb'[ -~]{5,160}',b):
    raw=match[0]
    if (b'teleport' in raw.lower() or b'grappleeanim' in raw.lower() or b'grappleanimation' in raw.lower()) and len(raw)<130:
        va=0x400000+pe.get_rva_from_offset(match.start())
        refs=[];needle=struct.pack('<I',va);pos=b.find(needle)
        while pos>=0:
            refs.append(hex(0x400000+pe.get_rva_from_offset(pos)));pos=b.find(needle,pos+1)
        print(hex(va),raw.decode(),refs)

g=json.loads((HERE/'stategraphs-boss_magnus.json').read_text())['StateGraph']
for key,s in g['States'].items():
    for path,value in __import__('investigate').walk(s):
        if value.get('Type') in ('setgrappleeanim','setgrapplestate','setgrappleanim','setgrapplee','grapple'):
            print('ACTION',s.get('name'),path,json.dumps(value))
