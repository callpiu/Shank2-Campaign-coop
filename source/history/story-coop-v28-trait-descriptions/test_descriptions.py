"""Execute native UI callbacks and verify the separate bilingual trait column."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from build_descriptions import HERE,WORK,make_routines,summaries,name_hash,Ks,KS_ARCH_X86,KS_MODE_32,TRAIT_BOUNDS,pefile,BASE,TABLE_OFFSET,font_path,parse_ui


def main():
    items=summaries()
    assert items['en']['bubbles']['lines']==['Health -20%','Heavy damage -30%','Ranged damage +30%']
    assert items['chs']['bubbles']['lines']==['生命上限 -20%','重武器伤害 -30%','远程伤害 +30%']
    assert items['en']['horror']['lines']==['Heavy damage +50%','Ranged damage -30%']
    assert items['chs']['hobo']['lines']==['生命上限 +15%','场景武器伤害 +50%','抓取伤害 +10%']
    for lang,rows in items.items():
        assert len(rows)==17
        for row in rows.values():
            assert row['text']=='\n'.join(row['lines'])
            assert not any(x in row['text'].lower() for x in ('shop','disarm','revive','商店','拆弹','救援'))
    B=0x20000000;C=B+0x2000;D=B+0x5000;CTRL=B+0x7000;SCREEN=B+0x8000;FRAME=B+0x8800;VECTOR=B+0x9000
    fixture=bytearray(0x10000);ks=Ks(KS_ARCH_X86,KS_MODE_32)
    def asm(a,s):
        code=bytes(ks.asm(s,a)[0]);fixture[a-B:a-B+len(code)]=code
    def write(a,fmt,*v):struct.pack_into(fmt,fixture,a-B,*v)
    blocks=make_routines(C,D,B+0x1980,ui_init=B+0x1800,ui_find=B+0x1840,ui_text=B+0x1880,
        ui_release=B+0x18c0,native_select=B+0x1900,native_apply=B+0x1940,warm_page=B+0x19c0)
    for a,code in blocks.items():fixture[a-B:a-B+len(code)]=code
    write(D+4,'<I',1);write(SCREEN+0x20,'<I',3)
    write(SCREEN+0x1e8,'<I',name_hash('corina'))
    write(FRAME-0x84,'<I',SCREEN);write(FRAME-0x108,'<I',SCREEN)
    write(VECTOR+4,'<I',B+0xa000)
    for i,name in enumerate(('shank','horror','bubbles')):write(B+0xa000+i*0x90,'<I',name_hash(name))
    for i,name in enumerate(items['en']):write(D+TABLE_OFFSET+i*8,'<2I',name_hash(name),B+0xb000+i*16)
    # Reproduce the real startup writes before executing the UI callbacks.
    # These writes destroyed the old +600 table but must not touch +800.
    keys=(0x41,0x44,0x57,0x53,0x20,0x4a,0x4b,0x4c,0x55,0x49,0x0d,0x51,0x4f,
        0x25,0x27,0x26,0x28,0x60,0x61,0x62,0x63,0x64,0x65,0x67,0x66,0x75,0x76)
    packet=b'S2K1'+struct.pack('<I',0)+struct.pack('<27I',*keys)
    write(D+0x600,'<I',len(packet))
    fixture[D+0x620-B:D+0x620-B+len(packet)]=packet
    asm(B+0x1800,f'inc dword ptr [{CTRL+4}];ret')
    asm(B+0x1840,f'mov [{CTRL+8}],eax;ret 4')
    asm(B+0x1880,f'mov [{CTRL}],ecx;inc dword ptr [{CTRL+12}];ret')
    asm(B+0x18c0,'ret')
    # Execute the real position-independent native selected-row implementation.
    raw=(WORK/'story-coop-v27-traits/dev/shank2-story-coop-chs.exe').read_bytes()
    pe=pefile.PE(data=raw,fast_load=True);offset=pe.get_offset_from_rva(0x43be20-BASE)
    native_select=raw[offset:offset+0x1c]
    assert native_select.endswith(bytes.fromhex('c20400'))
    fixture[0x1900:0x1900+len(native_select)]=native_select
    asm(B+0x1940,f'mov eax,[esp+4];mov [{CTRL+24}],eax;mov eax,0x777;ret 4')
    asm(B+0x1980,f'mov eax,[esp+4];mov [ecx+0x20],eax;inc dword ptr [{CTRL+16}];mov eax,123;ret 4')
    # v20's first-show warm-up calls its native trampoline directly, bypassing
    # 68d1c0 and therefore the ordinary page hook. Reproduce that exact order.
    asm(B+0x19c0,f'''push ebx;mov ebx,ecx
        push 1;call {B+0x1980}
        mov ecx,ebx;push 2;call {B+0x1980}
        mov ecx,ebx;push 3;call {B+0x1980}
        pop ebx;ret''')
    asm(B+0x1000,f'''push ebx;push esi;push edi;push ebp
        mov ebx,0x12345678;mov esi,0x23456781;mov edi,0x34567812;mov ebp,0x45678123
        mov ecx,{SCREEN};call {C+0x1d80};mov eax,[{CTRL}]
        cmp ebx,0x12345678;jne bad;cmp esi,0x23456781;jne bad
        cmp edi,0x34567812;jne bad;cmp ebp,0x45678123;jne bad;jmp done
        bad:mov eax,-1
        done:pop ebp;pop edi;pop esi;pop ebx;ret''')
    asm(B+0x1100,f'push ebp;mov ebp,{FRAME};mov ecx,{VECTOR};push 1;call {C+0x1e80};pop ebp;ret')
    asm(B+0x1200,f'push ebp;push esi;mov ebp,{FRAME};mov esi,{SCREEN+0x7c};push 0x1234;call {C+0x1f00};pop esi;pop ebp;ret')
    asm(B+0x1300,f'mov ecx,{SCREEN};push 3;call {C+0x1f80};ret')
    asm(B+0x1340,f'mov ecx,{SCREEN};push 1;call {C+0x1f80};ret')
    asm(B+0x1380,f'mov ecx,{SCREEN};call {B+0x19c0};ret')
    asm(B+0x13c0,f'mov ecx,{SCREEN};call {C+0x2000};ret')
    cases=[dict(name=name,hash=name_hash(name),expected=B+0xb000+i*16) for i,name in enumerate(items['en'])]
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    with tempfile.TemporaryDirectory(prefix='trait-column-',dir=HERE) as folder:
        folder=Path(folder);(folder/'fixture.bin').write_bytes(fixture);(folder/'cases.json').write_text(json.dumps(cases))
        subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_descriptions.ps1'),str(folder/'fixture.bin'),str(folder/'cases.json')],check=True)
    layout=[]
    for lang,rows in items.items():
        raw=(HERE/'dev'/f'coopsolo28sel{lang}.chui').read_bytes();reader,_,roots=parse_ui(raw)
        trait=next(n for n in roots if n['name']=='coopTraitSummary')
        bounds=struct.unpack_from('<4f',raw,trait['common'])
        reader.pos=trait['extra'];reader.string();reader.take(16);reader.string();size=struct.unpack('<f',reader.take(4))[0]
        font=ET.fromstring(font_path(lang).read_bytes());glyphs={int(x.attrib['id']):x.attrib for x in font.findall('./chars/char')}
        scale=size/abs(int(font.find('./info').attrib['size']))*(1.25 if lang=='en' else 1)
        for name,row in rows.items():
            count=0
            for line in row['text'].split('\n'):
                width=0
                for ch in line:
                    assert ord(ch) in glyphs,(lang,name,hex(ord(ch)))
                    advance=int(glyphs[ord(ch)]['xadvance'])*scale
                    if width+advance>bounds[2]*1280:count+=1;width=0
                    width+=advance
                count+=1
            height=count*int(font.find('./common').attrib['lineHeight'])*scale
            assert height<=bounds[3]*720
            bottom=bounds[1]+bounds[3]/2-height/720
            assert bottom>=0.28,(lang,name,'below visible gray card')
            layout.append(dict(language=lang,skin=name,lines=count,design_height=height,text_bottom_normalized=bottom,independent_root=True))
    (HERE/'validation.json').write_text(json.dumps(dict(passed=True,characters=17,languages=['en','chs'],
        native_hook_cases=25,first_show_cases=17,old_first_show_failure_reproduced=True,
        first_show_without_selection_event=True,scope='Co-op character page only; clear on equipment and non-coop',
        native_row_selection_executed=True,native_callbacks_preserved=True,callee_saved_registers_preserved=True,
        real_startup_settings_writes_before_ui=True,
        layout=layout,runtime_visual_verified=False),indent=2)+'\n')
    print('17 bilingual trait columns and 25 native update/selection/page cases passed; all glyphs fit.')


if __name__=='__main__':main()
