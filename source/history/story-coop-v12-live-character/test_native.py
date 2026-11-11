"""Execute native row construction and independent queued selection on x86."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

from build import Ks, KS_ARCH_X86, KS_MODE_32, selection
from selector import CATALOG, FAMILY_HASHES, STRIDE, constants, hash_name, routines

HERE = Path(__file__).resolve().parent


def main():
    base = 0x20000000
    data = base + 0x1000
    config = base + 0x1c00
    r0, r1, a0, a1 = (base+n for n in (0x2000, 0x2100, 0x2200, 0x2a00))
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda text, addr: bytes(ks.asm(text, addr)[0])
    blocks = {
        0: routines(asm, base, data, base+0x400),
        0x180: selection(asm, base+0x180, data, config),
        0x400: asm(f'''cmp dword ptr [esp+4],0x42
            jne missing
            cmp dword ptr [edi],{FAMILY_HASHES[0]}
            je shank
            cmp dword ptr [edi],{FAMILY_HASHES[1]}
            jne missing
            mov eax,{r1}
            ret 4
            shank: mov eax,{r0}; ret 4
            missing: xor eax,eax; ret 4''', base+0x400),
        0x500: asm(f'push 0x42; call {base}; ret', base+0x500),
        0x1000: constants(data),
    }
    buf = bytearray(0x4000)
    for off, blob in blocks.items():
        assert buf[off:off+len(blob)] == bytes(len(blob))
        buf[off:off+len(blob)] = blob
    for family, record, start in [('shank', r0, a0), ('corina', r1, a1)]:
        rows = [x for x in CATALOG if x['family'] == family]
        end = start + STRIDE*(len(rows)+1)
        struct.pack_into('<2I', buf, record-base+0x24, start, end)
        for i, item in enumerate(rows):
            off = start-base + i*STRIDE
            struct.pack_into('<I', buf, off, item['hash'])
            buf[off+0x69] = 1
        struct.pack_into('<I', buf, end-base-STRIDE, 0xfeed)
    for i, family in enumerate(('shank', 'corina')):
        o = config-base+64*i
        struct.pack_into('<I', buf, o, 1)
        buf[o+4:o+4+len(family)] = family.encode()
        struct.pack_into('<5I', buf, o+20, hash_name(family), 1111+i, 2222+i, 3333+i, 2+i)

    with tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp)/'character-test.bin'
        binary.write_bytes(buf)
        ids = Path(tmp)/'ids.json'
        ids.write_text(json.dumps(dict(skins=[item['hash'] for item in CATALOG],
                                       weapons=[hash_name(x) for x in ('machete','throwingknives','sword','revolver')])) )
        ps = Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
        subprocess.run([str(ps), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(HERE/'test_native.ps1'),
                        str(binary), str(ids)], check=True)


if __name__ == '__main__':
    main()
