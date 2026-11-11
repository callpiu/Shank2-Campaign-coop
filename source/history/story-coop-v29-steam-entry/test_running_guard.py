"""Use an owned inert process to prove both updaters preserve a running game."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from prepare import HERE,WORK,GAME,prepare
sys.path.insert(0,str(WORK/'story-coop-v28-trait-descriptions'))
spec=importlib.util.spec_from_file_location('guarded_description_update',WORK/'story-coop-v28-trait-descriptions/deploy_local.py')
updater=importlib.util.module_from_spec(spec);spec.loader.exec_module(updater)


def main():
    with tempfile.TemporaryDirectory(prefix='running-guard-',dir=HERE) as folder:
        root=Path(folder);(root/'bin').mkdir();prepare(root/'patch')
        target=root/'bin/shank2.exe';target.write_bytes((GAME/'.storycoop-steam/shank2.original.exe').read_bytes())
        mod=root/'bin/shank2-story-coop.exe';mod.write_bytes((GAME/'bin/shank2-story-coop.exe').read_bytes())
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (target,mod)}
        helper=root/'bin/shank2-entry-guard.exe'
        shutil.copyfile(Path(os.environ['WINDIR'])/'System32/cmd.exe',helper)
        # This is an inert owned stand-in, not a running game: wait on our
        # input pipe so there is no gameplay, Steam or save-data interaction.
        child=subprocess.Popen([str(helper),'/d','/c','set /p SHANK2_ENTRY_GUARD='],stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            assert child.poll() is None
            ps=str(Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe')
            result=subprocess.run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'patch/Coop-Steam-Entry.ps1'),'-GamePath',str(root),'-Action','Enable'],capture_output=True,text=True,errors='replace')
            assert result.returncode!=0 and 'running' in result.stderr.lower(),result.stderr
            try:
                updater.install(root,save_receipt=False)
                raise AssertionError('MOD updater accepted a running process.')
            except RuntimeError as error:assert 'running' in str(error).lower()
            assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (target,mod)}
            assert not (root/'.storycoop-steam/state.json').exists()
        finally:
            child.stdin.close()
            try:child.wait(timeout=3)
            except subprocess.TimeoutExpired:child.terminate();child.wait(timeout=3)
    report=dict(passed=True,steam_manager_refuses_running_process=True,mod_updater_refuses_running_process=True,
        files_unchanged=True,test_method='Owned inert stand-in, normal game untouched')
    (HERE/'running-guard-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Both entry and MOD updater refused running-process fixture without changing files.')


if __name__=='__main__':main()
