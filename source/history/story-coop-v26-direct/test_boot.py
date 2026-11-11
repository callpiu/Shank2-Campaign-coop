"""Run the native bootstrap in a disposable image and exit before the game CRT."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from build import BASE, CONFIG_FILE, DEFAULTS, GAME, HERE, MAGIC, Ks, KS_ARCH_X86, KS_MODE_32, pefile, sha

orig=pefile.PE(str(GAME/'bin/shank2.exe'),fast_load=True)
entry=BASE+orig.OPTIONAL_HEADER.AddressOfEntryPoint
ks=Ks(KS_ARCH_X86,KS_MODE_32)
env={k:v for k,v in os.environ.items() if k.casefold() not in {'steamappid','steamgameid'}}
env['PATH']=str(GAME/'bin')+os.pathsep+env.get('PATH','')
rows=json.loads((HERE/'builds.json').read_text())
cases=[]
with tempfile.TemporaryDirectory(prefix='native-keys-',dir=HERE) as name:
    work=Path(name)
    launch=work/'fixture'/'boot.exe'
    launch.parent.mkdir()
    keys=launch.parent/CONFIG_FILE
    for row in rows:
        image=(HERE/'dev'/f'shank2-story-coop-{row["language"]}.exe').read_bytes()
        assert sha(image)==row['sha256']
        p=pefile.PE(data=image,fast_load=True)
        data=int(row['data'],16)
        code=bytes(ks.asm(f'''mov eax,[{data+0x88}]
          shl eax,8;or eax,[{data+0x84}]
          push eax;call dword ptr [0x72e094]''',entry)[0])
        at=p.get_offset_from_rva(entry-BASE)
        fixture=bytearray(image)
        fixture[at:at+len(code)]=code
        launch.write_bytes(fixture)
        remap=struct.pack('<28I',1,0x5a,*DEFAULTS[1:])
        badmode=struct.pack('<28I',2,0x5a,*DEFAULTS[1:])
        badkey=struct.pack('<28I',1,0,*DEFAULTS[1:])
        for desc,packet,expected in [('missing',None,0x4100),('valid',MAGIC+remap,0x5a01),
                                      ('wrong magic',b'TEST'+remap,0x4100),('truncated',MAGIC+remap[:-1],0x4100),
                                      ('trailing data',MAGIC+remap+b'\0',0x4100),('invalid mode',MAGIC+badmode,0x4100),
                                      ('invalid key',MAGIC+badkey,0x4100)]:
            if packet is None:
                keys.unlink(missing_ok=True)
            else:
                keys.write_bytes(packet)
            status=subprocess.run([str(launch)],cwd=work,env=env,creationflags=subprocess.CREATE_NO_WINDOW,timeout=10).returncode
            assert status==expected,(row['language'],desc,hex(status),hex(expected))
            cases.append({'language':row['language'],'case':desc,'status':hex(status)})
(HERE/'boot-validation.json').write_text(json.dumps({'passed':True,'cases':cases},indent=2)+'\n',encoding='utf8')
print('Windows executed both bootstraps: configuration found relative to EXE; 14 cases passed.')

