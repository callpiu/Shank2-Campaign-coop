"""Archive and audit the simplified public layouts, preserving old releases."""
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from build_simple import HERE,VERSION,sha,save


def main():
    assert json.loads((HERE/'validation.json').read_text(encoding='utf8'))['passed']
    results=[]
    for row in json.loads((HERE/'prepared.json').read_text(encoding='utf8')):
        folder=Path(row['directory']);archive=folder.parent/(folder.name+'.zip');assert not archive.exists()
        manifest=json.loads((folder/'patch/manifest.json').read_text(encoding='utf8'))
        old=json.loads((Path(row['source_directory'])/'patch/manifest.json').read_text(encoding='utf8'))
        assert manifest['files']==old['files'] and manifest['guards']==old['guards']
        public={p.name for p in folder.iterdir()}
        expected={row['install_entry'],row['uninstall_entry'],row['readme'],'patch'}
        if row['profile']!='MOD-EN':expected.add('FONT-LICENSE.txt')
        assert public==expected,(public,expected)
        v=folder/'patch/VALIDATION.json';value=json.loads(v.read_text(encoding='utf8'))
        value.update(public_entries_verified=True,version_only_upgrade_receipt_verified=True);save(v,value)
        files=sorted(p for p in folder.rglob('*') if p.is_file())
        for p in files:
            if row['profile']=='MOD-EN':
                assert p.relative_to(folder).as_posix().isascii()
                if p.suffix.lower() in ('.cmd','.ps1','.md','.json','.txt'):assert not re.search(r'[\u3400-\u9fff\uf900-\ufaff]',p.read_text(encoding='utf-8-sig'))
            assert p.suffix.lower() not in ('.exe','.dll','.onnx','.dat')
        (folder/'patch/SHA256SUMS.txt').write_text(''.join(sha(p.read_bytes())+'  '+p.relative_to(folder).as_posix()+'\n' for p in files),encoding='utf8')
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(folder.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(folder).as_posix())
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None
        skill=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts')
        subprocess.run([sys.executable,str(skill/'verify_release_archive.py'),'--directory',str(folder),
            '--archive',str(archive),'--json',str(HERE/(row['profile']+'-archive-equality.json'))],check=True,stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable,str(skill/'audit_release_size.py'),'--archive',str(archive),
            '--json',str(HERE/(row['profile']+'-size-audit.json'))],check=True,stdout=subprocess.DEVNULL)
        report=dict(profile=row['profile'],version=VERSION,archive=str(archive),bytes=archive.stat().st_size,
            sha256=sha(archive.read_bytes()),public_entries=sorted(public),archive_matches_directory=True,
            runtime_payload_unchanged=True)
        results.append(report);print(json.dumps(report,ensure_ascii=False),flush=True)
    save(HERE/'release.json',dict(passed=True,packages=results))


if __name__=='__main__':main()
