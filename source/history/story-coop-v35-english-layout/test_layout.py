"""Check all English names, wrapped biographies and traits in separate bands."""
import json
from pathlib import Path
import re
import struct
import sys
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'story-coop-v28-trait-descriptions'))
from build_descriptions import parse_ui,summaries,font_path,sha


def font(node,reader):
    reader.pos=node['extra'];reader.string();reader.take(16);name=reader.string()
    size=struct.unpack('<f',reader.take(4))[0]
    xml=ET.fromstring(font_path('en',name).read_bytes())
    scale=size/abs(int(xml.find('./info').attrib['size']))*1.25
    widths={int(n.attrib['id']):int(n.attrib['xadvance'])*scale for n in xml.findall('./chars/char')}
    return widths,int(xml.find('./common').attrib['lineHeight'])*scale,size


def check(raw):
    reader,templates,roots=parse_ui(raw)
    bounds=lambda n:struct.unpack_from('<4f',raw,n['common'])
    skin=next(n for n in templates if n['name']=='SkinSpinnerTemplate')
    title=next(n for n in skin['children'] if n['name']=='name')
    desc=next(n for n in skin['children'] if n['name']=='desc')
    plate=next(n for n in skin['children'] if n['name']=='New Widget' and n['type']==10)
    trait=next(n for n in roots if n['name']=='coopTraitSummary')
    def origin(n,y=0):
        y+=bounds(n)[1]
        if n['name']=='skinspinner':return y
        for child in n['children']:
            found=origin(child,y)
            if found is not None:return found
        return None
    center=next(y for n in roots if (y:=origin(n)) is not None)
    tx,ty,tw,th=bounds(title);dx,dy,dw,dh=bounds(desc);_,ay,aw,ah=bounds(trait)
    title_widths,title_height,_=font(title,reader);body_widths,line_height,_=font(desc,reader)
    trait_widths,trait_height,_=font(trait,reader)
    title_top=center+ty+th/2;title_bottom=title_top-title_height/720
    trait_top=ay+ah/2;desc_top=center+dy+dh/2
    assert title_bottom>=trait_top+8/720,'Title and trait bands overlap.'
    assert title_height<=th*720,'Title height clipped.'
    _,py,_,ph=bounds(plate);plate_top=center+py+ph/2;plate_bottom=center+py-ph/2
    assert title_top<=plate_top and center+dy-dh/2>=plate_bottom
    assert py-ph/2>=-bounds(skin)[3]/2
    assert dy-dh/2>=-bounds(skin)[3]/2
    # Use the canonical Lua even though fonts live in a different subtree.
    lua=(WORK/'chs-compat/extracted/en/data/bootstrap/skins.lua').read_text(encoding='utf-8-sig')
    names=re.findall(r'displayname\s*=\s*"([^"]+)"',lua)
    rows=summaries()['en'];assert len(names)==len(rows)==17
    results=[]
    for (key,row),name in zip(rows.items(),names):
        assert sum(title_widths[ord(c)] for c in name)<=tw*1280,(key,'name clipped')
        for line in row['lines']:
            assert sum(trait_widths[ord(c)] for c in line)<=aw*1280,(key,'trait wraps')
        trait_bottom=trait_top-len(row['lines'])*trait_height/720
        assert trait_bottom>=desc_top+8/720,(key,'biography overlap')
        lines=1;used=0
        for word in row['original_description'].split(' '):
            width=sum(body_widths[ord(c)] for c in word);assert width<=dw*1280
            space=body_widths[32] if used else 0
            if used+space+width>dw*1280:lines+=1;used=width
            else:used+=space+width
        assert lines*line_height<=dh*720,(key,'biography clipped')
        results.append(dict(skin=key,name=name,biography_lines=lines,trait_lines=len(row['lines']),
            title_trait_gap_pixels=(title_bottom-trait_top)*720,trait_biography_gap_pixels=(trait_bottom-desc_top)*720))
    return results


def main():
    records=[]
    for kind in ('coopsolo28selen.chui','cooppreselv28en.chui'):
        p=WORK/'story-coop-v33-dodge/dev'/kind
        records.append(dict(resource=kind,cases=check(p.read_bytes())))
    old_failed=False
    try:check((HERE/'prior-solo-en.chui').read_bytes())
    except AssertionError as e:old_failed=True;reason=str(e)
    assert old_failed
    old=json.loads((HERE/'prior-builds.json').read_text(encoding='utf8'))
    current=json.loads((WORK/'story-coop-v28-trait-descriptions/builds.json').read_text(encoding='utf8'))
    before=next(r for r in old if r['language']=='chs');after=next(r for r in current if r['language']=='chs')
    assert before['sha256']==after['sha256'] and before['ui_assets']==after['ui_assets']
    (HERE/'layout-validation.json').write_text(json.dumps(dict(passed=True,old_overlap_reproduced=reason,
        glyph_metric_margin=1.25,english_character_cases=34,chs_bytes_unchanged=True,resources=records,
        runtime_visual_verified=False),indent=2)+'\n')
    print('All 17 English names/traits/biographies fit two selectors with 25% metric margin; old overlap reproduced; CHS unchanged.')


if __name__=='__main__':main()
