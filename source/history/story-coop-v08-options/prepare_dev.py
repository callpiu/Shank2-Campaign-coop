"""Compose camera/audio options without writing public outputs or game files."""
from pathlib import Path
import sys,json,hashlib,base64,shutil
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent/'story-coop-v06-camera'),str(HERE.parent/'story-coop-v07-dialogue')]
from build_camera import build as camera
from build_audio import build as audio
from native import pefile
sha=lambda b:hashlib.sha256(b).hexdigest()
DEV=HERE/'launcher';DEV.mkdir(exist_ok=True)
FINAL=HERE/'final';FINAL.mkdir(exist_ok=True)
BASE=HERE.parent/'story-coop-v05'
(DEV/'patch').mkdir(exist_ok=True)
shutil.copy2(HERE.parents[1]/'outputs/Shank2-StoryCoop-v0.5-Test/patch/manifest.json',DEV/'patch/manifest.json')
for name in ['Portraits.ps1','Launcher-Preferences.ps1','Game-Paths.ps1','catalog.json','Coop-Localization.ps1','keyboard-recipe.json','pads-recipe.json','keyboard-chs-recipe.json','pads-chs-recipe.json','ui-recipe.json','ui-chs-recipe.json','pause-en-recipe.json','pause-chs-recipe.json','equip-en-recipe.json','equip-chs-recipe.json']:
 shutil.copy2(BASE/'dev-launcher'/name,DEV/name)
reports=[]
for mode in ['keyboard','pads']:
 for lang in ['en','chs']:
  src=BASE/'final'/f'shank2-coop-v05-{mode}{"-chs" if lang=="chs" else ""}.exe'
  cam=FINAL/f'{mode}-{lang}-camera.exe';target=FINAL/f'{mode}-{lang}.exe'
  cm=camera(src,cam)
  am=audio(cam,target,'../data/movies/coop_dialogue_enhanced')
  a=src.read_bytes();b=target.read_bytes();pe=pefile.PE(data=b)
  sections={s.Name.rstrip(b'\0'):s for s in pe.sections};dat=sections[b'.camdat'].PointerToRawData
  changes=[];i=0
  while i<len(a):
   if a[i]==b[i]:i+=1;continue
   start=i
   while i<len(a) and a[i]!=b[i]:i+=1
   changes.append({'offset':start,'before':a[start:i].hex(),'after':b[start:i].hex()})
  recipe={'format':1,'input_sha256':sha(a),'output_sha256':sha(b),'source_size':len(a),'target_size':len(b),'patches':changes,'append':base64.b64encode(b[len(a):]).decode(),'camera_offset':dat+4,'audio_offset':dat+0x800+0x1c,'config_size':128,'mode':mode,'language':lang,'resource_root':am['resource_root']}
  # Configuration offset comes from the existing verified recipe, never inferred.
  base_recipe=json.loads((DEV/f'{mode}-recipe.json').read_text())
  recipe['config_offset']=base_recipe['config_offset']
  assert a[recipe['config_offset']:recipe['config_offset']+128]==b[recipe['config_offset']:recipe['config_offset']+128]
  (DEV/f'{mode}-{lang}-addon.json').write_text(json.dumps(recipe,indent=2))
  reports.append({k:v for k,v in recipe.items() if k not in ['patches','append']})
(HERE/'builds.json').write_text(json.dumps(reports,indent=2))
print('Built four input/language variants with relative audio paths; public outputs unchanged.')
