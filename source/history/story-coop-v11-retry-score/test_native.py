"""Run the actual score hook in 32-bit Windows without launching the game."""
import os
from pathlib import Path
import struct
import subprocess
import tempfile

from build import Ks, KS_ARCH_X86, KS_MODE_32, routines


def main():
    v = 0x20000000
    diag, screen, sim, alien = (v + x for x in (0x1000, 0x1100, 0x1200, 0x1300))
    a1, a2, b1, b2 = (v + x for x in (0x1400, 0x1500, 0x1600, 0x1700))
    i1, i2, j1, j2 = (v + x for x in (0x1800, 0x1900, 0x1a00, 0x1b00))
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda code, addr: bytes(ks.asm(code, addr)[0])
    patches = routines(asm, v, diag, v + 0x400, v + 0x500)
    for off, body in {
        0x400: f'''inc dword ptr [{diag+0x70}]
        cmp ecx,{screen}
        jne wrong_this
        mov edx,[{diag+0x74}]
        add [{diag+0x20}],edx
        mov dword ptr [{diag+12}],{b1}
        mov dword ptr [{diag+16}],{b2}
        mov dword ptr [{j1+0x50}],110
        mov dword ptr [{j2+0x50}],260
        cmp dword ptr [{diag+0x78}],1
        jne native_done
        mov dword ptr [{diag+36}],{alien}
        native_done:
        mov eax,50
        stc
        ret
        wrong_this:
        xor eax,eax
        ret''',
        0x500: 'mov eax,[ecx+0x24]; ret',
        0x600: f'mov ecx,{screen}; call {v}; adc eax,0; ret',
    }.items():
        patches[v + off] = asm(body, v + off)
    buf = bytearray(0x2000)
    for addr, body in patches.items():
        off = addr - v
        assert buf[off:off + len(body)] == bytes(len(body))
        buf[off:off + len(body)] = body
    for addr, word in {
        screen + 0x68: sim, diag + 4: 5, diag + 12: a1, diag + 16: a2,
        diag + 0x20: 10, diag + 0x24: sim, diag + 0x74: 1,
        **{actor + 0x20: sim for actor in (a1, a2, b1, b2)},
        **{actor + 0x24: inv for actor, inv in zip((a1, a2, b1, b2), (i1, i2, j1, j2))},
        **{inv + 8: actor for actor, inv in zip((a1, a2, b1, b2), (i1, i2, j1, j2))},
        i1 + 0x50: 425, i2 + 0x50: 875,
    }.items():
        struct.pack_into('<I', buf, addr - v, word)
    with tempfile.TemporaryDirectory() as tmp:
        fixture = Path(tmp) / 'retry-fixture.bin'
        fixture.write_bytes(buf)
        ps = Path(os.environ['WINDIR']) / 'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
        script = Path(__file__).with_name('test_native.ps1')
        subprocess.run([str(ps), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script), str(fixture)],
                       check=True)


if __name__ == '__main__':
    main()
