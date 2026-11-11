from pathlib import Path
import subprocess,json,hashlib,shutil,struct
root=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common')
here=Path(__file__).resolve().parent;package=root/'outputs/Shank2-StoryCoop-v0.3';fixture=here/'install-tests'
(fixture/'bin').mkdir(parents=True,exist_ok=True);(fixture/'data-pc/ui').mkdir(parents=True,exist_ok=True)
game=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
for rel in ['bin/shank2.exe','data-pc/ui/campaignscreen.chui']:shutil.copy2(game/rel,fixture/rel)
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
originals={rel:hashfile(fixture/rel) for rel in ['bin/shank2.exe','data-pc/ui/campaignscreen.chui']}
report=[]
def run(action,mode='Keyboard',settings=None,fail=False):
 args=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(package/'Manage-Coop.ps1'),'-Action',action,'-InputMode',mode,'-GamePath',str(fixture)]
 if settings:args+=['-LoadoutPath',str(settings)]
 p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
 if (p.returncode!=0)!=fail:raise AssertionError((args,p.returncode,p.stdout,p.stderr))
 report.append({'action':action,'mode':mode,'expected_failure':fail,'exit_code':p.returncode,'result':(p.stdout+p.stderr).strip()[:500]})
for mode in ['Keyboard','Pads']:run('Verify',mode);run('Install',mode);run('Install',mode)
custom={'players':[{'skin':'yakuza','melee':'saw','ranged':'shotgun','consumable':'weapon_mine'},{'skin':'sunshine','melee':'scythe','ranged':'uzi','consumable':'weapon_molotov'}]}
settings=here/'test-loadouts.json';settings.write_text(json.dumps(custom))
run('Install',settings=settings)
exe=fixture/'bin/shank2-coop-v03-keyboard.exe';b=exe.read_bytes();recipe=json.loads((package/'keyboard-recipe.json').read_text());o=recipe['config_offset']
catalog=json.loads((package/'catalog.json').read_text())
for i,entry in enumerate(custom['players']):
 skin=next(x for x in catalog['skins'] if x['id']==entry['skin']);at=o+i*64
 assert b[at+4:at+20].split(b'\0')[0].decode()==skin['family']
 expected=[skin['hash']]+[next(x['hash'] for x in catalog['weapons'][skin['family']][s] if x['id']==entry[s]) for s in ['melee','ranged','consumable']]+[3]
 assert list(struct.unpack_from('<5I',b,at+20))==expected
receipt=json.loads(Path(str(exe)+'.coop-install.json').read_text(encoding='utf-8-sig'));assert hashfile(exe)==receipt['installed_sha256']
report.append({'configured_bytes_match_catalog':True,'configured_sha256':hashfile(exe)})
custom['players'][0]['melee']='sword';settings.write_text(json.dumps(custom));before=hashfile(exe)
run('Install',settings=settings,fail=True);assert hashfile(exe)==before
exe.write_bytes(b'UNRELATED FILE');run('Install',fail=True);run('Remove',fail=True);assert exe.read_bytes()==b'UNRELATED FILE';exe.write_bytes(b)
ui=fixture/'data-pc/ui/campaigncoop.chui';uib=ui.read_bytes();ui.write_bytes(b'UNRELATED UI');run('Install',fail=True);run('Remove',fail=True);assert ui.read_bytes()==b'UNRELATED UI';ui.write_bytes(uib)
run('Remove');assert not exe.exists() and ui.exists();run('Remove','Pads');assert not ui.exists()
for rel,h in originals.items():assert hashfile(fixture/rel)==h
report.append({'original_files_unchanged':True,'shared_ui_retained_until_last_mode_removed':True})
dest=package/'validation/installer-tests.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(report),'report':str(dest)},ensure_ascii=False))
