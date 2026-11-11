from pathlib import Path
import sys,struct,json
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import pefile
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
b=(HERE/'shank2-coop-v06-camera-test.exe').read_bytes();pe=pefile.PE(data=b)
sections={s.Name.rstrip(b'\0'):s for s in pe.sections};cs=sections[b'.camx'];ds=sections[b'.camdat']
olddata=0x400000+ds.VirtualAddress;v=0x20000000
buf=bytearray(12288);buf[:4096]=b[cs.PointerToRawData:cs.PointerToRawData+4096];buf[4096:8192]=b[ds.PointerToRawData:ds.PointerToRawData+4096]
for pos in range(4093):
 value=struct.unpack_from('<I',buf,pos)[0]
 if olddata<=value<olddata+4096:struct.pack_into('<I',buf,pos,v+4096+value-olddata)
blob=bytes(Ks(KS_ARCH_X86,KS_MODE_32).asm(f'mov ecx,dword ptr [esp+4];call {v+0x900};ret',v+0x2000)[0])
buf[0x2000:0x2000+len(blob)]=blob;(HERE/'camera-test.bin').write_bytes(buf)
