"""Create a small reconstruction recipe using the user's original CHUI."""
from pathlib import Path
import argparse,base64,difflib,hashlib,json,struct
from chui import Reader
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('target',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
source=a.source.read_bytes();target=a.target.read_bytes()
r=Reader(source);assert r.u32()==2
[r.node() for _ in range(r.u32())];countpos=r.pos
roots=[r.node() for _ in range(r.u32())];assert r.pos==len(source)
root=next(n for n in roots if n['name']=='playerui');native=source[root['start']:root['end']]
patches=[{'offset':countpos,'before':source[countpos:countpos+4].hex(),'after':target[countpos:countpos+4].hex()}]
assert source[:countpos]==target[:countpos] and source[countpos+4:]==target[countpos+4:len(source)]
chunks=[]
for tag,x,y,u,v in difflib.SequenceMatcher(None,native,target[len(source):],autojunk=False).get_opcodes():
 if tag=='equal':chunks.append({'copy':root['start']+x,'length':y-x})
 elif tag!='delete':chunks.append({'literal':base64.b64encode(target[len(source)+u:len(source)+v]).decode()})
out=bytearray(source);out[countpos:countpos+4]=bytes.fromhex(patches[0]['after'])
for c in chunks:out.extend(source[c['copy']:c['copy']+c['length']] if 'copy'in c else base64.b64decode(c['literal']))
assert out==target
recipe={'format':1,'input_sha256':hashlib.sha256(source).hexdigest(),'output_sha256':hashlib.sha256(target).hexdigest(),'source_size':len(source),'target_size':len(target),'patches':patches,'append':chunks}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(recipe,indent=2),encoding='utf-8')
print(json.dumps({'verified':str(a.output),'size':a.output.stat().st_size,'target_sha256':recipe['output_sha256']}))
