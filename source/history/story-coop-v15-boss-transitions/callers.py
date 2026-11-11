import struct
from rtti import b,pe
targets=(0x58e380,0x58e6e0,0x58e800,0x504920,0x4d9500,0x58e020)
for target in targets:
    found=[]
    for section in pe.sections:
        if not section.Characteristics&0x20000000:continue
        raw=section.get_data();pos=raw.find(b'\xe8')
        while pos>=0:
            if pos+5<=len(raw):
                site=0x400000+section.VirtualAddress+pos
                if site+5+struct.unpack_from('<i',raw,pos+1)[0]==target:found.append(hex(site))
            pos=raw.find(b'\xe8',pos+1)
    print(hex(target),found)
