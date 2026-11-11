"""Freeze corrected controls-entry packages without overwriting old archives."""
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
from build_fix import HERE,ROOT,sha,save


def main():
    assert json.loads((HERE/'entry-validation.json').read_text(encoding='utf8'))['passed']
    results=[]
    for p in json.loads((HERE/'prepared.json').read_text(encoding='utf8')):
        folder=Path(p['directory']);archive=folder.parent/(folder.name+'.zip');assert not archive.exists()
        v=folder/'patch/VALIDATION.json';value=json.loads(v.read_text(encoding='utf8'))
        value.update(actual_installed_controls_cmd_verified=True,missing_helper_failure_reproduced=True)
        save(v,value)
        files=sorted(f for f in folder.rglob('*') if f.is_file())
        for f in files:
            assert f.suffix.lower() not in ('.exe','.dll','.dat','.onnx')
            if p['profile']=='MOD-EN':
                assert f.relative_to(folder).as_posix().isascii()
                if f.suffix.lower() in ('.md','.ps1','.cmd','.json','.txt'):
                    assert not re.search(r'[\u3400-\u9fff\uf900-\ufaff]',f.read_text(encoding='utf-8-sig'))
        (folder/'SHA256SUMS.txt').write_text(''.join(sha(f.read_bytes())+'  '+f.relative_to(folder).as_posix()+'\n' for f in files),encoding='utf8')
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for f in sorted(folder.rglob('*')):
                if f.is_file():z.write(f,f.relative_to(folder).as_posix())
        with zipfile.ZipFile(archive) as z:assert z.testzip() is None
        scripts=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts')
        subprocess.run([sys.executable,str(scripts/'verify_release_archive.py'),'--directory',str(folder),
            '--archive',str(archive),'--json',str(HERE/(p['profile']+'-archive-equality.json'))],check=True,stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable,str(scripts/'audit_release_size.py'),'--archive',str(archive),
            '--json',str(HERE/(p['profile']+'-size-audit.json'))],check=True,stdout=subprocess.DEVNULL)
        result=dict(profile=p['profile'],version=p['version'],archive=str(archive),bytes=archive.stat().st_size,
            sha256=sha(archive.read_bytes()),archive_matches_directory=True)
        results.append(result);print(json.dumps(result),flush=True)
    save(HERE/'release.json',dict(passed=True,packages=results))


if __name__=='__main__':main()
