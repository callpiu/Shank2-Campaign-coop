"""Verify configured previous test EXEs upgrade through their exact receipts."""
from pathlib import Path
import subprocess,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
old=HERE/'archive-smoke/中文 空格目录/Shank2-StoryCoop-v0.5-Test'
new=ROOT/'outputs/Shank2-StoryCoop-v0.5-Test'
ps=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
# verify_archive.py can refresh the smoke extraction with a newer ZIP. Never
# silently count reinstalling the current build as an old-build upgrade test.
assert json.loads((old/'keyboard-recipe.json').read_text())['output_sha256']=='f718f5e24a5457bda031ffaf4dcb10ce54efd8c8de21c72adb0e38f7fb9fcff4', 'Provide the original v0.5 test package to rerun old-build upgrade cases.'
cases=[]
for lang in ['en','chs']:
    fixture=HERE/'installer-tests-enterfix'/lang
    settings=fixture.parent/f'{lang}-loadouts.json'
    for mode in ['Keyboard','Pads']:
        for package,action in [(old,'Install'),(new,'Install'),(new,'Remove')]:
            cmd=[ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(package/'Manage-Coop.ps1'),'-Action',action,'-InputMode',mode,'-GamePath',str(fixture),'-LoadoutPath',str(settings)]
            p=subprocess.run(cmd,capture_output=True,text=True,errors='replace')
            assert p.returncode==0,(lang,mode,action,p.stdout,p.stderr)
            if package==new and action=='Install':
                path=fixture/'bin'/f'shank2-coop-v05-{mode.lower()}.exe'
                receipt=json.loads(Path(str(path)+'.coop-install.json').read_text(encoding='utf-8-sig'))
                assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['installed_sha256']
                assert receipt['players']==json.loads(settings.read_text())['players']
        cases.append({'language':lang,'input':mode,'configured_old_test_upgrade':True})
(HERE/'upgrade-tests.json').write_text(json.dumps(cases,indent=2))
print(json.dumps({'upgrade_cases_passed':len(cases)}))
