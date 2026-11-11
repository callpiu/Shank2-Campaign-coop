import base64
import hashlib
import importlib.util
import json
import struct
from pathlib import Path
from flow20 import HERE,BASE,routines
from chui import Reader

spec=importlib.util.spec_from_file_location('prelevel_builder18',HERE.parent/'story-coop-v18-prelevel-duo/build.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

def parse(b):
    r=Reader(b);assert r.u32()==2
    [r.node() for _ in range(r.u32())];[r.node() for _ in range(r.u32())];assert r.pos==len(b)
    return r

def selector(source,target):
    raw=source.read_bytes();out=bytearray(raw);r=parse(raw)
    label=next(n for n in r.nodes if n['name']=='coopPlayerLabel')
    # Native normalized y grows upward. Move the ASCII player marker to the
    # top, avoiding both bottom prompts and the limited large CJK font subset.
    struct.pack_into('<4f',out,label['common'],0.36,0.91,0.32,0.065)
    parse(out);target.write_bytes(out)
    return dict(sha256=hashlib.sha256(out).hexdigest(),source_sha256=hashlib.sha256(raw).hexdigest(),
        evil_both_preview_maps_preserved=True,player_label_bounds=[0.36,0.91,0.32,0.065])

def native_campaign(lang):
    if lang=='chs':return (HERE.parent/'story-coop-v14-transitions/game/data-pc/ui/campaigncoopv05.chui').read_bytes()
    root=HERE.parents[1]/'outputs/Shank2-StoryCoop-v0.8.3-CHS/patch'
    recipe=json.loads((root/'ui-recipe.json').read_text())
    original=(HERE.parent/'story-coop-v05/installer-tests-startfix/en/data-pc/ui/campaignscreen.chui').read_bytes()
    assert hashlib.sha256(original).hexdigest()==recipe['input_sha256']
    out=bytearray(original)
    for p in recipe['patches']:
        i=p['offset'];before=bytes.fromhex(p['before']);after=bytes.fromhex(p['after'])
        assert out[i:i+len(before)]==before;out[i:i+len(after)]=after
    for c in recipe['append']:out.extend(original[c['copy']:c['copy']+c['length']] if 'copy'in c else base64.b64decode(c['literal']))
    assert hashlib.sha256(out).hexdigest()==recipe['output_sha256']
    return bytes(out)

def hud(raw,target):
    r=parse(raw);edits=[];mapped=0
    for n in r.nodes:
        if n['name']!='face' or n['type'] not in(8,10):continue
        r.pos=n['extra'];r.take(1);countpos=r.pos;count=r.u32();rows=[]
        for _ in range(count):rows.append((r.string(),r.string(),r.take(4)))
        assert any(k=='shank' for k,v,t in rows) and not any(k=='evil' for k,v,t in rows)
        path=b'skin/skin_Evil.tex';entry=b'\x04evil'+bytes([len(path)])+path+b'\xff'*4
        edits.extend([(r.pos,0,entry),(countpos,4,struct.pack('<I',count+1))]);mapped+=1
    assert mapped==1 # Both playerui instances use this same native template.
    out=bytearray(raw)
    for pos,count,data in sorted(edits,reverse=True):out[pos:pos+count]=data
    q=parse(out);assert out.count(b'skin/skin_Evil.tex')==raw.count(b'skin/skin_Evil.tex')+1
    assert sum(n['name']=='playerui' for n in q.nodes)==1 and sum(n['name']=='playerui2' for n in q.nodes)==1
    target.write_bytes(out)
    return dict(sha256=hashlib.sha256(out).hexdigest(),source_sha256=hashlib.sha256(raw).hexdigest(),
        shared_face_template_patched=mapped,both_player_roots_preserved=True)

if __name__=='__main__':
    dest=HERE/'dev';dest.mkdir(exist_ok=True);rows=[];uis={};huds={}
    for source in sorted((HERE.parent/'story-coop-v17-grab-anchor/dev').glob('*.exe')):
        lang=source.stem.split('-')[-1]
        rows.append(builder.build(source,dest/source.name,lang,routine_factory=routines,asset_version=20,role_first=True,
            campaign_ui_name=f'campaigncoopv20{lang}.chui',short_titles=True,localized_prompts=True))
    for lang in ('en','chs'):
        uis[lang]=selector(BASE/f'dev/cooppreselv19{lang}.chui',dest/f'cooppreselv20{lang}.chui')
        huds[lang]=hud(native_campaign(lang),dest/f'campaigncoopv20{lang}.chui')
    (HERE/'builds.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    (HERE/'build-validation.json').write_text(json.dumps(dict(builds=rows,ui=uis,hud=huds),indent=2)+'\n',encoding='utf-8')
    print('Built 4 variants, 2 full-initialization selectors and 2 Evil-enabled dual HUDs.')
