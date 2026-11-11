"""Execute actual x86 audio wrappers from all four integrated builds."""
from pathlib import Path
import sys,struct,json,subprocess
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
v=0x20000000;ks=Ks(KS_ARCH_X86,KS_MODE_32);reports=[]
release='--release' in sys.argv
for row in json.loads((HERE/'builds.json').read_text()):
 name=row['mode']+'-'+row['language'];target=HERE/('final-release' if release else 'final')/f'{name}.exe'
 b=target.read_bytes();pe=pefile.PE(data=b);meta=json.loads(target.with_suffix('.audio.json').read_text());code=int(meta['code'],16);data=int(meta['data'],16)
 off=lambda a:pe.get_offset_from_rva(a-0x400000)
 buf=bytearray(16384);buf[:1024]=b[off(code):off(code)+1024];buf[4096:6144]=b[off(data):off(data)+2048]
 for pos in range(1021):
  value=struct.unpack_from('<I',buf,pos)[0]
  if data<=value<data+2048:struct.pack_into('<I',buf,pos,v+4096+value-data)
  elif value==0x72e2d8:struct.pack_into('<I',buf,pos,v+0x1f00)
 stub=bytes(ks.asm(f'''mov eax,dword ptr [esp+8];mov dword ptr [{v+0x1f20}],eax
inc dword ptr [{v+0x1f24}]
mov ecx,dword ptr [esp+4]
cmp dword ptr [{v+0x1f28}],0
je copy
mov dword ptr [{v+0x1f28}],0
xor eax,eax;ret 8
copy:
mov edx,{v+0x2400}
loop:
mov al,byte ptr [ecx];mov byte ptr [edx],al;inc ecx;inc edx;test al,al;jnz loop
mov eax,{v+0x2400};ret 8''',v+0x2000)[0])
 struct.pack_into('<I',buf,0x1f00,v+0x2000);buf[0x2000:0x2000+len(stub)]=stub
 folder=HERE/('native-tests-release' if release else 'native-tests')/name;folder.mkdir(parents=True,exist_ok=True)
 (folder/'audio-test.bin').write_bytes(buf);(folder/'audio-build.json').write_text(json.dumps(meta))
 script=(HERE.parent/'story-coop-v07-dialogue/test_audio.ps1').read_text(encoding='utf-8-sig')
 script=script.replace("$root=$meta.resource_root+'\\'", "$root=$meta.resource_root+'/'")
 (folder/'test_audio.ps1').write_text(script,encoding='utf-8-sig')
 result=subprocess.run([r'C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(folder/'test_audio.ps1')],capture_output=True,text=True)
 assert result.returncode==0,(name,result.stdout,result.stderr)
 reports.append({'build':name,**json.loads((folder/'audio-hook-tests.json').read_text(encoding='utf-8-sig'))})
(HERE/('native-release-tests.json' if release else 'native-tests.json')).write_text(json.dumps(reports,indent=2))
print('Passed',sum(r['passed'] for r in reports),'native path/flag/disabled/fallback cases across four builds.')
