"""Build direct campaign EXEs against the verified v25 keyboard baselines."""
import base64
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
sys.path[:0] = [str(WORK/'story-coop-v05'), str(WORK/'story-coop-v04')]
from native import GAME, pefile, b as stock, off as stock_offset
from chui import Reader
from keystone import Ks, KS_ARCH_X86, KS_MODE_32
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

BASE = 0x400000
CONFIG_FILE = 'Shank2-Coop-Keys.dat'
MAGIC = b'S2K1'
BUTTONS = (0x1000,0x4000,0x8000,0x2000,0x200,0x100)
DEFAULTS = (0x41,0x44,0x57,0x53,0x20,0x4a,0x4b,0x4c,0x55,0x49,0x0d,0x51,0x4f,
            0x25,0x27,0x26,0x28,0x60,0x61,0x62,0x63,0x64,0x65,0x67,0x66,0x75,0x76)
sha = lambda v: hashlib.sha256(v).hexdigest()
align = lambda n,a: (n+a-1)//a*a
u32 = lambda x: struct.pack('<I',x)


def baseline(lang):
    recipe = json.loads((WORK/f'story-coop-v25-recovery-hud/candidate/patch/keyboard-{lang}-addon.json').read_bytes())
    name = f'shank2-coop-v05-keyboard{"-chs" if lang=="chs" else ""}.exe'
    source = (WORK/'story-coop-v05/final'/name).read_bytes()
    assert sha(source) == recipe['input_sha256'] and len(source) == recipe['source_size']
    raw = bytearray(source)
    for row in recipe['patches']:
        pos = row['offset']
        before, after = (bytes.fromhex(row[key]) for key in ('before','after'))
        assert len(before)==len(after) and raw[pos:pos+len(before)]==before
        raw[pos:pos+len(before)]=after
    raw += base64.b64decode(recipe['append'])
    assert len(raw)==recipe['target_size'] and sha(raw)==recipe['output_sha256']
    return bytes(raw)


def labels(lang):
    folder = GAME if lang=='chs' else WORK/'story-coop-v09-fixes/upgrade-fixture'
    r=Reader((folder/'data-pc/ui/mainmenuscreen.chui').read_bytes())
    assert r.u32()==2
    [r.node() for _ in range(r.u32())]
    [r.node() for _ in range(r.u32())]
    assert r.pos==len(r.data)
    def label(name):
        r.pos=next(n['extra'] for n in r.nodes if n['name']==name)
        return r.string()
    return label('localMultiBtn'), label('quickMatchBtn')


