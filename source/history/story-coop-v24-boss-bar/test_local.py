"""Run the x86 guard and its native return/stack boundary in a local fixture."""
import os
from pathlib import Path
import struct
import subprocess

from build_local import HERE, Ks, KS_ARCH_X86, KS_MODE_32, routines


def main():
    base = 0x20000000
    diag, screen, action, values, vt, hud = (base+n for n in (0x1000,0x2000,0x4000,0x4100,0x4200,0x313c))
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda source, address: bytes(ks.asm(source, address)[0])
    image = bytearray(0x5000)
    code = base + 0x400
    setter, update = routines(asm, code, diag, values+8, base+0x600, vt)

    def put(offset, payload):
        image[offset:offset+len(payload)] = payload

    put(0x400, setter)
    put(0x480, update)
    bodies = {
        0: f'''push 1;mov ecx,{screen};mov edx,[ecx];call {code};mov [{action+0xc}],eax;ret''',
        0x40: f'''push 1;mov ecx,{screen};mov edx,[ecx];call dword ptr [edx+0x40];mov [{action+0x2c}],eax;ret''',
        0x80: f'''push dword ptr [{values+0x10}];mov ecx,{action};call {code+0x80};ret''',
        0xc0: f'''push dword ptr [{values+0x10}];mov ecx,{action+0x20};call {code+0x80};ret''',
        0x500: f'''inc dword ptr [{values}];lea eax,[ecx+0x113c];mov [ecx+0x11a0],eax;ret 4''',
        0x600: f'''inc dword ptr [{values+4}];cmp dword ptr [ebp+8],0;jne finish
            sub dword ptr [{values+0xc}],10;mov eax,1;jmp done
            finish:mov dword ptr [{screen+0x11a0}],{screen+0x10e0};mov eax,0
            done:mov esp,ebp;pop ebp;ret 4''',
    }
    for offset, source in bodies.items():
        put(offset, asm(source, base+offset))
    for addr, value in [(diag+4,5),(diag+12,1),(diag+16,2),(screen,vt),(screen+0x11a0,screen+0x10e0),
                        (vt+0x40,base+0x500),(vt+0x140,base+0x500),(values+0xc,61)]:
        struct.pack_into('<I', image, addr-base, value)
    fixture = HERE/'bar-fixture.bin'
    fixture.write_bytes(image)
    ps = Path(os.environ['WINDIR']) / 'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                    str(HERE/'test_local.ps1'), str(fixture)], check=True)


if __name__ == '__main__':
    main()
