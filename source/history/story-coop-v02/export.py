from pathlib import Path
import base64,difflib,json,sys,struct,re,hashlib
sys.path.insert(0,r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps')
import pefile
source=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\bin\shank2.exe').read_bytes()
target_path=Path(sys.argv[1]);target=target_path.read_bytes();manifest=json.loads(target_path.with_suffix('.coop.json').read_text())
assert hashlib.sha256(source).hexdigest()==manifest['input_sha256']
pe=pefile.PE(data=source);function_offset=pe.get_offset_from_rva(0x6a9290-0x400000)
native=source[function_offset:function_offset+0x2cb]
patches=[];a=0
while a<len(source):
    if source[a]==target[a]:a+=1;continue
    start=a
    while a<len(source) and source[a]!=target[a]:a+=1
    patches.append({'offset':start,'before':source[start:a].hex(),'after':target[start:a].hex()})
chunks=[]
def emit_blob(blob):
    for tag,a,b,c,d in difflib.SequenceMatcher(None,native,blob,autojunk=False).get_opcodes():
        if tag=='equal' and b-a>=12:chunks.append({'copy':function_offset+a,'length':b-a})
        elif tag!='delete':
            if d>c:chunks.append({'literal':base64.b64encode(blob[c:d]).decode()})
append=target[len(source):];previous=0
for match in re.finditer(b'\x00{32,}|\xcc{32,}',append):
    emit_blob(append[previous:match.start()]);chunks.append({'fill':append[match.start()],'length':match.end()-match.start()});previous=match.end()
emit_blob(append[previous:])
rebuilt=bytearray(source)
for p in patches:rebuilt[p['offset']:p['offset']+len(bytes.fromhex(p['after']))]=bytes.fromhex(p['after'])
for c in chunks:
    if 'copy'in c:rebuilt.extend(source[c['copy']:c['copy']+c['length']])
    elif 'fill'in c:rebuilt.extend(bytes([c['fill']])*c['length'])
    else:rebuilt.extend(base64.b64decode(c['literal']))
assert rebuilt==target
recipe={'format':1,**manifest,'source_size':len(source),'target_size':len(target),'patches':patches,'append':chunks}
output=Path(sys.argv[2]);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(recipe,indent=2),encoding='utf-8')
print('Verified reconstruction',output,len(chunks),'append chunks',len(patches),'fixed patches',output.stat().st_size,'bytes')
