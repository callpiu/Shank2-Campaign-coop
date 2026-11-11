"""Stage a fresh complete game copy, then install the frozen full release."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test')
GAME=HERE/'game'
PS=Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
PATCH=ROOT/'outputs/Shank2-StoryCoop-v0.8.3-CHS/patch'

def run(folder,script,action,*args):
    p=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(folder/script),
        '-Action',action,'-GamePath',str(GAME),*map(str,args)],capture_output=True,text=True,errors='replace',timeout=120)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    print(p.stdout.strip(),flush=True)

if __name__=='__main__':
    assert not GAME.exists(),'Do not overwrite an earlier test installation.'
    assert shutil.disk_usage(HERE).free>4*1024**3
    state=json.loads((SOURCE/'.storycoop-chs/state.json').read_text(encoding='utf-8-sig'))
    old=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS/patch'
    known=json.loads((old/'manifest.json').read_text())['files']
    assert all(any(r['path']==s['path'] and r['sha256']==s['sha256'] for r in known) for s in state['files'])
    def ignore(folder,names):
        if Path(folder)==SOURCE/'bin':
            return [name for name in names if (name.lower().endswith('.exe') and name.lower()!='shank2.exe') or name.endswith('.coop-install.json')]
        return []
    shutil.copytree(SOURCE,GAME,ignore=ignore)
    print('Copied complete game to a new isolated folder.',flush=True)
    run(old,'Coop-Localization.ps1','Remove','-Group','All','-NoUI')
    run(PATCH,'Coop-Localization.ps1','Install','-Group','All','-NoUI')
    run(PATCH,'Manage-Coop.ps1','Install','-InputMode','Keyboard')
    run(PATCH,'Manage-Coop.ps1','Verify','-InputMode','Keyboard')
    image=GAME/'bin/shank2-coop-v08-keyboard.exe'
    expected=ROOT/'work/story-coop-v12-live-character/dev/keyboard-chs.exe'
    assert image.read_bytes()==expected.read_bytes()
    report=dict(game=str(GAME),sha256=hashlib.sha256(image.read_bytes()).hexdigest(),release_exact=True,
                localization='96 files verified by release installer',live_game_started=False)
    (HERE/'setup.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
