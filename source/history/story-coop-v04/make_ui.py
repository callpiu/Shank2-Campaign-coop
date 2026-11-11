from pathlib import Path
import struct,hashlib,json,sys
from chui import Reader
source=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\data-pc\ui\campaignscreen.chui')
b=source.read_bytes();r=Reader(b);assert r.u32()==2
templates=[r.node() for _ in range(r.u32())];countpos=r.pos;count=r.u32();roots=[r.node() for _ in range(count)];assert r.pos==len(b)
node=next(n for n in roots if n['name']=='playerui')
clone=bytearray(b[node['start']:node['end']])
# Name grows by one byte; the following fields are relative to the cloned node.
clone[4:13]=b'\x09playerui2'
offset=node['common']-node['start']+1
x,y=struct.unpack_from('<2f',clone,offset);struct.pack_into('<2f',clone,offset,x,y-.18)
result=bytearray(b);struct.pack_into('<I',result,countpos,count+1);result.extend(clone)
check=Reader(result);check.u32();[check.node() for _ in range(check.u32())];newroots=[check.node() for _ in range(check.u32())];assert check.pos==len(result)
assert newroots[-1]['name']=='playerui2';assert bytes(result[:countpos])==b[:countpos]
dest=Path(sys.argv[1]);dest.write_bytes(result)
print(json.dumps({'source_sha256':hashlib.sha256(b).hexdigest(),'target_sha256':hashlib.sha256(result).hexdigest(),'root_count':len(newroots),'size':len(result),'source_root_count_offset':countpos,'copied_root_range':[node['start'],node['end']]},indent=2))
