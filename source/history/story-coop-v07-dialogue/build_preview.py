"""Redirect one movie in a development EXE; never replace managed resources."""
from pathlib import Path
import sys,struct,json,hashlib
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
TEST=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')
source=HERE.parent/'story-coop-v06-camera/shank2-coop-v06-camera-test.exe'
b=source.read_bytes();pe=pefile.PE(data=b);sections={s.Name.rstrip(b'\0'):s for s in pe.sections}
code=0x400000+sections[b'.camx'].VirtualAddress+0xc00
data=0x400000+sections[b'.camdat'].VirtualAddress+0x800
off=lambda a:pe.get_offset_from_rva(a-0x400000)
asm=lambda s,a:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(s,a)[0])
suffix=b'01_INT_003.bik';path=str(TEST/'data/movies/coop_dialogue_preview_intro.bik').encode('ascii')
hook=asm(f'''pushfd
pushad
mov esi,dword ptr [esp+40]
mov dword ptr [{data+12}],esi
test esi,esi
jz other
mov edx,esi
xor ecx,ecx
scan:
cmp byte ptr [edx],0
je found_end
inc edx
inc ecx
cmp ecx,1024
jb scan
jmp other
found_end:
mov dword ptr [{data+20}],ecx
mov edi,{data+64}
mov ebx,ecx
cmp ebx,255
jbe copy
mov ebx,255
copy:
test ebx,ebx
jz copied
mov al,byte ptr [esi]
mov byte ptr [edi],al
inc esi
inc edi
dec ebx
jmp copy
copied:
mov byte ptr [edi],0
cmp ecx,{len(suffix)}
jb other
je compare
cmp byte ptr [edx-{len(suffix)+1}],47
je compare
cmp byte ptr [edx-{len(suffix)+1}],92
jne other
compare:
lea esi,[edx-{len(suffix)}]
mov edi,{data+0x400}
mov ecx,{len(suffix)}
compare_char:
mov al,byte ptr [esi]
or al,32
mov bl,byte ptr [edi]
or bl,32
cmp al,bl
jne other
inc esi
inc edi
dec ecx
jnz compare_char
mov dword ptr [esp+40],{data+0x200}
inc dword ptr [{data+4}]
jmp invoke
other:
inc dword ptr [{data+8}]
invoke:
popad
popfd
push dword ptr [esp+8]
push dword ptr [esp+8]
call dword ptr [0x72e2d8]
mov dword ptr [{data+16}],eax
ret 8''',code)
assert len(hook)<0x400 and b[off(code):off(code)+len(hook)]==b'\xcc'*len(hook)
assert sum(i.size for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(hook,code))==len(hook)
out=bytearray(b);out[off(code):off(code)+len(hook)]=hook
needle=bytes.fromhex('ff15d8e27200');positions=[];start=0
while True:
    at=b.find(needle,start)
    if at<0:break
    positions.append(at);start=at+1
assert len(positions)==1
callva=pe.get_rva_from_offset(positions[0])+0x400000
out[positions[0]:positions[0]+6]=asm(f'call {code}',callva)+b'\x90'
struct.pack_into('<I',out,off(data),0x37445541)
for rel,blob in [(0x200,path+b'\0'),(0x400,suffix+b'\0')]:out[off(data+rel):off(data+rel)+len(blob)]=blob
target=HERE/'shank2-coop-v07-dialogue-test.exe';target.write_bytes(out)
report={'source_sha256':hashlib.sha256(b).hexdigest(),'sha256':hashlib.sha256(out).hexdigest(),'code':hex(code),'data':hex(data),'callsite':hex(callva),'movie_match':suffix.decode(),'new_resource_path':str(TEST/'data/movies/coop_dialogue_preview_intro.bik'),'camera_preserved':True,'original_movie_resource_unchanged':True,'status':'development-only preview; gameplay audio validation pending'}
(HERE/'preview-build.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
