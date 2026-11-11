"""Render Corina's own hit pose while grabbed by Magnus, using a packet copy."""
import hashlib
import json
import struct
import sys
from build_teleport import HERE,Ks,KS_ARCH_X86,KS_MODE_32,pefile
sys.path.insert(0,str(HERE.parent/'story-coop-v04'))
from loadout_code import hash_name

CODE=0x7fcc00
NATIVE=0x511460
TRAMPOLINE=CODE+0x180
PACKET_SIZE=0x26c  # verified native allocation/contiguous live packet stride
PROLOGUE=bytes.fromhex('558bec83e4f8')
FEMALE=hash_name('corina');BOSS=hash_name('boss_magnus');POSE=hash_name('hit_mid1')

def routine(asm,code=CODE,diag=0x7ff000,native=TRAMPOLINE,lookup=0x513170):
    return asm(f'''push ebp
        mov ebp,esp
        sub esp,0x270
        push ebx
        push esi
        push edi
        mov ebx,[ebp+12]
        cmp dword ptr [{diag+4}],5
        jne original
        test ebx,ebx
        jz original
        cmp dword ptr [ebx],0x759294
        jne original
        cmp dword ptr [ebx+0x7c],{FEMALE}
        jne original
        mov eax,[ebx+0x70]
        cmp eax,-1
        je original
        mov ecx,[ebp+8]
        test ecx,ecx
        jz original
        cmp dword ptr [ecx],0
        je original
        push dword ptr [ecx]
        call {lookup}
        test eax,eax
        jz original
        cmp dword ptr [eax],0x759294
        jne original
        cmp dword ptr [eax+0x7c],{BOSS}
        jne original
        lea edi,[ebp-0x270]
        mov esi,ebx
        mov ecx,{PACKET_SIZE//4}
        cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        lea ebx,[ebp-0x270]
        mov dword ptr [ebx+0x70],-1
        mov dword ptr [ebx+0x90],{POSE}
        mov dword ptr [ebx+0x98],0x3dcccccd
        mov byte ptr [ebx+0x6c],0
        original:
        push dword ptr [ebp+16]
        push ebx
        push dword ptr [ebp+8]
        call {native}
        add esp,12
        pop edi
        pop esi
        pop ebx
        mov esp,ebp
        pop ebp
        ret''',code)

def build(source,target):
    b=source.read_bytes();pe=pefile.PE(data=b);offset=lambda a:pe.get_offset_from_rva(a-0x400000)
    ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
    code=routine(asm)
    assert len(code)<TRAMPOLINE-CODE
    trampoline=asm('push ebp;mov ebp,esp;and esp,-8;jmp 0x511466',TRAMPOLINE)
    assert b[offset(NATIVE):offset(NATIVE)+6]==PROLOGUE
    assert b[offset(CODE):offset(CODE)+0x200]==b'\xcc'*0x200
    out=bytearray(b)
    out[offset(CODE):offset(CODE)+len(code)]=code
    out[offset(TRAMPOLINE):offset(TRAMPOLINE)+len(trampoline)]=trampoline
    out[offset(NATIVE):offset(NATIVE)+6]=asm(f'jmp {CODE};nop',NATIVE)
    target.write_bytes(out)
    return dict(name=target.name,sha256=hashlib.sha256(out).hexdigest(),base_sha256=hashlib.sha256(b).hexdigest(),
                render_packet_copy_only=True,grapple_and_damage_unchanged=True,pose='hit_mid1 at 0.1s',code_size=len(code))

if __name__=='__main__':
    target=HERE/'combined';target.mkdir(exist_ok=True)
    rows=[]
    for source in sorted((HERE/'dev').glob('*.exe')):rows.append(build(source,target/source.name))
    (HERE/'combined-builds.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print('Built four isolated combined variants; simulation, grapple damage and release functions unchanged.')
