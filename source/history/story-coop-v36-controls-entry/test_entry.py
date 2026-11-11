"""Reproduce the missing helper, then invoke the installed CMD itself."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from build_fix import HERE,ROOT,SOURCES

sys.path.insert(0,str(HERE.parent/'story-coop-v34-release'))
from test_release import fixture,run,installed,snapshot
from build_release import save


def invoke(path,cwd,*args):
    command='cmd.exe /d /s /c "'+subprocess.list2cmdline([str(path),*args])+'"'
    return subprocess.run(command,cwd=cwd,input='',capture_output=True,text=True,
        encoding='utf8',errors='replace',timeout=30)


def main():
    reports=[]
    with tempfile.TemporaryDirectory(prefix='controls entry 中文 空格-',dir=HERE) as name:
        temp=Path(name)
        for old,new,version,_ in SOURCES:
            previous=ROOT/'outputs'/old;package=ROOT/'outputs'/new
            m=json.loads((package/'patch/manifest.json').read_text(encoding='utf8'))
            game=temp/m['profile'];before=fixture(game,m)
            run(previous,game,'Install')
            assert not (game/'patch/Open-Window.ps1').exists()
            broken=invoke(game/'Coop-Key-Settings.cmd',temp,'-SmokeTest')
            assert broken.returncode!=0 and 'Open-Window.ps1' in broken.stdout+broken.stderr
            run(package,game,'Install');installed(game,m)
            for args in [('-SmokeTest',),('-GamePath',str(game),'-SmokeTest')]:
                result=invoke(game/'Coop-Key-Settings.cmd',temp,*args)
                assert result.returncode==0,(m['profile'],result.stdout,result.stderr)
                assert 'four dodge keys round trip passed' in result.stdout
            assert not (game/'patch/Open-Window.ps1').exists()
            run(package,game,'Verify');run(package,game,'Remove');assert snapshot(game)==before
            reports.append(dict(profile=m['profile'],old_missing_helper_reproduced=True,
                actual_installed_cmd_smoke=True,default_game_path=True,explicit_game_path=True,
                unicode_space_paths_and_foreign_working_dir=True,no_legacy_helper_required=True,
                upgrade_verify_uninstall=True,personal_files_preserved=True))
            print(m['profile']+': real CMD entry and default/explicit path passed.',flush=True)
    save(HERE/'entry-validation.json',dict(passed=True,profiles=reports))


if __name__=='__main__':main()
