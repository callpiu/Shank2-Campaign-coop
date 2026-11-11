"""Pause equipment selection that changes each actor on the next native spawn."""
import hashlib
import json
from pathlib import Path
import struct
import sys

from selector import CATALOG, FAMILIES, FAMILY_HASHES, constants, hash_name, routines

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'story-coop-v11-retry-score'
sys.path.insert(0, str(HERE.parent / 'story-coop-v05'))
from native import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

CODE, DATA, DIAG, CONFIG, MENU = 0x7fb400, 0x800000, 0x7ff000, 0x7ff800, 0x802000
SCOPE = DATA + 0xc00  # equipment-screen pointer and actor generation


def selection(asm, addr, data=DATA, config=CONFIG):
    # stdcall(slot, skin hash); returns 1 if accepted. The actor stays untouched.
    return asm(f'''mov ecx,[esp+4]
    cmp ecx,1
    ja invalid
    shl ecx,6
    add ecx,{config}
    mov eax,[esp+8]
    mov edx,{data+0x10}
    search:
    cmp edx,{data+0x10+8*len(CATALOG)}
    jae invalid
    cmp eax,[edx]
    je found
    add edx,8
    jmp search
    found:
    mov [ecx+20],eax
    cmp dword ptr [edx+4],0
    jne corina
    cmp byte ptr [ecx+4],0x73
    je accepted
    mov dword ptr [ecx+4],0x6e616873
    mov dword ptr [ecx+8],0x6b
    mov dword ptr [ecx+24],{hash_name('machete')}
    mov dword ptr [ecx+28],{hash_name('throwingknives')}
    jmp accepted
    corina:
    cmp byte ptr [ecx+4],0x63
    je accepted
    mov dword ptr [ecx+4],0x69726f63
    mov dword ptr [ecx+8],0x616e
    mov dword ptr [ecx+24],{hash_name('sword')}
    mov dword ptr [ecx+28],{hash_name('revolver')}
    accepted:
    mov eax,1
    ret 8
    invalid:
    xor eax,eax
    ret 8''', addr)


