"""Adverse transaction cases and shared-resource ownership in disposable fixtures."""
import ctypes
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from build_release import HERE,OUTPUT,sha,save

def main():
    patch=OUTPUT/'patch'
    tmp=Path(tempfile.mkdtemp(prefix='recovery 中文 ',dir=HERE)).resolve()
    assert tmp.parent==HERE.resolve()
    game=tmp/'game'
    shutil.copytree(HERE.parent/'story-coop-v09-fixes/upgrade-fixture',game)
    ps=Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
    rows=[]
    def run(script,action,*args,fail=None):
        p=subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(patch/script),
            '-GamePath',str(game),'-Action',action,*args],capture_output=True,text=True,errors='replace',timeout=90)
        if fail is None:assert p.returncode==0,(p.stdout,p.stderr)
        else:assert p.returncode and fail in p.stdout+p.stderr,(p.stdout,p.stderr)
        return p
    manifest=json.loads((patch/'manifest.json').read_text())['files']
    original_exe=sha(game/'bin/shank2.exe')
    try:
        run('Coop-Localization.ps1','Install','-Group','All','-NoUI')
        run('Manage-Coop.ps1','Install','-InputMode','Keyboard')
        run('Manage-Coop.ps1','Install','-InputMode','Pads')
        ui=game/'data-pc/ui/cooppreselv20chs.chui'
        run('Manage-Coop.ps1','Remove','-InputMode','Keyboard')
        assert ui.exists() and (game/'bin/shank2-coop-v08-pads.exe').exists()
        run('Manage-Coop.ps1','Remove','-InputMode','Pads')
        assert not any((game/'data-pc/ui').glob('*v20*.chui'))
        rows.append('two input modes retain shared UI until last removal')

        # Begin with a real old install, then fail the fourth file replacement.
        old=OUTPUT.parent/'Shank2-StoryCoop-v0.8.3-CHS/patch'
        p=subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(old/'Manage-Coop.ps1'),
            '-GamePath',str(game),'-Action','Install','-InputMode','Keyboard'],capture_output=True,text=True,errors='replace',timeout=90)
        assert p.returncode==0,(p.stdout,p.stderr)
        owned=[game/'bin/shank2-coop-v08-keyboard.exe',game/'bin/shank2-coop-v08-keyboard.exe.coop-install.json']
        owned+=list((game/'data-pc/ui').glob('*coopv05.chui'))
        before={p:p.read_bytes() for p in owned}
        ui.write_bytes((HERE.parent/'story-coop-v20-prelevel-layout/dev/cooppreselv20chs.chui').read_bytes())
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateFileW.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
        kernel.CreateFileW.restype=ctypes.c_void_p
        kernel.CloseHandle.argtypes=[ctypes.c_void_p]
        # Permit reads for ownership validation; deny delete/replacement.
        handle=kernel.CreateFileW(str(ui),0x80000000,1,None,3,0,None)
        assert handle not in (None,ctypes.c_void_p(-1).value),ctypes.get_last_error()
        try:run('Manage-Coop.ps1','Install','-InputMode','Keyboard',fail='Replace')
        finally:kernel.CloseHandle(handle)
        assert all(p.read_bytes()==b for p,b in before.items())
        assert not (game/'data-pc/ui/campaigncoopv20chs.chui').exists()
        assert not list(game.rglob('*.tmp'))
        rows.append('failed fourth UI replacement restores old executable receipt and first three UIs')
        run('Manage-Coop.ps1','Install','-InputMode','Keyboard')
        run('Manage-Coop.ps1','Remove','-InputMode','Keyboard')
        run('Coop-Localization.ps1','Remove','-Group','All','-NoUI')

        # Synthetic interrupted transactions model the persisted on-disk
        # states immediately before/after the atomic receipt write.
        state_root=game/'.storycoop-chs';state_path=state_root/'state.json'
        first=manifest[0];target=game/first['path'];payload=patch/'payload'/first['path']
        backup=state_root/'backups'/first['path']
        backup.parent.mkdir(parents=True,exist_ok=True)
        backup.write_bytes(target.read_bytes())
        target.write_bytes(payload.read_bytes())
        empty=dict(format=1,files=[]);one=dict(format=1,files=[first])
        save(state_path,empty)
        save(state_root/'transaction.json',dict(format=1,action='Install',paths=[first['path']],before=empty,after=one))
        result=run('Coop-Localization.ps1','Verify','-Group','All','-NoUI')
        assert 'Recovered interrupted' in result.stdout and sha(target)==first['original_sha256'] and not backup.exists()
        rows.append('uncommitted localization install recovered and original restored')

        run('Coop-Localization.ps1','Install','-Group','All','-NoUI')
        installed=json.loads(state_path.read_text(encoding='utf-8-sig'))
        after=dict(format=1,files=installed['files'][1:])
        shutil.copyfile(backup,target)
        save(state_root/'transaction.json',dict(format=1,action='Remove',paths=[first['path']],before=installed,after=after))
        result=run('Coop-Localization.ps1','Verify','-Group','All','-NoUI')
        assert 'Recovered interrupted' in result.stdout and sha(target)==first['sha256'] and backup.exists()
        rows.append('uncommitted localization removal recovered to installed payload')
        run('Coop-Localization.ps1','Remove','-Group','All','-NoUI')

        # Receipt committed but post-commit cleanup was interrupted.
        backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(target.read_bytes())
        target.write_bytes(payload.read_bytes());save(state_path,one)
        save(state_root/'transaction.json',dict(format=1,action='Install',paths=[first['path']],before=empty,after=one))
        run('Coop-Localization.ps1','Verify','-Group','All','-NoUI')
        assert sha(target)==first['sha256'] and backup.exists() and not (state_root/'transaction.json').exists()
        rows.append('committed localization install retained during journal cleanup')
        shutil.copyfile(backup,target);save(state_path,empty)
        save(state_root/'transaction.json',dict(format=1,action='Remove',paths=[first['path']],before=one,after=empty))
        run('Coop-Localization.ps1','Verify','-Group','All','-NoUI')
        assert sha(target)==first['original_sha256'] and not backup.exists()
        rows.append('committed localization removal cleans obsolete backup')
        assert all(sha(game/r['path'])==r['original_sha256'] for r in manifest)
        assert sha(game/'bin/shank2.exe')==original_exe
        assert not list(game.rglob('*.coop-chs-new'))
        save(HERE/'recovery-validation.json',dict(passed=True,cases=rows,live_game_started=False,originals_restored=True))
        print('PASS:',len(rows),'adverse/shared-resource cases; all 96 originals restored')
    finally:
        assert tmp.resolve().parent==HERE.resolve() and tmp.name.startswith('recovery 中文 ')
        shutil.rmtree(tmp)

if __name__=='__main__':main()
