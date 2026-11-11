"""Validate the consolidated installer using disposable game files only."""
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from build_release import HERE,OUTPUT,ROOT


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    patch=OUTPUT/'patch'
    builds={r['name']:r['sha256'] for r in json.loads((HERE.parent/'story-coop-v12-live-character/builds.json').read_text())}
    expected_plain=bytes.fromhex('6aff687e876f00')
    import sys
    sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
    from native import pefile
    for mode in ('keyboard','pads'):
        for lang in ('en','chs'):
            suffix='-chs' if lang=='chs' else ''
            source=(HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{suffix}.exe').read_bytes()
            recipe=json.loads((patch/f'{mode}-{lang}-addon.json').read_text())
            assert hashlib.sha256(source).hexdigest()==recipe['input_sha256']
            target=bytearray(source)
            for p in recipe['patches']:
                a,b=bytes.fromhex(p['before']),bytes.fromhex(p['after']);i=p['offset']
                assert target[i:i+len(a)]==a
                target[i:i+len(a)]=b
            target.extend(base64.b64decode(recipe['append']))
            assert hashlib.sha256(target).hexdigest()==recipe['output_sha256']==builds[f'{mode}-{lang}.exe']
            pe=pefile.PE(data=target)
            off=lambda a:pe.get_offset_from_rva(a-0x400000)
            assert target[off(0x4ee3b0):off(0x4ee3b0)+7]==expected_plain
            assert target[off(0x53de70):off(0x53de70)+6]==bytes.fromhex('558bec83e4f8')
            assert target[off(0x7ff900):off(0x7ff900)+60]==bytes(60)
    ps=Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
    checks=[]
    tmp=Path(tempfile.mkdtemp(prefix='完整包 验证 ',dir=HERE)).resolve()
    assert tmp.parent==HERE.resolve()
    game=tmp/'隔离游戏'
    shutil.copytree(HERE.parent/'story-coop-v09-fixes/upgrade-fixture',game)
    # The transactional fixture deliberately omits native portrait assets.
    # Supply them only to this disposable game, never to the distributable.
    portraits=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work\shank2-test\data-pc\textures\ui\skin')
    shutil.copytree(portraits,game/'data-pc/textures/ui/skin',dirs_exist_ok=True)
    settings=HERE.parent/'story-coop-v08-options/fixtures/settings.json'
    old=ROOT/'outputs/Shank2-StoryCoop-v0.8.1-CHS-Test/patch'
    def run(folder,script,action,*args,fail=None):
        assert action in ('Install','Verify','Remove')
        cmd=[str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(folder/script),
             '-Action',action,'-GamePath',str(game),*map(str,args)]
        p=subprocess.run(cmd,capture_output=True,text=True,errors='replace',timeout=90)
        if fail is None:assert p.returncode==0,(p.stdout,p.stderr)
        else:assert p.returncode!=0 and fail in p.stdout+p.stderr,(p.stdout,p.stderr)
        checks.append(dict(script=script,action=action,args=list(map(str,args)),expected_failure=fail is not None))
    try:
        manifest=json.loads((patch/'manifest.json').read_text())['files']
        original_exe=digest(game/'bin/shank2.exe')
        # An otherwise untouched installation must explain its missing movies.
        run(patch,'Manage-Coop.ps1','Verify','-InputMode','Keyboard',fail='Run Install-CHS.cmd')
        for lang,group in [('en','Movies'),('chs','All')]:
            run(patch,'Coop-Localization.ps1','Install','-Group',group,'-NoUI')
            state=(game/'.storycoop-chs/state.json').read_bytes()
            for mode in ('Keyboard','Pads'):
                low=mode.lower();args=('-InputMode',mode,'-LoadoutPath',settings)
                exe=game/'bin'/f'shank2-coop-v08-{low}.exe'
                run(old,'Manage-Coop.ps1','Install',*args)
                old_bytes=exe.read_bytes()
                run(patch,'Manage-Coop.ps1','Install',*args)
                config=json.loads((patch/f'{low}-recipe.json').read_text())['config_offset']
                expected=bytearray((HERE.parent/'story-coop-v12-live-character/dev'/f'{low}-{lang}.exe').read_bytes())
                expected[config:config+128]=old_bytes[config:config+128]
                assert exe.read_bytes()==expected
                run(patch,'Manage-Coop.ps1','Verify',*args)
                run(patch,'Manage-Coop.ps1','Install',*args)
                assert exe.read_bytes()==expected
                exe.write_bytes(b'unrecognized exe fixture')
                run(patch,'Manage-Coop.ps1','Install',*args,fail='refusing to overwrite')
                assert exe.read_bytes()==b'unrecognized exe fixture'
                exe.write_bytes(expected)
                run(patch,'Manage-Coop.ps1','Remove',*args)
                assert not exe.exists()
                run(old,'Manage-Coop.ps1','Install',*args)
                assert exe.read_bytes()==old_bytes
                run(old,'Manage-Coop.ps1','Remove',*args)
            assert (game/'.storycoop-chs/state.json').read_bytes()==state
            run(patch,'Coop-Localization.ps1','Verify','-Group',group,'-NoUI')
            if lang=='chs':
                verifier=Path(r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts\verify_overlay_manifest.py')
                subprocess.run([sys.executable,str(verifier),'--manifest',str(patch/'manifest.json'),'--root',str(game),
                                '--json',str(HERE/'installed-manifest.json')],check=True,capture_output=True)
                smoke=subprocess.run([str(ps),'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',
                    str(patch/'Coop-Launcher.ps1'),'-SmokeTest','-GamePath',str(game)],capture_output=True,text=True,errors='replace',timeout=60)
                assert smoke.returncode==0,(smoke.stdout,smoke.stderr)
            run(patch,'Coop-Localization.ps1','Remove','-Group',group,'-NoUI')
            assert all(digest(game/r['path'])==r['original_sha256'] for r in manifest)
        assert digest(game/'bin/shank2.exe')==original_exe
        gui=subprocess.run([str(ps),'-NoProfile','-STA','-ExecutionPolicy','Bypass','-File',
            str(HERE.parent/'story-coop-v05/test_bundle_manager.ps1'),'-Runtime',str(patch),
            '-Fixture',str(game),'-Report',str(HERE/'manager-validation.json')],capture_output=True,text=True,errors='replace',timeout=120)
        assert gui.returncode==0,(gui.stdout,gui.stderr)
        entries=[]
        def entry(name,fail=False):
            command=f'"{os.environ["COMSPEC"]}" /d /s /c ""{OUTPUT/name}" -GamePath "{game}" -NoUI"'
            result=subprocess.run(command,input='\n',capture_output=True,text=True,errors='replace',timeout=90)
            assert (result.returncode!=0)==fail,(name,result.stdout,result.stderr)
            entries.append(dict(entry=name,expected_failure=fail))
        entry('一键安装汉化.cmd')
        assert all(digest(game/r['path'])==r['sha256'] for r in manifest)
        entry('检查汉化安装.cmd')
        entry('Remove-CHS.cmd')
        assert all(digest(game/r['path'])==r['original_sha256'] for r in manifest)
        exe=game/'bin/shank2.exe';saved=exe.read_bytes()
        try:
            exe.write_bytes(saved+b'FOREIGN');entry('Install-CHS.cmd',fail=True)
        finally:exe.write_bytes(saved)
        assert digest(exe)==original_exe
        report=dict(operations=len(checks),four_variants_exact=True,no_godmode_or_probe=True,
                    restores_all_96_originals=True,launcher_smoke=True,live_game_started=False,checks=checks,
                    command_checks=entries,gui_operations=5)
        (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
        print(f'Passed {len(checks)} installer operations, four exact binaries, 96 restored assets and launcher smoke.')
    finally:
        assert tmp.resolve().parent==HERE.resolve() and tmp.name.startswith('完整包 验证 ')
        shutil.rmtree(tmp)


if __name__=='__main__':main()