def machine_code(asm):
    code = {}
    put = lambda r, s: code.setdefault(CODE+r, asm(s, CODE+r))
    code[CODE] = routines(asm, CODE, DATA)
    code[CODE+0x180] = selection(asm, CODE+0x180)
    # Capture the exact native equipment screen shown from the two pause buttons.
    put(0x240, f'''call {CODE+0x840}
        test al,al
        jz native
        mov [{SCOPE}],ecx
        mov eax,[{DIAG+32}]
        mov [{SCOPE+4}],eax
        native: jmp 0x5e33b0''')
    put(0x280, f'''push ecx
        call 0x801d00
        pop ecx
        pushfd
        cmp [{SCOPE}],ecx
        jne done
        mov dword ptr [{SCOPE}],0
        done: popfd
        ret''')
    # Three call sites carry the screen in different frame locals. The stock
    # lookup stays in use everywhere else, including pre-level and survival.
    for offset, local in zip((0x2c0, 0x300, 0x340), (0x120, 0x108, 0x84), strict=True):
        put(offset, f'''mov ecx,[ebp-{local}]
            call {CODE+0x380}
            test al,al
            jz native
            jmp {CODE}
            native: jmp 0x506980''')
    put(0x380, f'''xor eax,eax
        cmp dword ptr [{DIAG+4}],5
        jne done
        cmp ecx,[{SCOPE}]
        jne done
        test ecx,ecx
        jz done
        mov eax,[{DIAG+32}]
        cmp eax,[{SCOPE+4}]
        sete al
        movzx eax,al
        done: ret''')
    # Grant only the menu's curated rows. On fallback/other modes, use native unlocks.
    for offset, local in zip((0x3c0, 0x410, 0x460), (0x120, 0x108, 0x84), strict=True):
        put(offset, f'''push ecx
            mov ecx,[ebp-{local}]
            call {CODE+0x380}
            pop ecx
            test al,al
            jz native
            cmp dword ptr [{DATA+0x128}],{DATA+0x140+0x90*len(CATALOG)}
            jne native
            mov eax,[esp+4]
            mov edx,[eax]
            mov eax,{DATA+0x10}
            find:
            cmp eax,{DATA+0x10+8*len(CATALOG)}
            jae native
            cmp edx,[eax]
            je allowed
            add eax,8
            jmp find
            allowed: mov eax,1
            ret 4
            native: jmp 0x697630''')
    # On reopen, show the selected (possibly queued) costume without changing
    # the weapon categories for the still-live actor family.
    put(0x4b0, f'''call {CODE+0x840}
        test al,al
        jz native
        mov eax,[{MENU+0x100}]
        cmp eax,1
        ja native
        shl eax,6
        mov eax,[{CONFIG+20}+eax]
        mov [esp+20],eax
        native: jmp 0x68c420''')
    # The six-argument equipment callback has already applied melee/ranged.
    # Queue the skin in the selected player's config, skipping native immediate
    # skin replacement only for the paused co-op selector.
    put(0x4f0, f'''call {CODE+0x840}
        test al,al
        jz native
        mov ecx,[{SCOPE}]
        call {CODE+0x380}
        test al,al
        jz native
        mov eax,[{MENU+0x100}]
        cmp eax,1
        ja queued
        mov ecx,[{DIAG+12}+eax*4]
        cmp ecx,[ebp-4]
        jne queued
        push dword ptr [ebp+0x18]
        push eax
        call {CODE+0x180}
        queued: jmp 0x67b36b
        native:
        mov ecx,[ebp-4]
        call 0x406620
        jmp 0x67b2cc''')
    # Do not copy old archetype's gear over the new-family defaults while a
    # switch is queued. After spawn, actor/config match and normal sync resumes.
    put(0x570, f'''push ecx
        call 0x406620
        mov eax,[eax+0xc0]
        mov edx,ebx
        shl edx,6
        cmp byte ptr [{CONFIG+4}+edx],0x73
        jne corina
        cmp eax,{FAMILY_HASHES[0]}
        jmp matched
        corina: cmp eax,{FAMILY_HASHES[1]}
        matched:
        pop ecx
        jne skip
        jmp 0x40d7c0
        skip: xor eax,eax
        ret''')
    # Load BOTH player archetypes under the native level resource context. The
    # second stock call is redundant for campaign; its other modes are unchanged.
    put(0x5c0, f'''mov eax,[ebp-0x34]
        cmp dword ptr [eax+0x1e4],1
        jne native
        push ebx
        mov ebx,ecx
        push dword ptr [esp+16]
        push dword ptr [esp+16]
        push {DATA+0xc10}
        call 0x411080
        test eax,eax
        jz done
        mov ecx,ebx
        push dword ptr [esp+16]
        push dword ptr [esp+16]
        push {DATA+0xc18}
        call 0x411080
        done: pop ebx
        ret 12
        native: jmp 0x411080''')
    put(0x620, '''mov eax,[ebp-0x34]
        cmp dword ptr [eax+0x1e4],1
        jne native
        mov eax,1
        ret 12
        native: jmp 0x411080''')
    for offset, local in ((0x660, 0x34), (0x6a0, 0x20)):
        put(offset, f'''mov eax,[ebp-{local}]
            cmp dword ptr [eax+0x1e4],1
            jne native
            jmp {CODE+0x740}
            native: jmp 0x69a820''')
    for offset, local in ((0x6e0, 0x34), (0x710, 0x20)):
        put(offset, f'''mov eax,[ebp-{local}]
            cmp dword ptr [eax+0x1e4],1
            jne native
            ret
            native: jmp 0x69a820''')
    put(0x740, f'''push esi
        push edi
        mov edi,[esp+20]
        mov esi,{DATA+0x10}
        again:
        mov eax,[esi+4]
        push edi
        push dword ptr [esi]
        push dword ptr [{DATA}+eax*4]
        call 0x69a820
        add esp,12
        add esi,8
        cmp esi,{DATA+0x10+len(CATALOG)*8}
        jb again
        pop edi
        pop esi
        ret''')
    put(0x7a0, f'''mov eax,[ebp-0x20]
        cmp dword ptr [eax+0x1e4],1
        jne native
        push ebx
        mov ebx,ecx
        push dword ptr [{DATA}]
        call 0x410920
        mov ecx,ebx
        push dword ptr [{DATA+4}]
        call 0x410920
        pop ebx
        ret 4
        native: jmp 0x410920''')
    put(0x800, '''mov eax,[ebp-0x20]
        cmp dword ptr [eax+0x1e4],1
        jne native
        ret 4
        native: jmp 0x410920''')
    # Pause/menu callbacks share this native local, resolved from the current
    # screen each time. Stale campaign diagnostics alone cannot open the scope.
    put(0x840, f'''xor eax,eax
        cmp dword ptr [{DIAG+4}],5
        jne done
        mov edx,[ebp-8]
        test edx,edx
        jz done
        cmp edx,[{DIAG+36}]
        jne done
        cmp dword ptr [edx],0x75017c
        sete al
        done: ret''')
    return code


