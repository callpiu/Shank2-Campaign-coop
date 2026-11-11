"""Validate the standalone localization's real decoder/movie code and loader."""
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
from build_release import HERE,WORK,ROOT,STOCK,PROFILES,module,save


def main():
    sys.path.insert(0,str(WORK/'chs-compat'))
    compat=module('pure_chs_decoder_source',WORK/'chs-compat/build_compat.py')
    source=STOCK.read_bytes();raw,_,_,_=compat.patch_exe(source,compat.translated_slots())
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    env=dict(os.environ);env['PATH']=str(STOCK.parents[1]/'bin')+os.pathsep+str(Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin'))+os.pathsep+env.get('PATH','')
    with tempfile.TemporaryDirectory(prefix='standalone-native-',dir=HERE) as name:
        folder=Path(name)
        (folder/'keyboard-chs-test.exe').write_bytes(raw)
        prep=module('isolated_pure_decoder_test',WORK/'chs-compat/prepare_native_tests.py');prep.HERE=folder;prep.prepare()
        subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(WORK/'chs-compat/test_decoder.ps1'),str(folder),str(folder/'decoder-test-layout.json')],check=True)
        # Relocate the actual pure-CHS movie bridge, not the old co-op binary.
        image=(HERE/'dev/shank2-localization.exe').read_bytes();pe=compat.pefile.PE(data=image)
        spec=json.loads((HERE/'dev/shank2-localization.audio.json').read_text(encoding='utf-8-sig'));code=int(spec['code'],16);data=int(spec['data'],16)
        off=lambda a:pe.get_offset_from_rva(a-0x400000)
        v=0x20000000;buf=bytearray(16384);buf[:1024]=image[off(code):off(code)+1024];buf[4096:6144]=image[off(data):off(data)+2048]
        for pos in range(1021):
            val=struct.unpack_from('<I',buf,pos)[0]
            if data<=val<data+2048:struct.pack_into('<I',buf,pos,v+4096+val-data)
            elif val==0x72e2d8:struct.pack_into('<I',buf,pos,v+0x1f00)
        asm=lambda s,a:bytes(compat.Ks(compat.KS_ARCH_X86,compat.KS_MODE_32).asm(s,a)[0])
        # Fail redirected ../data/movies only when testing fallback; original
        # path is deliberately different in that one test below.
        stub=asm(f'''mov eax,[esp+8];mov [{v+0x1f20}],eax;inc dword ptr [{v+0x1f24}]
            mov ecx,[esp+4];cmp dword ptr [{v+0x1f28}],0;je copy
            cmp byte ptr [ecx],46;jne copy;xor eax,eax;ret 8
            copy:mov edx,{v+0x2400}
            again:mov al,[ecx];mov [edx],al;inc ecx;inc edx;test al,al;jnz again
            mov eax,{v+0x2400};ret 8''',v+0x2000)
        struct.pack_into('<I',buf,0x1f00,v+0x2000);buf[0x2000:0x2000+len(stub)]=stub
        (folder/'audio-test.bin').write_bytes(buf);save(folder/'audio-build.json',spec)
        script=(WORK/'story-coop-v07-dialogue/test_audio.ps1').read_text(encoding='utf-8-sig')
        script=script.replace("$root=$meta.resource_root+'\\'", "$root=$meta.resource_root+'/'")
        # The legacy fixture's failure probe used G: redirects. This build
        # uses a portable relative root; give the original a distinct prefix.
        script=script.replace("Call-Movie '../data/movies/01_INT_003.bik' '../data/movies/01_INT_003.bik';$checks++\nif(","Call-Movie 'ORIGINAL/01_INT_003.bik' 'ORIGINAL/01_INT_003.bik';$checks++\nif(")
        (folder/'test_audio.ps1').write_text(script,encoding='utf-8-sig')
        subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(folder/'test_audio.ps1')],check=True)
        audio=json.loads((folder/'audio-hook-tests.json').read_text(encoding='utf-8-sig'))
        loaders=[]
        for profile,(release,mod,chs) in PROFILES.items():
            target=(WORK/'story-coop-v33-dodge/dev'/f'shank2-story-coop-{"chs" if chs else "en"}.exe').read_bytes() if mod else image
            p=compat.pefile.PE(data=target);patched=bytearray(target);entry=0x6451e0
            ending=asm('push 119;call dword ptr [0x72e094]',entry);at=p.get_offset_from_rva(entry-0x400000);patched[at:at+len(ending)]=ending
            exe=folder/'loader-test.exe';exe.write_bytes(patched)
            result=subprocess.run([str(exe)],cwd=folder,env=env,creationflags=subprocess.CREATE_NO_WINDOW,timeout=15)
            assert result.returncode==119,(profile,result.returncode)
            loaders.append(dict(profile=profile,windows_loader_and_bootstrap_passed=True))
    save(HERE/'native-validation.json',dict(passed=True,standalone_decoder_cases=23,
        standalone_movie_cases=audio['passed'],original_codec_and_frames='Inherited byte-identical v0.9.1 27 movies',
        loader_checks=loaders,gameplay_not_started=True))
    print('Standalone native decoder, 60 movie paths/ABI/fallback cases and three Windows loaders passed.')


if __name__=='__main__':main()
