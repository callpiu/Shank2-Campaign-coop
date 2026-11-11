"""Install the description UI and matching EXE as a reversible transaction."""
import json
from pathlib import Path
import subprocess
import uuid
import os

from build_descriptions import HERE, PREVIOUS, sha

GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
STOCK='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'


def atomic(path,data):
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex[:8]+'.tmp')
    try:
        temp.write_bytes(data)
        assert sha(temp.read_bytes())==sha(data)
        temp.replace(path)
    finally:temp.unlink(missing_ok=True)


def sync_steam(game):
    ps=Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
    result=subprocess.run([str(ps),'-NoProfile','-ExecutionPolicy','Bypass','-File',
        str(game/'patch/Coop-Steam-Entry.ps1'),'-GamePath',str(game),'-Action','Sync'],
        capture_output=True,text=True,errors='replace',check=True)
    report=json.loads(result.stdout)
    assert report['Enabled'] and report['SteamEntrySHA256']==sha((game/'bin/shank2-story-coop.exe').read_bytes())


def install(game=GAME,language='chs',*,save_receipt=True):
    game=game.resolve()
    assert json.loads((HERE/'validation.json').read_text())['passed']
    rows=json.loads((HERE/'builds.json').read_text())
    row=next(r for r in rows if r['language']==language)
    running=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter \"Name LIKE 'shank2%'\" -ErrorAction Stop | ForEach-Object ExecutablePath"],
        capture_output=True,text=True,check=True)
    for name in running.stdout.splitlines():
        if name.strip() and Path(name.strip()).resolve().is_relative_to(game):
            raise RuntimeError('Keep the running installed game. Update after it exits.')
    steam_exe=game/'bin/shank2.exe'
    steam_before=steam_exe.read_bytes()
    steam_state_path=game/'.storycoop-steam/state.json'
    steam_state_bytes=steam_state_path.read_bytes() if steam_state_path.exists() else None
    steam_state=json.loads(steam_state_bytes) if steam_state_bytes else None
    steam_enabled=bool(steam_state and steam_state.get('Enabled'))
    if sha(steam_before)!=STOCK:
        assert steam_enabled and steam_state['Version']==1
        assert steam_state['OriginalSHA256']==STOCK and steam_state['ActiveModSHA256']==sha(steam_before)
    if steam_enabled:
        assert sha((game/'.storycoop-steam/shank2.original.exe').read_bytes())==STOCK
        assert (game/'patch/Coop-Steam-Entry.ps1').is_file()
    target=game/'bin/shank2-story-coop.exe'
    before=target.read_bytes()
    assert sha(before) in (row['v27_sha256'],row['sha256'],*row.get('description_predecessors',[]))
    asset=game/'data-pc/ui'/row['description_asset']
    asset.parent.mkdir(parents=True,exist_ok=True)
    after=(HERE/'dev'/f'shank2-story-coop-{language}.exe').read_bytes()
    newui=(HERE/'dev'/asset.name).read_bytes()
    payload={game/'data-pc/ui'/name:(HERE/'dev'/name).read_bytes() for name in row['ui_assets']}
    for path,data in payload.items():assert sha(data)==row['ui_assets'][path.name]
    assert sha(after)==row['sha256'] and not row['test_assists']
    for path in (target,*payload):assert path.resolve().is_relative_to(game)
    if before==after and all(path.exists() and path.read_bytes()==data for path,data in payload.items()):
        if steam_enabled:sync_steam(game)
        return dict(already_installed=True,game=str(game),language=language,steam_entry_synced=steam_enabled)
    lock=game/'bin/.shank2-description-update.lock'
    with lock.open('x') as stream:stream.write('v28 description update\n')
    backup=HERE/'local-backups'/uuid.uuid4().hex[:12]
    backup.mkdir(parents=True)
    oldui=asset.read_bytes() if asset.exists() else None
    previous={path:path.read_bytes() if path.exists() else None for path in payload}
    (backup/'previous.exe').write_bytes(before)
    if steam_enabled:
        (backup/'steam-entry-before.exe').write_bytes(steam_before)
        (backup/'steam-state-before.json').write_bytes(steam_state_bytes)
    if oldui is not None:(backup/'previous.chui').write_bytes(oldui)
    resources=[]
    for i,(path,data) in enumerate(payload.items()):
        name=f'resource-{i}.chui'
        if previous[path] is not None:(backup/name).write_bytes(previous[path])
        resources.append(dict(path=str(path),sha256=sha(data),previous_present=previous[path] is not None,backup_name=name))
    receipt=dict(game=str(game),language=language,exe=str(target),asset=str(asset),
        before_sha256=sha(before),after_sha256=sha(after),asset_sha256=sha(newui),
        previous_asset_present=oldui is not None,resources=resources,backup=str(backup),test_assists=False,
        original_exe_sha256=STOCK,settings_and_saves_untouched=True,package_generated=False)
    receipt['steam_entry_synced']=steam_enabled
    if steam_enabled:receipt['steam_entry_before_sha256']=sha(steam_before)
    (backup/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    try:
        # Commit EXE last so it cannot reference a missing UI resource.
        for path,data in payload.items():atomic(path,data)
        atomic(target,after)
        assert sha(target.read_bytes())==row['sha256']
        assert all(path.read_bytes()==data for path,data in payload.items())
        assert steam_exe.read_bytes()==steam_before
        if steam_enabled:
            sync_steam(game)
            assert steam_exe.read_bytes()==after
    except BaseException:
        atomic(target,before)
        if steam_enabled:
            atomic(steam_exe,steam_before)
            atomic(steam_state_path,steam_state_bytes)
        for path,data in previous.items():
            if data is None:path.unlink(missing_ok=True)
            else:atomic(path,data)
        raise
    finally:lock.unlink(missing_ok=True)
    if save_receipt:(HERE/'local-install.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def rollback(receipt):
    game=Path(receipt['game']).resolve()
    exe=Path(receipt['exe']);asset=Path(receipt['asset']);backup=Path(receipt['backup'])
    assert exe.resolve().is_relative_to(game) and asset.resolve().is_relative_to(game)
    assert sha(exe.read_bytes())==receipt['after_sha256']
    for item in receipt['resources']:
        path=Path(item['path'])
        assert path.resolve().is_relative_to(game)
        assert sha(path.read_bytes())==item['sha256']
    before=(backup/'previous.exe').read_bytes()
    assert sha(before)==receipt['before_sha256']
    if receipt.get('steam_entry_synced'):
        steam_exe=game/'bin/shank2.exe'
        assert sha(steam_exe.read_bytes())==receipt['after_sha256']
        steam_before=(backup/'steam-entry-before.exe').read_bytes()
        assert sha(steam_before)==receipt['steam_entry_before_sha256']
    atomic(exe,before)
    if receipt.get('steam_entry_synced'):
        atomic(steam_exe,steam_before)
        atomic(game/'.storycoop-steam/state.json',(backup/'steam-state-before.json').read_bytes())
    for item in receipt['resources']:
        path=Path(item['path'])
        if item['previous_present']:atomic(path,(backup/item['backup_name']).read_bytes())
        else:path.unlink()


if __name__=='__main__':print(json.dumps(install(),indent=2))
