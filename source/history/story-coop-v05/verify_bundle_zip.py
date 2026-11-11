from pathlib import Path
import zipfile,subprocess,json,hashlib,os
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
archive=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS.zip'
dest=HERE/'bundle-zip-smoke/分享包 中文 空格';dest.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(archive) as z:
    for info in z.infolist():assert (dest/info.filename).resolve().is_relative_to(dest.resolve())
    z.extractall(dest)
for row in (dest/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines():
    digest,name=row.split('  ',1);assert hashlib.sha256((dest/name).read_bytes()).hexdigest()==digest
fixture=HERE/'bundle-fixture';ps=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
def entry(name):
    action=f'"{os.environ.get("COMSPEC",r"C:\Windows\System32\cmd.exe")}" /d /s /c ""{dest/name}" -GamePath "{fixture}" -Group Text -NoUI"'
    p=subprocess.run(action,input='\n',capture_output=True,text=True,errors='replace',timeout=60)
    assert p.returncode==0,(p.stdout,p.stderr)
entry('Install-CHS.cmd')
try:
    for mode in ['Keyboard','Pads']:
        p=subprocess.run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(dest/'patch/Manage-Coop.ps1'),'-Action','Verify','-InputMode',mode,'-GamePath',str(fixture)],capture_output=True,text=True,errors='replace')
        assert p.returncode==0,(p.stdout,p.stderr)
finally:entry('Remove-CHS.cmd')
manifest=json.loads((dest/'patch/manifest.json').read_text())
for row in manifest['files']:assert hashlib.sha256((fixture/row['path']).read_bytes()).hexdigest()==row['original_sha256']
result={'safe_flat_zip':True,'all_130_hashes_match':True,'unicode_spaces_extraction':True,'actual_zip_install_remove_entrypoints':True,'both_chs_mod_modes_verify':True,'all_original_resources_restored':True}
(HERE/'analysis/bundle-zip-smoke.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
