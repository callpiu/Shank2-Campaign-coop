"""Terrain rescue prototype: move downed partners without reviving them."""
from pathlib import Path
import sys,struct,json,hashlib
sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parent.parent/'story-coop-v04')]
from native import pefile
from loadout_code import hash_name
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'chs-compat/keyboard-chs-test.exe'
align=lambda v,a:(v+a-1)//a*a

def build(source=SOURCE,target=None):
 source=Path(source);target=Path(target) if target else HERE/'shank2-coop-v05-terrain-test.exe'
 b=source.read_bytes();pe=pefile.PE(data=b);out=bytearray(b);base=0x400000
 off=lambda va:pe.get_offset_from_rva(va-base)
 assert struct.unpack_from('<I',b,off(0x750188))[0]==0x7fc500
 rv=align(max(s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData) for s in pe.sections),4096);codeva=base+rv;data=codeva+4096
 asm=lambda src,va:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(src,va)[0])
 wrapper=asm(f'''
push ebp
mov ebp, esp
push esi
mov esi, ecx
push dword ptr [ebp+8]
call 0x7fc500
cmp dword ptr [0x7ff004], 5
jne done
cmp esi, dword ptr [0x7ff024]
jne done
mov eax, dword ptr [0x7ff00c]
mov edx, dword ptr [0x7ff010]
test eax, eax
jz done
test edx, edx
jz done
push ebx
push edi
mov esi, eax
mov edi, edx
mov ebx, 0
call {codeva+0x100}
mov esi, dword ptr [0x7ff010]
mov edi, dword ptr [0x7ff00c]
mov ebx, 1
call {codeva+0x100}
pop edi
pop ebx
done:
pop esi
pop ebp
ret 4
''',codeva)
 hashes=[hash_name(n) for n in ['dead_fall','dead_fall_loop','dead_spike','dead_spike_loop','dead_gib']]
 checks='\n'.join(f'cmp eax, {v}; je terrain' for v in hashes)
 helper=asm(f'''
push esi
push edi
push ebx
mov ecx, esi
call 0x40e290
test eax, eax
jz done
mov eax, dword ptr [eax+0x34]
{checks}
mov dword ptr [{data+32}+ebx*4], 0
jmp done
terrain:
inc dword ptr [{data+8}+ebx*4]
cmp dword ptr [{data+32}+ebx*4], 0
jne done
mov ecx, edi
call 0x40e270
test eax, eax
jz done
cmp byte ptr [eax+0x3c], 0
jne done
movss xmm0, dword ptr [eax+0xa0]
xorps xmm1, xmm1
comiss xmm0, xmm1
jbe done
mov ecx, edi
call 0x40bb40
test eax, eax
jz done
push {data+64}
push eax
call 0x4e77c0
mov ecx, esi
call 0x40bb40
test eax, eax
jz done
push 0
push 0
mov edx, eax
mov ecx, {data+64}
call 0x4e9b60
push {hash_name('dead')}
call 0x4d1520
mov dword ptr [{data+32}+ebx*4], 1
inc dword ptr [{data+16}+ebx*4]
done:
pop ebx
pop edi
pop esi
ret
''',codeva+0x100)
 assert len(wrapper)<0x100 and len(helper)<0x500
 code=bytearray(b'\xcc'*4096);code[:len(wrapper)]=wrapper;code[0x100:0x100+len(helper)]=helper
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for address,blob in [(codeva,wrapper),(codeva+0x100,helper)]:assert sum(i.size for i in md.disasm(blob,address))==len(blob)
 table=pe.sections[-1].get_file_offset()+40;assert table+80<=pe.OPTIONAL_HEADER.SizeOfHeaders
 for i,(name,rva,payload,flags) in enumerate([(b'.terrain',rv,bytes(code),0x60000020),(b'.terdata',rv+4096,bytes(4096),0xc0000040)]):
  raw=align(len(out),512);out.extend(bytes(raw-len(out)));out.extend(payload)
  out[table+i*40:table+(i+1)*40]=struct.pack('<8sIIIIIIHHI',name,4096,rva,4096,raw,0,0,0,0,flags)
 struct.pack_into('<H',out,pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),pe.FILE_HEADER.NumberOfSections+2)
 struct.pack_into('<I',out,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),rv+8192)
 struct.pack_into('<I',out,off(0x750188),codeva)
 target.write_bytes(out)
 report={'source_sha256':hashlib.sha256(b).hexdigest(),'output_sha256':hashlib.sha256(out).hexdigest(),'code':hex(codeva),'data':hex(data),'terrain_state_hashes':hashes,'teleport':'native physics 4e9b60; does not reset health/extensions','state_after':'dead','both_down':'skip automatic recall','status':'requires gameplay validation'}
 target.with_suffix('.terrain.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
 return report

if __name__=='__main__':build()
