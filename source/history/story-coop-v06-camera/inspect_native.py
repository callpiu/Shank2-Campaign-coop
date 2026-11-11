"""Read-only RTTI/vtable and string-reference inventory of Steam camera code."""
from pathlib import Path
import sys,struct,json
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import b,pe,off,dis
def references(value):
    start=0;needle=struct.pack('<I',value);out=[]
    while True:
        at=b.find(needle,start)
        if at<0:return out
        out.append(pe.get_rva_from_offset(at)+0x400000);start=at+1
types={name:va for name,va in [('Focus',0x7cc7f0),('CameraView',0x7cca18),('Rail',0x7d0494),('Follow',0x7d04d4),('Positional',0x7d0518),('Survival',0x7ce6e8),('Boss',0x7d0478)]}
result={}
for name,string in types.items():
    cols=[]
    for ref in references(string-8):
        col=ref-12
        fields=struct.unpack_from('<5I',b,off(col))
        if fields[0]==0 and fields[1]<0x10000 and 0x700000<fields[4]<0x7fa000:
            for vptr in references(col):
                vtable=vptr+4
                values=struct.unpack_from('<12I',b,off(vtable))
                if 0x400000<=values[0]<0x700000:cols.append({'col':hex(col),'offset':fields[1],'vtable':hex(vtable),'functions':[hex(v) for v in values]})
    result[name]=cols
result['manager_string_refs']={hex(va):[hex(x) for x in references(va)] for va in [0x759d78,0x759ec0,0x759ee8,0x75a024]}
(HERE/'native-inventory.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
