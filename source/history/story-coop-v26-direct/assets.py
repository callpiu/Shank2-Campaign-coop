"""Add only the missing Evil mappings to solo's unmodified UI layouts."""
import hashlib
from pathlib import Path
import struct
from chui import Reader

WORK=Path(__file__).resolve().parents[1]
EN=WORK/'story-coop-v09-fixes/upgrade-fixture'
CHS=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
ART={'img':'skin/skin_evil.tex','portrait':'skin/portraits_evil.tex','face':'skin/skin_evil.tex'}
sha=lambda v:hashlib.sha256(v).hexdigest()

def parse(b):
    r=Reader(b)
    assert r.u32()==2
    [r.node() for _ in range(r.u32())]
    [r.node() for _ in range(r.u32())]
    assert r.pos==len(b)
    return r

def maps(b):
    r=parse(b)
    result={}
    for n in r.nodes:
        name=n['name']
        if n['type'] not in (8,10) or name not in ART:continue
        r.pos=n['extra']+1
        countpos=r.pos
        values=[(r.string(),r.string(),r.take(4)) for _ in range(r.u32())]
        if not any(k=='shank' and p.lower().startswith('skin/') for k,p,t in values):continue
        assert name not in result
        result[name]=(countpos,r.pos,values)
    return result

def fix(source,names):
    before=maps(source)
    assert set(before)==set(names)
    output=bytearray(source)
    edits=[]
    for n,(start,end,rows) in before.items():
        assert not any(k=='evil' for k,p,t in rows)
        path=ART[n].encode()
        edits.extend(((start,4,struct.pack('<I',len(rows)+1)),(end,0,b'\x04evil'+bytes([len(path)])+path+b'\xff'*4)))
    for at,n,data in sorted(edits,reverse=True):output[at:at+n]=data
    after=maps(output)
    for n,(_,_,rows) in before.items():
        assert after[n][2]==rows+[('evil',ART[n],b'\xff'*4)]
    return bytes(output)

def build_solo_assets(lang,dest):
    root=CHS if lang=='chs' else EN
    results={}
    for kind,native,names in (('sel','singleplayerloadoutscreen.chui',('img','portrait')),
                              ('hud','campaignscreen.chui',('face',))):
        data=(root/'data-pc/ui'/native).read_bytes()
        fixed=fix(data,names)
        path=dest/f'coopsolo26{kind}{lang}.chui'
        path.write_bytes(fixed)
        results[path.name]={'sha256':sha(fixed),'native':native,'native_sha256':sha(data)}
    return results
