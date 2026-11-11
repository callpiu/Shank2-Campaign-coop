import hashlib
import importlib.util
import json
import struct
from flow19 import HERE,BASE,routines
from chui import Reader

spec=importlib.util.spec_from_file_location('prelevel18_builder',BASE/'build.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

def image_maps(b):
    r=Reader(b);assert r.u32()==2
    [r.node() for _ in range(r.u32())];[r.node() for _ in range(r.u32())]
    assert r.pos==len(b)
    maps={}
    for node in r.nodes:
        if node['type'] not in(8,10):continue
        r.pos=node['extra'];r.take(1);countpos=r.pos;count=r.u32();values=[]
        for _ in range(count):values.append((r.string(),r.string(),r.take(4)))
        if node['name'] in ('img','portrait'):
            maps[node['name']]=dict(countpos=countpos,insertpos=r.pos,values=values)
    assert set(maps)=={'img','portrait'}
    return maps

def repair_ui(source,target):
    raw=source.read_bytes();before=image_maps(raw);out=bytearray(raw)
    scan=Reader(raw);scan.u32();[scan.node() for _ in range(scan.u32())];[scan.node() for _ in range(scan.u32())]
    label=next(n for n in scan.nodes if n['name']=='coopPlayerLabel')
    # Native common fields are x,y,width,height (then rotation/tint/visible),
    # not relative/absolute coordinate pairs. Give the new label real bounds.
    struct.pack_into('<4f',out,label['common'],0.36,0.015,0.32,0.065)
    paths={'img':'skin/skin_evil.tex','portrait':'skin/portraits_evil.tex'}
    def string(s):
        b=s.encode();assert len(b)<128;return bytes([len(b)])+b
    edits=[]
    for name,record in before.items():
        assert not any(k=='evil' for k,v,t in record['values'])
        edits.append((record['insertpos'],string('evil')+string(paths[name])+b'\xff'*4))
        edits.append((record['countpos'],struct.pack('<I',len(record['values'])+1)))
    for pos,data in sorted(edits,reverse=True):
        if pos in {m['countpos'] for m in before.values()}:out[pos:pos+4]=data
        else:out[pos:pos]=data
    after=image_maps(out)
    for name in before:
        assert after[name]['values'][:-1]==before[name]['values']
        assert after[name]['values'][-1]==('evil',paths[name],b'\xff'*4)
    art=HERE.parent/'story-coop-v14-transitions/game/data-pc/textures/ui'
    sizes={}
    for name,path in paths.items():
        b=(art/path).read_bytes();assert b[:4]==b'KTEX'
        sizes[name]=list(struct.unpack_from('<2H',b,8))
    assert sizes=={'img':[148,148],'portrait':[640,720]}
    target.write_bytes(out)
    return dict(sha256=hashlib.sha256(out).hexdigest(),source_sha256=hashlib.sha256(raw).hexdigest(),
        missing_evil_mapping_reproduced=True,existing_mappings_unchanged=True,evil_texture_sizes=sizes,
        player_stage_label_bounds=[0.36,0.015,0.32,0.065])

if __name__=='__main__':
    dest=HERE/'dev';dest.mkdir(exist_ok=True)
    rows=[]
    for source in sorted((HERE.parent/'story-coop-v17-grab-anchor/dev').glob('*.exe')):
        lang=source.stem.split('-')[-1]
        rows.append(builder.build(source,dest/source.name,lang,routine_factory=routines,asset_version=19,role_first=True))
    assert len(rows)==4
    ui={lang:repair_ui(BASE/f'dev/cooppreselv18{lang}.chui',dest/f'cooppreselv19{lang}.chui') for lang in ('en','chs')}
    (HERE/'builds.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    (HERE/'build-validation.json').write_text(json.dumps(dict(builds=rows,ui=ui),indent=2)+'\n',encoding='utf-8')
    print('Built 4 character-first variants and repaired both Evil UI mappings in English/Chinese.')
