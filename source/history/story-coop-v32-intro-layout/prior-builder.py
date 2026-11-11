"""Add bilingual campaign-only trait summaries to the native skin spinner."""
import json
from pathlib import Path
import re
import struct
import sys
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
sys.path.insert(0,str(WORK/'story-coop-v27-traits'))
from build_traits import BASE, Cs, CS_ARCH_X86, CS_MODE_32, Ks, KS_ARCH_X86, KS_MODE_32, pefile, sha
sys.path.insert(0,str(WORK/'story-coop-v04'))
from chui import Reader

PREVIOUS=WORK/'story-coop-v27-traits'
SOURCE_LUA={
    'en':WORK/'chs-compat/extracted/en/data/bootstrap/skins.lua',
    'chs':WORK/'chs-compat/extracted/cn/data/bootstrap/skins.lua',
}
LABELS={
    'en':{'hp':'Health','knife':'Light damage','heavy':'Heavy damage',
          'ranged':'Ranged damage','grapplehit':'Grapple damage','pickup':'Pickup damage'},
    'chs':{'hp':'生命上限','knife':'轻攻击伤害','heavy':'重武器伤害',
           'ranged':'远程伤害','grapplehit':'抓取伤害','pickup':'场景武器伤害'},
}
DESCRIPTION_SITE=0x68cb24
# +600 is the boot ReadFile byte count; +620..+694 holds key settings.
# +1000..+1fff is the executable-path buffer. Keep persistent UI data in
# the gap between these two scratch areas, never in initially-zero buffers.
TABLE_OFFSET=0x800
STRING_OFFSET=0x900
HOOK_OFFSET=0x1d00
# Extra lines extend downward beneath the retained character description.
DESC_BOUNDS=(-0.095,-0.11,0.18,0.11)
TRAIT_BOUNDS=(0.84,0.40,0.18,0.26)
TRAIT_LABEL='coopTraitSummary'


def name_hash(s):
    v=0
    for b in s.encode():v=(v*0x1003f+b)&0xffffffff
    return v


def parse_skins(path):
    text=path.read_text(encoding='utf-8-sig')
    matches=list(re.finditer(r'\bname\s*=\s*"([^"]+)"',text))
    result={}
    for i,m in enumerate(matches):
        chunk=text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)]
        if not re.search(r'\bsources\s*=',chunk):continue
        desc=re.search(r'\bdesc\s*=\s*"((?:\\.|[^"\\])*)"',chunk)
        hp=re.search(r'\bhealthbonus\s*=\s*([^,\n]+)',chunk).group(1).strip()
        base=float(hp.split('*')[0].strip()) if '*' in hp else 1.0
        tags={tag:float(adjust) for tag,adjust in re.findall(r'tag\s*=\s*"([^"\n]+)"\s*,\s*adjust\s*=\s*([0-9.]+)',chunk)}
        assert desc and set(tags)<=set(LABELS['en'])
        result[m.group(1)]=dict(desc=desc.group(1).replace('\\n','\n').replace('\\"','"'),health=base,damage=tags)
    assert len(result)==17
    return result


def summaries():
    original={lang:parse_skins(path) for lang,path in SOURCE_LUA.items()}
    result={}
    for lang,skins in original.items():
        result[lang]={}
        for name,item in skins.items():
            actual=original['en'][name]
            assert actual['health']==item['health'] and actual['damage']==item['damage']
            lines=[]
            health=round((actual['health']-1)*100)
            if health:lines.append(f'{LABELS[lang]["hp"]} {health:+d}%')
            for tag,factor in actual['damage'].items():
                percent=round((factor-1)*100)
                if percent:lines.append(f'{LABELS[lang][tag]} {percent:+d}%')
            assert lines
            result[lang][name]=dict(original_description=item['desc'],lines=lines,
                text='\n'.join(lines),health=actual['health'],damage=actual['damage'])
    return result


