"""Check extracted overlay and both input modes with the offline installer."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

from package_update import ARCHIVE, BASE, HERE


def main():
    parent = HERE.resolve()
    tmp = Path(tempfile.mkdtemp(prefix='安装 验证 ', dir=parent)).resolve()
    assert tmp.parent == parent and tmp.name.startswith('安装 验证 ')
    game = tmp / '隔离游戏'
    update = tmp / '升级包'
    old_fixture = HERE.parent / 'story-coop-v09-fixes/upgrade-fixture'
    settings = HERE.parent / 'story-coop-v08-options/fixtures/settings.json'
    ps = Path(os.environ['WINDIR']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
    results = []

    def run(folder, script, action, *args, fail=False):
        assert action in ('Install', 'Verify', 'Remove')  # Never start Steam or Shank.
        cmd = [str(ps), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(folder / script),
               '-Action', action, '-GamePath', str(game), *args]
        p = subprocess.run(cmd, capture_output=True, text=True, errors='replace', timeout=90)
        assert (p.returncode != 0) == fail, (p.stdout, p.stderr)
        results.append(dict(script=script, action=action, args=args, expected_rejection=fail))

    try:
        shutil.copytree(old_fixture, game)
        shutil.copytree(BASE, update / 'patch', ignore=shutil.ignore_patterns('payload'))
        with zipfile.ZipFile(ARCHIVE) as z:
            z.extractall(update)
        run(BASE, 'Coop-Localization.ps1', 'Install', '-NoUI')
        manifest = json.loads((BASE / 'manifest.json').read_text())['files']
        payload_before = {r['path']: hashlib.sha256((game/r['path']).read_bytes()).hexdigest() for r in manifest}
        assert all(payload_before[r['path']] == r['sha256'] for r in manifest)
        receipt = game / '.storycoop-chs/state.json'
        receipt_before = receipt.read_bytes()
        original = game / 'bin/shank2.exe'
        original_hash = hashlib.sha256(original.read_bytes()).hexdigest()
        for mode in ('Keyboard', 'Pads'):
            low = mode.lower()
            args = ('-InputMode', mode, '-LoadoutPath', str(settings))
            manager = 'Manage-Coop.ps1'
            run(BASE, manager, 'Install', *args)
            exe = game / 'bin' / f'shank2-coop-v08-{low}.exe'
            before = exe.read_bytes()
            offset = json.loads((BASE / f'{low}-recipe.json').read_text())['config_offset']
            expected = bytearray((HERE / 'dev' / f'{low}-chs.exe').read_bytes())
            expected[offset:offset+128] = before[offset:offset+128]
            for _ in range(2):
                run(update / 'patch', manager, 'Install', *args)
                assert exe.read_bytes() == expected
            exe.write_bytes(b'unrecognized executable fixture')
            run(update / 'patch', manager, 'Install', *args, fail=True)
            assert exe.read_bytes() == b'unrecognized executable fixture'
            exe.write_bytes(expected)
            run(update / 'patch', manager, 'Remove', *args)
            assert not exe.exists()
            run(BASE, manager, 'Install', *args)
            assert exe.read_bytes() == before
        assert receipt.read_bytes() == receipt_before
        assert all(hashlib.sha256((game/path).read_bytes()).hexdigest() == h for path, h in payload_before.items())
        assert hashlib.sha256(original.read_bytes()).hexdigest() == original_hash
        report = dict(passed=len(results), original_and_localization_unchanged=True,
                      archive_sha256=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(), operations=results)
        (HERE / 'upgrade-validation.json').write_text(json.dumps(report, indent=2) + '\n')
        print(f'Passed {len(results)} offline installer operations; 96 localization files and original executable unchanged.')
    finally:
        if tmp.resolve().parent != parent or not tmp.name.startswith('安装 验证 '):
            raise RuntimeError('Fixture outside its intended directory')
        shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
