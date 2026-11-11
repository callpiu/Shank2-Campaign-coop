"""Exercise the real x86 detours against controlled native-call fixtures."""
from pathlib import Path
import struct
import subprocess
import tempfile
import os

import build_boss_probe as probe


def main():
    base = 0x20000000
    data = base + 0x1000
    coop = base + 0x1200
    context, player, target, graph, combat, hit = (base + n for n in range(0x1400, 0x2000, 0x200))
    attempt, resolve, damage, scope = (base + n for n in (0, 0x80, 0x100, 0x200))
    ks = probe.Ks(probe.KS_ARCH_X86, probe.KS_MODE_32)
    asm = lambda text, addr: bytes(ks.asm(text, addr)[0])
    probe.ATTEMPT, probe.RESOLVE, probe.DAMAGE, probe.SCOPE = attempt, resolve, damage, scope
    probe.DATA, probe.COOP = data, coop
    stubs = {
        '0x40e290': (0x400, f'mov eax,{graph}; ret'),
        '0x53de76': (0x420, 'mov esp,ebp; pop ebp; mov eax,61; ret 4'),
        '0x5053b0': (0x440, f'mov eax,[{data+60}]; stc; ret 8'),
        '0x53deeb': (0x460, 'adc eax,0; ret'),
        '0x4f0c00': (0x480, f'''cmp dword ptr [esp+4],{combat}; jne bad
            cmp dword ptr [esp+8],222; jne bad
            cmp dword ptr [esp+12],{player}; jne bad
            cmp dword ptr [esp+16],{hit}; jne bad
            cmp dword ptr [esp+20],555; jne bad
            mov dword ptr [{combat+0xa0}],0x41a00000
            mov eax,72; stc; ret 20
            bad: xor eax,eax; ret 20'''),
        '0x40bb60': (0x4e0, f'mov eax,{combat}; ret'),
        '0x53e19b': (0x500, 'adc eax,0; ret'),
    }

    def remap(text, addr):
        for address, (offset, _) in stubs.items():
            text = text.replace(address, str(base + offset))
        return asm(text, addr)

    blocks = probe.routines(remap)
    for offset, code in stubs.values():
        blocks[base + offset] = asm(code, base + offset)
    for offset, code in {
        0x600: f'push {context}; call {attempt}; ret',
        0x640: f'push edi; mov edi,{context}; call setup; pop edi; ret; setup: push 44; push 33; jmp {resolve}',
        0x680: f'''push edi; push esi; mov edi,{context}; mov esi,{target}
            call setup; pop esi; pop edi; ret
            setup: push 555; push {hit}; push {player}; push 222; push {combat}; jmp {damage}''',
    }.items():
        blocks[base + offset] = asm(code, base + offset)
    buf = bytearray(0x2000)
    for addr, code in blocks.items():
        off = addr - base
        assert buf[off:off + len(code)] == bytes(len(code))
        buf[off:off + len(code)] = code
    for addr, word in {
        coop + 4: 5, coop + 12: player, coop + 0x20: 7, context + 8: player,
        graph + 0x34: probe.STATE, combat + 0xa0: 0x42a00000, hit + 0xc: 0x43700000,
    }.items():
        struct.pack_into('<I', buf, addr - base, word)
    with tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp) / 'fixture.bin'
        binary.write_bytes(buf)
        ps = Path(os.environ['WINDIR']) / 'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
        script = Path(__file__).with_name('test_boss_probe.ps1')
        subprocess.run([str(ps), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script), str(binary)], check=True)


if __name__ == '__main__':
    main()