def make_routines(code,data,old_page,*,ui_init=0x5e4540,ui_find=0x5e3e00,
                  ui_text=0x5e45a0,ui_release=0x4604e0,
                  native_select=0x43be20,native_apply=0x5e4480,warm_page=None):
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    blocks={}
    def put(offset,s):
        a=code+offset;blocks[a]=bytes(ks.asm(s,a)[0]);return a
    lookup=put(0x1d00,f'''push esi;mov esi,{data+TABLE_OFFSET}
        again:cmp dword ptr [esi],0;je empty
        cmp eax,[esi];je selected
        add esi,8;jmp again
        selected:mov eax,[esi+4];pop esi;ret
        empty:mov eax,{data+0x570};pop esi;ret''')
    update=put(0x1d80,f'''push ebx;push esi;sub esp,28
        mov ebx,ecx;mov esi,esp;mov ecx,esi;call {ui_init}
        push esi;mov ecx,{data+0x540};mov eax,ebx;call {ui_find}
        mov ecx,{data+0x570}
        cmp dword ptr [{data+4}],1;jne set_text
        cmp dword ptr [ebx+0x20],3;jne set_text
        mov eax,[{data+0x580}];call {lookup};mov ecx,eax
        set_text:mov eax,esi;call {ui_text}
        mov ecx,esi;call {ui_release}
        add esp,28;pop esi;pop ebx;ret''')
    put(0x1e80,f'''push dword ptr [esp+4];call {native_select}
        pushfd;pushad
        mov edx,[eax];mov [{data+0x580}],edx
        mov ecx,[ebp-0x84];call {update}
        popad;popfd;ret 4''')
    put(0x1f00,f'''push dword ptr [esp+4];call {native_apply}
        pushfd;pushad
        mov ecx,[ebp-0x108];mov edx,[ecx+0x1e8];mov [{data+0x580}],edx
        call {update};popad;popfd;ret 4''')
    put(0x1f80,f'''push ebx;mov ebx,ecx
        push dword ptr [esp+8];call {old_page}
        pushfd;pushad;mov ecx,ebx;call {update};popad;popfd
        pop ebx;ret 4''')
    if warm_page is not None:
        # Initial page preparation calls the native page trampoline directly,
        # bypassing the normal page wrapper above. Refresh after preparation
        # has finished and the character page/initial selection are stable.
        put(0x2000,f'''push ebx;mov ebx,ecx;call {warm_page}
            pushfd;pushad;mov ecx,ebx;call {update};popad;popfd
            pop ebx;ret''')
    return blocks


def parse_ui(raw):
    r=Reader(raw)
    assert r.u32()==2
    templates=[r.node() for _ in range(r.u32())]
    roots=[r.node() for _ in range(r.u32())]
    assert r.pos==len(raw)
    return r,templates,roots


def selector(lang,*,solo=False):
    source=WORK/f'story-coop-v26-direct/dev/coopsolo26sel{lang}.chui' if solo else WORK/f'story-coop-v20-prelevel-layout/dev/cooppreselv20{lang}.chui'
    raw=source.read_bytes();r,templates,_=parse_ui(raw)
    skin=next(n for n in templates if n['name']=='SkinSpinnerTemplate')
    desc=next(n for n in skin['children'] if n['name']=='desc')
    output=bytearray(raw)
    struct.pack_into('<4f',output,desc['common'],*DESC_BOUNDS)
    # Separate root overlay avoids the native spinner's item clipping. It is
    # populated only on the character page, and cleared on equipment pages.
    def s(t):
        b=t.encode('utf8');assert len(b)<128;return bytes([len(b)])+b
    block=bytearray(raw[desc['start']:desc['end']])
    name_end=4+len(s(desc['name']))
    block=bytearray(block[:4]+s(TRAIT_LABEL)+block[name_end:])
    shift=len(s(TRAIT_LABEL))-len(s(desc['name']))
    common=desc['common']-desc['start']+shift
    extra=desc['extra']-desc['start']+shift
    struct.pack_into('<4f',block,common,*TRAIT_BOUNDS)
    reader=Reader(block);reader.pos=extra;reader.string()
    block[extra:reader.pos]=s('')
    q=Reader(raw);q.u32();[q.node() for _ in range(q.u32())]
    countpos=q.pos;count=q.u32()
    struct.pack_into('<I',output,countpos,count+1)
    output.extend(block)
    # Keep the native multiline Antilles24 binding, body text, maps and count.
    r.pos=desc['extra'];r.string();settings=r.take(16);font=r.string();size=struct.unpack('<f',r.take(4))[0]
    assert font=='antilles24' and size==24.0
    changes={desc['common']+i for i in range(16)}|set(range(countpos,countpos+4))
    assert all(i in changes for i,(a,b) in enumerate(zip(raw,output)) if a!=b)
    _,_,newroots=parse_ui(output)
    assert sum(n['name']==TRAIT_LABEL for n in newroots)==1
    return bytes(output),dict(source_sha256=sha(raw),sha256=sha(output),
        text_node=TRAIT_LABEL,font=font,size=size,bounds=TRAIT_BOUNDS,
        original_description_bounds=DESC_BOUNDS,root_overlay_avoids_spinner_clip=True,
        image_maps_unchanged=True,original_text_unchanged=True)


