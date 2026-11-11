"""Install the verified direct EXE, solo UI, and controls tool into the local game."""
import json
from pathlib import Path
import subprocess
import uuid
from build import BASE, GAME, HERE, WORK, pefile, sha
from assets import maps

def deploy():
    assert GAME.resolve()==GAME
    if not json.loads((HERE/'boot-validation.json').read_text())['passed']:
        raise RuntimeError('Run bootstrap validation first.')
    running=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter \"Name LIKE 'shank2%'\" | ForEach-Object ExecutablePath"],
        capture_output=True,text=True,check=True)
    for line in running.stdout.splitlines():
        if line.strip() and Path(line.strip()).is_relative_to(GAME):
            raise RuntimeError('A game in the destination is open. Keep its progress and exit before installing.')
    row=next(item for item in json.loads((HERE/'builds.json').read_text()) if item['language']=='chs')
    record=json.loads((WORK/'story-coop-v20-prelevel-layout/build-validation.json').read_text())
    for category,name in [('ui','cooppreselv20chs.chui'),('hud','campaigncoopv20chs.chui')]:
        existing=GAME/'data-pc/ui'/name
        assert sha(existing.read_bytes())==record[category]['chs']['sha256'], existing
        assert all(any(key=='evil' for key,p,t in values) for _,_,values in maps(existing.read_bytes()).values())
    for name in ('skin_evil.tex','portraits_evil.tex'):
        art=GAME/'data-pc/textures/ui/skin'/name
        assert art.read_bytes()[:4]==b'KTEX'
    image=(HERE/'dev/shank2-story-coop-chs.exe').read_bytes()
    assert sha(image)==row['sha256'] and not row['test_assists']
    pe=pefile.PE(data=image,fast_load=True)
    damage=pe.get_offset_from_rva(0x4ee3b0-BASE)
    assert image[damage:damage+7]==bytes.fromhex('6aff687e876f00')
    stock=GAME/'bin/shank2.exe'
    stock_hash=sha(stock.read_bytes())
    assert stock_hash=='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
    targets={GAME/'bin/shank2-story-coop.exe':image}
    for name,meta in row['solo_assets'].items():
        ui=GAME/'data-pc/ui'
        assert sha((ui/meta['native']).read_bytes())==meta['native_sha256']
        b=(HERE/'dev'/name).read_bytes()
        assert sha(b)==meta['sha256']
        targets[ui/name]=b
    targets[GAME/'patch/Coop-Key-Settings.ps1']=(HERE/'Coop-Key-Settings.ps1').read_bytes()
    targets[GAME/'patch/Coop-Launcher.ps1']=(HERE/'Coop-Launcher.ps1').read_bytes()
    targets[GAME/'Coop-Key-Settings.cmd']=(HERE/'Coop-Key-Settings.cmd').read_bytes()
    settings=GAME/'bin/Shank2-Coop-Keys.dat'
    if not settings.exists():
        old=GAME/'patch/loadouts.json'
        if old.exists():
            import struct
            from build import DEFAULTS, MAGIC
            preference=json.loads(old.read_text(encoding='utf-8-sig')).get('inputMode','Keyboard')
            assert preference.casefold() in ('keyboard','pads')
            targets[settings]=MAGIC+struct.pack('<28I',int(preference.casefold()=='pads'),*DEFAULTS)
    backup=HERE/f'local-backup-{uuid.uuid4().hex[:8]}'
    backup.mkdir()
    saved={}
    for path,b in targets.items():
        assert path.resolve().is_relative_to(GAME),path
        saved[path]=path.read_bytes() if path.exists() else None
        if saved[path] is not None:
            copy=backup/path.relative_to(GAME)
            copy.parent.mkdir(parents=True,exist_ok=True)
            copy.write_bytes(saved[path])
    applied=[]
    try:
        for path,b in targets.items():
            if saved[path]==b:continue
            temp=path.with_name(path.name+'.'+uuid.uuid4().hex[:8]+'.tmp')
            temp.write_bytes(b)
            try:
                temp.replace(path)
                applied.append(path)
            finally:
                temp.unlink(missing_ok=True)
        assert all(path.read_bytes()==b for path,b in targets.items())
        assert sha(stock.read_bytes())==stock_hash
    except BaseException:
        for path in reversed(applied):
            if saved[path] is None:path.unlink()
            else:path.write_bytes(saved[path])
        raise
    previous=HERE/'local-install.json'
    earlier=json.loads(previous.read_text()) if previous.exists() else {}
    prior_backups=earlier.get('prior_backups',[])+([earlier['backup']] if 'backup' in earlier else [])
    audit={'prior_backups':prior_backups,'game':str(GAME),'backup':str(backup),'stock_executable_sha256':stock_hash,
           'files':{str(p.relative_to(GAME)):{'sha256':sha(b),'new':saved[p] is None} for p,b in targets.items()},
           'test_assists':False,'archive_generated':False}
    (HERE/'local-install.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print('Installed and verified direct campaign build and standalone controls tool.')

if __name__=='__main__':
    deploy()

