import re
import struct
from inspect_native import b,pe,off,dis
for match in re.finditer(rb'\.\?A[UV][ -~]{3,130}?\x00',b):
    name=match[0][:-1].decode()
    if 'Grappl' in name or 'Viz' in name and 'Ext' in name:
        type_address=0x400000+pe.get_rva_from_offset(match.start())-8
        refs=[]
        for pos in range(b.find(struct.pack('<I',type_address)),len(b)):
            break
        needle=struct.pack('<I',type_address);pos=b.find(needle)
        while pos>=0:
            refs.append(hex(0x400000+pe.get_rva_from_offset(pos)));pos=b.find(needle,pos+1)
        print(hex(type_address),name,refs[:12])