def font_check(items):
    chs='\n'.join(v['text'] for v in items['chs'].values())
    font=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\data-pc\bootstrap\fonts\antilles24.fnt')
    root=ET.fromstring(font.read_bytes())
    glyphs={int(x.attrib['id']) for x in root.findall('./chars/char')}
    missing=sorted({ord(c) for c in chs if not c.isspace() and ord(c) not in glyphs})
    assert not missing,[hex(x) for x in missing]
    return dict(font=str(font),font_sha256=sha(font.read_bytes()),format='BMFont XML explicit Unicode glyph IDs',
        all_required_glyphs_present=True,missing=missing,characters=len(set(chs)))


def build(source,row,items):
    assert sha(source)==row['sha256']
    p=pefile.PE(data=source,fast_load=True);out=bytearray(source)
    c,d=int(row['code'],16),int(row['data'],16)
    off=lambda a:p.get_offset_from_rva(a-BASE)
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    edits=[]
    def patch(a,old,new):
        assert len(old)==len(new) and source[off(a):off(a)+len(old)]==old,hex(a)
        assert all(a>=b+n or a+len(old)<=b for b,n in edits)
        out[off(a):off(a)+len(new)]=new;edits.append((a,len(old)))
    table=bytearray(0x100)
    pool=bytearray()
    for i,(name,item) in enumerate(items.items()):
        value=item['text'].encode('utf8')+b'\0'
        struct.pack_into('<2I',table,i*8,name_hash(name),d+STRING_OFFSET+len(pool))
        pool.extend(value)
    assert TABLE_OFFSET+len(table)<=STRING_OFFSET
    assert len(pool)<=0x1000-STRING_OFFSET
    assert d+TABLE_OFFSET>=d+0x620+117
    patch(d+TABLE_OFFSET,bytes(len(table)),table)
    patch(d+STRING_OFFSET,bytes(len(pool)),pool)
    label=TRAIT_LABEL.encode()+b'\0'
    patch(d+0x540,bytes(len(label)),label)
    page=0x68d1c0
    assert source[off(page)]==0xe9
    old_page=page+5+struct.unpack_from('<i',source,off(page)+1)[0]
    precode=BASE+next(s.VirtualAddress for s in p.sections if s.Name.rstrip(b'\0')==b'.precoop')
    warm_page=precode+0x1c00
    blocks=make_routines(c,d,old_page,warm_page=warm_page)
    spans=[]
    for address,code in sorted(blocks.items()):
        assert len(code)<=0x80,(hex(address),len(code))
        assert all(address>=a+n or address+len(code)<=a for a,n in spans)
        spans.append((address,len(code)))
        assert sum(i.size for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(code,address))==len(code)
        patch(address,b'\xcc'*len(code),code)
    for site,native,hook in ((0x68d139,0x43be20,c+0x1e80),(0x68cc29,0x5e4480,c+0x1f00)):
        patch(site,bytes(ks.asm(f'call {native}',site)[0]),bytes(ks.asm(f'call {hook}',site)[0]))
    patch(page,source[off(page):off(page)+5],bytes(ks.asm(f'jmp {c+0x1f80}',page)[0]))
    md=Cs(CS_ARCH_X86,CS_MODE_32)
    warm_calls=[i.address for i in md.disasm(source[off(precode+0x1000):off(precode+0x1100)],precode+0x1000)
        if i.mnemonic=='call' and i.op_str==hex(warm_page)]
    assert len(warm_calls)==1,'Expected one title/first-show preparation call.'
    site=warm_calls[0]
    patch(site,bytes(ks.asm(f'call {warm_page}',site)[0]),bytes(ks.asm(f'call {c+0x2000}',site)[0]))
    # Unique new resource name; existing cached UI stays untouched.
    predat=BASE+next(s.VirtualAddress for s in p.sections if s.Name.rstrip(b'\0')==b'.predat')
    lang=row['language'];old=f'cooppreselv20{lang}.chui'.encode();new=f'cooppreselv28{lang}.chui'.encode()
    patch(predat+0x200,old,new)
    solo_old=f'coopsolo26sel{lang}.chui'.encode();solo_new=f'coopsolo28sel{lang}.chui'.encode()
    patch(d+0x340,solo_old,solo_new)
    allowed={off(a)+i for a,n in edits for i in range(n)}
    assert len(out)==len(source)
    assert all(i in allowed for i,(a,b) in enumerate(zip(source,out)) if a!=b)
    for site,n in ((0x4ee3b0,7),(0x4f3f40,7),(0x4f4061,5),(0x4f18c1,7),
                   (0x4f3fb6,8),(0x53ed6a,7),(0x7ff800,128)):
        assert out[off(site):off(site)+n]==source[off(site):off(site)+n]
    return bytes(out),{**row,'v27_sha256':row['sha256'],'sha256':sha(out),
        'description_site':hex(DESCRIPTION_SITE),'description_hook':None,
        'description_table':hex(d+TABLE_OFFSET),'description_asset':new.decode(),
        'solo_description_asset':solo_new.decode(),
        'description_patches':[(hex(a),n) for a,n in edits],'description_count':len(items),
        'string_bytes':len(pool),'test_assists':False}


