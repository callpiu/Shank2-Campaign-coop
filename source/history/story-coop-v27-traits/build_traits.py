"""Reuse native Survival skin calculations inside the local co-op campaign."""
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'story-coop-v26-direct'
sys.path.insert(0,str(PREVIOUS))
from build import BASE, GAME, Cs, CS_ARCH_X86, CS_MODE_32, Ks, KS_ARCH_X86, KS_MODE_32, pefile, sha

DIAG=0x7ff000
DAMAGE_SITE=0x4f3fb6
HEALTH_SITE=0x4f18c1
TAG_SITE=0x4f404a
RANGED_SITE=0x53ed6a
SPAWN_SITES=(0x7fa267,0x7fb267)
RELATIVE={'scope':0x1800,'health_gate':0x1900,'attack_gate':0x1980,'spawn':0x1a00,'observe_tag':0x1b00,'ranged_gate':0x1c00}
STATS_OFFSET=0x400

def routines(c,d,*,diag=DIAG, max_hp=0x4f17f0, fill=0x4f0410, combat=0x40bb60, appearance=0x4d1d70,
             health_yes=0x4f18c8, health_no=0x4f192f, attack_yes=0x4f3fbe, attack_no=0x4f405d,
             tag_continue=0x4f4055, ranged_yes=0x53ed71, ranged_no=0x53ed8a):
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    result={}
    def put(name,source):
        addr=c+RELATIVE[name]
        result[name]=(addr,bytes(ks.asm(source,addr)[0]))
        return addr
    stats=d+STATS_OFFSET
    # Match only one of the players registered for this live simulation.
    # Stage 2/4 cover actor construction, stage 5 covers combat and retries.
    scope=put('scope',f'''push edx
        xor eax,eax
        cmp dword ptr [{d+4}],1;jne done
        test ecx,ecx;jz done
        cmp dword ptr [{diag+4}],2;je member
        cmp dword ptr [{diag+4}],4;je member
        cmp dword ptr [{diag+4}],5;jne done
        member:cmp ecx,[{diag+12}];je first
        cmp ecx,[{diag+16}];je second
        jmp done
        second:mov edx,ecx
        mov eax,2;jmp owner
        first:mov edx,ecx
        mov eax,1
        owner:mov edx,[edx+0x20];test edx,edx;jz wrong
        cmp edx,[{diag+36}];je valid
        wrong:xor eax,eax
        valid:
        done:pop edx
        ret''')
    def gate(yes,no,replay=''):
        return f'''test al,al;jnz native_yes
            push eax;push ecx;mov ecx,[ebp+8];call {scope}
            test eax,eax;pop ecx;pop eax;jz native_no
            native_yes:{replay}
            jmp {yes}
            native_no:jmp {no}'''
    put('health_gate',gate(health_yes,health_no,'mov esi,[ebp+8]'))
    put('attack_gate',gate(attack_yes,attack_no))
    # Projectile construction has a separate Survival-only gate BEFORE it
    # calls 4f3f40. EBX is the existing attack context, context+8 its actor.
    # Keep that original context/actor intact; admit registered co-op actors.
    put('ranged_gate',f'''test al,al;jnz native_yes
        push eax;push ecx;push edx
        mov ecx,[ebx+8];call {scope}
        test eax,eax;pop edx;pop ecx;pop eax;jz native_no
        native_yes:mov ecx,[ebx+8];jmp {ranged_yes}
        native_no:jmp {ranged_no}''')
    # At these two exact campaign call sites the real skin ID is already
    # written. Recalculate and fill HP just as Survival does after skin load.
    put('spawn',f'''push esi;push ebx;push edi
        mov ebx,[esp+16];mov ecx,ebx;call {scope}
        test eax,eax;jz original
        dec eax;shl eax,5;lea edi,[eax+{stats}]
        mov ecx,ebx;call {combat}
        test eax,eax;jz original
        mov esi,eax
        push esi;call {max_hp}
        push 0x3f800000;call {fill}
        mov eax,[esi+0x200];mov [edi+4],eax
        mov eax,[esi+0xa0];mov [edi+8],eax
        inc dword ptr [edi]
        original:pop edi;pop ebx;pop esi
        jmp {appearance}''')
    # Record the matched native tag and exact before/after values to check
    # player ownership and the result without a damage-vs-difficulty estimate.
    put('observe_tag',f'''push eax;push ecx;push edx
        mov ecx,[ebp+8];call {scope}
        xor edx,edx;test eax,eax;jz native
        dec eax;shl eax,5;lea edx,[eax+{stats}]
        inc dword ptr [edx+12]
        mov eax,[esi];mov [edx+16],eax
        mov eax,[esi+4];mov [edx+20],eax
        mov eax,[esp+0x24];mov [edx+24],eax
        native:
        fld dword ptr [esi+4]
        fmul dword ptr [esp+0x24]
        fstp dword ptr [esp+0x24]
        test edx,edx;jz done
        mov ecx,[esp+0x24];mov [edx+28],ecx
        done:pop edx;pop ecx;pop eax;jmp {tag_continue}''')
    return result


