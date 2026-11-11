"""Exercise the public three-profile installers only in disposable game roots."""
import ctypes as C
from ctypes import wintypes as W
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
from build_release import HERE,ROOT,WORK,STOCK,ORIGINAL,PROFILES,sha,save

PS=Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe'


def run(package,game,action,expect_error=False):
    result=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',
        str(package/'patch/Install-Patch.ps1'),'-Action',action,'-GamePath',str(game),'-NoUI'],
        capture_output=True,text=True,encoding='utf8',errors='replace',timeout=180)
    if expect_error:assert result.returncode!=0,(action,result.stdout)
    else:assert result.returncode==0,(action,result.stdout,result.stderr)
    return result


def fixture(game,manifest):
    (game/'bin').mkdir(parents=True);(game/'data-pc/ui').mkdir(parents=True)
    paths=set(manifest['guards'])|{f['path'] for f in manifest['files'] if f['original_sha256']}
    paths.add('data-pc/ui/campaignscreen.chui')
    for name in paths:
        source=STOCK if name=='bin/shank2.exe' else ORIGINAL/name
        target=game/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    personal={'bin/Shank2-Coop-Keys.dat':b'preserve personal key mappings',
        'bin/Shank2-Coop-Dodge.dat':b'preserve personal dodge mappings',
        'patch/launcher-settings.json':b'{"language":"zh"}',
        'userdata/example-save.dat':b'never touch saves','settings.ini':b'user display settings'}
    for name,data in personal.items():
        p=game/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return snapshot(game)


def snapshot(game):
    return {p.relative_to(game).as_posix():sha(p.read_bytes()) for p in game.rglob('*')
        if p.is_file() and '.shank2-patch' not in p.relative_to(game).parts and p.name!='.shank2-patch.lock'}


def installed(game,manifest):
    for f in manifest['files']:
        p=game/f['path'];assert p.stat().st_size==f['size'] and sha(p.read_bytes())==f['sha256'],f['path']
    for name,digest in manifest['guards'].items():assert sha((game/name).read_bytes())==digest


def lock(path):
    k=C.WinDLL('kernel32',use_last_error=True)
    k.CreateFileW.argtypes=[W.LPCWSTR,W.DWORD,W.DWORD,C.c_void_p,W.DWORD,W.DWORD,W.HANDLE];k.CreateFileW.restype=W.HANDLE
    k.CloseHandle.argtypes=[W.HANDLE]
    handle=k.CreateFileW(str(path),0x80000000,1,None,3,0,None)
    if handle==C.c_void_p(-1).value:raise C.WinError(C.get_last_error())
    return k,handle


def pending(game,manifest,*,removing=False,committed=False):
    meta=game/'.shank2-patch';stage_name='.shank2-patch/stage-'+uuid.uuid4().hex
    stage=game/stage_name;stage.mkdir(parents=True)
    selected=next(f for f in manifest['files'] if f.get('relative') and f['path'].startswith('data-pc/ui/'))
    target=game/selected['path'];state=meta/'state.json'
    if removing:
        before=target.read_bytes();b=stage/'rollback'/selected['path'];b.parent.mkdir(parents=True);b.write_bytes(before)
        entry=next(f for f in json.loads(state.read_text(encoding='utf-8-sig'))['files'] if f['path']==selected['path'])
        after=(meta/'backups'/selected['path']).read_bytes() if entry['original_present'] else None
        if after is None:target.unlink()
        else:target.write_bytes(after)
        before_hash=sha(before);after_hash=sha(after) if after is not None else None
        state_before=sha(state.read_bytes());state_after=None
    elif committed:
        before_hash=None;after_hash=selected['sha256'];state_before=None;state_after=sha(state.read_bytes())
    else:
        assert not state.exists()
        before=target.read_bytes() if target.exists() else None
        before_hash=sha(before) if before is not None else None
        if before is not None:
            b=stage/'rollback'/selected['path'];b.parent.mkdir(parents=True);b.write_bytes(before)
        payload=(ROOT/'outputs'/PROFILES[manifest['profile']][0]/'patch'/selected['relative']).read_bytes()
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(payload)
        after_hash=selected['sha256'];state_before=None;state_after='1'*64
    save(meta/'transaction.json',dict(format=1,profile=manifest['profile'],action='Remove' if removing else 'Install',
        stage=stage_name,beforeHash=state_before,afterHash=state_after,
        operations=[dict(path=selected['path'],beforeHash=before_hash,afterHash=after_hash,newBackup=False)]))


