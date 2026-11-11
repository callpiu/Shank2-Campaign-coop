"""Verify clean install, v0.10.0 upgrade, English tools and exact restore."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent;WORK=HERE.parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(WORK/'story-coop-v34-release'))
from test_release import fixture,run,snapshot,installed,PS
from build_release import save


def main():
    package=ROOT/'outputs/Shank2-v0.10.1-MOD-EN'
    previous=ROOT/'outputs/Shank2-v0.10.0-MOD-EN'
    m=json.loads((package/'patch/manifest.json').read_text(encoding='utf8'))
    with tempfile.TemporaryDirectory(prefix='english-release-',dir=HERE) as name:
        game=Path(name)/'game';before=fixture(game,m)
        run(previous,game,'Install')
        original_backup=(game/'.shank2-patch/backups/bin/shank2.exe').read_bytes()
        run(package,game,'Install');installed(game,m);run(package,game,'Verify');run(package,game,'Install')
        assert (game/'.shank2-patch/backups/bin/shank2.exe').read_bytes()==original_backup
        subprocess.run([sys.executable,r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts\verify_overlay_manifest.py',
            '--manifest',str(package/'patch/manifest.json'),'--root',str(game),'--json',str(HERE/'installed-manifest.json')],check=True,stdout=subprocess.DEVNULL)
        result=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(game/'patch/Coop-Key-Settings.ps1'),'-GamePath',str(game),'-SmokeTest'],capture_output=True,text=True,errors='replace',timeout=30)
        assert result.returncode==0,result.stderr
        run(package,game,'Remove');assert snapshot(game)==before
        result=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(WORK/'story-coop-v34-release/test_gui.ps1'),str(package),str(game)],capture_output=True,text=True,errors='replace',timeout=90)
        assert result.returncode==0,(result.stdout,result.stderr);assert snapshot(game)==before
    save(HERE/'package-validation.json',dict(passed=True,previous_english_upgrade=True,
        personal_keys_and_language_preserved=True,original_backup_preserved=True,
        clean_gui_install_verify_remove=True,repeat_install=True,exact_uninstall=True,
        english_controls_smoke=True,installed_manifest_matches=True))
    print('English v0.10.0 upgrade, clean GUI install/verify/remove, controls and exact restore passed.')


if __name__=='__main__':main()
