"""Four isolated dual pre-level selectors, preserving all verified Boss fixes."""
import hashlib
import json
from pathlib import Path
import struct
import sys
from flow import HERE,CODE,DATA,routines,v12
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from native import pefile
sys.path.insert(0,str(HERE.parent/'story-coop-v04'))
from chui import Reader

def ui(source,target):
    b=source.read_bytes();r=Reader(b);assert r.u32()==2
    [r.node() for _ in range(r.u32())];countpos=r.pos;count=r.u32()
    [r.node() for _ in range(count)];assert r.pos==len(b)
    node=next(n for n in r.nodes if n['name']=='weapontype' and n['type']==4)
    spin=next(n for n in r.nodes if n['name']=='skinspinner')
    def s(value):
        raw=value.encode('utf-8');assert len(raw)<128;return bytes([len(raw)])+raw
    raw=b[node['start']:node['end']]
    oldend=4+len(s(node['name']));label=bytearray(raw[:4]+s('coopPlayerLabel')+raw[oldend:])
    shift=len(s('coopPlayerLabel'))-len(s(node['name']))
    common=node['common']-node['start']+shift
    struct.pack_into('<4f',label,common,0.5,0,0.035,0)
    extra=node['extra']-node['start']+shift
    q=Reader(bytes(label));q.pos=extra;q.string();end=q.pos
    label[extra:end]=s('')
    out=bytearray(b);out[spin['common']+24]=1
    struct.pack_into('<I',out,countpos,count+1);out.extend(label)
    check=Reader(out);check.u32();[check.node() for _ in range(check.u32())];[check.node() for _ in range(check.u32())]
    assert check.pos==len(out) and sum(n['name']=='coopPlayerLabel' for n in check.nodes)==1
    target.write_bytes(out)
    return dict(source_sha256=hashlib.sha256(b).hexdigest(),sha256=hashlib.sha256(out).hexdigest())

