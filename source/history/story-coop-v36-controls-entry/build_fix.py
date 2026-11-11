"""Rebuild the two affected packages with a self-contained controls shortcut."""
import json
from pathlib import Path
import sys
import zipfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];WORK=HERE.parent
sys.path.insert(0,str(WORK/'story-coop-v34-release'))
from build_release import sha,save

SOURCES=[('Shank2-v0.10.1-MOD-EN','Shank2-v0.10.2-MOD-EN','0.10.2',
    'f2c8089441414a4753a87ff0c24dc22eb5707de37d8fe4081154ee07e73dfeb7'),
    ('Shank2-v0.10.0-MOD-CHS','Shank2-v0.10.1-MOD-CHS','0.10.1',
    '31d41636d23741a9f2d4d525b90eec30629248400a625cd3b028d51b9a1c7425')]


def main():
    cmd=(WORK/'story-coop-v26-direct/Coop-Key-Settings.cmd').read_bytes();assert b'Open-Window' not in cmd
    reports=[]
    for old,new,version,digest in SOURCES:
        source=ROOT/'outputs'/(old+'.zip');assert sha(source.read_bytes())==digest
        dest=ROOT/'outputs'/new;assert not dest.exists();dest.mkdir()
        with zipfile.ZipFile(source) as z:
            for entry in z.infolist():
                if entry.is_dir() or entry.filename=='SHA256SUMS.txt':continue
                p=Path(entry.filename);assert not p.is_absolute() and '..' not in p.parts
                target=dest/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(entry))
        patch=dest/'patch';m=json.loads((patch/'manifest.json').read_text(encoding='utf8'))
        previous=m['version'];m['version']=version
        (patch/'payload/Coop-Key-Settings.cmd').write_bytes(cmd)
        row=next(f for f in m['files'] if f['path']=='Coop-Key-Settings.cmd')
        row.update(size=len(cmd),sha256=sha(cmd));save(patch/'manifest.json',m)
        p=patch/'PatchManager.ps1';p.write_text(p.read_text(encoding='utf-8-sig').replace('v'+previous,'v'+version),encoding='utf-8-sig')
        p=dest/'README.md';p.write_text(p.read_text(encoding='utf8').replace('v'+previous,'v'+version,1)+
            '\nControls shortcut fix: Coop-Key-Settings.cmd directly launches its installed settings script; no legacy Open-Window helper is required.\n',encoding='utf8')
        p=patch/'VALIDATION.json';v=json.loads(p.read_text(encoding='utf8'));v.update(version=version,controls_shortcut_direct=True);save(p,v)
        reports.append(dict(directory=str(dest),profile=m['profile'],version=version,source_archive=str(source)))
    save(HERE/'prepared.json',reports)
    print('Prepared corrected English and combined packages; original releases preserved.')


if __name__=='__main__':main()
