"""Keep each campaign player's score on death-screen Retry, based on v0.8.1."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / 'story-coop-v09-fixes'
sys.path.insert(0, str(HERE.parent / 'story-coop-v05'))
from native import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

CODE = 0x7fd400
DIAG = 0x7ff000
RETRY = 0x67abe0
INVENTORY = 0x40d760
RETRY_SITES = (0x6c297c, 0x6c28e7)


def routines(asm, code=CODE, diag=DIAG, retry=RETRY, inventory=INVENTORY):
    pair = code + 0x100
    # EBX: expected live simulation. Return ESI/EDI as a verified inventory pair;
    # EAX=0 means either slot is unavailable or no longer belongs to that sim.
    lookup = asm(f'''xor eax,eax
    cmp dword ptr [{diag+4}],5
    jne done
    cmp ebx,[{diag+36}]
    jne done
    mov esi,[{diag+12}]
    mov edi,[{diag+16}]
    test esi,esi
    jz done
    test edi,edi
    jz done
    cmp esi,edi
    je done
    cmp [esi+0x20],ebx
    jne done
    cmp [edi+0x20],ebx
    jne done
    mov ecx,esi
    call {inventory}
    test eax,eax
    jz done
    cmp [eax+8],esi
    jne invalid
    mov esi,eax
    mov ecx,edi
    call {inventory}
    test eax,eax
    jz done
    cmp [eax+8],edi
    jne invalid
    cmp eax,esi
    je invalid
    mov edi,eax
    ret
    invalid:
    xor eax,eax
    done:
    ret''', pair)
    wrapper = asm(f'''push ebp
    mov ebp,esp
    lea esp,[esp-16]
    pushfd
    pushad
    mov dword ptr [ebp-4],0
    mov ebx,[ecx+0x68]
    test ebx,ebx
    jz invoke
    call {pair}
    test eax,eax
    jz invoke
    mov [ebp-4],ebx
    mov edx,[{diag+32}]
    inc edx
    mov [ebp-8],edx
    mov eax,[esi+0x50]
    mov [ebp-12],eax
    mov eax,[edi+0x50]
    mov [ebp-16],eax
    invoke:
    popad
    popfd
    call {retry}
    pushfd
    pushad
    mov ebx,[ebp-4]
    test ebx,ebx
    jz done
    mov edx,[ebp-8]
    cmp [{diag+32}],edx
    jne done
    call {pair}
    test eax,eax
    jz done
    mov eax,[ebp-12]
    mov [esi+0x50],eax
    mov eax,[ebp-16]
    mov [edi+0x50],eax
    done:
    popad
    popfd
    mov esp,ebp
    pop ebp
    ret''', code)
    assert len(wrapper) <= pair - code
    return {code: wrapper, pair: lookup}


def build(source, output, expected):
    original = source.read_bytes()
    if hashlib.sha256(original).hexdigest() != expected:
        raise ValueError(f'Unexpected source image: {source}')
    pe = pefile.PE(data=original)
    assert pe.OPTIONAL_HEADER.ImageBase == 0x400000 and pe.FILE_HEADER.Machine == 0x14c
    assert not (pe.OPTIONAL_HEADER.DllCharacteristics & 0x40)
    result = bytearray(original)
    off = lambda addr: pe.get_offset_from_rva(addr - pe.OPTIONAL_HEADER.ImageBase)
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda text, addr: bytes(ks.asm(text, addr)[0])

    def patch(addr, before, after):
        i = off(addr)
        assert len(before) == len(after)
        assert original[i:i + len(before)] == before and result[i:i + len(before)] == before, hex(addr)
        result[i:i + len(after)] = after

    for addr, blob in routines(asm).items():
        patch(addr, b'\xcc' * len(blob), blob)
    for site in RETRY_SITES:
        patch(site, asm(f'call {RETRY}', site), asm(f'call {CODE}', site))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(result)
    return dict(name=output.name, baseline_sha256=expected, sha256=hashlib.sha256(result).hexdigest(),
                hooks=[hex(x) for x in RETRY_SITES], original_game_unchanged=True, gameplay_verified=False)


if __name__ == '__main__':
    checks = json.loads((BASELINE / 'builds.json').read_text())
    names = [f'{mode}-{lang}.exe' for mode in ('keyboard', 'pads') for lang in ('en', 'chs')]
    reports = [build(BASELINE / 'final' / name, HERE / 'dev' / name, check['sha256'])
               for name, check in zip(names, checks, strict=True)]
    (HERE / 'builds.json').write_text(json.dumps(reports, indent=2) + '\n')
    print(f'Built {len(reports)} offline development variants.')