def build(source,row):
    assert sha(source)==row['sha256']
    pe=pefile.PE(data=source,fast_load=True)
    assert pe.OPTIONAL_HEADER.ImageBase==BASE
    c,d=(int(row[k],16) for k in ('code','data'))
    assert not any(source[pe.get_offset_from_rva(d+STATS_OFFSET-BASE):][:64])
    out=bytearray(source)
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    md=Cs(CS_ARCH_X86,CS_MODE_32)
    edits={}
    def patch(a,old,new):
        start=pe.get_offset_from_rva(a-BASE)
        assert len(old)==len(new) and source[start:start+len(old)]==old,hex(a)
        assert all(a>=o+n or a+len(old)<=o for o,n in edits.items())
        out[start:start+len(new)]=new
        edits[a]=len(old)
    code=routines(c,d)
    for name,(a,blob) in code.items():
        assert sum(i.size for i in md.disasm(blob,a))==len(blob)
        patch(a,b'\xcc'*len(blob),blob)
    for a,expected,name in ((HEALTH_SITE,'84c0746a8b7508','health_gate'),
                           (DAMAGE_SITE,'84c00f849f000000','attack_gate'),
                           (TAG_SITE,'d94604d84c2418d95c2418','observe_tag'),
                           (RANGED_SITE,'84c0741c8b4b08','ranged_gate')):
        old=bytes.fromhex(expected)
        jmp=bytes(ks.asm(f'jmp {code[name][0]}',a)[0])
        assert sum(i.size for i in md.disasm(old,a))==len(old)
        patch(a,old,jmp.ljust(len(old),b'\x90'))
    for a in SPAWN_SITES:
        patch(a,bytes(ks.asm('call 0x4d1d70',a)[0]),bytes(ks.asm(f'call {code["spawn"][0]}',a)[0]))
    allowed={pe.get_offset_from_rva(a-BASE)+i for a,n in edits.items() for i in range(n)}
    assert len(out)==len(source) and all(i in allowed for i,(x,y) in enumerate(zip(source,out)) if x!=y)
    assist=pe.get_offset_from_rva(0x4ee3b0-BASE)
    assert out[assist:assist+7]==bytes.fromhex('6aff687e876f00')
    row={**row,'v26_sha256':row['sha256'],'sha256':sha(out),'trait_sites':[hex(a) for a in edits],
         'stats':hex(d+STATS_OFFSET)}
    return bytes(out),row

if __name__=='__main__':
    dest=HERE/'dev'
    dest.mkdir(exist_ok=True)
    rows=[]
    for row in json.loads((PREVIOUS/'builds.json').read_text()):
        exe=f'shank2-story-coop-{row["language"]}.exe'
        result,report=build((PREVIOUS/'dev'/exe).read_bytes(),row)
        (dest/exe).write_bytes(result)
        rows.append(report)
    (HERE/'builds.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
    print('Built EN/CHS campaign trait candidates; original Survival logic preserved.')

