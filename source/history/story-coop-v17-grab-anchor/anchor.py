"""Read the actual pelvis anchor of hit_mid1 at 0.1s from ANIM v12.

Entire file is consumed: declared node/key counts and exact EOF checked.
No resource modifications, no guessed pixel correction or gameplay position.
"""
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import zipfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v16-crash-recovery'))
from pose3 import routine as base_routine

GAME=HERE.parent/'story-coop-v14-transitions/game'

def load_anchor():
    source=GAME/'data-pc/canims/corina_basic_hit.zip'
    with zipfile.ZipFile(source) as z:b=z.read('corina_basic_hit/corina_basic_hit.canim')
    assert b[:8]==b'ANIM\x0c\0\0\0' and b[16:25]==b'character'
    fps=b[25];nclips,nnodes,nkeys,nsymbols=struct.unpack_from('<HHIH',b,26)
    pos=36
    def string():
        nonlocal pos
        n=struct.unpack_from('<I',b,pos)[0];pos+=4
        assert n<=512 and pos+n<=len(b)
        result=b[pos:pos+n].decode('ascii');pos+=n;return result
    symbols=[string() for _ in range(nsymbols)]
    clips={}
    for _ in range(nclips):
        name=string();clips[name]=struct.unpack_from('<H',b,pos)[0];pos+=2
    frame=clips['hit_mid1']+int(0.1*fps)
    matches=[];seen_keys=0
    for _ in range(nnodes):
        node=string();count=struct.unpack_from('<H',b,pos+7)[0];pos+=9
        assert pos+count*43<=len(b)
        for _ in range(count):
            start,duration,symbol,image=struct.unpack_from('<4H',b,pos)
            xs,ys,sx,sy,x,y=struct.unpack_from('<6f',b,pos+8)
            if start<=frame<start+duration and symbol<len(symbols) and symbols[symbol]=='plv':
                matches.append(dict(node=node,start_frame=start,duration=duration,image=image,
                    transform=[xs,ys,sx,sy,x,y]))
            pos+=43
        seen_keys+=count
    assert pos==len(b) and seen_keys==nkeys
    assert len(matches)==1 and all(math.isfinite(v) for v in matches[0]['transform'])
    x,y=matches[0]['transform'][4:6]
    assert -256<x<256 and 0<y<512
    return dict(source=str(source),canim_sha256=hashlib.sha256(b).hexdigest(),
        pose='hit_mid1',pose_seconds=0.1,global_frame=frame,fps=fps,
        node_count=nnodes,key_count=nkeys,exact_eof=True,match=matches[0],local_pelvis=[x,y])

def routine(asm,code,**kwargs):
    return base_routine(asm,code,anchor=load_anchor()['local_pelvis'],**kwargs)

if __name__=='__main__':
    report=load_anchor()
    (HERE/'anchor-source.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
