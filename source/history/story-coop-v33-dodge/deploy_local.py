"""Reversibly install dodge support using the existing guarded updater."""
import importlib.util
import json
from pathlib import Path
import subprocess
from build_dodge import HERE,WORK,sha

GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')


def updater():
    spec=importlib.util.spec_from_file_location('dodge_guarded_updater',WORK/'story-coop-v28-trait-descriptions/deploy_local.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.HERE=HERE
    return module


def prepare(dest):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    rows=json.loads((HERE/'builds.json').read_text())
    allow=[dict(Language=r['language'],SHA256=r['sha256'],TestAssists=False,
        Assets=[dict(Name=n,SHA256=h) for n,h in r['ui_assets'].items()]) for r in rows]
    (dest/'steam-entry-builds.json').write_text(json.dumps(allow,indent=2)+'\n')
    (dest/'Coop-Steam-Entry.ps1').write_bytes((WORK/'story-coop-v29-steam-entry/Coop-Steam-Entry.ps1').read_bytes())
    (dest/'Coop-Key-Settings.ps1').write_bytes((WORK/'story-coop-v26-direct/Coop-Key-Settings.ps1').read_bytes())


def main():
    assert json.loads((HERE/'validation.json').read_text())['passed']
    assert json.loads((HERE/'install-validation.json').read_text())['passed']
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "Get-CimInstance Win32_Process -Filter \"Name LIKE 'shank2%'\" | ForEach-Object ExecutablePath"],capture_output=True,text=True,check=True)
    for name in result.stdout.splitlines():
        if name.strip() and Path(name.strip()).resolve().is_relative_to(GAME.resolve()):
            raise RuntimeError('Preserve the running game; install after the user exits.')
    prepare(HERE/'candidate/patch')
    module=updater()
    targets=[GAME/'patch'/n for n in ('steam-entry-builds.json','Coop-Key-Settings.ps1')]
    before={p:p.read_bytes() for p in targets}
    backup=HERE/'settings-backup';backup.mkdir(exist_ok=True)
    for p,data in before.items():(backup/p.name).write_bytes(data)
    receipt=None
    try:
        module.atomic(targets[0],(HERE/'candidate/patch/steam-entry-builds.json').read_bytes())
        receipt=module.install(GAME,'chs',save_receipt=False)
        module.atomic(targets[1],(HERE/'candidate/patch/Coop-Key-Settings.ps1').read_bytes())
    except BaseException:
        if receipt and not receipt.get('already_installed'):module.rollback(receipt)
        for p,data in before.items():module.atomic(p,data)
        raise
    (HERE/'local-install.json').write_text(json.dumps(dict(passed=True,receipt=receipt,
        settings_ui_sha256=sha(targets[1].read_bytes()),user_key_files_untouched=True,
        test_assists=False,package_generated=False),indent=2)+'\n')
    print('Installed clean dodge support and bilingual controls UI; existing user key files untouched.')


if __name__=='__main__':main()
