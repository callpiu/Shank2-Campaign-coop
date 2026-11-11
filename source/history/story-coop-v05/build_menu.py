"""Reuse native campaign loadout UI for either player, with live persistence."""
from pathlib import Path
import sys,struct,json,hashlib
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parent/'story-coop-v04')]
from native import pefile
from chui import Reader
from loadout_code import hash_name
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
TEST=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')

def string(s):
    b=s.encode('utf8');assert len(b)<128;return bytes([len(b)])+b

def ui(source,dest,english=False):
    b=source.read_bytes();r=Reader(b);assert r.u32()==2
    [r.node() for _ in range(r.u32())];countpos=r.pos;count=r.u32();roots=[r.node() for _ in range(count)];assert r.pos==len(b)
    target=next(n for n in roots if n['name']=='loadoutBtn')
    def clone(player):
        # Preserve the button's native fonts, state styles and signal behavior.
        raw=b[target['start']:target['end']];name='loadoutBtn' if player==1 else 'coopLoadout2Btn'
        endname=4+len(string('loadoutBtn'))
        out=bytearray(raw[:4]+string(name)+raw[endname:])
        shift=len(string(name))-len(string('loadoutBtn'))
        common=target['common']-target['start']+shift
        struct.pack_into('<f',out,common,.4 if player==1 else .6)
        struct.pack_into('<f',out,common+8,.18)
        extra=target['extra']-target['start']+shift
        rr=Reader(bytes(out));rr.pos=extra;rr.string();after=rr.pos
        text=f'P{player} LOADOUT' if english else f'{player}P 装备'
        out[extra:after]=string(text)
        rr=Reader(bytes(out));rr.pos=extra;rr.string();rr.string();rr.font()
        navstart=rr.pos;[rr.string() for _ in range(4)];navend=rr.pos
        # left,right,up,down navigation: either mouse or one keyboard works.
        out[navstart:navend]=b''.join(map(string,['loadoutBtn' if player==2 else '', 'coopLoadout2Btn' if player==1 else '', 'resumeBtn','helpOptionsBtn']))
        return bytes(out)
    one=clone(1);two=clone(2);out=bytearray(b[:target['start']]+one+b[target['end']:]);struct.pack_into('<I',out,countpos,count+1);out.extend(two)
    check=Reader(out);check.u32();[check.node() for _ in range(check.u32())];nodes=[check.node() for _ in range(check.u32())];assert check.pos==len(out)
    assert any(n['name']=='coopLoadout2Btn' for n in nodes)
    dest.write_bytes(out);return {'source_sha256':hashlib.sha256(b).hexdigest(),'target_sha256':hashlib.sha256(out).hexdigest(),'roots':len(nodes)}

def equipment_ui(source,dest):
    b=source.read_bytes();r=Reader(b);assert r.u32()==2
    [r.node() for _ in range(r.u32())];[r.node() for _ in range(r.u32())];assert r.pos==len(b)
    node=next(n for n in r.nodes if n['name']=='skinspinner')
    out=bytearray(b);assert out[node['common']+24]==1
    out[node['common']+24]=0
    dest.write_bytes(out)
    return {'source_sha256':hashlib.sha256(b).hexdigest(),'target_sha256':hashlib.sha256(out).hexdigest(),'costume_selector_hidden':True}

