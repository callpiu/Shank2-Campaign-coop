"""Exercise the original/patched campaign HUD dispatch in an x86 fixture."""
import os
from pathlib import Path
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'story-coop-v05'))
from native import pefile
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

SOURCE = HERE.parent / 'story-coop-v20-prelevel-layout/dev/keyboard-chs.exe'
PATCH_START = 0x695c1c
PATCH_END = 0x695c31
DISPATCH = 0x695b53
EPILOGUE = 0x695c7a
ORIGINAL = bytes.fromhex('8b4dd881c138060000c745fcffffffffe83fcffdff')
FIXED = bytes.fromhex('8b4dd881c1380600006aff8f45fce841cffdffeb3d')


def fixture(source):
    image = pefile.PE(data=source)
    offset = lambda address: image.get_offset_from_rva(address - 0x400000)
    assert source[offset(PATCH_START):offset(PATCH_END)] == ORIGINAL
    original = source[offset(DISPATCH):offset(EPILOGUE)]
    fixed = bytearray(original)
    fixed[PATCH_START - DISPATCH:PATCH_END - DISPATCH] = FIXED
    assert len(fixed) == len(original)
    base = 0x20000000
    state, event, screen, actor = (base + value for value in (0x1000, 0x1100, 0x1200, 0x1500))
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    result = bytearray(0x2000)

    def put(address, assembly):
        encoded = bytes(ks.asm(assembly, address)[0])
        result[address - base:address - base + len(encoded)] = encoded

    stubs = {
        0x403440: ('mov eax,[esp+4];mov eax,[eax];mov [ecx],eax;ret 4', 0x700),
        0x442630: (f'lea eax,[{event:#x}+0x20];ret', 0x720),
        0x4103f0: ('mov eax,[esp+4];mov edx,[eax];mov [ecx],edx;mov edx,[eax+4];mov [ecx+4],edx;mov eax,ecx;ret 4', 0x740),
        0x672b70: (f'inc dword ptr [{state+8}];mov eax,[esp+16];mov [{state+12}],eax;mov eax,[esp+12];mov [{state+16}],eax;mov [{state+44}],ecx;mov eax,[ebp-4];mov [{state+48}],eax;ret 16', 0x780),
        0x4ab480: ('mov eax,[eax+0x10];ret', 0x7c0),
        0x673830: (f'inc dword ptr [{state+20}];mov eax,[esp+8];mov [{state+24}],eax;mov eax,[esp+4];mov [{state+28}],eax;mov [{state+52}],ecx;ret 8', 0x7e0),
        0x66e800: (f'inc dword ptr [{state+32}];ret 4', 0x820),
        0x6940b0: (f'inc dword ptr [{state+36}];mov eax,[esp+4];mov [{state+40}],eax;ret 4', 0x840),
    }
    for code, dest in [(original, 0x100), (fixed, 0x300)]:
        translated = bytearray(code)
        for site in [0x695bea, 0x695bf9, 0x695c07, (0x695c2a if dest == 0x300 else 0x695c2c),
                     0x695c41, 0x695c50, 0x695c5a, 0x695c69, 0x695c75]:
            pos = site - DISPATCH
            assert translated[pos] == 0xe8, hex(site)
            target = site + 5 + struct.unpack_from('<i', translated, pos + 1)[0]
            struct.pack_into('<i', translated, pos + 1, stubs[target][1] - (dest + pos + 5))
        result[dest:dest + len(translated)] = translated
        put(base + dest + len(translated), f'mov eax,esp;sub eax,[{state+4}];mov esp,ebp;pop ebp;ret 4')
    for assembly, dest in stubs.values():
        put(base + dest, assembly)
    for entry, inner, dispatch in [(0, 0x580, 0x100), (0x40, 0x5c0, 0x300)]:
        put(base + entry, f'push {event};call {base+inner};ret')
        put(base + inner, f'''push ebp;mov ebp,esp;sub esp,0x40
            mov [{state+4}],esp
            mov eax,[{state}];mov [ebp-0x2c],eax
            mov dword ptr [ebp-0x28],{screen}
            jmp {base+dispatch}''')
    for address, value in [(event+0x10, actor), (event+0x14, 2), (event+0x18, 0xe82f946b),
                           (event+0x20, 0x12345678), (event+0x24, 0x87654321)]:
        struct.pack_into('<I', result, address - base, value)
    return result


if __name__ == '__main__':
    path = HERE / 'dispatch-fixture.bin'
    path.write_bytes(fixture(SOURCE.read_bytes()))
    ps = Path(os.environ['WINDIR']) / 'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                    str(HERE / 'test_dispatch.ps1'), str(path)], check=True)
