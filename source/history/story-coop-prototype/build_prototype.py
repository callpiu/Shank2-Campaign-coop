"""Version-locked experimental Shank 2 campaign second-player patch.

Only the campaign Init vtable entry is redirected. Two relocated copies of the
original campaign initialization preserve its ABI and checkpoint selection.
The second copy registers player index 1 and a distinct input device, while
skipping checkpoint actions. No game code/assets are distributed by this file.
"""
from pathlib import Path
import argparse, hashlib, json, struct, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pydeps'))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_JUMP, CS_GRP_CALL
from capstone.x86 import X86_OP_IMM
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

EXPECTED='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
START,END=0x6a9290,0x6a955b
ENTRY=0x75023c+0x44
align=lambda n,a:(n+a-1)//a*a

def build(source:Path,destination:Path,p1:int,p2:int):
    data=source.read_bytes()
    if hashlib.sha256(data).hexdigest()!=EXPECTED:
        raise ValueError('Unsupported EXE hash; refusing to patch. Use the untouched Steam executable.')
    if not 0<=p1<=4 or not 1<=p2<=4 or p1==p2:
        raise ValueError('p1 must be 0..4, p2 1..4, and distinct. Xbox pads 1 and 2 use IDs 1 and 2.')
    pe=pefile.PE(data=data);base=pe.OPTIONAL_HEADER.ImageBase
    if base!=0x400000 or pe.FILE_HEADER.Machine!=0x14c or pe.OPTIONAL_HEADER.DllCharacteristics&0x40:
        raise ValueError('Unexpected image layout or ASLR; refusing patch.')
    off=lambda a:pe.get_offset_from_rva(a-base)
    if struct.unpack_from('<I',data,off(ENTRY))[0]!=START:raise ValueError('Unexpected vtable.')
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
    original=list(md.disasm(data[off(START):off(START)+(END-START)],START))
    if original[-1].address+original[-1].size!=END:raise ValueError('Incomplete decode')
    rv=align(max(s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData) for s in pe.sections),0x1000)
    codebase=base+rv;diag=codebase+0x3000
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    def assemble(src,address):return bytes(ks.asm(src,address)[0])
    def relocate(address,second):
        out=[]
        for ins in original:
            a=ins.address;out.append(f'L{a:x}:')
            # Main controller is explicit, so keyboard menu navigation cannot
            # accidentally bind player one to keyboard in a two-pad experiment.
            if a==0x6a9363:
                out.append(f'mov ecx, {p2 if second else p1}')
                out.append(f'mov dword ptr [{diag+(24 if second else 20):#x}], ecx')
                continue
            if a==0x6a9388:
                out.append(f'mov esi, {1 if second else 0}');continue
            if second and a==0x6a951f:
                out.append('jmp L6a953a');continue
            op=ins.op_str
            if (ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_CALL)) and ins.operands and ins.operands[0].type==X86_OP_IMM:
                target=ins.operands[0].imm
                if START<=target<END:op=f'L{target:x}'
            out.append(f'{ins.mnemonic} {op}')
            if a==0x6a9356:
                out.append(f'mov dword ptr [{diag+(16 if second else 12):#x}], eax')
                out.append(f'mov dword ptr [{diag+4:#x}], {4 if second else 2}')
            if a==0x6a92b8:
                out.append(f'mov dword ptr [{diag+8:#x}], ecx')
            if a==0x6a92c6:
                out.append(f'mov dword ptr [{diag+28:#x}], eax')
        src='\n'.join(out)
        return assemble(src,address),src
    first,src1=relocate(codebase+0x100,False)
    second,src2=relocate(codebase+0x1100,True)
    if len(first)>0x1000 or len(second)>0x1000:raise ValueError('Function overlap')
    wrapper=assemble(f'''
push esi
mov esi, ecx
mov dword ptr [{diag+4:#x}], 1
inc dword ptr [{diag+32:#x}]
mov dword ptr [{diag+12:#x}], 0
mov dword ptr [{diag+16:#x}], 0
call {codebase+0x100:#x}
mov dword ptr [{diag+4:#x}], 3
mov ecx, esi
call {codebase+0x1100:#x}
mov dword ptr [{diag+4:#x}], 5
pop esi
ret
''',codebase)
    code=bytearray(b'\xcc'*0x3000)
    code[:len(wrapper)]=wrapper;code[0x100:0x100+len(first)]=first;code[0x1100:0x1100+len(second)]=second
    # The code and diagnostics have separate RX / RW PE sections.
    sections=[(b'.coop',rv,bytes(code),0x60000020),(b'.coopdat',rv+0x3000,struct.pack('<I',0x504f4f43)+b'\0'*60,0xc0000040)]
    raw=bytearray(data);table=pe.sections[-1].get_file_offset()+40
    if table+80>pe.OPTIONAL_HEADER.SizeOfHeaders:raise ValueError('Insufficient section headers')
    for j,(name,rva,blob,flags) in enumerate(sections):
        fileoff=align(len(raw),pe.OPTIONAL_HEADER.FileAlignment)
        size=align(len(blob),pe.OPTIONAL_HEADER.FileAlignment)
        raw.extend(b'\0'*(fileoff-len(raw)));raw.extend(blob);raw.extend(b'\0'*(size-len(blob)))
        header=struct.pack('<8sIIIIIIHHI',name,len(blob),rva,size,fileoff,0,0,0,0,flags)
        raw[table+j*40:table+(j+1)*40]=header
    struct.pack_into('<H',raw,pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),len(pe.sections)+2)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),rv+0x4000)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfCode'),pe.OPTIONAL_HEADER.SizeOfCode+0x3000)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfInitializedData'),pe.OPTIONAL_HEADER.SizeOfInitializedData+0x200)
    struct.pack_into('<I',raw,off(ENTRY),codebase)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),0)
    checked=pefile.PE(data=bytes(raw))
    if checked.get_dword_at_rva(ENTRY-base)!=codebase:raise ValueError('Patch verification failed')
    for addr,blob in [(codebase,wrapper),(codebase+0x100,first),(codebase+0x1100,second)]:
        decoded=list(md.disasm(blob,addr))
        if sum(i.size for i in decoded)!=len(blob):raise ValueError('Generated code decode failed')
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.resolve()==source.resolve():raise ValueError('Output must differ from input')
    destination.write_bytes(raw)
    manifest={'version':'0.1-experimental','input_sha256':EXPECTED,'output_sha256':hashlib.sha256(raw).hexdigest(),'p1_device':p1,'p2_device':p2,'wrapper':hex(codebase),'diagnostics':hex(diag),'first_clone_bytes':len(first),'second_clone_bytes':len(second),'status':'Built and statically checked; gameplay validation required'}
    destination.with_suffix('.coop.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    destination.with_suffix('.coop.asm').write_text('; P1\n'+src1+'\n; P2\n'+src2,encoding='utf-8')
    print(json.dumps(manifest,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path);ap.add_argument('--p1',type=int,default=1);ap.add_argument('--p2',type=int,default=2);args=ap.parse_args()
    build(args.source,args.destination,args.p1,args.p2)