def build(source=None,dest=None,versioned=False,write_ui=True):
    source=Path(source) if source else HERE/'shank2-coop-v05-terrain-test.exe'
    dest=Path(dest) if dest else HERE/'shank2-coop-v05-menu-test.exe'
    b=source.read_bytes();pe=pefile.PE(data=b);out=bytearray(b)
    sections={s.Name.rstrip(b'\0'):s for s in pe.sections}
    code=0x400000+sections[b'.terrain'].VirtualAddress;data=0x400000+sections[b'.terdata'].VirtualAddress
    off=lambda va:pe.get_offset_from_rva(va-0x400000)
    asm=lambda s,a:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(s,a)[0])
    patches=[]
    def patch(va,before,after):
        assert b[off(va):off(va)+len(before)]==before,hex(va)
        assert len(before)==len(after);out[off(va):off(va)+len(after)]=after;patches.append(hex(va))
    routines={}
    # Global ordinal is only consulted by the native pause loadout callbacks.
    getplayer=asm(f'''cmp dword ptr [esp], 0x67b073
je selected
cmp dword ptr [esp], 0x67b284
jne native
selected:
cmp dword ptr [0x7ff004], 5
jne native
mov eax, dword ptr [{data+0x100}]
mov dword ptr [esp+4], eax
native:
jmp 0x6a9640''',code+0x400);routines[0x400]=getplayer
    patch(0x7501a8,struct.pack('<I',0x6a9640),struct.pack('<I',code+0x400))
    getter=asm(f'''cmp dword ptr [{data+0x100}], 1
jne native
jmp 0x408d70
native:
jmp 0x404960''',code+0x450);routines[0x450]=getter
    for va in [0x67b093,0x67b0a6]:patch(va,b'\xe8'+struct.pack('<i',0x404960-va-5),asm(f'call {code+0x450}',va))
    for player,offset in [(0,0x480),(1,0x4b0)]:
        routines[offset]=asm(f'''cmp dword ptr [0x7ff004], 5
jne ignore
mov dword ptr [{data+0x100}], {player}
mov dword ptr [{data+0x144}], 0
inc dword ptr [{data+0x104+player*4}]
jmp 0x67b040
ignore:
ret 4''',code+offset)
    patch(0x67bafe,b'\x68'+struct.pack('<I',0x67b040),b'\x68'+struct.pack('<I',code+0x480))
    # The native reference wrapper owns the button signal, so P2 needs its own
    # properly constructed/destroyed wrapper rather than reusing P1's wrapper.
    init=asm(f'''
push esi
push edi
sub esp, 8
mov esi, dword ptr [ebp-0x80]
mov dword ptr [{data+0x10c}], esi
mov dword ptr [{data+0x160}], 0
mov edi, {data+0x300}
cmp dword ptr [{data+0x120}], 0
je construct
mov ecx, edi
call 0x4604e0
construct:
push edi
call 0x5e5920
mov dword ptr [{data+0x120}], 1
push edi
mov ecx, {data+0x200}
mov eax, esi
call 0x5e3e00
push {code+0x4b0}
push esi
lea eax, [esp+8]
push eax
call 0x45ff70
add esp, 12
mov ecx, edi
call 0x5e5a00
inc dword ptr [{data+0x110}]
add esp, 8
pop edi
pop esi
mov dword ptr [ebp-4], 0xffffffff
jmp 0x67bb28
''',code+0x500);routines[0x500]=init
    patch(0x67bb21,bytes.fromhex('c745fcffffffff'),asm(f'jmp {code+0x500}',0x67bb21)+b'\x90\x90')
    cleanup=asm(f'''call 0x4604e0
cmp dword ptr [{data+0x120}], 0
je done
mov ecx, {data+0x300}
call 0x4604e0
mov dword ptr [{data+0x120}], 0
mov dword ptr [{data+0x10c}], 0
done:
ret''',code+0x850);routines[0x850]=cleanup
    patch(0x4600a6,b'\xe8'+struct.pack('<i',0x4604e0-0x4600a6-5),asm(f'call {code+0x850}',0x4600a6))
    patch(0x67b61b,b'\x68'+struct.pack('<I',0x7546e0),b'\x68'+struct.pack('<I',data+0x220))
    # The shared native screen also serves pre-level equipment selection.
    # Only the in-level co-op menu uses our costume-hidden variant.
    equipment_path=asm(f'''pushfd
cmp dword ptr [0x7ff004], 5
jne native
popfd
push {data+0x240}
jmp 0x68e14d
native:
popfd
push 0x75312c
jmp 0x68e14d''',code+0xd80);routines[0xd80]=equipment_path
    patch(0x68e148,b'\x68'+struct.pack('<I',0x75312c),asm(f'jmp {code+0xd80}',0x68e148))
    # Native setters keep inventory logic, including no-ammunition refills.
    apply=asm(f'''
push ebp
mov ebp, esp
push esi
push edi
push ebx
push dword ptr [ebp+28]
push dword ptr [ebp+24]
push dword ptr [ebp+20]
push dword ptr [ebp+16]
push dword ptr [ebp+12]
push dword ptr [ebp+8]
call 0x67b250
cmp dword ptr [0x7ff004], 5
jne done
mov eax, dword ptr [{data+0x100}]
mov ecx, dword ptr [0x7ff00c+eax*4]
test ecx, ecx
jz done
call 0x40d7c0
test eax, eax
jz done
mov ecx, eax
push dword ptr [ebp+20]
call 0x40bc90
call {code+0x700}
inc dword ptr [{data+0x114}]
done:
pop ebx
pop edi
pop esi
pop ebp
ret 24
''',code+0x600);routines[0x600]=apply
    patch(0x67b928,b'\x68'+struct.pack('<I',0x67b250),b'\x68'+struct.pack('<I',code+0x600))
    # Synchronize actual equipment to the next-level descriptors. This reads
    # inventory; it never overwrites an in-level weapon selected by the game.
    sync=asm(f'''
push esi
push edi
push ebx
cmp dword ptr [0x7ff004], 5
jne done
xor ebx, ebx
loopplayer:
mov ecx, dword ptr [0x7ff00c+ebx*4]
test ecx, ecx
jz nextplayer
call 0x40d7c0
test eax, eax
jz nextplayer
mov esi, eax
mov edi, ebx
shl edi, 6
add edi, 0x7ff800
mov eax, dword ptr [esi+0x2c]
mov dword ptr [edi+24], eax
mov eax, dword ptr [esi+0x30]
mov dword ptr [edi+28], eax
mov eax, dword ptr [esi+0x48]
mov dword ptr [edi+32], eax
mov eax, dword ptr [esi+0x4c]
mov dword ptr [edi+36], eax
nextplayer:
inc ebx
cmp ebx, 2
jb loopplayer
inc dword ptr [{data+0x118}]
done:
pop ebx
pop edi
pop esi
ret
''',code+0x700);routines[0x700]=sync
    # Call the confirmed terrain step, then persist actual inventory choices.
    step=asm(f'''push ebp
mov ebp, esp
push dword ptr [ebp+8]
call {code}
call {code+0x700}
pop ebp
ret 4''',code+0x800);routines[0x800]=step
    patch(0x750188,struct.pack('<I',code),struct.pack('<I',code+0x800))
    # Filter only the weapon spinner's population loop. Metadata and unlock
    # trees stay native/read-only. Record the source index of each visible row
    # so native selection resolves the right item after locked rows are skipped.
    category=f"""cmp eax, {hash_name('melee')}
+je melee
+cmp eax, {hash_name('ranged')}
+je ranged
+mov edx, {data+0x480}
+jmp ready
+melee:
+mov edx, {data+0x400}
+jmp ready
+ranged:
+mov edx, {data+0x440}
+ready:""".replace('\n+','\n')
    reset=asm(f"""cmp dword ptr [0x7ff004], 5
+jne native
+push ebp
+mov ebp, esp
+push dword ptr [ebp+12]
+push dword ptr [ebp+8]
+call 0x6bfb30
+push eax
+mov eax, dword ptr [ebp+12]
+{category}
+mov dword ptr [edx], 0
+mov dword ptr [edx+4], 0
+pop eax
+pop ebp
+ret 8
+native:
+jmp 0x6bfb30""".replace('\n+','\n'),code+0x900);routines[0x900]=reset
    patch(0x68cd54,b'\xe8'+struct.pack('<i',0x6bfb30-0x68cd54-5),asm(f'call {code+0x900}',0x68cd54))
    filtercode=asm(f"""pushfd
+pushad
+cmp dword ptr [0x7ff004], 5
+jne passthrough
+mov eax, dword ptr [ebp-0x22c]
+mov dword ptr [{data+0x140}], eax
+mov eax, dword ptr [eax+0x20]
+mov dword ptr [{data+0x148}], eax
+mov eax, dword ptr [ebp-0x230]
+mov dword ptr [{data+0x14c}], eax
+shl eax, 6
+add eax, {data+0x400}
+mov edi, eax
+inc dword ptr [edi+4]
+lea ecx, [ebp-0x80]
+call 0x46fea0
+cmp byte ptr [eax+0x58], 0
+jne allowed
+push eax
+lea ecx, [ebp-0x7c]
+call 0x697680
+test al, al
+jz skip
+allowed:
+mov ecx, dword ptr [edi]
+cmp ecx, 9
+jae skip
+mov eax, dword ptr [edi+4]
+dec eax
+mov dword ptr [edi+8+ecx*4], eax
+inc dword ptr [edi]
+inc dword ptr [{data+0x150}]
+passthrough:
+popad
+popfd
+lea ecx, [ebp-0x1f4]
+jmp 0x68cda5
+skip:
+inc dword ptr [{data+0x154}]
+popad
+popfd
+jmp 0x68cd74""".replace('\n+','\n'),code+0x980);routines[0x980]=filtercode
    patch(0x68cd9f,bytes.fromhex('8d8d0cfeffff'),asm(f'jmp {code+0x980}',0x68cd9f)+b'\x90')
    lookup=asm(f"""cmp dword ptr [0x7ff004], 5
+jne native
+push ecx
+mov eax, dword ptr [esp+12]
+{category}
+mov eax, dword ptr [esp+16]
+cmp eax, dword ptr [edx]
+jae empty
+mov eax, dword ptr [edx+8+eax*4]
+mov dword ptr [esp+16], eax
+pop ecx
+jmp 0x6bfa80
+empty:
+pop ecx
+xor eax, eax
+ret 12
+native:
+jmp 0x6bfa80""".replace('\n+','\n'),code+0xa40);routines[0xa40]=lookup
    patch(0x68d7cb,b'\xe8'+struct.pack('<i',0x6bfa80-0x68d7cb-5),asm(f'call {code+0xa40}',0x68d7cb))
    family_calls=[]
    # Both local characters use the host campaign's unlock progress. Keep P2's
    # input device unchanged; only profile lookup is redirected in this screen.
    profile=asm('''cmp dword ptr [0x7ff004], 5
jne native
mov eax, dword ptr [0x7ff014]
mov dword ptr [esp+4], eax
native:
jmp 0x404d70''',code+0xb00);routines[0xb00]=profile
    profile_calls=[]
    for va in range(0x68c000,0x68e600):
        at=off(va)
        if b[at]==0xe8 and va+5+struct.unpack_from('<i',b,at+1)[0]==0x404d70:
            profile_calls.append(va)
            patch(va,b[at:at+5],asm(f'call {code+0xb00}',va))
    assert profile_calls
    # Enter is Start during play and A/confirm in the pause UI. Latch the
    # meaning until key-up, preventing one held key from opening and closing
    # the menu or becoming a jump immediately after resuming.
    shown=asm(f'mov dword ptr [{data+0x160}], 1; jmp 0x67b4d0',code+0xb80)
    hidden=asm(f'mov dword ptr [{data+0x160}], 0; jmp 0x67b450',code+0xba0)
    routines[0xb80]=shown;routines[0xba0]=hidden
    patch(0x754768,struct.pack('<I',0x67b4d0),struct.pack('<I',code+0xb80))
    patch(0x754770,struct.pack('<I',0x67b450),struct.pack('<I',code+0xba0))
    # Equipment screens bind Continue to A, while gameplay binds Enter to Start.
    # Track their native show/hide lifecycle separately from the pause dialog.
    routines[0xce0]=asm(f'mov dword ptr [{data+0x170}], 1; jmp 0x68de70',code+0xce0)
    routines[0xd00]=asm(f'mov dword ptr [{data+0x170}], 0; jmp 0x68c330',code+0xd00)
    patch(0x7532b8,struct.pack('<I',0x68de70),struct.pack('<I',code+0xce0))
    patch(0x7532c0,struct.pack('<I',0x68c330),struct.pack('<I',code+0xd00))
    enter=asm(f'''
push ebx
push dword ptr [esp+8]
call dword ptr [0x72e224]
movzx ebx, ax
test bx, 0x8000
jnz held
mov dword ptr [{data+0x164}], 0
jmp done
held:
cmp dword ptr [{data+0x164}], 0
jne mapped
mov eax, dword ptr [{data+0x160}]
inc eax
cmp dword ptr [{data+0x170}], 0
je latch
mov eax, 3
latch:
mov dword ptr [{data+0x164}], eax
mapped:
cmp dword ptr [{data+0x164}], 1
jne confirm
or word ptr [esi+4], 0x10
inc dword ptr [{data+0x16c}]
jmp done
confirm:
cmp dword ptr [{data+0x164}], 3
je equipment
cmp dword ptr [{data+0x160}], 1
jne done
jmp sendconfirm
equipment:
cmp dword ptr [{data+0x170}], 1
jne done
sendconfirm:
or word ptr [esi+4], 0x1000
inc dword ptr [{data+0x168}]
done:
mov eax, ebx
pop ebx
ret 4
''',code+0xc00);routines[0xc00]=enter
    keypattern=bytes.fromhex('6a0dff1524e27200')
    keyat=b.find(keypattern,off(0x7fd000),off(0x7fdb00))
    if keyat>=0:
        assert b.find(keypattern,keyat+1,off(0x7fdb00))<0
        callva=pe.get_rva_from_offset(keyat+2)+0x400000
        patch(callva,keypattern[2:],asm(f'call {code+0xc00}',callva)+b'\x90')
        startbytes=bytes.fromhex('66834e0410');startat=b.find(startbytes,keyat+8,keyat+48);assert startat>=0
        startva=pe.get_rva_from_offset(startat)+0x400000
        patch(startva,startbytes,b'\x90'*5)
    md=Cs(CS_ARCH_X86,CS_MODE_32);occupied=[]
    for rel,blob in routines.items():
        assert rel+len(blob)<4096 and all(rel>=end or rel+len(blob)<=start for start,end in occupied)
        assert sum(i.size for i in md.disasm(blob,code+rel))==len(blob)
        out[off(code+rel):off(code+rel)+len(blob)]=blob;occupied.append((rel,rel+len(blob)))
    pause_name='pausecoopv05.chui' if versioned else 'pausecoop.chui'
    equip_name='equipcoopv05.chui' if versioned else 'equipcoop.chui'
    for rel,s in [(0x200,b'coopLoadout2Btn\0'),(0x220,pause_name.encode()+b'\0'),(0x240,equip_name.encode()+b'\0')]:out[off(data+rel):off(data+rel)+len(s)]=s
    if versioned:
        campaign=off(0x7ff400);assert b[campaign:campaign+32].startswith(b'campaigncoop.chui\0')
        out[campaign:campaign+32]=b'campaigncoopv05.chui\0'.ljust(32,b'\0')
    dest.write_bytes(out)
    report={'sha256':hashlib.sha256(out).hexdigest(),'patches':patches,'native_unlock_filter':'Weapon rows only: alwaysUnlocked or native host weapon IsUnlocked(697680); visible-to-source index map','code':hex(code),'data':hex(data),'keyboard_enter':keyat>=0,'status':'requires runtime UI validation'}
    if write_ui:
        report['ui']=ui(TEST/'data-pc/ui/pausedialog.chui',TEST/'data-pc/ui'/pause_name)
        report['equipment_ui']=equipment_ui(TEST/'data-pc/ui/singleplayerloadoutscreen.chui',TEST/'data-pc/ui'/equip_name)
    dest.with_suffix('.menu.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
    return report

if __name__=='__main__':build()
