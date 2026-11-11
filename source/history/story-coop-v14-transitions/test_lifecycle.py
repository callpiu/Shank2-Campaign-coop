"""Run the released resource hooks on x86 with bounded native-call fixtures."""
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v12-live-character'))
from build import machine_code, Ks, KS_ARCH_X86, KS_MODE_32, CODE, DATA, DIAG, CONFIG, MENU
from selector import constants, CATALOG, FAMILY_HASHES

BASE=0x20000000
KS=Ks(KS_ARCH_X86,KS_MODE_32)
NATIVE={0x411080:BASE+0x1000,0x69a820:BASE+0x1100,0x410920:BASE+0x1200}
def relocate(value):
    if CODE<=value<CODE+0x900:return BASE+value-CODE
    for origin,target,size in ((DATA,BASE+0x4000,0xd00),(CONFIG,BASE+0x3800,128),(DIAG,BASE+0x3000,0x100),(MENU,BASE+0x6000,0x200)):
        if origin<=value<origin+size:return target+value-origin
    return NATIVE.get(value,value)
def asm(text,addr):
    text=re.sub(r'(?<![A-Za-z_])(?:0x[0-9a-fA-F]+|\d+)',lambda m:str(relocate(int(m[0],0) if m[0].startswith('0x') else int(m[0]))),text)
    return bytes(KS.asm(text,relocate(addr))[0])

buf=bytearray(0x10000)
def put(offset,value):
    assert buf[offset:offset+len(value)]==bytes(len(value))
    buf[offset:offset+len(value)]=value
for addr,value in machine_code(asm).items():put(relocate(addr)-BASE,value)
put(0x4000,constants(BASE+0x4000)+bytes(16)+b'shank\0\0\0corina\0\0')
for kind,(native,argc) in enumerate(((0x411080,3),(0x69a820,3),(0x410920,1)),1):
    code=f'''mov edx,[{BASE+0x8000}]
        imul edx,edx,20
        add edx,{BASE+0x8100}
        mov dword ptr [edx],{kind}
        mov [edx+4],ecx
        mov eax,[esp+4]
        mov [edx+8],eax'''
    for index in range(1,argc):code+=f'\nmov eax,[esp+{4+index*4}]; mov [edx+{8+index*4}],eax'
    cleanup=0 if native==0x69a820 else argc*4
    code+=f'\ninc dword ptr [{BASE+0x8000}]; mov eax,1; ret {cleanup}'
    put(NATIVE[native]-BASE,asm(code,NATIVE[native]))
entries=[]
for i,offset in enumerate((0x5c0,0x620,0x660,0x6a0,0x6e0,0x710,0x7a0,0x800)):
    addr=BASE+0x2000+i*0x80
    argc=1 if offset>=0x7a0 else 3
    code=f'''push ebp;mov ebp,esp; sub esp,0x40
        push ebx;push esi;push edi
        mov eax,{BASE+0x7000};mov [ebp-0x34],eax;mov [ebp-0x20],eax
        mov edx,[ebp+8];mov [eax+0x1e4],edx
        mov ecx,{BASE+0x7300}'''
    if argc==3:code+='\npush 0x33;push 0x22'
    code+=f'\npush {BASE+0x7400};call {BASE+offset}'
    if offset in (0x660,0x6a0,0x6e0,0x710):code+='\nadd esp,12'
    code+='\npop edi;pop esi;pop ebx;mov esp,ebp;pop ebp;ret 4'
    put(addr-BASE,asm(code,addr));entries.append(dict(offset=offset,entry=addr))

with tempfile.TemporaryDirectory(prefix='lifecycle-',dir=HERE) as temp:
    path=Path(temp)
    (path/'fixture.bin').write_bytes(buf)
    (path/'metadata.json').write_text(json.dumps(dict(entries=entries,families=FAMILY_HASHES,skins=[x['hash'] for x in CATALOG],skin_families=[x['family']=='corina' for x in CATALOG])),encoding='utf-8')
    ps=Path(os.environ['WINDIR'])/'SysWOW64/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_lifecycle.ps1'),
        str(path/'fixture.bin'),str(path/'metadata.json'),str(HERE/'lifecycle-validation.json')],check=True)
