"""A narrow dual-player teleport fix for the Slums boss entrance."""
import hashlib
import json
from pathlib import Path
import struct
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32

CODE=0x7fc900
DIAG=0x7ff000
NATIVE=0x54b3b0
TARGET=tuple(struct.unpack('<2I',struct.pack('<2f',55751,1189)))

def routine(asm,code=CODE,diag=DIAG,native=NATIVE):
    return asm(f'''push ebp
        mov ebp,esp
        sub esp,0x10
        push ebx
        push esi
        push edi
        mov esi,ecx
        mov ebx,[ebp+8]
        cmp dword ptr [{diag+4}],5
        jne fallback
        cmp dword ptr [esi+8],{TARGET[0]}
        jne fallback
        cmp dword ptr [esi+12],{TARGET[1]}
        jne fallback
        test ebx,ebx
        jz fallback
        mov eax,[ebx+8]
        test eax,eax
        jz fallback
        mov ecx,[{diag+36}]
        test ecx,ecx
        jz fallback
        cmp [eax+0x20],ecx
        jne fallback
        cmp eax,[{diag+12}]
        je first
        cmp eax,[{diag+16}]
        jne fallback
        mov edi,[{diag+12}]
        jmp partner
        first: mov edi,[{diag+16}]
        partner:
        test edi,edi
        jz fallback
        cmp edi,eax
        je fallback
        cmp [edi+0x20],ecx
        jne fallback
        mov eax,[ebx]
        mov [ebp-16],eax
        mov eax,[ebx+4]
        mov [ebp-12],eax
        mov [ebp-8],edi
        mov eax,[ebx+12]
        mov [ebp-4],eax
        push ebx
        mov ecx,esi
        call {native}
        push eax
        lea eax,[ebp-16]
        push eax
        mov ecx,esi
        call {native}
        pop eax
        jmp done
        fallback:
        push ebx
        mov ecx,esi
        call {native}
        done:
        pop edi
        pop esi
        pop ebx
        mov esp,ebp
        pop ebp
        ret 4''',code)

def build(source,target):
    b=source.read_bytes();pe=pefile.PE(data=b)
    offset=lambda a:pe.get_offset_from_rva(a-0x400000)
    ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
    blob=routine(asm)
    assert len(blob)<0x300
    assert b[offset(CODE):offset(CODE)+len(blob)]==b'\xcc'*len(blob)
    assert struct.unpack_from('<I',b,offset(0x75ae04))[0]==NATIVE
    out=bytearray(b);out[offset(CODE):offset(CODE)+len(blob)]=blob
    struct.pack_into('<I',out,offset(0x75ae04),CODE)
    target.parent.mkdir(exist_ok=True);target.write_bytes(out)
    return dict(name=target.name,baseline=hashlib.sha256(b).hexdigest(),sha256=hashlib.sha256(out).hexdigest(),
                target=[55751,1189],native_health_logic_unchanged=True,bytes=len(blob))

if __name__=='__main__':
    records=[]
    for row in json.loads((HERE.parent/'story-coop-v12-live-character/builds.json').read_text()):
        source=HERE.parent/'story-coop-v12-live-character/dev'/row['name']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
        records.append(build(source,HERE/'dev'/row['name']))
    (HERE/'builds.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
    print('Built four isolated boss-teleport variants; released ZIP unchanged.')
