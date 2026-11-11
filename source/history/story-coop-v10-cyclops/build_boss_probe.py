"""Build an isolated Cyclops execution trace; never change combat outcomes."""
from pathlib import Path
import hashlib
import struct
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / d) for d in ('story-coop-v05', 'story-coop-v04')]
from native import pefile
from loadout_code import hash_name
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

CODE, DATA, COOP = 0x7fc900, 0x7ff900, 0x7ff000
ATTEMPT, RESOLVE, DAMAGE, SCOPE = CODE, CODE + 0x80, CODE + 0x100, CODE + 0x200
STATE = hash_name('grab_boss_cyclops_atk')


def routines(asm):
    # EDI is the native action context. Scope includes either campaign player.
    scope = asm(f'''cmp dword ptr [{COOP+4}],5
    jne no
    test edi,edi
    jz no
    mov ecx,[edi+8]
    test ecx,ecx
    jz no
    cmp ecx,[{COOP+12}]
    je check_state
    cmp ecx,[{COOP+16}]
    jne no
    check_state:
    call 0x40e290
    test eax,eax
    jz no
    cmp dword ptr [eax+0x34],{STATE}
    jne no
    mov eax,[edi+8]
    ret
    no:
    xor eax,eax
    ret''', SCOPE)
    attempt = asm(f'''pushfd
    pushad
    mov edi,[esp+40]
    call {SCOPE}
    test eax,eax
    jz done
    inc dword ptr [{DATA+4}]
    mov [{DATA+8}],eax
    mov edx,[{COOP+0x20}]
    mov [{DATA+12}],edx
    done:
    popad
    popfd
    push ebp
    mov ebp,esp
    and esp,0xfffffff8
    jmp 0x53de76''', ATTEMPT)
    resolve = asm(f'''call 0x5053b0
    pushfd
    pushad
    call {SCOPE}
    test eax,eax
    jz done
    mov edx,[esp+28]
    mov [{DATA+20}],edx
    mov edx,[{DATA+4}]
    mov [{DATA+52}],edx
    inc dword ptr [{DATA+16}]
    done:
    popad
    popfd
    jmp 0x53deeb''', RESOLVE)
    damage = asm(f'''pushfd
    pushad
    call {SCOPE}
    test eax,eax
    jz original
    mov [{DATA+28}],eax
    mov [{DATA+32}],esi
    mov edx,[{DATA+4}]
    mov [{DATA+56}],edx
    mov ecx,[esp+36]
    mov [{DATA+48}],ecx
    mov edx,[esp+48]
    mov edx,[edx+0xc]
    mov [{DATA+36}],edx
    mov dword ptr [{DATA+40}],0x7fc00000
    mov dword ptr [{DATA+44}],0x7fc00000
    test ecx,ecx
    jz before_done
    mov edx,[ecx+0xa0]
    mov [{DATA+40}],edx
    before_done:
    popad
    popfd
    call 0x4f0c00
    pushfd
    pushad
    mov ecx,esi
    call 0x40bb60
    test eax,eax
    jz after_done
    cmp eax,[{DATA+48}]
    jne after_done
    mov eax,[eax+0xa0]
    mov [{DATA+44}],eax
    after_done:
    inc dword ptr [{DATA+24}]
    popad
    popfd
    jmp 0x53e19b
    original:
    popad
    popfd
    call 0x4f0c00
    jmp 0x53e19b''', DAMAGE)
    return {ATTEMPT: attempt, RESOLVE: resolve, DAMAGE: damage, SCOPE: scope}


def build(source, output):
    original = source.read_bytes()
    pe = pefile.PE(data=original)
    result = bytearray(original)
    off = lambda addr: pe.get_offset_from_rva(addr - pe.OPTIONAL_HEADER.ImageBase)
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda text, addr: bytes(ks.asm(text, addr)[0])

    def replace(addr, expected, replacement):
        start = off(addr)
        assert len(expected) == len(replacement)
        assert original[start:start + len(expected)] == expected, hex(addr)
        assert result[start:start + len(expected)] == expected, hex(addr)
        result[start:start + len(replacement)] = replacement

    for addr, blob in routines(asm).items():
        replace(addr, b'\xcc' * len(blob), blob)
    replace(DATA, bytes(60), b'CYCP' + bytes(56))
    replace(0x53de70, bytes.fromhex('558bec83e4f8'), asm(f'jmp {ATTEMPT}; nop', 0x53de70))
    for site, native, probe in [(0x53dee6, 0x5053b0, RESOLVE), (0x53e196, 0x4f0c00, DAMAGE)]:
        replace(site, asm(f'call {native}', site), asm(f'jmp {probe}', site))
    # Reproduce the reported default Corina P1, preserving the two stock loadouts.
    config = 0x7ff800
    slots = original[off(config):off(config) + 128]
    assert slots[4:10] == b'shank\0' and slots[68:75] == b'corina\0'
    replace(config, slots, slots[64:] + slots[:64])
    output.write_bytes(result)
    print(hashlib.sha256(result).hexdigest(), output)


if __name__ == '__main__':
    build(HERE.parent / 'story-coop-v12-live-character/dev/keyboard-chs.exe',
          HERE / 'shank2-coop-cyclops-probe.exe')
