"""Package the targeted HUD dispatch correction for the sealed v0.9.1 bundle."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

from test_dispatch import HERE, FIXED, ORIGINAL, PATCH_START, PATCH_END, pefile

OUTPUTS = HERE.parents[1] / 'outputs'
BASE = OUTPUTS / 'Shank2-StoryCoop-v0.9.1-CHS.zip'
BASE_SHA = '64a5e0a18dc0dc11261dcd2c856fbe316797cefa9725ed9efb3d93bf44672753'
ARCHIVE = OUTPUTS / 'Shank2-StoryCoop-v0.9.1-ComboFix.zip'
DEV = HERE.parent / 'story-coop-v20-prelevel-layout/dev'
README = '''# Shank 2 v0.9.1 连击显示修复

故事模式拾取投掷物时，原生 HUD 在处理拾取提示后误进入连击分支，会把手雷类型 ID 显示成 `-399534997`。本补丁只修复这条错误的跳转，拾取数量提示、真实连击和分数照常工作。

1. 退出游戏。把本包解压到**已解压的 v0.9.1 完整汉化整合包目录**，也就是能看到 `Launch-Coop.cmd` 的位置。合并 `patch` 文件夹并覆盖同名文件。不要解压到 Steam 游戏目录。
2. 用该目录里的 `Launch-Coop.cmd` 照常启动。启动器会重新生成修好的 MOD 程序，无需重新安装汉化。已安装的新版过场音量、角色配装和启动器设置继续使用。

键盘／手柄、中文／英文四个组合均通过隔离升级验证。原版分支在 x86 测试中复现了截图里的负数，修正后拾取提示、真实连击、归零和事件继续派发均通过。尚未在实际游戏关卡中重测。包中不含游戏程序、诊断、测试无敌或一击必杀。

回退：退出游戏，在当前修复版目录运行 `Remove-v08.cmd`，然后从重新解压的原 v0.9.1 包启动；无需卸载汉化。原 v0.9.1 ZIP 可保留作备份。
'''


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def make_members(bundle):
    content = {'README-连击修复.md': README.encode('utf-8')}
    previous = json.loads(bundle.read('patch/previous-baselines.json'))
    offsets = {}
    for mode in ('keyboard', 'pads'):
        for lang in ('en', 'chs'):
            name = f'patch/{mode}-{lang}-addon.json'
            recipe = json.loads(bundle.read(name))
            before = (DEV / f'{mode}-{lang}.exe').read_bytes()
            assert sha(before) == recipe['output_sha256']
            pe = pefile.PE(data=before)
            offset = pe.get_offset_from_rva(PATCH_START - 0x400000)
            end = pe.get_offset_from_rva(PATCH_END - 0x400000)
            assert before[offset:end] == ORIGINAL and end - offset == len(FIXED)
            assert end <= recipe['source_size']
            for patch in recipe['patches']:
                assert patch['offset'] >= end or patch['offset'] + len(bytes.fromhex(patch['after'])) <= offset
            recipe['patches'].append(dict(offset=offset, before=ORIGINAL.hex(), after=FIXED.hex()))
            recipe['patches'].sort(key=lambda patch: patch['offset'])
            previous[mode].append(recipe['output_sha256'])
            recipe['output_sha256'] = sha(before[:offset] + FIXED + before[end:])
            offsets[(mode, lang)] = offset
            content[name] = dump(recipe)
    content['patch/previous-baselines.json'] = dump(previous)
    checksum = {}
    for line in bundle.read('SHA256SUMS.txt').decode('utf-8-sig').splitlines():
        digest, path = line.split('  ', 1)
        checksum[path] = digest
    checksum.update({name: sha(data) for name, data in content.items()})
    content['SHA256SUMS.txt'] = ''.join(f'{digest}  {name}\n' for name, digest in sorted(checksum.items())).encode('utf-8')
    return content, offsets


def validate(bundle, content, offsets):
    powershell = Path(os.environ['WINDIR']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
    with tempfile.TemporaryDirectory(prefix='combo-update-', dir=HERE) as temp:
        scratch = Path(temp).resolve()
        assert scratch.parent == HERE
        old = scratch / 'base'
        bundle.extractall(old)
        new = scratch / 'fixed'
        shutil.copytree(old / 'patch', new)
        for name, data in content.items():
            if name.startswith('patch/'):
                (new / Path(name).name).write_bytes(data)
        game = scratch / '隔离游戏'
        shutil.copytree(HERE.parent / 'story-coop-v09-fixes/upgrade-fixture', game)
        manifest = json.loads(bundle.read('patch/manifest.json'))
        settings = HERE.parent / 'story-coop-v08-options/fixtures/settings.json'

        def run(folder, script, action, *args):
            result = subprocess.run([str(powershell), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                                     str(folder / script), '-Action', action, '-GamePath', str(game), *args],
                                    capture_output=True, text=True, errors='replace', timeout=120)
            assert result.returncode == 0, (action, result.stdout, result.stderr)

        def localize(action, group):
            run(old / 'patch', 'Coop-Localization.ps1', action, '-Group', group, '-NoUI')

        cases = []
        localize('Install', 'Movies')
        for lang in ('en', 'chs'):
            if lang == 'chs':
                localize('Install', 'Text')
            receipt_path = game / '.storycoop-chs/state.json'
            receipt = receipt_path.read_bytes()
            for mode in ('keyboard', 'pads'):
                args = ('-InputMode', mode, '-LoadoutPath', str(settings))
                exe = game / 'bin' / f'shank2-coop-v08-{mode}.exe'
                run(old / 'patch', 'Manage-Coop.ps1', 'Install', *args)
                before = exe.read_bytes()
                run(new, 'Manage-Coop.ps1', 'Install', *args)
                offset = offsets[(mode, lang)]
                assert before[offset:offset+len(ORIGINAL)] == ORIGINAL
                assert exe.read_bytes() == before[:offset] + FIXED + before[offset+len(ORIGINAL):]
                run(new, 'Manage-Coop.ps1', 'Verify', *args)
                run(new, 'Manage-Coop.ps1', 'Remove', *args)
                run(old / 'patch', 'Manage-Coop.ps1', 'Install', *args)
                assert exe.read_bytes() == before
                run(old / 'patch', 'Manage-Coop.ps1', 'Remove', *args)
                cases.append(f'{mode}-{lang}')
            assert receipt_path.read_bytes() == receipt
        localize('Verify', 'All')
        assert all(sha((game / item['path']).read_bytes()) == item['sha256'] for item in manifest['files'])
        assert all(sha((game / path).read_bytes()) == digest for path, digest in manifest['guards'].items())
    return cases


def main():
    assert not ARCHIVE.exists() and sha(BASE.read_bytes()) == BASE_SHA
    with zipfile.ZipFile(BASE) as bundle:
        content, offsets = make_members(bundle)
        cases = validate(bundle, content, offsets)
    with zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(content.items()):
            archive.writestr(name, data)
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        assert {name: archive.read(name) for name in archive.namelist()} == content
    report = dict(archive=str(ARCHIVE), size=ARCHIVE.stat().st_size, sha256=sha(ARCHIVE.read_bytes()),
                  modes_upgraded_verified_rolled_back=cases, original_game_files_unchanged=True,
                  localization_and_movies_unchanged=True, gameplay_verified=False)
    (HERE / 'release.json').write_bytes(dump(report))
    print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
