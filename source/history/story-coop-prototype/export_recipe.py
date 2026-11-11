"""Export a small reconstruction recipe without shipping the game EXE."""
from pathlib import Path
import base64,difflib,json,sys
sys.path.insert(0,str(Path('work/pydeps').resolve()))
import pefile
source=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin\shank2.exe').read_bytes()
target=Path('work/shank2-test/bin/shank2-coop.exe').read_bytes()
manifest=json.loads(Path('work/shank2-test/bin/shank2-coop.coop.json').read_text())
pe=pefile.PE(data=source);off=pe.get_offset_from_rva(0x6a9290-0x400000)
native=source[off:off+0x2cb]
patches=[];a=0
while a<len(source):
    if source[a]==target[a]:a+=1;continue
    start=a
    while a<len(source) and source[a]!=target[a]:a+=1
    patches.append({'offset':start,'before':source[start:a].hex(),'after':target[start:a].hex()})
outpe=pefile.PE(data=target);code=outpe.sections[-2];raw=code.PointerToRawData
chunks=[]
def literal(data):
    if data:chunks.append({'literal':base64.b64encode(data).decode()})
def fill(byte,n):
    if n:chunks.append({'fill':byte,'length':n})
def relocated(blob):
    for tag,a,b,c,d in difflib.SequenceMatcher(None,native,blob,autojunk=False).get_opcodes():
        if tag=='equal':chunks.append({'copy':off+a,'length':b-a})
        elif tag in ('insert','replace'):literal(blob[c:d])
fill(0,raw-len(source))
# Boundary before the first cloned function: wrapper ends with ret, padding is cc.
prefix=target[raw:raw+0x100];end=len(prefix.rstrip(b'\xcc'))
literal(prefix[:end]);fill(0xcc,0x100-end)
for rel,size,nextrel in [(0x100,manifest['first_clone_bytes'],0x1100),(0x1100,manifest['second_clone_bytes'],0x3000)]:
    relocated(target[raw+rel:raw+rel+size]);fill(0xcc,nextrel-rel-size)
literal(target[raw+0x3000:raw+0x3004]);fill(0,len(target)-(raw+0x3004))
reconstructed=bytearray(source)
for p in patches:reconstructed[p['offset']:p['offset']+len(bytes.fromhex(p['after']))]=bytes.fromhex(p['after'])
for c in chunks:
    if 'copy'in c:reconstructed.extend(source[c['copy']:c['copy']+c['length']])
    elif 'fill'in c:reconstructed.extend(bytes([c['fill']])*c['length'])
    else:reconstructed.extend(base64.b64decode(c['literal']))
assert bytes(reconstructed)==target
output=Path('outputs/Shank2-StoryCoop-Prototype');output.mkdir(parents=True,exist_ok=True)
recipe={'format':1,**manifest,'source_size':len(source),'target_size':len(target),'patches':patches,'append':chunks}
(output/'patch-recipe.json').write_text(json.dumps(recipe,indent=2),encoding='utf-8')
print('Verified recipe reconstruction:',len(chunks),'append chunks,',len(patches),'fixed patches,',(output/'patch-recipe.json').stat().st_size,'bytes')