def build(lang):
    source = baseline(lang)
    pe = pefile.PE(data=source)
    assert pe.OPTIONAL_HEADER.ImageBase==BASE and len(pe.sections) in (13,14)
    off = lambda a: pe.get_offset_from_rva(a-BASE)
    read = lambda a,n: source[off(a):off(a)+n]
    ptr = lambda a: struct.unpack('<I',read(a,4))[0]
    target = lambda a: a+5+struct.unpack('<i',read(a+1,4))[0]
    section = lambda name: BASE+next(s.VirtualAddress for s in pe.sections if s.Name.rstrip(b'\0')==name)
    c = BASE+pe.OPTIONAL_HEADER.SizeOfImage
    d = c+0x3000
    predat=section(b'.predat')
    code=bytearray(b'\xcc'*0x3000)
    data=bytearray(0x2000)
    out=bytearray(source)
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    md=Cs(CS_ARCH_X86,CS_MODE_32)
    asm=lambda s,a: bytes(ks.asm(s,a)[0])
    emitted={}
    edits=[]
    def put(r,s):
        a=c+r; blob=asm(s,a)
        assert sum(i.size for i in md.disasm(blob,a))==len(blob)
        assert all(r>=p+n or r+len(blob)<=p for p,n in emitted.items())
        assert r+len(blob)<=len(code)
        code[r:r+len(blob)]=blob
        emitted[r]=len(blob)
        return a
    def patch(a,before,after):
        assert len(before)==len(after) and read(a,len(before))==before
        assert all(a>=p+n or a+len(after)<=p for p,n in edits)
        out[off(a):off(a)+len(after)]=after;edits.append((a,len(after)))
    def jmp(a, old, to):
        assert sum(i.size for i in md.disasm(old,a))==len(old)
        patch(a,old,asm(f'jmp {to}',a).ljust(len(old),b'\x90'))
    def call(a, old, to):
        patch(a,asm(f'call {old}',a),asm(f'call {to}',a))
    def string(r,s,encoding='ascii'):
        suffix='\0'.encode(encoding)
        raw=s.encode(encoding)+suffix
        assert not any(data[r:r+len(raw)])
        data[r:r+len(raw)]=raw
        return d+r

    # Same application identity used by the existing launcher, now in the
    # executable itself. Set the original bin working directory before CRT.
    filename=string(0x100,CONFIG_FILE,'utf-16-le')
    kernel=string(0x150,'kernel32.dll')
    chdir=string(0x170,'SetCurrentDirectoryW')
    create=string(0x190,'CreateFileW')
    app=string(0x1b0,'SteamAppId')
    game=string(0x1c0,'SteamGameId')
    appid=string(0x1d0,'102840')
    cfg=d+0x80
    packet=MAGIC+u32(0)+struct.pack(f'<{len(DEFAULTS)}I',*DEFAULTS)
    assert len(packet)==116 and len(set(DEFAULTS))==len(DEFAULTS)
    data[0x80:0x80+len(packet)]=packet
    boot=put(0x000,f'''pushfd;pushad;cld
        push {appid};push {app};call dword ptr [0x72e018]
        push {appid};push {game};call dword ptr [0x72e018]
        push {kernel};call dword ptr [0x72e060]
        test eax,eax;jz done
        mov ebx,eax
        push {chdir};push ebx;call dword ptr [0x72e1f8]
        test eax,eax;jz done
        mov esi,eax
        push 2048;push {d+0x1000};push 0
        call dword ptr [0x72e0c0]
        cmp eax,1;jbe done
        cmp eax,2048;jae done
        lea edx,[{d+0x1000}+eax*2]
        path:sub edx,2
        cmp edx,{d+0x1000};jbe done
        cmp word ptr [edx],92;jne path
        mov word ptr [edx],0
        push {d+0x1000};call esi
        test eax,eax;jz done
        push {create};push ebx;call dword ptr [0x72e1f8]
        test eax,eax;jz done
        push 0;push 0x80;push 3;push 0;push 7;push 0x80000000;push {filename}
        call eax
        cmp eax,-1;je done
        mov edi,eax
        push 0;push {d+0x600};push {len(packet)+1};push {d+0x620};push edi
        call dword ptr [0x72e13c]
        mov esi,eax
        push edi;call dword ptr [0x72e17c]
        test esi,esi;jz done
        cmp dword ptr [{d+0x600}],{len(packet)};jne done
        call {c+0x2700}
        done:popad;popfd;jmp {BASE+pe.OPTIONAL_HEADER.AddressOfEntryPoint}''')
    # Only copy a complete validated packet. Malformed config leaves defaults.
    put(0x2700,f'''cmp dword ptr [{d+0x620}],{int.from_bytes(MAGIC,'little')};jne invalid
        cmp dword ptr [{d+0x624}],1;ja invalid
        mov ecx,{len(DEFAULTS)};mov esi,{d+0x628}
        keycheck:mov eax,[esi];add esi,4;dec eax;cmp eax,253;ja invalid;loop keycheck
        mov ecx,{len(packet)//4};mov esi,{d+0x620};mov edi,{cfg};rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        invalid:ret''')
    struct.pack_into('<I',out,pe.OPTIONAL_HEADER.get_field_absolute_offset('AddressOfEntryPoint'),boot-BASE)

    # Reuse native XInput and vibration thunks when physical pads are selected.
    def key(i): return cfg+8+i*4
    lines=[f'''cmp dword ptr [{cfg+4}],1;je physical
        cmp dword ptr [esp+4],2;jae physical
        push ebp;mov ebp,esp;push esi
        mov esi,[ebp+12];test esi,esi;jz bad
        xor eax,eax;mov [esi+4],eax;mov [esi+8],eax;mov [esi+12],eax
        inc dword ptr [0x7ff080];mov eax,[0x7ff080];mov [esi],eax
        call dword ptr [0x72e234];cmp eax,[0x7d7ed4];jne done
        cmp dword ptr [ebp+8],0;jne player2''']
    for player,first in enumerate((0,13)):
        if player: lines.append('player2:')
        def mapkey(i,instruction):
            return f'''push dword ptr [{key(i)}];call dword ptr [0x72e224]
                test ax,0x8000;jz key{i}_done;{instruction};key{i}_done:'''
        for i,(off2,val) in enumerate(((8,-32767),(8,32767),(10,32767),(10,-32767))):
            lines.append(mapkey(first+i,f'mov word ptr [esi+{off2}],{val}'))
        for i,mask in enumerate(BUTTONS):
            lines.append(mapkey(first+4+i,f'or word ptr [esi+4],{mask}'))
        next_key=first+10
        if not player:
            lines.append(f'push dword ptr [{key(next_key)}];call 0x801c00')
            next_key+=1
        for i in range(2): lines.append(mapkey(next_key+i,f'mov byte ptr [esi+{6+i}],255'))
        lines.append('jmp done')
    lines.append('''done:xor eax,eax;jmp finish
        bad:mov eax,87
        finish:pop esi;pop ebp;ret 8
        physical:jmp dword ptr [0x72e294]''')
    state=put(0x400,'\n'.join(lines))
    for i,(a,old,iat) in enumerate([(0x6655ce,0x7fd000,0x72e294),(0x6655c2,0x7fdb00,0x72e290),
                        (0x6655b6,0x7fdc00,0x72e288),(0x6655c8,0x7fdd00,0x72e298)]):
        wrapper=state if not i else put(0x800+i*0x20,f'''cmp dword ptr [{cfg+4}],1;je physical
            jmp {old}
            physical:jmp dword ptr [{iat}]''')
        patch(a,asm(f'jmp {old};nop',a),asm(f'jmp {wrapper};nop',a))
    for i,(section_name,vk) in enumerate(((b'.coop',0x75),(b'.camx',0x76))):
        start=section(section_name)
        sig=bytes((0x6a,vk))+bytes.fromhex('ff1524e27200')
        matches=list(re.finditer(re.escape(sig),read(start,0x5000 if not i else 0x1000)))
        assert len(matches)==1
        a=start+matches[0].start()
        # Keep the existing edge latch and only replace the configured key.
        patch(a,sig,asm(f'call {c+0x8c0+i*0x20};nop;nop;nop',a))
        put(0x8c0+i*0x20,f'push dword ptr [{key(25+i)}];call dword ptr [0x72e224];ret')

    # Shared submenu widgets live in the native MainMenuScreen. Restore the
    # survival-only buttons and their visibility when leaving Campaign.
    submenu=d
    mode=d+4
    old1,old2=labels(lang)
    solo=string(0x200,'单人战役' if lang=='chs' else 'Single Player','utf-8')
    duo=string(0x240,'本地双人' if lang=='chs' else 'Local Co-op','utf-8')
    local=string(0x280,old1,'utf-8')
    quick=string(0x2c0,old2,'utf-8')
    others=(0x298,0x2cc,0x300,0x334)
    save='\n'.join(f'''mov eax,[ebx+{o+4}];test eax,eax;jz skip{i}
        mov dl,[eax+0x31];mov [{d+0x10+i}],dl
        lea eax,[ebx+{o}];xor edx,edx;call 0x5e4180
        skip{i}:''' for i,o in enumerate(others))
    restore='\n'.join(f'lea eax,[ebx+{o}];mov dl,[{d+0x10+i}];call 0x5e4180' for i,o in enumerate(others))
    open_menu=put(0xa00,f'''push ebx;mov ebx,ecx
        cmp [{submenu}],ebx;je focus
        mov [{submenu}],ebx
        mov dword ptr [{mode}],0
        lea eax,[ebx+0x230];mov ecx,{solo};call 0x5e59c0
        lea eax,[ebx+0x264];mov ecx,{duo};call 0x5e59c0
        {save}
        lea eax,[ebx+0xd88];mov dl,1;call 0x5e4180
        mov byte ptr [ebx+0xc00],1
        focus:push 1;lea eax,[ebx+0x230];call 0x5e4230
        pop ebx;ret 4''')
    close_menu=put(0xb40,f'''cmp [{submenu}],ecx;jne done
        push ebx;mov ebx,ecx
        mov dword ptr [{submenu}],0
        lea eax,[ebx+0x230];mov ecx,{local};call 0x5e59c0
        lea eax,[ebx+0x264];mov ecx,{quick};call 0x5e59c0
        {restore}
        lea eax,[ebx+0xd88];xor edx,edx;call 0x5e4180
        pop ebx
        done:ret''')
    start_campaign=put(0xc40,'push ebp;mov ebp,esp;sub esp,0x10;jmp 0x6b6f86')
    jmp(0x6b6f80,bytes.fromhex('558bec83ec10'),open_menu)
    patch(0x6b6f9b,u32(0x6b6f80),u32(start_campaign))
    for i,original in enumerate((0x6b7440,0x6b72d0)):
        select=put(0xd00+i*0x80,f'''cmp [{submenu}],ecx;jne native
            push ecx;call {close_menu};pop ecx
            mov dword ptr [{mode}],{i}
            jmp {start_campaign}
            native:push ebp;mov ebp,esp;push -1;jmp {original+5}''')
        jmp(original,bytes.fromhex('558bec6aff'),select)
    survival=put(0xe00,f'''push ecx;call {close_menu};pop ecx
        mov dword ptr [{mode}],0
        push ebp;mov ebp,esp;push -1;jmp 0x6b78f5''')
    jmp(0x6b78f0,bytes.fromhex('558bec6aff'),survival)
    tutorial=put(0xe40,f'''cmp [{submenu}],ecx;je ignore
        push ebp;mov ebp,esp;push ecx;mov [ebp-4],ecx;jmp 0x6b6367
        ignore:ret 4''')
    jmp(0x6b6360,bytes.fromhex('558bec51894dfc'),tutorial)
    back=put(0xe80,f'''push ebx;mov ebx,ecx;push dword ptr [esp+8];call 0x6b60c0
        test al,al;jz done
        push eax;mov ecx,ebx;call {close_menu};pop eax
        done:pop ebx;ret 4''')
    clear=put(0xf80,'''mov dword ptr [0x7ff004],0;mov dword ptr [0x7ff00c],0
        mov dword ptr [0x7ff010],0;mov dword ptr [0x7ff024],0;ret''')
    show=put(0xf00,f'''push ecx;call {close_menu};pop ecx
        mov dword ptr [{submenu}],0;call {clear};jmp 0x6b7ab0''')
    patch(0x752f7c,u32(0x6b7ab0),u32(show))
    patch(0x752f8c,u32(0x6b60c0),u32(back))

    # Only the selected campaign path may construct player two. Leave native
    # single player controller IDs and resource lookups intact.
    init=put(0x1000,f'''cmp dword ptr [{mode}],1;je coop
        call {clear};jmp 0x6a9290
        coop:jmp 0x7fa000''')
    patch(0x750280,u32(0x7fa000),u32(init))
    load=put(0x1080,f'''cmp dword ptr [{mode}],1;je coop
        jmp 0x434c00
        coop:jmp 0x7fe700''')
    call(0x4346a0,0x7fe700,load)
    solo_hud=string(0x300,f'coopsolo26hud{lang}.chui')
    solo_loadout=string(0x340,f'coopsolo26sel{lang}.chui')
    for i,(a,coop_path,solo_path) in enumerate(((0x6968d8,0x7ff400,solo_hud),
                  (0x67b61b,0x802220,0x7546e0),(0x68e148,predat+0x200,solo_loadout))):
        wrapper=put(0x1100+i*0x40,f'''pushfd
            cmp dword ptr [{mode}],1;je coop
            popfd;push {solo_path};jmp {a+5}
            coop:popfd;push {coop_path};jmp {a+5}''')
        jmp(a,asm(f'push {coop_path}',a),wrapper)
    for i,(a,original) in enumerate(((0x696a19,0x672c00),(0x6956fd,0x66e820))):
        current=target(a)
        wrapper=put(0x1200+i*0x40,f'''cmp dword ptr [{mode}],1;je coop
            jmp {original}
            coop:jmp {current}''')
        call(a,current,wrapper)
    for i,(a,native) in enumerate(((0x751e08,0x6966a0),(0x7532b8,0x801ce0))):
        current=ptr(a)
        wrapper=put(0x1300+i*0x40,f'''cmp dword ptr [{mode}],1;je coop
            jmp {native}
            coop:jmp {current}''')
        patch(a,u32(current),u32(wrapper))
    p1action=ptr(0x67baff)
    wrapper=put(0x1380,f'''cmp dword ptr [{mode}],1;je coop
        mov dword ptr [0x802100],0;jmp 0x67b040
        coop:jmp {p1action}''')
    patch(0x67baff,u32(p1action),u32(wrapper))
    # Native pre-level non-coop readers still share the palette/fixes.
    assert read(0x7ff800,4)==read(0x7ff840,4)==u32(1)

    headers=pe.sections[-1].get_file_offset()+40
    assert headers+80<=pe.OPTIONAL_HEADER.SizeOfHeaders
    for i,(name,va,buf,flags) in enumerate(((b'.direct',c,code,0x60000020),(b'.dirdata',d,data,0xc0000040))):
        assert len(out)%pe.OPTIONAL_HEADER.FileAlignment==0
        raw=len(out);out.extend(buf)
        struct.pack_into('<8sIIIIIIHHI',out,headers+40*i,name,len(buf),va-BASE,len(buf),raw,0,0,0,0,flags)
    struct.pack_into('<H',out,pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),len(pe.sections)+2)
    struct.pack_into('<I',out,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),d+len(data)-BASE)
    for field,increase in [('SizeOfCode',len(code)),('SizeOfInitializedData',len(data))]:
        struct.pack_into('<I',out,pe.OPTIONAL_HEADER.get_field_absolute_offset(field),getattr(pe.OPTIONAL_HEADER,field)+increase)
    checked=pefile.PE(data=out)
    assert len(checked.sections)==len(pe.sections)+2 and checked.OPTIONAL_HEADER.AddressOfEntryPoint==boot-BASE
    allowed={p for a,n in edits for p in range(off(a),off(a)+n)}
    assert all(i<0x400 or i in allowed for i,(x,y) in enumerate(zip(source,out)) if x!=y)
    for old,new in zip(pe.sections,checked.sections):
        assert (old.VirtualAddress,old.PointerToRawData,old.Name)==(new.VirtualAddress,new.PointerToRawData,new.Name)
    return bytes(out),dict(language=lang,baseline_sha256=sha(source),sha256=sha(out),code=hex(c),data=hex(d),
                            edits=[hex(a) for a,n in edits],key_count=len(DEFAULTS),test_assists=False)


if __name__=='__main__':
    dest=HERE/'dev'
    dest.mkdir(exist_ok=True)
    report=[]
    from assets import build_solo_assets
    for lang in ('en','chs'):
        raw,row=build(lang)
        (dest/f'shank2-story-coop-{lang}.exe').write_bytes(raw)
        row['solo_assets']=build_solo_assets(lang,dest)
        report.append(row)
    (HERE/'builds.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Built two direct EXEs from verified v25 baselines.')






