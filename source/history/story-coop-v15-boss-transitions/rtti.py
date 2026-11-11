import struct
import sys
from investigate import ROOT
sys.path.insert(0,str(ROOT/'work/story-coop-v05'))
from native import b,pe,off

def refs(value):
    found=[];key=struct.pack('<I',value);p=b.find(key)
    while p>=0:
        found.append(0x400000+pe.get_rva_from_offset(p));p=b.find(key,p+1)
    return found

for name in ('cGrappleComponent@Sim','cAnimCharacterRenderer@Animation','cVizComponent@Sim'):
    p=b.find(('.?AV'+name+'@@').encode())
    if p<0:print(name,'no class RTTI');continue
    td=0x400000+pe.get_rva_from_offset(p)-8
    for ref in refs(td):
        col=ref-12
        if b[off(col):off(col)+12]!=bytes(12):continue
        for link in refs(col):
            table=link+4
            ptrs=struct.unpack_from('<16I',b,off(table))
            print(name,hex(table),[hex(x) for x in ptrs], 'refs', [hex(x) for x in refs(table)[:15]])

for r in refs(0x4fd000):
    table=r-12
    col=struct.unpack_from('<I',b,off(table-4))[0]
    td=struct.unpack_from('<I',b,off(col+12))[0]
    print('RENDER OBJECT',hex(table),b[off(td+8):off(td+8)+100].split(b'\0')[0])
    print('VTABLE',[hex(x) for x in struct.unpack_from('<8I',b,off(table))],'CTOR',[hex(x) for x in refs(table)])
