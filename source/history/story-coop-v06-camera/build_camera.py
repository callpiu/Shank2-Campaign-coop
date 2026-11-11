"""Development-only shared framing, layered on the tested v0.5 game copy."""
from pathlib import Path
import sys,struct,json,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
align=lambda x,a:(x+a-1)//a*a

def build(source=None,target=None):
 source=Path(source) if source else HERE.parent/'story-coop-v05/final/shank2-coop-v05-keyboard-chs.exe'
 target=Path(target) if target else HERE/'shank2-coop-v06-camera-test.exe'
 b=source.read_bytes();pe=pefile.PE(data=b);out=bytearray(b);base=0x400000
 off=lambda a:pe.get_offset_from_rva(a-base)
 rva=align(max(s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData) for s in pe.sections),4096)
 code=base+rva;data=code+4096
 asm=lambda s,a:bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(s,a)[0])
 routines={}
 # Update methods all take (GameSim*, dt) and return with ret8. Fixed cameras
 # are observed, never reframed. Both rail and default follow retain native
 # update/rail behavior before a bounded zoom correction is applied.
 for kind,entry,vtable in [(0,0x52ea30,0x75a158),(1,0x52fb40,0x75a180),(2,0x52e6e0,0x75a130)]:
  slot=data+0x40+kind*0x40
  routines[kind*0x100]=asm(f'''push ebp
mov ebp,esp
push esi
mov esi,ecx
push dword ptr [ebp+12]
push dword ptr [ebp+8]
call {entry}
pushfd
pushad
inc dword ptr [{slot}]
mov dword ptr [{slot+4}],esi
mov eax,dword ptr [ebp+8]
mov dword ptr [{slot+8}],eax
mov eax,dword ptr [esi+0x48]
mov dword ptr [{slot+12}],eax
mov eax,dword ptr [esi+0x4c]
mov dword ptr [{slot+16}],eax
mov eax,dword ptr [esi+0x50]
mov dword ptr [{slot+20}],eax
mov dword ptr [{slot+24}],eax
mov dword ptr [{slot+28}],0
mov ebx,{kind}
mov edi,dword ptr [ebp+8]
call {code+0x400}
popad
popfd
pop esi
pop ebp
ret 8''',code+kind*0x100)
  assert struct.unpack_from('<I',b,off(vtable))[0]==entry
  struct.pack_into('<I',out,off(vtable),code+kind*0x100)
 # SSE fitter: ECX state has native center/zoom, two positions, dt and the
 # previous output. Does not modify a character, native zoom definition or Y.
 fitter=f'''movss xmm0,dword ptr [ecx+8]
xorps xmm7,xmm7
comiss xmm0,xmm7
jbe invalid
jp invalid
comiss xmm0,dword ptr [{data+0x124}]
ja invalid
movss xmm1,dword ptr [ecx+12]
subss xmm1,dword ptr [ecx]
andps xmm1,xmmword ptr [{data+0x140}]
movss xmm2,dword ptr [ecx+20]
subss xmm2,dword ptr [ecx]
andps xmm2,xmmword ptr [{data+0x140}]
maxss xmm1,xmm2
comiss xmm1,dword ptr [{data+0x128}]
ja invalid
jp invalid
addss xmm1,dword ptr [{data+0x100}]
movss xmm2,dword ptr [{data+0x108}]
divss xmm2,xmm1
movss xmm3,dword ptr [ecx+16]
subss xmm3,dword ptr [ecx+4]
andps xmm3,xmmword ptr [{data+0x140}]
movss xmm4,dword ptr [ecx+24]
subss xmm4,dword ptr [ecx+4]
andps xmm4,xmmword ptr [{data+0x140}]
maxss xmm3,xmm4
comiss xmm3,dword ptr [{data+0x128}]
ja invalid
jp invalid
addss xmm3,dword ptr [{data+0x104}]
movss xmm4,dword ptr [{data+0x10c}]
divss xmm4,xmm3
minss xmm2,xmm4
minss xmm2,xmm0
movaps xmm5,xmm0
mulss xmm5,dword ptr [{data+0x110}]
maxss xmm2,xmm5
movss dword ptr [ecx+44],xmm2
movss dword ptr [ecx+48],xmm5
cmp dword ptr [ecx+36],0
jne previous
movss dword ptr [ecx+32],xmm0
previous:
movss xmm6,dword ptr [ecx+32]
minss xmm6,xmm0
maxss xmm6,xmm5
movss xmm1,dword ptr [ecx+28]
maxss xmm1,xmm7
minss xmm1,dword ptr [{data+0x11c}]
comiss xmm2,xmm6
jb widening
mulss xmm1,dword ptr [{data+0x118}]
jmp interpolate
widening:
mulss xmm1,dword ptr [{data+0x114}]
interpolate:
minss xmm1,dword ptr [{data+0x120}]
subss xmm2,xmm6
mulss xmm2,xmm1
addss xmm2,xmm6
minss xmm2,xmm0
maxss xmm2,xmm5
movss dword ptr [ecx+32],xmm2
movss dword ptr [ecx+40],xmm2
mov dword ptr [ecx+36],1
ret
invalid:
movss dword ptr [ecx+40],xmm0
mov dword ptr [ecx+36],0
ret'''
 routines[0x900]=asm(fitter,code+0x900)
 helper=f'''cmp ebx,2
je done
cmp dword ptr [0x7ff004],5
jne done
cmp edi,dword ptr [0x7ff024]
jne done
cmp dword ptr [edi],0x75017c
jne done
test ebx,ebx
jnz eligible
cmp dword ptr [esi+8],0xffffffff
jne done
eligible:
mov eax,ebx
shl eax,6
lea edx,[eax+{data+0x40}]
mov dword ptr [edx+28],1
call dword ptr [0x72e234]
cmp eax,dword ptr [0x7d7ed4]
jne keyboard_done
push 0x76
call dword ptr [0x72e224]
test ax,0x8000
jz released
cmp dword ptr [{data+8}],0
jne keyboard_done
mov dword ptr [{data+8}],1
xor dword ptr [{data+4}],1
inc dword ptr [{data+12}]
jmp keyboard_done
released:
mov dword ptr [{data+8}],0
keyboard_done:
mov eax,ebx
shl eax,7
add eax,{data+0x200}
push eax
cmp dword ptr [{data+4}],0
je inactive
cmp dword ptr [eax+52],esi
je same_camera
mov dword ptr [eax+52],esi
mov dword ptr [eax+36],0
same_camera:
mov ecx,dword ptr [esi+0x48]
mov dword ptr [eax],ecx
mov ecx,dword ptr [esi+0x4c]
mov dword ptr [eax+4],ecx
mov ecx,dword ptr [esi+0x50]
mov dword ptr [eax+8],ecx
mov ecx,dword ptr [ebp+12]
mov dword ptr [eax+28],ecx
push 0
mov ecx,edi
call 0x6a9640
test eax,eax
jz inactive
mov ecx,eax
call 0x40bb40
test eax,eax
jz inactive
mov edx,dword ptr [esp]
add edx,12
push edx
push eax
call 0x4e77c0
push 1
mov ecx,edi
call 0x6a9640
test eax,eax
jz inactive
mov ecx,eax
call 0x40bb40
test eax,eax
jz inactive
mov edx,dword ptr [esp]
add edx,20
push edx
push eax
call 0x4e77c0
mov ecx,dword ptr [esp]
movups xmm0,xmmword ptr [ecx+12]
andps xmm0,xmmword ptr [{data+0x140}]
cmpps xmm0,xmmword ptr [{data+0x150}],1
movmskps eax,xmm0
cmp eax,15
jne inactive
test ebx,ebx
jnz fit
movss xmm0,dword ptr [ecx+20]
subss xmm0,dword ptr [ecx+12]
mulss xmm0,dword ptr [{data+0x12c}]
addss xmm0,dword ptr [ecx]
movss dword ptr [ecx],xmm0
movss dword ptr [esi+0x48],xmm0
movss xmm0,dword ptr [ecx+24]
subss xmm0,dword ptr [ecx+16]
mulss xmm0,dword ptr [{data+0x12c}]
addss xmm0,dword ptr [ecx+4]
movss dword ptr [ecx+4],xmm0
movss dword ptr [esi+0x4c],xmm0
fit:
call {code+0x900}
mov ecx,dword ptr [esp]
mov eax,dword ptr [ecx+40]
mov dword ptr [esi+0x50],eax
mov edx,ebx
shl edx,6
mov dword ptr [edx+{data+0x58}],eax
inc dword ptr [{data+16}]
add esp,4
jmp done
inactive:
mov eax,dword ptr [esp]
mov dword ptr [eax+36],0
add esp,4
done:
ret'''
 routines[0x400]=asm(helper,code+0x400)
 codebytes=bytearray(b'\xcc'*4096);occupied=[]
 for rel,blob in routines.items():
  assert rel+len(blob)<=4096 and all(rel>=end or rel+len(blob)<=start for start,end in occupied),(hex(rel),len(blob))
  assert sum(i.size for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(blob,code+rel))==len(blob)
  occupied.append((rel,rel+len(blob)));codebytes[rel:rel+len(blob)]=blob
 state=bytearray(4096);struct.pack_into('<II',state,0,0x364d4143,1)
 for rel,value in [(0x100,160.),(0x104,180.),(0x108,640.),(0x10c,360.),(0x110,.625),(0x114,8.),(0x118,2.),(0x11c,.1),(0x120,1.),(0x124,4.),(0x128,1e7),(0x12c,.5)]:struct.pack_into('<f',state,rel,value)
 struct.pack_into('<4I',state,0x140,*([0x7fffffff]*4))
 struct.pack_into('<4f',state,0x150,*([1e7]*4))
 table=pe.sections[-1].get_file_offset()+40;assert table+80<=pe.OPTIONAL_HEADER.SizeOfHeaders
 for i,(name,rv,payload,flags) in enumerate([(b'.camx',rva,codebytes,0x60000020),(b'.camdat',rva+4096,state,0xc0000040)]):
  raw=align(len(out),pe.OPTIONAL_HEADER.FileAlignment);out.extend(bytes(raw-len(out)));out.extend(payload)
  out[table+i*40:table+(i+1)*40]=struct.pack('<8sIIIIIIHHI',name,4096,rv,4096,raw,0,0,0,0,flags)
 struct.pack_into('<H',out,pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),len(pe.sections)+2)
 struct.pack_into('<I',out,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),rva+8192)
 target.write_bytes(out)
 report={'source_sha256':hashlib.sha256(b).hexdigest(),'sha256':hashlib.sha256(out).hexdigest(),'code':hex(code),'data':hex(data),'max_view_expansion':1.6,'toggle':'F7','automatic_recall':False,'modified_camera_types':['Rail','Follow with default target'],'fixed_and_script_targets':'untouched','status':'development build; native fitter tests and gameplay validation required'}
 target.with_suffix('.camera.json').write_text(json.dumps(report,indent=2))
 if target.name=='shank2-coop-v06-camera-test.exe':(HERE/'build.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report));return report

if __name__=='__main__':build()
