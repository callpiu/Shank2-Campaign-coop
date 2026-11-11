"""Exercise the simplified CMD routes and existing GUI/backend in isolation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent;WORK=HERE.parent
sys.path.insert(0,str(WORK/'story-coop-v34-release'))
from test_release import fixture,run,snapshot,installed,PS
from build_release import save


def cmd(path,game,*args):
    command='cmd.exe /d /s /c "'+subprocess.list2cmdline([str(path),'-GamePath',str(game),*args])+'"'
    result=subprocess.run(command,input='',cwd=HERE,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=90)
    assert result.returncode==0,(path,result.stdout,result.stderr)


def main():
    results=[]
    with tempfile.TemporaryDirectory(prefix='simple 包 空格-',dir=HERE) as name:
        temp=Path(name)
        for row in json.loads((HERE/'prepared.json').read_text(encoding='utf8')):
            package=Path(row['directory']);m=json.loads((package/'patch/manifest.json').read_text(encoding='utf8'))
            root_cmds={p.name for p in package.glob('*.cmd')}
            assert root_cmds=={row['install_entry'],row['uninstall_entry']}
            assert not list(package.glob('*.ps1'))
            game=temp/row['profile'];before=fixture(game,m)
            cmd(package/row['install_entry'],game,'-NoShow')
            run(Path(row['source_directory']),game,'Install')
            run(package,game,'Install');installed(game,m);run(package,game,'Verify')
            assert json.loads((game/'.shank2-patch/state.json').read_text(encoding='utf8'))['version']==m['version']
            cmd(package/row['uninstall_entry'],game,'-NoUI');assert snapshot(game)==before
            result=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(WORK/'story-coop-v34-release/test_gui.ps1'),str(package),str(game)],capture_output=True,text=True,errors='replace',timeout=180)
            assert result.returncode==0,(result.stdout,result.stderr);assert snapshot(game)==before
            results.append(dict(profile=row['profile'],exactly_two_public_cmds=True,no_public_ps1=True,
                real_install_cmd_constructs_manager=True,real_uninstall_cmd_restores=True,
                old_package_upgrade=True,gui_install_verify_remove=True,personal_files_preserved=True))
            print(row['profile']+': simplified entries, upgrade, GUI and restore passed.',flush=True)
    save(HERE/'validation.json',dict(passed=True,profiles=results))


if __name__=='__main__':main()
