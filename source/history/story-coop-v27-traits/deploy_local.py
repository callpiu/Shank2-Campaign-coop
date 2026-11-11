"""Replace only the installed direct EXE, keeping settings and saves."""
import json
from pathlib import Path
import subprocess
import uuid
from build_traits import BASE, GAME, HERE, pefile, sha

def deploy():
    assert json.loads((HERE/'native-validation.json').read_text())['passed']
    assert json.loads((HERE/'ranged-validation.json').read_text())['passed']
    gameplay=json.loads((HERE/'gameplay-validation.json').read_text())
    assert gameplay['passed'] and gameplay['no_test_assists']
    assert GAME.resolve()==GAME
    processes=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter \"Name LIKE 'shank2%'\" | ForEach-Object ExecutablePath"],
        capture_output=True,text=True,check=True)
    for line in processes.stdout.splitlines():
        if line.strip() and Path(line.strip()).is_relative_to(GAME):
            raise RuntimeError('Keep the game in progress. Exit it before updating the local EXE.')
    row=next(r for r in json.loads((HERE/'builds.json').read_text()) if r['language']=='chs')
    target=GAME/'bin/shank2-story-coop.exe'
    assert target.resolve()==target
    before=target.read_bytes()
    after=(HERE/'dev/shank2-story-coop-chs.exe').read_bytes()
    assert sha(after)==row['sha256']
    assert gameplay['build_sha256']==row['sha256']
    # Exact earlier v27 image documented in the prior local-install receipt.
    # Its process-only experiments were never part of the installed image.
    predecessor='e9a55cc6c318def16aed5de8eb4ea8f0d2421c1b5af761c3b36572f0c024b8d5'
    assert sha(before) in (row['v26_sha256'],predecessor,row['sha256'])
    stock=GAME/'bin/shank2.exe'
    stock_hash=sha(stock.read_bytes())
    assert stock_hash=='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
    assert len(before)==len(after)
    check=pefile.PE(data=after,fast_load=True)
    assert not row['test_assists']
    at=check.get_offset_from_rva(0x4ee3b0-BASE)
    assert after[at:at+7]==before[at:at+7]==bytes.fromhex('6aff687e876f00')
    for site,original in ((0x4f3f40,'5153558b6c2410'),(0x4f4061,'5f5e5d5b59')):
        pos=check.get_offset_from_rva(site-BASE)
        expected=bytes.fromhex(original)
        assert after[pos:pos+len(expected)]==expected
    if before==after:
        print('Exact direct build already installed.')
        return
    backup=HERE/f'local-backup-{uuid.uuid4().hex[:8]}.exe'
    backup.write_bytes(before)
    temp=target.with_name(target.name+'.'+uuid.uuid4().hex[:8]+'.tmp')
    try:
        temp.write_bytes(after)
        temp.replace(target)
        assert target.read_bytes()==after and sha(stock.read_bytes())==stock_hash
    finally:
        temp.unlink(missing_ok=True)
    (HERE/'local-install.json').write_text(json.dumps(dict(game=str(GAME),target=str(target),backup=str(backup),
        sha256=sha(after),stock_sha256=stock_hash,only_direct_exe_changed=True,archive_generated=False,
        test_assists=False,gameplay_validation_sha256=gameplay['build_sha256']),indent=2)+'\n',encoding='utf8')
    print('Installed verified campaign traits into the local direct EXE.')

if __name__=='__main__':
    deploy()
