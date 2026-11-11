from pathlib import Path
import re
root=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
for name in ['campaignscreen','survivalscreen','singleplayerloadoutscreen','multiplayerlobbyscreen','costumeselectscreen']:
 p=root/'data-pc/ui'/f'{name}.chui';b=p.read_bytes()
 strings=[m.group().decode() for m in re.finditer(rb'[ -~]{4,}',b)]
 print(name,len(b),'\n'+'\n'.join(x for x in strings if re.search(r'player|health|weapon|hud|portrait|skin|loadout|character|ammo|grenade',x,re.I)))
exe=(root/'bin/shank2.exe').read_bytes()
print('NATIVE TYPES')
for m in re.finditer(rb'\.\?A[UV][ -~]{4,}',exe):
 s=m.group().decode()
 if re.search(r'health|hud|status|loadout|costume|survival|campaign',s,re.I):print(s)
print('DATA TABLES')
for p in (root/'data').glob('*.lua'):
 if re.search(r'char|skin|loadout|costume|weapon',p.name,re.I):print(p)