def main():
    dest=HERE/'dev';dest.mkdir(parents=True,exist_ok=True)
    items=summaries();fonts=font_check(items);rows=[];uis={}
    old_rows=json.loads((HERE/'builds.json').read_text()) if (HERE/'builds.json').exists() else []
    previous_by_language={r['language']:r for r in old_rows}
    for row in json.loads((PREVIOUS/'builds.json').read_text()):
        lang=row['language'];name=f'shank2-story-coop-{lang}.exe'
        exe,report=build((PREVIOUS/'dev'/name).read_bytes(),row,items[lang]);(dest/name).write_bytes(exe)
        ui,uis[lang]=selector(lang);(dest/report['description_asset']).write_bytes(ui)
        ui,uis[lang+'_cached_solo']=selector(lang,solo=True);(dest/report['solo_description_asset']).write_bytes(ui)
        report['ui_assets']={name:sha((dest/name).read_bytes()) for name in (report['description_asset'],report['solo_description_asset'])}
        previous=previous_by_language.get(lang)
        history=set(previous.get('description_predecessors',[])) if previous else set()
        if previous and previous['sha256']!=report['sha256']:history.add(previous['sha256'])
        report['description_predecessors']=sorted(history)
        rows.append(report)
    (HERE/'descriptions.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (HERE/'builds.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
    (HERE/'source-validation.json').write_text(json.dumps(dict(source_ok=True,build_ok=True,runtime_verified=False,
        lua_sources={k:sha(v.read_bytes()) for k,v in SOURCE_LUA.items()},font=fonts,ui=uis),indent=2)+'\n')
    print('Built EN/CHS native campaign descriptions for 17 characters; font and exact-change checks passed.')


if __name__=='__main__':main()
