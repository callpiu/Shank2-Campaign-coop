import struct
import zipfile
from investigate import GAME,ROOT
import sys
sys.path.insert(0,str(ROOT/'work/story-coop-v04'))
from loadout_code import hash_name

for p in (GAME/'data-pc/canims').glob('*.zip'):
    if not any(w in p.stem for w in ('corina','shank','magnus')):continue
    with zipfile.ZipFile(p) as z:
        names=[n for n in z.namelist() if n.endswith('.canim')]
        for entry in names:
            b=z.read(entry)
            if b[:8]!=b'ANIM\x0c\0\0\0' or struct.unpack_from('<I',b,12)[0]!=9 or b[16:25]!=b'character':continue
            pos=36
            for _ in range(struct.unpack_from('<H',b,34)[0]):
                n=struct.unpack_from('<I',b,pos)[0];pos+=4+n
            clips=[]
            for _ in range(struct.unpack_from('<H',b,26)[0]):
                n=struct.unpack_from('<I',b,pos)[0];pos+=4
                name=b[pos:pos+n].decode('ascii');pos+=n+2
                clips.append(name)
                if hash_name(name) in (0x3f9129c8,0x4f1858a5,0x39368afd):print('HASH MATCH',p.stem,name,hex(hash_name(name)))
            if p.stem in ('corina_basic','shank_basic','corina_basic_hit'):print(p.stem,clips)
