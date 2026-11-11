"""Install the verified combo repair into this user's existing v0.9.1 copy."""
import json
import os
from pathlib import Path
import subprocess
import uuid
import zipfile

from build_update import BASE, BASE_SHA, HERE, make_members, sha
from test_dispatch import FIXED, ORIGINAL

GAME = Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
PS = Path(os.environ['WINDIR']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'


def run(*args):
    return subprocess.run([str(PS), '-NoProfile', '-ExecutionPolicy', 'Bypass', *args],
                          capture_output=True, text=True, errors='replace', check=True, timeout=120).stdout


def replace(path, data):
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temporary.write_bytes(data)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    assert GAME.resolve() == GAME and sha(BASE.read_bytes()) == BASE_SHA
    running = run('-Command', "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }")
    assert not running.strip()
    patch = GAME / 'patch'
    with zipfile.ZipFile(BASE) as bundle:
        content, offsets = make_members(bundle)
        files = {GAME / name: data for name, data in content.items() if name.startswith('patch/')}
        old = {path: path.read_bytes() for path in files}
        for path, data in old.items():
            assert data == bundle.read(path.relative_to(GAME).as_posix()), path
        manifest = json.loads(bundle.read('patch/manifest.json'))
        assert (patch / 'manifest.json').read_bytes() == bundle.read('patch/manifest.json')
        for name, digest in manifest['guards'].items():
            assert sha((GAME / name).read_bytes()) == digest
        keyboard = GAME / 'bin/shank2-coop-v08-keyboard.exe'
        receipt = keyboard.with_name(keyboard.name + '.coop-install.json')
        install = json.loads(receipt.read_bytes())
        assert install['baseline_sha256'] == json.loads(bundle.read('patch/keyboard-chs-addon.json'))['output_sha256']
        before = keyboard.read_bytes()
        assert sha(before) == install['installed_sha256']
        pos = offsets['keyboard', 'chs']
        assert before[pos:pos+len(ORIGINAL)] == ORIGINAL
        expected = before[:pos] + FIXED + before[pos+len(ORIGINAL):]
    saved = old | {keyboard: before, receipt: receipt.read_bytes()}
    backup = HERE / ('local-backup-' + uuid.uuid4().hex[:8])
    backup.mkdir()
    for path, data in saved.items():
        copy = backup / path.relative_to(GAME)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(data)
    command = ['-File', str(patch / 'Manage-Coop.ps1'), '-GamePath', str(GAME),
               '-InputMode', 'Keyboard', '-LoadoutPath', str(backup / receipt.relative_to(GAME))]
    run(*command, '-Action', 'Verify')
    try:
        for path, data in files.items():
            replace(path, data)
        run(*command, '-Action', 'Install')
        assert keyboard.read_bytes() == expected
        run(*command, '-Action', 'Verify')
        for name, digest in manifest['guards'].items():
            assert sha((GAME / name).read_bytes()) == digest
    except BaseException:
        for path, data in saved.items():
            if path.read_bytes() != data:
                replace(path, data)
        raise
    report = {'game': str(GAME), 'backup': str(backup), 'installed_sha256': sha(expected),
              'exact_hud_dispatch_only': True, 'launcher_recipes_updated': True, 'game_started': False}
    (HERE / 'local-install.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
