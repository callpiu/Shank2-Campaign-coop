"""Exercise the recovery effect-stop thunk with the original stack layout."""
import os
from pathlib import Path
import struct
import subprocess


def test(here, routine, ks_type, arch, mode, red, hit_loop, hit):
    base = 0x20000000
    diag, values, context, actor, combat, manager = (base+x for x in (0x1000,0x1100,0x1200,0x1300,0x1400,0x1700))
    ks = ks_type(arch,mode)
    asm = lambda source,address: bytes(ks.asm(source,address)[0])
    image = bytearray(0x2000)

    def put(offset, data):
        image[offset:offset+len(data)] = data

    put(0x400,routine(asm,base+0x400,diag,base+0x580,base+0x600))
    code = {
        0: f'push dword ptr [{values+0x20:#x}];call {base+0x100:#x};ret',
        0x40: f'push dword ptr [{values+0x20:#x}];call {base+0x200:#x};ret',
        0x100: f'''sub esp,8;push ebx;push ebp;push esi;push edi
            mov esi,{manager:#x};lea edx,[esp+16];mov dword ptr [edx],0x12345678;mov dword ptr [edx+4],773
            push dword ptr [{values+0x18:#x}];push dword ptr [{values+0x1c:#x}];push edx
            mov eax,{base+0x680:#x};jmp {base+0x400:#x}''',
        0x200: f'''sub esp,8;push ebx;push ebp;push esi;push edi
            mov esi,{manager:#x};lea edx,[esp+16];mov dword ptr [edx],0x12345678;mov dword ptr [edx+4],773
            push dword ptr [{values+0x18:#x}];push dword ptr [{values+0x1c:#x}];push edx
            mov eax,{base+0x680:#x};mov ecx,esi;call eax;pop edi;jmp {base+0x600:#x}''',
        0x580: f'mov eax,[{values+0x24:#x}];ret',
        0x600: 'pop esi;pop ebp;pop ebx;add esp,8;mov eax,0x1234;ret 4',
        0x680: f'''cmp ecx,{manager:#x};jne fail
            mov edx,[esp+4];cmp dword ptr [edx],0x12345678;jne fail
            cmp dword ptr [edx+4],773;jne fail
            mov edx,[esp+0xc];cmp edx,[{values+0x18:#x}];jne fail
            mov edx,[{values:#x}];cmp edx,3;jae fail
            mov eax,[esp+8];mov [{values+4:#x}+edx*4],eax
            inc dword ptr [{values:#x}]
            cmp eax,{hit_loop:#x};jne check_hit
            and dword ptr [{values+0x14:#x}],0xfffffffe
            check_hit:cmp eax,{hit:#x};jne done
            and dword ptr [{values+0x14:#x}],0xfffffffd
            done:ret 12
            fail:inc dword ptr [{values+0x10:#x}];ret 12''',
    }
    for offset,source in code.items():
        put(offset,asm(source,base+offset))
    for address, word in [(diag+4,5),(diag+12,actor+0x40),(diag+16,actor),(diag+36,0x4242),
                          (context+8,actor),(actor+0x20,0x4242),(values+0x14,3),
                          (values+0x18,2),(values+0x1c,red),(values+0x20,context),(values+0x24,combat)]:
        struct.pack_into('<I',image,address-base,word)
    struct.pack_into('<f',image,combat-base+0xa0,32)
    struct.pack_into('<f',image,combat-base+0x200,80)
    fixture = here/'recovery-fixture.bin'
    fixture.write_bytes(image)
    ps = Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(here/'test_recovery.ps1'),str(fixture)],check=True)
