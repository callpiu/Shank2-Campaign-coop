from pathlib import Path
import sys,json,subprocess,zipfile,shutil,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];SKILL=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts');AUDIT=HERE/'package-analysis';AUDIT.mkdir(exist_ok=True)
reports=json.loads((HERE/'packages.json').read_text())
for index,row in enumerate(reports):
 archive=Path(row['zip']);folder=archive.parent/archive.stem
 p=subprocess.run([sys.executable,str(SKILL/'verify_release_archive.py'),'--directory',str(folder),'--archive',str(archive),'--json',str(AUDIT/f'equality-{index}.json')],capture_output=True,text=True,encoding='utf-8',errors='replace');assert p.returncode==0,p.stderr
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==row['sha256']
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  assert not any(Path(x).name in ['loadouts.json','features.json','launcher-settings.json'] or x.endswith(('.exe','.dll')) for x in z.namelist())
  if index==0:assert sum(x.endswith('.bik') for x in z.namelist())==27
full=ROOT/'outputs/Shank2-StoryCoop-v0.8.1-CHS-Test'
p=subprocess.run([sys.executable,str(SKILL/'audit_release_size.py'),'--archive',reports[0]['zip'],'--reference',str(ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS.zip'),'--json',str(AUDIT/'size.json')],capture_output=True,text=True,encoding='utf-8',errors='replace');assert p.returncode==0,p.stderr
merged=HERE/'overlay-smoke'/'\u5347\u7ea7 \u4e2d\u6587 \u7a7a\u683c'
if not merged.exists():shutil.copytree(ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS',merged)
with zipfile.ZipFile(reports[1]['zip']) as z:z.extractall(merged)
for relative in json.loads((HERE/'changed-files.json').read_text()):assert (merged/relative).read_bytes()==(full/relative).read_bytes()
PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe';fixture=HERE/'upgrade-fixture'
def call(script,action,mode=None):
 args=[PS,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(merged/'patch'/script),'-Action',action,'-GamePath',str(fixture)]
 args+=['-InputMode',mode] if mode else ['-NoUI']
 p=subprocess.run(args,capture_output=True,text=True,errors='replace');assert p.returncode==0,(p.stdout[-1000:],p.stderr[-1000:])
call('Coop-Localization.ps1','Install')
for mode in ['Keyboard','Pads']:
 call('Manage-Coop.ps1','Install',mode)
 assert (fixture/'bin'/f'shank2-coop-v08-{mode.lower()}.exe').read_bytes()==(HERE/'final'/f'{mode.lower()}-chs.exe').read_bytes()
for mode in ['Keyboard','Pads']:call('Manage-Coop.ps1','Remove',mode)
call('Coop-Localization.ps1','Remove')
manifest=json.loads((full/'patch/manifest.json').read_text())
assert all(hashlib.sha256((fixture/r['path']).read_bytes()).hexdigest()==r['original_sha256'] for r in manifest['files'])
assert hashlib.sha256((ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS.zip').read_bytes()).hexdigest()=='d73e65b33fd686cf4c5696616d973c00603c71840b7662676cbc64fb45ea8c27'
result={'both_archives_equal_folders':True,'overlay_actual_chinese_space_path_install_both_modes':True,'all_96_originals_restored':True,'old_v08_zip_unchanged':True,'remote_blur_gameplay':None}
(AUDIT/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
