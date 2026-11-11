"""Exercise real Windows PowerShell transactions against a disposable fixture."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from prepare import HERE,WORK,GAME,prepare


def main():
    ps=str(Path(os.environ['WINDIR'])/'System32/WindowsPowerShell/v1.0/powershell.exe')
    stock=(GAME/'bin/shank2.exe').read_bytes()
    # Also supports re-running these checks after Steam integration is enabled.
    import hashlib
    digest=lambda b:hashlib.sha256(b).hexdigest()
    stock_sha='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
    if digest(stock)!=stock_sha:stock=(GAME/'.storycoop-steam/shank2.original.exe').read_bytes()
    assert digest(stock)==stock_sha
    cases=[]
    with tempfile.TemporaryDirectory(prefix='steam-entry-',dir=HERE) as folder:
        root=Path(folder)/'Shared Game';(root/'bin').mkdir(parents=True);(root/'data-pc/ui').mkdir(parents=True)
        builds=prepare(root/'patch')
        source={lang:(WORK/'story-coop-v28-trait-descriptions/dev'/f'shank2-story-coop-{lang}.exe').read_bytes() for lang in ('en','chs')}
        original=root/'bin/shank2.exe';mod=root/'bin/shank2-story-coop.exe'
        original.write_bytes(stock);mod.write_bytes(source['chs'])
        for row in builds:
            for asset in row['Assets']:
                shutil.copyfile(WORK/'story-coop-v28-trait-descriptions/dev'/asset['Name'],root/'data-pc/ui'/asset['Name'])
        settings=root/'bin/Shank2-Coop-Keys.dat';settings.write_bytes(b'KEEP USER KEYBINDS')
        config=root/'users/display.cfg';config.parent.mkdir();config.write_bytes(b'KEEP RESOLUTION AND FULLSCREEN')
        def call(action,success=True):
            result=subprocess.run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'patch/Coop-Steam-Entry.ps1'),'-GamePath',str(root),'-Action',action],capture_output=True,text=True,errors='replace')
            if (result.returncode==0)!=success:raise RuntimeError((action,result.stdout,result.stderr))
            assert settings.read_bytes()==b'KEEP USER KEYBINDS' and config.read_bytes()==b'KEEP RESOLUTION AND FULLSCREEN'
            return json.loads(result.stdout) if success else None
        assert not call('Sync')['Synced'];assert original.read_bytes()==stock;cases.append('disabled Sync preserves original')
        call('Enable');assert original.read_bytes()==source['chs'];assert (root/'.storycoop-steam/shank2.original.exe').read_bytes()==stock;cases.append('enable CHS, verified immutable original backup')
        assert call('Verify')['Active'];call('Enable');cases.append('verify and repeat enable')
        mod.write_bytes(source['en']);call('Sync');assert original.read_bytes()==source['en'];cases.append('active source update syncs to EN build')
        original.write_bytes(stock);assert call('Verify')['ReenableRequired'];call('Sync');assert original.read_bytes()==source['en'];cases.append('known stock restored by Steam can be re-enabled')
        call('Disable');assert original.read_bytes()==stock;call('Disable');assert original.read_bytes()==stock;cases.append('disable and repeat restore original exactly')
        assert not call('Verify')['Enabled']
        mod.write_bytes(b'unknown mod');call('Enable',False);assert original.read_bytes()==stock;cases.append('unknown source rejected')
        mod.write_bytes(source['chs'])
        missing=root/'data-pc/ui'/next(r for r in builds if r['Language']=='chs')['Assets'][0]['Name']
        before=missing.read_bytes();missing.write_bytes(b'bad asset');call('Enable',False);assert original.read_bytes()==stock;missing.write_bytes(before);cases.append('mismatched resource rejected before commit')
        call('Enable');original.write_bytes(b'foreign changes');call('Disable',False);assert original.read_bytes()==b'foreign changes';cases.append('foreign target edits not overwritten')
        original.write_bytes(source['chs']);backup=root/'.storycoop-steam/shank2.original.exe';backup.write_bytes(b'damaged backup');call('Disable',False);assert original.read_bytes()==source['chs'];backup.write_bytes(stock);cases.append('damaged original backup rejected')
        call('Disable');assert original.read_bytes()==stock
    (HERE/'manager-validation.json').write_text(json.dumps(dict(passed=True,checks=cases,settings_untouched=True,stock_restored_exactly=True),indent=2)+'\n',encoding='utf8')
    print(f'{len(cases)} Steam integration transaction checks passed.')


if __name__=='__main__':main()
