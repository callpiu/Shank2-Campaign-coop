"""Transactionally refresh the Steam allowlist and install the startup fix."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
sys.path.insert(0,str(WORK/'story-coop-v28-trait-descriptions'))
from build_descriptions import sha


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def main():
    assert json.loads((HERE/'startup-validation.json').read_text())['passed']
    updater=module('ui_table_fix_installer',WORK/'story-coop-v28-trait-descriptions/deploy_local.py')
    prepare=module('steam_table_fix_prepare',WORK/'story-coop-v29-steam-entry/prepare.py')
    game=prepare.GAME
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter \"Name LIKE 'shank2%'\" -ErrorAction Stop | ForEach-Object ExecutablePath"],capture_output=True,text=True,check=True)
    for path in result.stdout.splitlines():
        if path.strip() and Path(path.strip()).resolve().is_relative_to(game.resolve()):
            raise RuntimeError('Keep current game progress; install after it exits.')
    prepare.prepare(HERE/'steam-candidate/patch')
    manifest=game/'patch/steam-entry-builds.json'
    before=manifest.read_bytes()
    assert sha((game/'patch/Coop-Steam-Entry.ps1').read_bytes())==sha((HERE/'steam-candidate/patch/Coop-Steam-Entry.ps1').read_bytes())
    try:
        updater.atomic(manifest,(HERE/'steam-candidate/patch/steam-entry-builds.json').read_bytes())
        receipt=updater.install(game,'chs')
    except BaseException:
        updater.atomic(manifest,before)
        raise
    (HERE/'previous-steam-builds.json').write_bytes(before)
    (HERE/'local-install.json').write_text(json.dumps(dict(passed=True,receipt=receipt,
        steam_allowlist_updated=True,steam_and_direct_equal=sha((game/'bin/shank2.exe').read_bytes())==sha((game/'bin/shank2-story-coop.exe').read_bytes()),
        test_assists=False,package_generated=False),indent=2)+'\n')
    print('Updated clean direct and Steam entries with the non-overlapping trait table.')


if __name__=='__main__':main()
