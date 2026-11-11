"""Reuse the existing transactional suite against the combined package layout."""
from pathlib import Path
import subprocess,sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS'
(HERE/'analysis').mkdir(exist_ok=True)
source=(HERE.parent/'chs-compat/validate_compat.py').read_text()
source=source.replace('from build_compat import HERE,OUT,GAME',f"HERE=Path({str(HERE)!r});OUT=Path({str(OUT/'patch')!r});GAME=Path(r'E:\\SteamLibrary\\steamapps\\common\\Shank 2')")
source=source.replace("HERE/'fixture'","HERE/'bundle-fixture'")
source=source.replace("OUT/'patch/manifest.json'","OUT/'manifest.json'").replace("OUT/'patch/payload'","OUT/'payload'")
source=source.replace("(HERE/f'{mode}-chs-test.exe')","(HERE/'final'/f'shank2-coop-v05-{mode}-chs.exe')")
source=source.replace('shank2-coop-v04-','shank2-coop-v05-')
source=source.replace("HERE/'analysis/installer-validation.json'","HERE/'analysis/bundle-installer.json'")
generated=HERE/'analysis/run_bundle_transaction_tests.py';generated.write_text(source)
subprocess.run([sys.executable,str(generated)],check=True)
ps=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
subprocess.run([ps,'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',str(HERE/'test_bundle_manager.ps1'),'-Runtime',str(OUT/'patch'),'-Fixture',str(HERE/'bundle-fixture'),'-Report',str(HERE/'analysis/bundle-manager.json')],check=True)
manifest=json.loads((OUT/'patch/manifest.json').read_text())
for entry in manifest['files']:
    p=HERE/'bundle-fixture'/entry['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['original_sha256']
print(json.dumps({'all_96_originals_restored_after_gui':True}))
