"""Install and activate the reviewed Steam entry manager on the local game."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

from prepare import HERE,GAME,prepare,shortcuts


def main():
    assert json.loads((HERE/'manager-validation.json').read_text())['passed']
    assert json.loads((HERE/'sync-validation.json').read_text())['passed']
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before={str(p.relative_to(GAME)):sha(p) for p in (GAME/'users').rglob('*') if p.is_file()}
    keys=GAME/'bin/Shank2-Coop-Keys.dat'
    if keys.exists():before[str(keys.relative_to(GAME))]=sha(keys)
    prepare(GAME/'patch');shortcuts(GAME)
    ps=str(Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe')
    def call(action):
        r=subprocess.run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(GAME/'patch/Coop-Steam-Entry.ps1'),'-GamePath',str(GAME),'-Action',action],capture_output=True,text=True,errors='replace',check=True)
        return json.loads(r.stdout)
    enabled=call('Enable');verified=call('Verify')
    assert verified['Active'] and verified['OriginalBackupValid'] and verified['EntryMatchesDirectMOD']
    assert all(sha(GAME/name)==digest for name,digest in before.items())
    report=dict(game=str(GAME),enabled=enabled,verified=verified,settings_and_game_user_files_unchanged=True,
        steam_configuration_files_modified=False,steam_launch_metadata='AppID102840 config/launch/0 executable bin\\shank2.exe',
        helper_files=['patch/Coop-Steam-Entry.ps1','patch/steam-entry-builds.json','Enable-Steam-Coop.cmd','Restore-Steam-Original.cmd'],
        mod_sha256=sha(GAME/'bin/shank2-story-coop.exe'),native_entry_sha256=sha(GAME/'bin/shank2.exe'),package_generated=False)
    (HERE/'local-install.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
