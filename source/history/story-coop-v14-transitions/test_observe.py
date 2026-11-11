"""Check sampling offsets and rejection of stale/mixed snapshots without a game."""
import struct
from observe import sample, SKINS, WEAPONS

class Fixture:
    def __init__(self):self.bytes={};self.change=False;self.reads=0
    def store(self,address,data):self.bytes.update({address+i:value for i,value in enumerate(data)})
    def put(self,address,value):self.store(address,struct.pack('<I',value))
    def read(self,address,size):
        if address==0x7ff000:
            self.reads+=1
            if self.change and self.reads>1:return bytes(size)
        try:return bytes(self.bytes[address+i] for i in range(size))
        except KeyError:return b''
    def u32(self,address):
        data=self.read(address,4)
        return struct.unpack('<I',data)[0] if len(data)==4 else None

p=Fixture();sim=0x100000;actors=(0x110000,0x120000)
words=[0,5,0,*actors,0,0,0,7,sim]
p.store(0x7ff000,struct.pack('<10I',*words));p.store(0x7ff800,bytes(128));p.put(0x7db2d4,42)
skins=list(SKINS);weapons=list(WEAPONS)
for slot,actor in enumerate(actors):
    head,node,handle,inv=(actor+x for x in (0x1000,0x1100,0x1200,0x2000))
    p.put(actor+0x20,sim);p.put(actor+0x160,head);p.put(head+4,node)
    p.put(node+12,42);p.put(node+16,handle);p.put(handle,0);p.put(handle+4,inv);p.put(inv+8,actor)
    p.store(inv+0x2c,bytes(0x28))
    for offset,value in ((0x2c,weapons[slot]),(0x30,weapons[slot+2]),(0x48,weapons[slot+4]),(0x4c,2+slot),(0x50,65+slot*95)):
        p.put(inv+offset,value)
    c=0x7ff800+64*slot;p.store(c+4,b'shank\0');p.store(c+20,struct.pack('<5I',skins[slot],weapons[slot],weapons[slot+2],weapons[slot+4],2+slot))
row=sample(p)
assert [x['score'] for x in row['players']]==[65,160]
assert [x['throwable_count'] for x in row['players']]==[2,3]
assert row['players'][0]['actual_weapons']['melee']==WEAPONS[weapons[0]]
assert row['players'][1]['next_spawn']['skin']==SKINS[skins[1]]
p.put(actors[1]+0x20,sim+4);assert sample(p) is None
p.put(actors[1]+0x20,sim);p.put(actors[1]+0x2008,actors[0]);assert sample(p) is None
p.put(actors[1]+0x2008,actors[1]);p.change=True;p.reads=0;assert sample(p) is None
p.change=False;p.put(0x7ff004,1);assert sample(p)['players']==[]
p.store(0x7ff000,b'');p.bytes.pop(0x7ff000);assert sample(p) is None
print('PASS: distinct scores/gear/queued skins, wrong-simulation, wrong-owner, torn-snapshot, init-stage, unreadable memory.')
