from pathlib import Path
import subprocess,json,hashlib,sys,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS';FIXTURE=HERE/'release-fixture'
manifest=json.loads((OUT/'patch/manifest.json').read_text());results=[]
def call(entry,fail=False):
    command=f'"{os.environ.get("COMSPEC",r"C:\Windows\System32\cmd.exe")}" /d /s /c ""{OUT/entry}" -GamePath "{FIXTURE}" -NoUI"'
    p=subprocess.run(command,input='\n',capture_output=True,text=True,errors='replace',timeout=60)
    assert (p.returncode!=0)==fail,(entry,p.returncode,p.stdout,p.stderr)
    results.append({'entry':entry,'expected_failure':fail,'passed':True})
call('一键安装汉化.cmd')
for row in manifest['files']:assert hashlib.sha256((FIXTURE/row['path']).read_bytes()).hexdigest()==row['sha256']
verifier=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts\verify_overlay_manifest.py')
subprocess.run([sys.executable,str(verifier),'--manifest',str(OUT/'patch/manifest.json'),'--root',str(FIXTURE),'--json',str(HERE/'release-analysis/installed-manifest.json')],check=True,capture_output=True)
call('检查汉化安装.cmd');call('Remove-CHS.cmd')
for row in manifest['files']:assert hashlib.sha256((FIXTURE/row['path']).read_bytes()).hexdigest()==row['original_sha256']
exe=FIXTURE/'bin/shank2.exe';saved=exe.read_bytes()
try:
    exe.write_bytes(saved+b'FOREIGN');call('Install-CHS.cmd',fail=True)
finally:exe.write_bytes(saved)
(HERE/'release-analysis/command-tests.json').write_text(json.dumps({'checks':results,'all_96_restored':True,'failure_exit_code_propagated':True},indent=2))
print(json.dumps({'command_checks':len(results),'all_96_assets_installed_and_restored':True,'failure_exit_code_propagated':True}))
