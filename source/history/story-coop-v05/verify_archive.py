from pathlib import Path
import zipfile,subprocess,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
archive=ROOT/'outputs/Shank2-StoryCoop-v0.5-Test.zip'
dest=HERE/'archive-smoke/中文 空格目录';dest.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for item in z.infolist():
        target=(dest/item.filename).resolve();assert target.is_relative_to(dest.resolve())
    z.extractall(dest)
pkg=dest/'Shank2-StoryCoop-v0.5-Test'
for row in (pkg/'SHA256SUMS.txt').read_text().splitlines():
    digest,path=row.split('  ',1);assert hashlib.sha256((pkg/path).read_bytes()).hexdigest()==digest
cases=[]
for lang in ['en','chs']:
    for mode in ['Keyboard','Pads']:
        p=subprocess.run([r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(pkg/'Manage-Coop.ps1'),'-Action','Verify','-InputMode',mode,'-GamePath',str(HERE/'installer-tests'/lang)],capture_output=True,text=True,errors='replace')
        assert p.returncode==0,(p.stdout,p.stderr)
        cases.append({'language':lang,'input':mode,'verified':True})
result={'zip_integrity':True,'all_file_hashes':True,'unicode_and_spaces_extract':True,'reconstruction':cases}
(HERE/'archive-smoke.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
