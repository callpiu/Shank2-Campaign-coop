"""Build the portable Steam entry manager from the current clean MOD builds."""
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')


def prepare(dest):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    rows=json.loads((WORK/'story-coop-v28-trait-descriptions/builds.json').read_text(encoding='utf8'))
    builds=[dict(Language=r['language'],SHA256=r['sha256'],TestAssists=r['test_assists'],
        Assets=[dict(Name=name,SHA256=digest) for name,digest in r['ui_assets'].items()]) for r in rows]
    (dest/'steam-entry-builds.json').write_text(json.dumps(builds,indent=2)+'\n',encoding='utf8')
    shutil.copyfile(HERE/'Coop-Steam-Entry.ps1',dest/'Coop-Steam-Entry.ps1')
    return builds


def shortcuts(game):
    for name,action in (('Enable-Steam-Coop.cmd','Enable'),('Restore-Steam-Original.cmd','Disable')):
        data='@echo off\r\n"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0patch\\Coop-Steam-Entry.ps1" -GamePath "%~dp0." -Action '+action+'\r\nif errorlevel 1 pause\r\n'
        (Path(game)/name).write_bytes(data.encode('ascii'))


if __name__=='__main__':
    prepare(HERE/'candidate/patch')
    shortcuts(HERE/'candidate')
    print('Prepared clean EN/CHS allowlist, manager, enable and restore commands.')
