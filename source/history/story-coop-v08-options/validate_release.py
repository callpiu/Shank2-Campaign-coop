"""Exercise actual complete release: install, native reconstruction, rollback, restore."""
from pathlib import Path
import json,hashlib,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS';PKG=OUT/'patch'
AUDIT=HERE/'release-analysis';AUDIT.mkdir(exist_ok=True)
source=(HERE.parent/'chs-compat/validate_compat.py').read_text()
source=source.replace('from build_compat import HERE,OUT,GAME',f"HERE=Path({str(HERE)!r});OUT=Path({str(PKG)!r});GAME=Path({str(HERE.parent/'story-coop-v05/bundle-fixture')!r})")
source=source.replace("HERE/'fixture'","HERE/'release-fixture'").replace("OUT/'patch/manifest.json'","OUT/'manifest.json'").replace("OUT/'patch/payload'","OUT/'payload'")
source=source.replace("['powershell.exe',", "[r'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',")
source=source.replace("run(manage,'Install');run(manage,'Install','-InputMode','Pads')\n",'')
start=source.index("run(manage,'Verify');");end=source.index("run(local,'Install','-Group','Movies'",start)
source=source[:start]+source[end:]
source=source.replace("run(manage,'Remove');run(manage,'Remove','-InputMode','Pads');all_original()", "run(manage,'Remove');run(manage,'Remove','-InputMode','Pads');all_original()")
anchor="for rel,h in manifest['guards'].items():assert hashfile(fixture/rel)==h"
source=source.replace(anchor,anchor+"""
for mode in ['keyboard','pads']:
    run(manage,'Install','-InputMode',mode)
    installed=(fixture/f'bin/shank2-coop-v08-{mode}.exe').read_bytes()
    expected=(HERE/'final-release'/f'{mode}-chs.exe').read_bytes()
    assert installed==expected
    run(manage,'Verify','-InputMode',mode)
""")
source=source.replace("(HERE/'analysis/installer-validation.json')","(HERE/'release-analysis/installer-validation.json')")
generated=AUDIT/'transaction-tests.py';generated.write_text(source)
subprocess.run([sys.executable,str(generated)],check=True)
PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
subprocess.run([PS,'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(HERE.parent/'story-coop-v05/test_bundle_manager.ps1'),'-Runtime',str(PKG),'-Fixture',str(HERE/'release-fixture'),'-Report',str(AUDIT/'gui.json')],check=True)
# Old v0.5 receipt must be rejected without changing any registered resource.
old=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS/patch/Coop-Localization.ps1'
fixture=HERE/'release-fixture'
def command(script,action,fail=False):
 r=subprocess.run([PS,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),'-Action',action,'-GamePath',str(fixture),'-NoUI'],capture_output=True,text=True,errors='replace')
 assert (r.returncode!=0)==fail,(r.stdout,r.stderr)
 return r
command(old,'Install')
before={r['path']:hashlib.sha256((fixture/r['path']).read_bytes()).hexdigest() for r in json.loads((PKG/'manifest.json').read_text())['files']}
r=command(PKG/'Coop-Localization.ps1','Install',True)
assert 'OLD v0.5/v0.4' in r.stderr
assert before=={p:hashlib.sha256((fixture/p).read_bytes()).hexdigest() for p in before}
command(old,'Remove');command(PKG/'Coop-Localization.ps1','Install');command(PKG/'Coop-Localization.ps1','Verify');command(PKG/'Coop-Localization.ps1','Remove')
(AUDIT/'upgrade.json').write_text(json.dumps({'old_receipt_refused_before_write':True,'old_uninstall_then_new_install_verify_remove':True},indent=2))
fulltest=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')
subprocess.run([PS,'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(PKG/'Coop-Launcher.ps1'),'-SmokeTest','-GamePath',str(fulltest)],check=True)
assert not (PKG/'loadouts.json').exists() and not (PKG/'launcher-settings.json').exists()
print('Complete release transaction/GUI/old-version upgrade/native reconstruction/launcher checks passed.')
