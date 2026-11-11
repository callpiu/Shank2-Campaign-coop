"""Optional allowlisted movie-audio overlay for the camera development build."""
from pathlib import Path
import sys,struct,json,hashlib
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
TEST=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')
def build(source=None,target=None,resource_root=None,code_address=None,data_address=None):
 source=Path(source) if source else HERE.parent/'story-coop-v06-camera/shank2-coop-v06-camera-test.exe'
 b=source.read_bytes();pe=pefile.PE(data=b);sec={s.Name.rstrip(b'\0'):s for s in pe.sections}
 code=code_address if code_address is not None else 0x400000+sec[b'.camx'].VirtualAddress+0xc00
 data=data_address if data_address is not None else 0x400000+sec[b'.camdat'].VirtualAddress+0x800
 off=lambda a:pe.get_offset_from_rva(a-0x400000)
 asm=lambda s,a:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(s,a)[0])
 manifest=json.loads((HERE/'enhanced-manifest.json').read_text());assert manifest['complete'] and len(manifest['files'])==27
 names=sorted(r['file'] for r in manifest['files']);table=b''.join(s.encode()+b'\0' for s in names)+b'\0'
 assert len(table)<=0x2c0
 root=(str(resource_root) if resource_root is not None else str(TEST/'data/movies/coop_dialogue_enhanced')).encode('ascii').rstrip(b'/\\')+b'/'
 assert len(root)+max(map(len,names))+1<480
 hook=asm(f'''push ebp
 mov ebp,esp
 sub esp,512
 mov dword ptr [ebp-4],0
 pushfd
 pushad
 mov esi,dword ptr [ebp+8]
 mov dword ptr [{data+12}],esi
 cmp dword ptr [{data+28}],0
 je other
 test esi,esi
 jz other
 mov edx,esi
 mov edi,esi
 xor ecx,ecx
 scan:
 mov al,byte ptr [edx]
 test al,al
 jz found_end
 cmp al,47
 je separator
 cmp al,92
 jne next_char
 separator:
 lea edi,[edx+1]
 next_char:
 inc edx
 inc ecx
 cmp ecx,1024
 jb scan
 jmp other
 found_end:
 mov dword ptr [ebp-8],edi
 mov dword ptr [{data+20}],ecx
 mov edi,{data+64}
 cmp ecx,255
 jbe copy_original
 mov ecx,255
 copy_original:
 test ecx,ecx
 jz copied_original
 mov al,byte ptr [esi]
 mov byte ptr [edi],al
 inc esi
 inc edi
 dec ecx
 jmp copy_original
 copied_original:
 mov byte ptr [edi],0
 mov esi,{data+0x140}
 xor edx,edx
 entry:
 cmp byte ptr [esi],0
 je other
 mov edi,dword ptr [ebp-8]
 compare:
 mov al,byte ptr [esi]
 mov bl,byte ptr [edi]
 or al,32
 or bl,32
 cmp al,bl
 jne mismatch
 cmp byte ptr [esi],0
 je matched
 inc esi
 inc edi
 jmp compare
 mismatch:
 cmp byte ptr [esi],0
 je next_entry
 inc esi
 jmp mismatch
 next_entry:
 inc esi
 inc edx
 jmp entry
 matched:
 inc dword ptr [{data+4}]
 inc dword ptr [{data+0x740}+edx*4]
 mov dword ptr [{data+32}],edx
 mov dword ptr [ebp-4],1
 lea edi,[ebp-512]
 mov esi,{data+0x400}
 copy_root:
 mov al,byte ptr [esi]
 test al,al
 jz root_done
 mov byte ptr [edi],al
 inc esi
 inc edi
 jmp copy_root
 root_done:
 mov esi,dword ptr [ebp-8]
 copy_basename:
 mov al,byte ptr [esi]
 mov byte ptr [edi],al
 inc esi
 inc edi
 test al,al
 jnz copy_basename
 lea esi,[ebp-512]
 mov edi,{data+0x500}
 copy_debug:
 mov al,byte ptr [esi]
 mov byte ptr [edi],al
 inc esi
 inc edi
 test al,al
 jnz copy_debug
 lea eax,[ebp-512]
 mov dword ptr [esp+28],eax
 jmp invoke
 other:
 inc dword ptr [{data+8}]
 mov eax,dword ptr [ebp+8]
 mov dword ptr [esp+28],eax
 invoke:
 popad
 popfd
 push dword ptr [ebp+12]
 push eax
 call dword ptr [0x72e2d8]
 test eax,eax
 jnz finished
 cmp dword ptr [ebp-4],1
 jne finished
 inc dword ptr [{data+24}]
 push dword ptr [ebp+12]
 push dword ptr [ebp+8]
 call dword ptr [0x72e2d8]
 finished:
 mov dword ptr [{data+16}],eax
 mov esp,ebp
 pop ebp
 ret 8''',code)
 assert len(hook)<1024 and b[off(code):off(code)+len(hook)]==b'\xcc'*len(hook)
 assert sum(i.size for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(hook,code))==len(hook)
 out=bytearray(b);out[off(code):off(code)+len(hook)]=hook
 needle=bytes.fromhex('ff15d8e27200');at=b.find(needle);assert at>=0 and b.find(needle,at+1)<0
 call=pe.get_rva_from_offset(at)+0x400000;out[at:at+6]=asm(f'call {code}',call)+b'\x90'
 struct.pack_into('<I',out,off(data),0x37445541);struct.pack_into('<I',out,off(data+28),1);struct.pack_into('<I',out,off(data+32),0xffffffff);struct.pack_into('<I',out,off(data+36),len(names))
 for delta,payload in [(0x140,table),(0x400,root+b'\0')]:out[off(data+delta):off(data+delta)+len(payload)]=payload
 target=Path(target) if target else HERE/'shank2-coop-v07-background-test.exe';target.write_bytes(out)
 report={'sha256':hashlib.sha256(out).hexdigest(),'source_sha256':hashlib.sha256(b).hexdigest(),'code':hex(code),'data':hex(data),'hook_bytes':len(hook),'profile':manifest['profile'],'files':names,'resource_root':root.decode().rstrip('/'),'fallback_to_original_on_failure':True,'filename_buffer':'per-call stack','camera_preserved':True,'status':'development-only; gameplay validation pending'}
 target.with_suffix('.audio.json').write_text(json.dumps(report,indent=2))
 if target.name=='shank2-coop-v07-background-test.exe':(HERE/'audio-build.json').write_text(json.dumps(report,indent=2))
 return report

if __name__=='__main__':
 print(json.dumps(build(),indent=2))