def build(source,target,language,*,routine_factory=None,asset_version=18,role_first=False,
          campaign_ui_name=None,short_titles=False,localized_prompts=False):
    b=source.read_bytes();p=pefile.PE(data=b);out=bytearray(b)
    CODE=0x400000+p.OPTIONAL_HEADER.SizeOfImage
    DATA=CODE+0x2000
    # All 12 existing sections are retained byte-for-byte. Reclaim unused DOS
    # stub space for two section headers; raw offsets and all old RVAs stay put.
    nt=p.DOS_HEADER.e_lfanew;section_end=p.sections[-1].get_file_offset()+40
    assert nt>=0x100 and p.OPTIONAL_HEADER.SizeOfHeaders==0x400
    headers=b[nt:section_end]
    out[0x80:0x400]=bytes(0x380);out[0x80:0x80+len(headers)]=headers
    struct.pack_into('<I',out,0x3c,0x80)
    p=pefile.PE(data=out);off=lambda a:p.get_offset_from_rva(a-0x400000)
    assert p.OPTIONAL_HEADER.SizeOfImage<=CODE-0x400000
    ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
    patches=[]
    def patch(address,old,new):
        i=off(address);assert len(old)==len(new) and out[i:i+len(old)]==old,hex(address)
        out[i:i+len(new)]=new;patches.append((address,len(new)))
    patch(0x68c2e0,bytes.fromhex('558bec51894dfc'),asm(f'jmp {CODE};nop;nop',0x68c2e0))
    patch(0x7532b8,struct.pack('<I',0x801ce0),struct.pack('<I',CODE+0x180))
    patch(0x7532c0,struct.pack('<I',0x7fb680),struct.pack('<I',CODE+0x400))
    patch(0x7532c4,struct.pack('<I',0x68c470),struct.pack('<I',CODE+0xb00))
    patch(0x68c7d7,asm('call 0x5e33c0',0x68c7d7),asm(f'call {CODE+0x600}',0x68c7d7))
    patch(0x7fb780,out[off(0x7fb780):off(0x7fb780)+5],asm(f'jmp {CODE+0x500}',0x7fb780))
    patch(0x80180b,asm('call 0x801700',0x80180b),asm(f'call {CODE+0xf00}',0x80180b))
    patch(0x68dd60,bytes.fromhex('558bec83ec08'),asm(f'jmp {CODE+0x1200};nop',0x68dd60))
    patch(0x68e148,asm('push 0x75312c',0x68e148),asm(f'push {DATA+0x200}',0x68e148))
    if role_first:
        patch(0x68d1c0,bytes.fromhex('558bec6aff'),asm(f'jmp {CODE+0x1700}',0x68d1c0))
    if campaign_ui_name:
        original=b[off(0x7ff400):off(0x7ff400)+32]
        assert original.split(b'\0')[0]==b'campaigncoopv05.chui'
        name=campaign_ui_name.encode('ascii')+b'\0';assert len(name)<=32
        patch(0x7ff400,original,name.ljust(32,b'\0'))
    for a in (0x801900,0x801982,0x801a40):
        patch(a,asm('cmp dword ptr [0x7ff004],5',a),asm(f'call {CODE+0x1680};nop;nop',a))
    code=bytearray(b'\xcc'*0x2000);occupied=[]
    for addr,blob in sorted((routine_factory or routines)(asm,CODE,DATA).items()):
        pos=addr-CODE
        assert pos>=0 and pos+len(blob)<=len(code)
        assert all(pos>=end or pos+len(blob)<=start for start,end in occupied)
        assert sum(i.size for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(blob,addr))==len(blob)
        code[pos:pos+len(blob)]=blob;occupied.append((pos,pos+len(blob)))
    data=bytearray(0x2000)
    strings=[(0x200,f'cooppreselv{asset_version}{language}.chui'),(0x240,'coopPlayerLabel'),
        (0x260,'1P 装备' if language=='chs' else '1P LOADOUT'),(0x290,'2P 装备' if language=='chs' else '2P LOADOUT')
    ]
    if role_first:
        strings=[(p,t) for p,t in strings if p not in (0x260,0x290)]
        strings.extend([(0x260,'1P 角色' if language=='chs' else '1P CHARACTER'),
            (0x290,'2P 角色' if language=='chs' else '2P CHARACTER'),
            (0x2c0,'1P 装备' if language=='chs' else '1P LOADOUT'),
            (0x2f0,'2P 装备' if language=='chs' else '2P LOADOUT'),
            (0x320,'|FORWARD CONTINUE')])
    if short_titles:
        strings=[(pos,('1P' if pos in (0x260,0x2c0) else '2P') if pos in (0x260,0x290,0x2c0,0x2f0) else text) for pos,text in strings]
    if localized_prompts:
        strings=[(pos,text) for pos,text in strings if pos!=0x320]
        strings.extend([(0x320,'|FORWARD 继续' if language=='chs' else '|FORWARD CONTINUE'),
            (0x350,'|FORWARD 开始' if language=='chs' else '|FORWARD START')])
    for pos,text in strings:
        value=text.encode('utf-8')+b'\0';assert len(value)<0x30;data[pos:pos+len(value)]=value
    table=p.sections[-1].get_file_offset()+40;assert table+80<=p.OPTIONAL_HEADER.SizeOfHeaders
    for i,(name,va,payload,flags) in enumerate(((b'.precoop',CODE,code,0x60000020),(b'.predat',DATA,data,0xc0000040))):
        assert len(out)%512==0;raw=len(out);out.extend(payload)
        out[table+i*40:table+(i+1)*40]=struct.pack('<8sIIIIIIHHI',name,len(payload),va-0x400000,len(payload),raw,0,0,0,0,flags)
    struct.pack_into('<H',out,p.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),p.FILE_HEADER.NumberOfSections+2)
    struct.pack_into('<I',out,p.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),DATA+0x2000-0x400000)
    newpe=pefile.PE(data=out)
    assert len(newpe.sections)==p.FILE_HEADER.NumberOfSections+2 and newpe.OPTIONAL_HEADER.ImageBase==0x400000
    # Existing resources, all verified Boss hooks, native damage, and launcher
    # config bytes are exact. Only declared UI/sync sites and headers differ.
    original=pefile.PE(data=b)
    allowed={i for a,n in patches for i in range(off(a),off(a)+n)}
    assert all(i<0x400 or i in allowed for i,(old,new) in enumerate(zip(b,out)) if old!=new)
    for section in original.sections:
        n=next(s for s in newpe.sections if s.Name==section.Name)
        assert n.VirtualAddress==section.VirtualAddress and n.PointerToRawData==section.PointerToRawData
    for a,n in ((0x4ee3b0,0x80),(0x7fcc00,0x400),(0x7fc900,0x250),(0x7ff800,128)):
        assert out[off(a):off(a)+n]==b[off(a):off(a)+n]
    target.write_bytes(out)
    return dict(name=target.name,sha256=hashlib.sha256(out).hexdigest(),baseline_sha256=hashlib.sha256(b).hexdigest(),
        header_relocated_to='0x80',old_rvas_and_raw_offsets_unchanged=True,code=hex(CODE),data=hex(DATA),code_ranges=occupied,
        patches=[hex(a) for a,n in patches],native_damage_and_boss_fixes_unchanged=True,gameplay_verified=False)

if __name__=='__main__':
    dest=HERE/'dev';dest.mkdir(exist_ok=True)
    rows=[]
    for source in sorted((HERE.parent/'story-coop-v17-grab-anchor/dev').glob('*.exe')):
        rows.append(build(source,dest/source.name,source.stem.split('-')[-1]))
    assert len(rows)==4
    uirows={}
    for lang,source in [('en',HERE.parent/'story-coop-v05/final/equip-en.chui'),
        ('chs',HERE.parent/'story-coop-v14-transitions/game/data-pc/ui/singleplayerloadoutscreen.chui')]:
        uirows[lang]=ui(source,dest/f'cooppreselv18{lang}.chui')
    (HERE/'build-validation.json').write_text(json.dumps(dict(builds=rows,ui=uirows),indent=2)+'\n',encoding='utf-8')
    (HERE/'builds.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print('Built four isolated pre-level P1/P2 variants; gameplay validation pending.')
