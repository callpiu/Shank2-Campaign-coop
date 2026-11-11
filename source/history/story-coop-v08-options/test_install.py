"""Real PS5.1 composition/ownership/option tests in isolated small fixtures."""
from pathlib import Path
import json,subprocess,shutil,hashlib,struct,os
HERE=Path(__file__).resolve().parent;DEV=HERE/'launcher';ROOT=HERE/'fixtures';ROOT.mkdir(exist_ok=True)
PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
TEST=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reports=[]
settings={'players':[{'skin':'yakuza','melee':'saw','ranged':'shotgun','consumable':'weapon_mine'},{'skin':'sunshine','melee':'scythe','ranged':'uzi','consumable':'weapon_molotov'}]}
catalog=json.loads((DEV/'catalog.json').read_text());assets=json.loads((DEV/'movie-assets.json').read_text())
def run(root,action,mode,features,fail=False):
 settings['features']=features;path=ROOT/'settings.json';path.write_text(json.dumps(settings))
 p=subprocess.run([PS,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(DEV/'Manage-Coop.ps1'),'-Action',action,'-InputMode',mode,'-GamePath',str(root),'-LoadoutPath',str(path)],capture_output=True,text=True,errors='replace')
 assert (p.returncode!=0)==fail,(p.returncode,p.stdout[-1500:],p.stderr[-1500:])
 return p
for lang in ['en','chs']:
 root=ROOT/lang
 if not root.exists():shutil.copytree(HERE.parent/'story-coop-v05/installer-tests'/lang,root)
 original={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name in ['shank2.exe','graphics.ini']}
 # Obsolete false settings must never bypass the now-required enhancement.
 for row in assets:
  for sub in ['','coop_dialogue_enhanced/']:
   dst=root/'data/movies'/sub/row['file'];dst.parent.mkdir(parents=True,exist_ok=True)
   if not dst.exists():os.link(TEST/'data/movies'/sub/row['file'],dst)
 for mode in ['Keyboard','Pads']:
  meta=json.loads((DEV/f'{mode.lower()}-{lang}-addon.json').read_text());target=root/'bin'/f'shank2-coop-v08-{mode.lower()}.exe'
  for camera,audio in [(False,False),(True,False),(False,True),(True,True)]:
   run(root,'Install',mode,{'sharedCamera':camera,'dialogueMix':audio})
   actual=target.read_bytes();expected=bytearray((HERE/'final'/f'{mode.lower()}-{lang}.exe').read_bytes())
   struct.pack_into('<I',expected,meta['camera_offset'],1);struct.pack_into('<I',expected,meta['audio_offset'],1)
   for i,entry in enumerate(settings['players']):
    skin=next(s for s in catalog['skins'] if s['id']==entry['skin']);o=meta['config_offset']+i*64
    struct.pack_into('<I',expected,o,1);expected[o+4:o+20]=skin['family'].encode().ljust(16,b'\0')
    ids=[skin['hash']]+[next(w['hash'] for w in catalog['weapons'][skin['family']][slot] if w['id']==entry[slot]) for slot in ['melee','ranged','consumable']]+[3]
    struct.pack_into('<5I',expected,o+20,*ids)
   assert actual==expected,(lang,mode,camera,audio)
   receipt=json.loads(target.with_suffix('.exe.coop-install.json').read_text(encoding='utf-8-sig'))
   assert receipt['features']=={'sharedCamera':True,'dialogueMix':True}
   reports.append({'language':lang,'mode':mode,'obsolete_camera_setting':camera,'obsolete_audio_setting':audio,'both_always_enabled':True,'exact_output_and_receipt':True})
  saved=target.read_bytes();target.write_bytes(b'FOREIGN FILE')
  before={str(p):sha(p) for p in (root/'data-pc/ui').glob('*coopv05.chui')}
  run(root,'Install',mode,{'sharedCamera':True,'dialogueMix':False},fail=True)
  assert target.read_bytes()==b'FOREIGN FILE' and before=={p:sha(Path(p)) for p in before}
  target.write_bytes(saved);reports.append({'language':lang,'mode':mode,'foreign_target_preserved':True})
 # Corrupt asset must be refused before any executable/UI writes. Rename hardlink,
 # never mutate linked media; restore the original directory entry afterwards.
 missing=root/'data/movies/coop_dialogue_enhanced'/assets[0]['file'];hold=missing.with_suffix('.held')
 missing.rename(hold)
 try:
  before={str(p):sha(p) for p in (root/'bin').glob('shank2-coop-v08*')}
  run(root,'Install','Keyboard',{'sharedCamera':True,'dialogueMix':True},fail=True)
  run(root,'Install','Keyboard',{'sharedCamera':False,'dialogueMix':False},fail=True)
  assert before=={p:sha(Path(p)) for p in before}
 finally:hold.rename(missing)
 reports.append({'language':lang,'missing_audio_resource_refused_before_commit':True})
 for rel,digest in original.items():assert sha(root/rel)==digest,rel
 # Shared v0.5 owner sentinel protects shared UI during v0.8 removal.
 sentinel=root/'bin/shank2-coop-v05-keyboard.exe';sentinel.write_bytes(b'PREVIOUS VERSION SENTINEL')
 ui={str(p):sha(p) for p in (root/'data-pc/ui').glob('*coopv05.chui')}
 for mode in ['Keyboard','Pads']:run(root,'Remove',mode,{'sharedCamera':False,'dialogueMix':False})
 assert sentinel.read_bytes()==b'PREVIOUS VERSION SENTINEL' and ui=={p:sha(Path(p)) for p in ui}
 sentinel.unlink()
 reports.append({'language':lang,'original_display_settings_and_previous_version_preserved':True})
(HERE/'installer-tests.json').write_text(json.dumps(reports,indent=2))
print('Passed',len(reports),'installer/configuration/resource/ownership cases.')
