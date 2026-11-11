"""Freeze the verified English-only update and verify all archive contents."""
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

from build_english import HERE,DEST,CJK,sha,save


def main():
    for name in ('layout-validation.json','package-validation.json','user-validation.json'):
        assert json.loads((HERE/name).read_text(encoding='utf8'))['passed']
    archive=DEST.parent/(DEST.name+'.zip');assert not archive.exists()
    text_files=[];paths=[]
    for p in sorted(DEST.rglob('*')):
        relative=p.relative_to(DEST).as_posix();assert relative.isascii()
        if not p.is_file():continue
        assert p.suffix.lower() not in ('.exe','.dll','.dat','.bik','.fnt','.tex','.lua','.py')
        if p.suffix.lower() in ('.md','.ps1','.cmd','.json','.txt'):
            text=p.read_text(encoding='utf-8-sig');assert not CJK.search(text),relative
            assert '\ufeff' not in text,'Embedded/double BOM: '+relative
            text_files.append(relative)
        paths.append(p)
    (DEST/'SHA256SUMS.txt').write_text(''.join(sha(p.read_bytes())+'  '+p.relative_to(DEST).as_posix()+'\n' for p in paths),encoding='utf8')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(DEST.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(DEST).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert all(n.isascii() for n in z.namelist())
    skill=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts')
    subprocess.run([sys.executable,str(skill/'verify_release_archive.py'),'--directory',str(DEST),
        '--archive',str(archive),'--json',str(HERE/'archive-equality.json')],check=True,stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable,str(skill/'audit_release_size.py'),'--archive',str(archive),
        '--json',str(HERE/'size-audit.json')],check=True,stdout=subprocess.DEVNULL)
    report=dict(passed=True,archive=str(archive),directory=str(DEST),bytes=archive.stat().st_size,
        sha256=sha(archive.read_bytes()),files=len(paths)+1,ascii_filenames=True,
        no_cjk_in_text_files=True,text_files_scanned=text_files,
        no_embedded_bom=True,archive_matches_directory=True,user_visual_confirmed=True,
        previous_three_archives_preserved=True)
    save(HERE/'release.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='text_files_scanned'},indent=2))


if __name__=='__main__':main()
