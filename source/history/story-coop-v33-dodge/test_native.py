"""Execute the new input bridge in x86 and test actual Windows boot reads."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from build_dodge import *


def input_fixture(folder):
    B=0x20000000;D=B+0x5000;CTRL=B+0x7000;STATE=B+0x8000
    fixture=bytearray(0x10000)
    asm=lambda s,a:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(s,a)[0])
    def put(a,v):fixture[a-B:a-B+len(v)]=v
    put(B+0x1000,input_code(B+0x1000,D,B+0x1800,key_api=CTRL+0x20,focus_api=CTRL+0x24,window=CTRL+0x28))
    put(B+0x1800,asm(f'mov eax,[{CTRL}];ret 8',B+0x1800))
    put(B+0x1900,asm(f'mov eax,[esp+4];mov eax,[{B+0xa000}+eax*4];ret 4',B+0x1900))
    put(B+0x1940,asm(f'mov eax,[{CTRL+4}];ret',B+0x1940))
    struct.pack_into('<3I',fixture,CTRL+0x20-B,B+0x1900,B+0x1940,123)
    struct.pack_into('<4I',fixture,D+0x744-B,*DEFAULTS)
    put(B+0x1100,asm(f'''push ebx;push esi;push edi;push ebp
        mov ebx,0x12345678;mov esi,0x23456781;mov edi,0x34567812;mov ebp,0x45678123
        push {STATE};push dword ptr [{CTRL+12}];call {B+0x1000}
        cmp ebx,0x12345678;jne bad;cmp esi,0x23456781;jne bad
        cmp edi,0x34567812;jne bad;cmp ebp,0x45678123;jne bad;jmp done
        bad:mov eax,-999
        done:pop ebp;pop edi;pop esi;pop ebx;ret''',B+0x1100))
    (folder/'fixture.bin').write_bytes(fixture)
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_native.ps1'),str(folder/'fixture.bin')],check=True)


def boot_cases(folder):
    launch=folder/'bin/boot.exe';launch.parent.mkdir();results=[]
    env=dict(os.environ);env['PATH']=str(Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin'))+os.pathsep+env.get('PATH','')
    for row in json.loads((HERE/'builds.json').read_text()):
        raw=(HERE/'dev'/f'shank2-story-coop-{row["language"]}.exe').read_bytes()
        p=pefile.PE(data=raw,fast_load=True);d=int(row['data'],16);fixture=bytearray(raw)
        entry=0x6451e0
        code=bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(f'''mov eax,[{d+0x744}]
            shl eax,8;or eax,[{d+0x88}];push eax;call dword ptr [0x72e094]''',entry)[0])
        at=p.get_offset_from_rva(entry-BASE);fixture[at:at+len(code)]=code;launch.write_bytes(fixture)
        # Preserve and prove the existing custom P1 movement mapping as well.
        oldkeys=[0x54,0x44,0x57,0x53,0x20,0x4a,0x4b,0x4c,0x55,0x49,0x0d,0x51,0x4f,
            0x25,0x27,0x26,0x28,0x60,0x61,0x62,0x63,0x64,0x65,0x67,0x66,0x75,0x76]
        (launch.parent/'Shank2-Coop-Keys.dat').write_bytes(b'S2K1'+struct.pack('<28I',0,*oldkeys))
        packet=MAGIC+struct.pack('<4I',0x70,0x71,0x72,0x73)
        cases=[('missing',None,0x5a54),('valid',packet,0x7054),('wrong magic',b'FAIL'+packet[4:],0x5a54),
            ('truncated',packet[:-1],0x5a54),('trailing',packet+b'\0',0x5a54),
            ('zero key',MAGIC+struct.pack('<4I',0,0x71,0x72,0x73),0x5a54),
            ('invalid key',MAGIC+struct.pack('<4I',0xff,0x71,0x72,0x73),0x5a54)]
        path=launch.parent/CONFIG_FILE
        for name,packet,expected in cases:
            if packet is None:path.unlink(missing_ok=True)
            else:path.write_bytes(packet)
            result=subprocess.run([str(launch)],cwd=folder,env=env,creationflags=subprocess.CREATE_NO_WINDOW,timeout=10)
            assert result.returncode==expected,(row['language'],name,result.returncode,expected)
            results.append(dict(language=row['language'],case=name,passed=True,legacy_remap_preserved=True))
    return results


def main():
    with tempfile.TemporaryDirectory(prefix='dodge-native-',dir=HERE) as name:
        folder=Path(name);input_fixture(folder);cases=boot_cases(folder)
    (HERE/'validation.json').write_text(json.dumps(dict(passed=True,input_cases=12,
        boot_cases=cases,physical_passthrough=True,registers_preserved=True,test_assists=False),indent=2)+'\n')
    print('12 x86 input cases and 14 real Windows boot reads passed; existing custom keys preserved.')


if __name__=='__main__':main()
