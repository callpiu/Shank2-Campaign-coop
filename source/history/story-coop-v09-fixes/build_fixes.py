"""Narrow native fixes layered on frozen v0.8 production binaries."""
from pathlib import Path
import sys,struct,json,hashlib
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent/'story-coop-v05'),str(HERE.parent/'story-coop-v04')]
from native import pefile
from loadout_code import hash_name
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
def routines(asm,code,data,diag,old_bool,common=0x53d3f0,get_body=0x40bb40,move=0x4e9b60):
 scoped=asm(f'''push ebp
mov ebp,esp
push esi
push edi
push ebx
push dword ptr [{data+4}]
mov esi,ecx
mov edi,dword ptr [ebp+8]
cmp dword ptr [esi+8],{hash_name('resetPounceBlur')}
jne invoke
cmp dword ptr [{diag+4}],5
jne invoke
test edi,edi
jz invoke
mov eax,dword ptr [edi+8]
test eax,eax
jz invoke
cmp eax,dword ptr [{diag+12}]
je actor
cmp eax,dword ptr [{diag+16}]
jne invoke
actor:
mov edx,dword ptr [{diag+36}]
test edx,edx
jz invoke
cmp dword ptr [eax+0x20],edx
jne invoke
mov dword ptr [{data+4}],eax
inc dword ptr [{data+8}]
invoke:
push edi
mov ecx,esi
call {common}
pushfd
mov ecx,dword ptr [esp+4]
mov dword ptr [{data+4}],ecx
popfd
lea esp,[esp+4]
pop ebx
pop edi
pop esi
pop ebp
ret 4''',code)
 boolean=asm(f'''cmp dword ptr [{data+4}],0
je original
cmp ebx,dword ptr [{data+4}]
jne original
cmp ecx,dword ptr [{diag+36}]
jne original
inc dword ptr [{data+12}]
xor eax,eax
ret
original:
jmp {old_bool}''',code+0xc0)
 recall=asm(f'''push ebp
mov ebp,esp
push esi
mov esi,eax
mov ecx,esi
call {get_body}
test eax,eax
jz done
mov edx,eax
mov ecx,dword ptr [ebp+8]
push 0
push 0
call {move}
inc dword ptr [{data+16}]
done:
pop esi
pop ebp
ret 8''',code+0x100)
 assert len(scoped)<=0xc0 and len(boolean)<=0x40 and len(recall)<=0x80
 return {0:scoped,0xc0:boolean,0x100:recall}
def build(source,target):
 b=Path(source).read_bytes();pe=pefile.PE(data=b);base=0x400000
 sections={s.Name.rstrip(b'\0'):s for s in pe.sections};off=lambda va:pe.get_offset_from_rva(va-base)
 code=base+sections[b'.camx'].VirtualAddress+0xe00;data=base+sections[b'.camdat'].VirtualAddress+0xfc0
 old_bool=0x4d09df+5+struct.unpack_from('<i',b,off(0x4d09df)+1)[0]
 assert b[off(0x4d09df)]==0xe8 and old_bool==base+sections[b'.coop'].VirtualAddress+0x4e00
 assert struct.unpack_from('<I',b,off(0x75aa64))[0]==0x53d3f0
 ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
 blobs=routines(asm,code,data,0x7ff000,old_bool);out=bytearray(b)
 for rel,blob in blobs.items():
  assert b[off(code+rel):off(code+rel)+len(blob)]==b'\xcc'*len(blob)
  out[off(code+rel):off(code+rel)+len(blob)]=blob
 assert b[off(data):off(data)+32]==bytes(32)
 struct.pack_into('<I',out,off(data),0x39495846)
 out[off(0x4d09df):off(0x4d09df)+5]=asm(f'call {code+0xc0}',0x4d09df)
 struct.pack_into('<I',out,off(0x75aa64),code)
 follow=base+sections[b'.coop'].VirtualAddress+0x2500
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 calls=[i for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(b[off(follow):off(follow)+0x300],follow) if i.mnemonic=='call' and i.op_str=='0x4d25e0']
 assert len(calls)==1
 a=calls[0].address;out[off(a):off(a)+5]=asm(f'call {code+0x100}',a)
 target=Path(target);target.parent.mkdir(exist_ok=True);target.write_bytes(out)
 report={'source_sha256':hashlib.sha256(b).hexdigest(),'sha256':hashlib.sha256(out).hexdigest(),'code':hex(code),'data':hex(data),'old_bool':hex(old_bool),'recall_call':hex(a),'f7_and_audio_unchanged':True,'status':'native scoped cleanup and physics-only recall; gameplay pending'}
 target.with_suffix('.fixes.json').write_text(json.dumps(report,indent=2));return report
if __name__=='__main__':
 reports=[]
 for mode in ['keyboard','pads']:
  for lang in ['en','chs']:
   name=f'{mode}-{lang}.exe';reports.append(build(HERE.parent/'story-coop-v08-options/final-release'/name,HERE/'final'/name))
 (HERE/'builds.json').write_text(json.dumps(reports,indent=2));print('Built four isolated fixes; frozen v0.8 release unchanged.')
