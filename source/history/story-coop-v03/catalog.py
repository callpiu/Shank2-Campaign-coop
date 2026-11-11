from pathlib import Path
import sys,json
sys.path.insert(0,r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\pydeps')
from lupa.lua51 import LuaRuntime
root=Path(r'E:\SteamLibrary\steamapps\common\Shank 2\data')
lua=LuaRuntime();lua.execute((root/'bootstrap/skins.lua').read_text());lua.execute((root/'weapondata.lua').read_text())
def hash_name(s):
 v=0
 for c in s.lower().encode('ascii'):v=(v*0x1003f+c)&0xffffffff
 return v
assert hash_name('shank')==0x9a257669
skins=[]
for _,family in lua.globals().skinsets.items():
 for _,skin in family.skins.items():skins.append({'id':skin.name,'name':skin.displayname,'family':family.name,'hash':hash_name(skin.name)})
weapons={}
for _,family in lua.globals().WeaponData.items():
 weapons[family.name]={}
 for _,slot in family.weapons.items():weapons[family.name][slot['class']]=[{'id':weapon.name,'name':weapon.displayName,'hash':hash_name(weapon.name)} for _,weapon in slot.Weapons.items()]
out={'skins':skins,'weapons':weapons};Path(__file__).with_name('catalog.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
