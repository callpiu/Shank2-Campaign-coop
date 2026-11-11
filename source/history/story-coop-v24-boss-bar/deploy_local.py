"""Validate and install only the local HUD fixes. Leave gameplay and assets alone."""
import base64
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

from build_local import HERE, DEV, BASE, BASE_SHA, sha, make_members, pefile, PATCH_START, ORIGINAL, FIXED
from deploy_local import GAME, run, replace


def reconstruct(recipe, source):
    assert sha(source) == recipe['input_sha256'] and len(source) == recipe['source_size']
    rebuilt = bytearray(source)
    for patch in recipe['patches']:
        pos = patch['offset']
        before, after = (bytes.fromhex(patch[key]) for key in ('before','after'))
        assert len(before) == len(after) and rebuilt[pos:pos+len(before)] == before
        rebuilt[pos:pos+len(after)] = after
    rebuilt += base64.b64decode(recipe['append'])
    assert len(rebuilt) == recipe['target_size'] and sha(rebuilt) == recipe['output_sha256']
    return bytes(rebuilt)


def main():
    import zipfile
    assert GAME.resolve() == GAME and sha(BASE.read_bytes()) == BASE_SHA
    run('-Command', "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }")
    patch = GAME / 'patch'
    with zipfile.ZipFile(BASE) as bundle:
        combo, _ = make_members(bundle)
        manifest = json.loads(bundle.read('patch/manifest.json'))
        assert (patch/'manifest.json').read_bytes() == bundle.read('patch/manifest.json')
    files = {patch / source.name: source.read_bytes() for source in (HERE/'candidate/patch').glob('*.json')}
    assert len(files) == 5
    saved = {path: path.read_bytes() for path in files}
    for path, data in saved.items():
        assert data == combo[f'patch/{path.name}'], path
    variants = json.loads((HERE/'builds.json').read_text())
    targets = {}
    for row in variants:
        mode, lang = row['mode'], row['lang']
        suffix = '-chs' if lang == 'chs' else ''
        base = HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{suffix}.exe'
        name = patch/f'{mode}-{lang}-addon.json'
        before = reconstruct(json.loads(saved[name]), base.read_bytes())
        after = reconstruct(json.loads(files[name]), base.read_bytes())
        assert sha(before) == row['baseline_sha256'] and sha(after) == row['sha256']
        targets[mode, lang] = (before, after)
    keyboard = GAME/'bin/shank2-coop-v08-keyboard.exe'
    receipt = keyboard.with_name(keyboard.name+'.coop-install.json')
    receipt_bytes = receipt.read_bytes()
    installed = json.loads(receipt_bytes)
    current = keyboard.read_bytes()
    before, after = targets['keyboard','chs']
    assert sha(current) == installed['installed_sha256'] and sha(before) == installed['baseline_sha256']
    expected = bytearray(current)
    for offset, (old_byte,new_byte) in enumerate(zip(before,after)):
        if old_byte != new_byte:
            assert current[offset] == old_byte
            expected[offset] = new_byte
    for path, digest in manifest['guards'].items():
        assert sha((GAME/path).read_bytes()) == digest
    saved.update({keyboard: current, receipt: receipt_bytes})
    backup = HERE/('local-backup-'+uuid.uuid4().hex[:8])
    backup.mkdir()
    for path, data in saved.items():
        dest = backup/path.relative_to(GAME)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    args = ['-GamePath',str(GAME),'-InputMode','Keyboard','-LoadoutPath',str(backup/receipt.relative_to(GAME))]
    with tempfile.TemporaryDirectory(prefix='preflight-', dir=HERE) as temporary:
        stage = Path(temporary).resolve()
        assert stage.parent == HERE
        for source in patch.iterdir():
            if source.is_file() and source.name not in ('loadouts.json','launcher-settings.json'):
                (stage/source.name).write_bytes(files.get(source, source.read_bytes()))
        run('-File',str(stage/'Manage-Coop.ps1'),'-Action','Verify',*args)
    try:
        run('-Command', "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }")
        for path, data in files.items():
            replace(path,data)
        run('-File',str(patch/'Manage-Coop.ps1'),'-Action','Install',*args)
        assert keyboard.read_bytes() == expected
        run('-File',str(patch/'Manage-Coop.ps1'),'-Action','Verify',*args)
        for path, digest in manifest['guards'].items():
            assert sha((GAME/path).read_bytes()) == digest
    except BaseException:
        for path,data in saved.items():
            if path.read_bytes() != data:
                replace(path,data)
        raise
    report = dict(game=str(GAME),backup=str(backup),sha256=sha(expected),
                  four_variants_exact=True,combo_fix_preserved=True,original_damage_unchanged=True,
                  game_started=False,gameplay_verified=False,archive_generated=False)
    (HERE/'local-install.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(error.stdout or '', error.stderr or '', file=sys.stderr)
        raise
