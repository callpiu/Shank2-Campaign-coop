from pathlib import Path
import sys,json,hashlib,subprocess,zipfile,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS';ARCHIVE=OUT.parent/(OUT.name+'.zip');AUDIT=HERE/'release-analysis'
SKILL=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts')
for script,args in [('verify_release_archive.py',['--directory',str(OUT),'--archive',str(ARCHIVE),'--json',str(AUDIT/'archive-equality.json')]),('audit_release_size.py',['--archive',str(ARCHIVE),'--reference',str(ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS.zip'),'--json',str(AUDIT/'size-audit.json')])]:
 p=subprocess.run([sys.executable,str(SKILL/script),*args],capture_output=True,text=True,encoding='utf-8',errors='replace')
 assert p.returncode==0,(script,p.stdout[-1200:],p.stderr[-1200:])
extract=HERE/'archive-smoke'/'\u5206\u4eab\u5305 \u4e2d\u6587 \u7a7a\u683c';extract.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(ARCHIVE) as z:
 assert z.testzip() is None
 assert sum(n.endswith('.bik') for n in z.namelist())==27
 assert not any(n.endswith(('.exe','.dll')) for n in z.namelist())
 z.extractall(extract)
PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe';fixture=HERE/'archive-fixture'
if not fixture.exists():shutil.copytree(HERE/'release-fixture',fixture)
manifest=json.loads((extract/'patch/manifest.json').read_text())
def call(script,*args):
 p=subprocess.run([PS,'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(extract/'patch'/script),'-GamePath',str(fixture),*args],capture_output=True,text=True,errors='replace')
 assert p.returncode==0,(script,p.stdout[-1500:],p.stderr[-1500:])
call('Coop-Localization.ps1','-Action','Install','-NoUI')
for mode in ['Keyboard','Pads']:
 call('Manage-Coop.ps1','-Action','Install','-InputMode',mode)
 actual=(fixture/'bin'/f'shank2-coop-v08-{mode.lower()}.exe').read_bytes()
 assert actual==(HERE/'final-release'/f'{mode.lower()}-chs.exe').read_bytes()
call('Coop-Localization.ps1','-Action','Verify','-NoUI')
for row in manifest['files']:assert hashlib.sha256((fixture/row['path']).read_bytes()).hexdigest()==row['sha256']
for mode in ['Keyboard','Pads']:call('Manage-Coop.ps1','-Action','Remove','-InputMode',mode)
call('Coop-Localization.ps1','-Action','Remove','-NoUI')
for row in manifest['files']:assert hashlib.sha256((fixture/row['path']).read_bytes()).hexdigest()==row['original_sha256']
report={'archive_bytes_equal_release':True,'flat_root':True,'movies_exactly_27':True,'chinese_space_extraction_install_verify_remove':True,'both_modes_exact_binary':True,'all_96_originals_restored':True,'personal_files_absent':True}
(AUDIT/'zip-smoke.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