def build(source, output, expected):
    b = source.read_bytes()
    assert hashlib.sha256(b).hexdigest() == expected
    pe = pefile.PE(data=b)
    assert pe.OPTIONAL_HEADER.ImageBase == 0x400000
    out = bytearray(b)
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda s, a: bytes(ks.asm(s, a)[0])
    off = lambda va: pe.get_offset_from_rva(va-0x400000)

    def write(va, old, new):
        o = off(va)
        assert len(old) == len(new) and b[o:o+len(old)] == old and out[o:o+len(old)] == old, hex(va)
        out[o:o+len(new)] = new

    for addr, blob in sorted(machine_code(asm).items()):
        write(addr, b'\xcc' * len(blob), blob)
    raw = constants(DATA) + bytes(0x10) + b'shank\0\0\0corina\0\0'
    write(DATA, bytes(len(raw)), raw)
    for addr, native, rel in [
        (0x67b149, 0x5e33b0, 0x240), (0x68c74f, 0x506980, 0x2c0), (0x68c9f6, 0x506980, 0x300),
        (0x68d111, 0x506980, 0x340), (0x68c78e, 0x697630, 0x3c0), (0x68cae2, 0x697630, 0x410),
        (0x68d17e, 0x697630, 0x460), (0x67b10d, 0x68c420, 0x4b0), (0x801719, 0x40d7c0, 0x570),
        (0x43481e, 0x411080, 0x5c0), (0x434883, 0x411080, 0x620),
        (0x4348ee, 0x69a820, 0x660), (0x434aae, 0x69a820, 0x6a0),
        (0x43494e, 0x69a820, 0x6e0), (0x434b0e, 0x69a820, 0x710),
        (0x434b5c, 0x410920, 0x7a0), (0x434ba7, 0x410920, 0x800),
    ]:
        write(addr, asm(f'call {native}', addr), asm(f'call {CODE+rel}', addr))
    write(0x67b2c4, bytes.fromhex('8b4dfce854b3d8ff'), asm(f'jmp {CODE+0x4f0}; nop; nop; nop', 0x67b2c4))
    write(0x7532c0, struct.pack('<I', 0x801d00), struct.pack('<I', CODE+0x280))
    # The stock asset has the costume spinner visible. Keep the same screen
    # and native binding, but stop redirecting it to the old hidden-skin copy.
    write(0x68e148, asm('jmp 0x801d80', 0x68e148), asm('push 0x75312c', 0x68e148))
    output.write_bytes(out)
    return dict(name=output.name, baseline_sha256=expected, sha256=hashlib.sha256(out).hexdigest())


if __name__ == '__main__':
    (HERE/'dev').mkdir(exist_ok=True)
    checks = json.loads((BASE/'builds.json').read_text())
    report = [build(BASE/'dev'/row['name'], HERE/'dev'/row['name'], row['sha256']) for row in checks]
    (HERE/'builds.json').write_text(json.dumps(report, indent=2)+'\n')
    print(f'Built {len(report)} isolated development variants.')
