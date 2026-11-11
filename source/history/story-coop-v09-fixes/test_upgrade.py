from pathlib import Path
import sys,json,subprocess,shutil,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS/patch';NEW=ROOT/'outputs/Shank2-StoryCoop-v0.8.1-CHS-Test/patch'
FIX=HERE/'upgrade-fixture';PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe';results=[]
if not FIX.exists():shutil.copytree(HERE.parent/'story-coop-v08-options/release-fixture',FIX)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((NEW/'manifest.json').read_text())
def call(folder,script,action,mode=None,settings=None,fail=False):
 args=[PS,'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(folder/script),'-Action',action,'-GamePath',str(FIX)]
 if mode:args+=['-InputMode',mode]
 else:args+=['-NoUI']
 if settings:args+=['-LoadoutPath',str(settings)]
 p=subprocess.run(args,capture_output=True,text=True,errors='replace')
 assert (p.returncode!=0)==fail,(p.stdout[-1200:],p.stderr[-1200:])
 results.append({'action':action,'mode':mode,'expected_failure':fail,'passed':True})
assert all(sha(FIX/r['path'])==r['original_sha256'] for r in manifest['files'])
call(OLD,'Coop-Localization.ps1','Install')
receipt=sha(FIX/'.storycoop-chs/state.json')
settings=HERE.parent/'story-coop-v08-options/fixtures/settings.json'
for mode in ['Keyboard','Pads']:
 call(OLD,'Manage-Coop.ps1','Install',mode,settings)
 target=FIX/'bin'/f'shank2-coop-v08-{mode.lower()}.exe'
 before=target.read_bytes();recipe=json.loads((NEW/f'{mode.lower()}-recipe.json').read_text());o=recipe['config_offset']
 call(NEW,'Manage-Coop.ps1','Install',mode,settings)
 expected=bytearray((HERE/'final'/f'{mode.lower()}-chs.exe').read_bytes());expected[o:o+128]=before[o:o+128]
 assert target.read_bytes()==expected
 call(NEW,'Manage-Coop.ps1','Install',mode,settings)
 assert target.read_bytes()==expected
 saved=target.read_bytes();target.write_bytes(b'FOREIGN FILE')
 call(NEW,'Manage-Coop.ps1','Install',mode,settings,fail=True)
 assert target.read_bytes()==b'FOREIGN FILE';target.write_bytes(saved)
assert sha(FIX/'.storycoop-chs/state.json')==receipt
call(NEW,'Coop-Localization.ps1','Verify')
for mode in ['Keyboard','Pads']:call(NEW,'Manage-Coop.ps1','Remove',mode)
call(NEW,'Coop-Localization.ps1','Remove')
assert all(sha(FIX/r['path'])==r['original_sha256'] for r in manifest['files'])
assert all(sha(NEW/'payload'/r['path'])==r['sha256'] and sha(OLD/'payload'/r['path'])==r['sha256'] for r in manifest['files'])
fulltest=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')
p=subprocess.run([PS,'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(NEW/'Coop-Launcher.ps1'),'-SmokeTest','-GamePath',str(fulltest)],capture_output=True,text=True,errors='replace');assert p.returncode==0,(p.stdout,p.stderr)
report={'cases':len(results),'configured_v08_upgrade_both_modes':True,'repeat_install':True,'unknown_target_refused':True,'localization_receipt_and_96_payloads_unchanged':True,'all_96_originals_restored':True,'bilingual_launcher_and_portraits':True,'results':results}
(HERE/'upgrade-tests.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='results'}))