def main():
    reports=[]
    with tempfile.TemporaryDirectory(prefix='three-pack-tests-',dir=HERE) as folder:
        temp=Path(folder)
        for profile,(name,mod,chs) in PROFILES.items():
            package=ROOT/'outputs'/name;manifest=json.loads((package/'patch/manifest.json').read_text(encoding='utf-8-sig'))
            game=temp/profile;before=fixture(game,manifest);checks=[]
            run(package,game,'Install');installed(game,manifest);checks.append('clean install exact')
            run(package,game,'Verify');run(package,game,'Install');installed(game,manifest);checks.append('verify and repeat install')
            pending(game,manifest,committed=True);run(package,game,'Verify');checks.append('committed journal cleanup')
            pending(game,manifest,removing=True);run(package,game,'Verify');installed(game,manifest);checks.append('interrupted removal rollback')
            exe=game/'bin/shank2.exe';clean=exe.read_bytes();exe.write_bytes(b'BAD!'+clean[4:])
            run(package,game,'Verify',True);run(package,game,'Remove',True);assert exe.read_bytes().startswith(b'BAD!');exe.write_bytes(clean);checks.append('modified executable refusal')
            other=ROOT/'outputs'/next(v[0] for k,v in PROFILES.items() if k!=profile)
            current=snapshot(game);run(other,game,'Install',True);assert snapshot(game)==current;checks.append('other profile refused without writes')
            run(package,game,'Remove');assert snapshot(game)==before;checks.append('exact uninstall including personal data')
            k,handle=lock(exe)
            try:run(package,game,'Install',True)
            finally:k.CloseHandle(handle)
            assert snapshot(game)==before and not (game/'.shank2-patch/transaction.json').exists();checks.append('locked executable rollback')
            pending(game,manifest);run(package,game,'Install');installed(game,manifest);run(package,game,'Remove');assert snapshot(game)==before;checks.append('interrupted install recovery')
            # Corrupt the first payload in a tiny copy; no need to copy large movies.
            bad=temp/(profile+'-bad-package');(bad/'patch').mkdir(parents=True)
            for file in ('Install-Patch.ps1','Game-Paths.ps1','manifest.json','exe-recipe.json'):shutil.copyfile(package/'patch'/file,bad/'patch'/file)
            first=next(f for f in manifest['files'] if f.get('relative'));p=bad/'patch'/first['relative'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'bad payload')
            run(bad,game,'Install',True);assert snapshot(game)==before;checks.append('damaged payload refused before commit')
            old=exe.read_bytes();exe.write_bytes(b'WRONG'+old[5:]);current=snapshot(game)
            run(package,game,'Install',True);assert snapshot(game)==current;exe.write_bytes(old);checks.append('wrong game executable refusal')
            if mod:
                result=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(package/'patch/Coop-Key-Settings.ps1'),'-GamePath',str(game),'-SmokeTest'],capture_output=True,text=True,timeout=30)
                assert result.returncode==0,result.stderr;assert snapshot(game)==before;checks.append('31-key bilingual controls smoke')
            result=subprocess.run([str(PS),'-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'test_gui.ps1'),str(package),str(game)],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=180)
            assert result.returncode==0,(result.stdout,result.stderr);assert snapshot(game)==before;checks.append('GUI install verify remove error handling')
            reports.append(dict(profile=profile,passed=True,checks=checks))
            print(profile+': '+str(len(checks))+' install/recovery/GUI checks passed.',flush=True)
    save(HERE/'installer-validation.json',dict(passed=True,profiles=reports))


if __name__=='__main__':main()
