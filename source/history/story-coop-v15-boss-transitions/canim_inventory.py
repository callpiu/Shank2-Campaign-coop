"""Inspect bounded header string tables from native ANIM v12 resources."""
import struct
import zipfile
from investigate import GAME

for name in ('boss_magnus_grapple','corina_build','shank_build_new','corina_basic_hit','boss_grappler_attacks_corina'):
    with zipfile.ZipFile(GAME/'data-pc/canims'/f'{name}.zip') as z:
        b=z.read(f'{name}/{name}.canim')
    pos=36
    n=struct.unpack_from('<H',b,34)[0]
    strings=[]
    for index in range(n):
        length=struct.unpack_from('<I',b,pos)[0];pos+=4
        if length>200 or length+pos>len(b):
            print(name,'STOP',index,hex(pos-4),length);break
        strings.append(b[pos:pos+length].decode('ascii','replace'));pos+=length
    print(name,'header',b[8:36].hex(),'strings',strings,'next',hex(pos),b[pos:pos+60].hex())
