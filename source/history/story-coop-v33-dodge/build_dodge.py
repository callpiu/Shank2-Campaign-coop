"""Add independently configurable native right-stick dodges to clean v28."""
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
SOURCE=WORK/'story-coop-v28-trait-descriptions'
sys.path.insert(0,str(SOURCE))
from build_descriptions import BASE,pefile,Ks,KS_ARCH_X86,KS_MODE_32,Cs,CS_ARCH_X86,CS_MODE_32,sha
sys.path.insert(0,str(HERE))

DEFAULTS=(0x5a,0x43,0x68,0x69) # P1 Z/C; P2 Num8/Num9
MAGIC=b'S2D1'
CONFIG_FILE='Shank2-Coop-Dodge.dat'


def input_code(address,data,old_state,*,key_api=0x72e224,focus_api=0x72e234,window=0x7d7ed4):
    return bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(f'''
        push ebp;mov ebp,esp;push esi;push ebx;push edi
        push dword ptr [ebp+12];push dword ptr [ebp+8];call {old_state}
        push eax;test eax,eax;jnz done
        cmp dword ptr [{data+0x84}],0;jne done
        cmp dword ptr [ebp+8],2;jae done
        mov esi,[ebp+12];test esi,esi;jz done
        call dword ptr [{focus_api}];cmp eax,[{window}];jne done
        mov ebx,[ebp+8];shl ebx,3;add ebx,{data+0x744}
        xor edi,edi
        push dword ptr [ebx];call dword ptr [{key_api}]
        test ax,0x8000;jz right;sub edi,32767
        right:push dword ptr [ebx+4];call dword ptr [{key_api}]
        test ax,0x8000;jz apply;add edi,32767
        apply:mov [esi+12],di
        done:pop eax;pop edi;pop ebx;pop esi;pop ebp;ret 8
    ''',address)[0])


def build(raw,row):
    assert sha(raw)==row['sha256'] and not row['test_assists']
    pe=pefile.PE(data=raw,fast_load=True);out=bytearray(raw)
    c,d=int(row['code'],16),int(row['data'],16)
    off=lambda a:pe.get_offset_from_rva(a-BASE)
    asm=lambda s,a:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(s,a)[0])
    edits=[]
    def patch(a,before,after):
        assert len(before)==len(after) and raw[off(a):off(a)+len(before)]==before,hex(a)
        assert all(a>=b+n or a+len(after)<=b for b,n in edits)
        out[off(a):off(a)+len(after)]=after;edits.append((a,len(after)))
    def put(a,code):patch(a,b'\xcc'*len(code),code)
    filename=CONFIG_FILE.encode('utf-16-le')+b'\0\0'
    assert len(filename)<=0x40
    patch(d+0x700,bytes(len(filename)),filename)
    defaults=MAGIC+struct.pack('<4I',*DEFAULTS)
    patch(d+0x740,bytes(len(defaults)),defaults)
    boot=asm(f'''pushfd;pushad
        push {d+0x150};call dword ptr [0x72e060]
        test eax,eax;jz done
        push {d+0x190};push eax;call dword ptr [0x72e1f8]
        test eax,eax;jz done
        push 0;push 0x80;push 3;push 0;push 7;push 0x80000000;push {d+0x700}
        call eax;cmp eax,-1;je done;mov edi,eax
        push 0;push {d+0x760};push 21;push {d+0x780};push edi
        call dword ptr [0x72e13c];mov esi,eax
        push edi;call dword ptr [0x72e17c]
        test esi,esi;jz done
        cmp dword ptr [{d+0x760}],20;jne done
        cmp dword ptr [{d+0x780}],{int.from_bytes(MAGIC,'little')};jne done
        mov esi,{d+0x784};mov ecx,4
        validate:mov eax,[esi];dec eax;cmp eax,253;ja done;add esi,4;loop validate
        mov esi,{d+0x784};mov edi,{d+0x744};mov ecx,4;cld;rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        done:popad;popfd;jmp 0x6451e0''',c+0x2100)
    assert len(boot)<=0x100
    put(c+0x2100,boot)
    put(c+0x2200,input_code(c+0x2200,d,c+0x400))
    patch(c+0xfe,asm('jmp 0x6451e0',c+0xfe),asm(f'jmp {c+0x2100}',c+0xfe))
    patch(0x6655ce,asm(f'jmp {c+0x400};nop',0x6655ce),asm(f'jmp {c+0x2200};nop',0x6655ce))
    assert len(out)==len(raw)
    allowed={off(a)+i for a,n in edits for i in range(n)}
    assert all(i in allowed for i,(a,b) in enumerate(zip(raw,out)) if a!=b)
    for a,n in ((0x4ee3b0,7),(d+0x800,0x800),(c+0x1d00,0x320),(c+0x2700,100)):
        assert out[off(a):off(a)+n]==raw[off(a):off(a)+n]
    return bytes(out),{**row,'sha256':sha(out),'dodge_baseline_sha256':row['sha256'],
        'description_predecessors':sorted(set(row.get('description_predecessors',[])+[row['sha256']])),
        'dodge_keys':4,'dodge_config':CONFIG_FILE,'dodge_config_version':'S2D1',
        'dodge_patches':[(hex(a),n) for a,n in edits],'test_assists':False}


def main():
    dest=HERE/'dev';dest.mkdir(parents=True,exist_ok=True);rows=[]
    for row in json.loads((SOURCE/'builds.json').read_text()):
        name=f'shank2-story-coop-{row["language"]}.exe'
        raw,report=build((SOURCE/'dev'/name).read_bytes(),row)
        (dest/name).write_bytes(raw)
        for asset,digest in row['ui_assets'].items():
            ui=(SOURCE/'dev'/asset).read_bytes();assert sha(ui)==digest
            (dest/asset).write_bytes(ui)
        rows.append(report)
    (HERE/'builds.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('Built clean EN/CHS four-key native right-stick dodge extension; old keys and gameplay retained.')


if __name__=='__main__':main()
