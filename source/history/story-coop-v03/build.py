"""Version-locked experimental Shank 2 campaign second-player patch.

Two relocated copies of campaign initialization register distinct players.
Native start descriptors and the survival partner relation are prepared first;
an optional simulation-tick tether and keyboard-backed XInput thunks follow.
No game assets are distributed by this file.
"""
from pathlib import Path
import argparse, hashlib, json, struct, sys
local_deps=Path(__file__).resolve().parent/'pydeps'
if local_deps.is_dir():sys.path.insert(0,str(local_deps))
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_JUMP, CS_GRP_CALL
from capstone.x86 import X86_OP_IMM
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

EXPECTED='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
START,END=0x6a9290,0x6a955b
ENTRY=0x75023c+0x44
align=lambda n,a:(n+a-1)//a*a

def build(source:Path,destination:Path,p1:int,p2:int,keyboard=False,follow=True,input_probe=False,hud=False,loadouts=False):
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
    codebase=base+rv;diag=codebase+0x5000
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
            if second and ins.mnemonic=='call' and op=='0x404960':op='0x408d70'
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
push edi
push ebx
mov esi, ecx
mov dword ptr [{diag+4:#x}], 1
inc dword ptr [{diag+32:#x}]
mov dword ptr [{diag+12:#x}], 0
mov dword ptr [{diag+16:#x}], 0
call {codebase+0x2100:#x}
mov ecx, esi
call {codebase+0x100:#x}
mov dword ptr [{diag+4:#x}], 3
mov ecx, esi
call {codebase+0x1100:#x}
push dword ptr [{diag+16:#x}]
mov ecx, dword ptr [{diag+12:#x}]
call 0x40bb40
push eax
call 0x4eb360
mov dword ptr [{diag+4:#x}], 5
pop ebx
pop edi
pop esi
ret
''',codebase)
    prepare=assemble(f'''
mov ecx, dword ptr [esi+8]
mov dword ptr [{diag+36:#x}], ecx
call 0x404990
mov ebx, eax
mov ecx, eax
call 0x404960
mov edi, eax
mov dword ptr [edi+0x60], {p1}
mov dword ptr [edi+0x64], {p1}
push {p2}
push {p2}
lea eax, [edi+0x3c]
push eax
lea ecx, [edi+0x20]
call 0x4033c0
push eax
lea ecx, [edi+4]
call 0x4033c0
push eax
mov ecx, ebx
call 0x6aa7b0
mov ecx, ebx
call 0x408d70
mov dword ptr [{diag+100:#x}], eax
push esi
push edi
lea esi, [edi+0x40]
lea edi, [eax+0x40]
mov ecx, 12
rep movsd dword ptr es:[edi], dword ptr [esi]
pop edi
pop esi
mov eax, dword ptr [{diag+100:#x}]
mov dword ptr [eax+0x60], {p2}
mov dword ptr [eax+0x64], {p2}
{f'mov ecx, ebx; call {codebase+0x4500:#x}' if loadouts else ''}
ret
''',codebase+0x2100)
    extras={0x2100:prepare}
    patches=[]
    from extra_code import build_player_count
    extras[0x2800]=build_player_count(assemble,codebase,diag)
    patches.append((0x75019c,struct.pack('<I',0x6a9560),struct.pack('<I',codebase+0x2800)))
    if follow:
        from extra_code import build_follow
        extras[0x2500]=build_follow(assemble,codebase,diag)
        patches.append((0x750188,struct.pack('<I',0x4ac550),struct.pack('<I',codebase+0x2500)))
    if keyboard:
        from extra_code import build_keyboard
        kextras,kpatches=build_keyboard(assemble,codebase,diag,data,off)
        extras.update(kextras);patches.extend(kpatches)
    if input_probe:
        from extra_code import build_input_probe
        extras[0x3e00]=build_input_probe(assemble,codebase,diag)
        before=b'\xe8'+struct.pack('<i',0x5d1940-0x6775e3-5)
        after=b'\xe8'+struct.pack('<i',codebase+0x3e00-0x6775e3-5)
        patches.append((0x6775e3,before,after))
    if hud:
        from hud_code import build_hud
        hextras,hpatches=build_hud(assemble,codebase,diag)
        extras.update(hextras);patches.extend(hpatches)
    if loadouts:
        from loadout_code import build_loadouts
        lextras,lpatches=build_loadouts(assemble,codebase,diag,p1,p2)
        extras.update(lextras);patches.extend(lpatches)
        from death_code import build_death
        dextras,dpatches=build_death(assemble,codebase,diag)
        extras.update(dextras);patches.extend(dpatches)
        from revive_code import build_revive
        rextras,rpatches=build_revive(assemble,codebase,diag)
        extras.update(rextras);patches.extend(rpatches)
    code=bytearray(b'\xcc'*0x5000)
    code[:len(wrapper)]=wrapper;code[0x100:0x100+len(first)]=first;code[0x1100:0x1100+len(second)]=second
    occupied=[(0,len(wrapper)),(0x100,0x100+len(first)),(0x1100,0x1100+len(second))]
    for rel,blob in extras.items():
        assert rel+len(blob)<=len(code)
        assert all(rel>=end or rel+len(blob)<=start for start,end in occupied)
        code[rel:rel+len(blob)]=blob;occupied.append((rel,rel+len(blob)))
    # The code and diagnostics have separate RX / RW PE sections.
    diagnostics=bytearray(struct.pack('<I',0x504f4f43)+b'\0'*(0x2000-4))
    for rel,blob in [(0x400,b'campaigncoop.chui\0'),(0x420,b'playerui2\0')]:diagnostics[rel:rel+len(blob)]=blob
    if loadouts:
        from loadout_code import defaults
        diagnostics[0x800:0x880]=defaults()
    assert len(diagnostics)==0x2000
    sections=[(b'.coop',rv,bytes(code),0x60000020),(b'.coopdat',rv+0x5000,bytes(diagnostics),0xc0000040)]
    raw=bytearray(data);table=pe.sections[-1].get_file_offset()+40
    if table+80>pe.OPTIONAL_HEADER.SizeOfHeaders:raise ValueError('Insufficient section headers')
    for j,(name,rva,blob,flags) in enumerate(sections):
        fileoff=align(len(raw),pe.OPTIONAL_HEADER.FileAlignment)
        size=align(len(blob),pe.OPTIONAL_HEADER.FileAlignment)
        raw.extend(b'\0'*(fileoff-len(raw)));raw.extend(blob);raw.extend(b'\0'*(size-len(blob)))
        header=struct.pack('<8sIIIIIIHHI',name,len(blob),rva,size,fileoff,0,0,0,0,flags)
        raw[table+j*40:table+(j+1)*40]=header
    struct.pack_into('<H',raw,pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),len(pe.sections)+2)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),rv+0x7000)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfCode'),pe.OPTIONAL_HEADER.SizeOfCode+0x5000)
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfInitializedData'),pe.OPTIONAL_HEADER.SizeOfInitializedData+0x2000)
    struct.pack_into('<I',raw,off(ENTRY),codebase)
    for addr,before,after in patches:
        assert data[off(addr):off(addr)+len(before)]==before,hex(addr)
        assert len(before)==len(after)
        raw[off(addr):off(addr)+len(after)]=after
    struct.pack_into('<I',raw,pe.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum'),0)
    checked=pefile.PE(data=bytes(raw))
    if checked.get_dword_at_rva(ENTRY-base)!=codebase:raise ValueError('Patch verification failed')
    for addr,blob in [(codebase,wrapper),(codebase+0x100,first),(codebase+0x1100,second)]+[(codebase+r,c) for r,c in extras.items()]:
        decoded=list(md.disasm(blob,addr))
        if sum(i.size for i in decoded)!=len(blob):raise ValueError('Generated code decode failed')
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.resolve()==source.resolve():raise ValueError('Output must differ from input')
    destination.write_bytes(raw)
    manifest={'version':'0.2-experimental','input_sha256':EXPECTED,'output_sha256':hashlib.sha256(raw).hexdigest(),'p1_device':p1,'p2_device':p2,'wrapper':hex(codebase),'diagnostics':hex(diag),'first_clone_bytes':len(first),'second_clone_bytes':len(second),'status':'Built and statically checked; gameplay validation required'}
    manifest.update(version='0.3-experimental',keyboard=keyboard,follow=follow,input_probe=input_probe,hud=hud,recall_key='F6',automatic_recall=False,loadouts=loadouts,config_offset=checked.get_offset_from_rva(diag+0x800-base),config_size=128)
    destination.with_suffix('.coop.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    destination.with_suffix('.coop.asm').write_text('; P1\n'+src1+'\n; P2\n'+src2,encoding='utf-8')
    print(json.dumps(manifest,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path);ap.add_argument('--p1',type=int,default=1);ap.add_argument('--p2',type=int,default=2);ap.add_argument('--keyboard',action='store_true');ap.add_argument('--no-follow',action='store_true');ap.add_argument('--input-probe',action='store_true');ap.add_argument('--hud',action='store_true');ap.add_argument('--loadouts',action='store_true');args=ap.parse_args()
    build(args.source,args.destination,args.p1,args.p2,args.keyboard,not args.no_follow,args.input_probe,args.hud,args.loadouts)
