"""Create a small overlay for the existing v0.8.1 package; never launch the game."""
import base64
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
OUTPUTS = HERE.parents[1] / 'outputs'
BASE = OUTPUTS / 'Shank2-StoryCoop-v0.8.1-CHS-Test' / 'patch'
ARCHIVE = OUTPUTS / 'Shank2-StoryCoop-v0.8.2-RetryScore-Test.zip'
README = '''# Shank 2 故事双人 v0.8.2 分数保留测试版

双方倒地后选「重试」，1P 和 2P 会各自保留倒地前的分数，并从各自的分数继续累积。
退出关卡、另开关卡、生存模式仍沿用原有计分规则。这个升级包不含汉化资源或游戏程序。

1. 准备一份已解压的 **v0.8.1 完整汉化补丁包**。建议复制整份补丁文件夹做测试，保留原包。
2. 把本 ZIP 的内容解压到该测试补丁文件夹（能看到 `Launch-Coop.cmd` 的位置），覆盖其中的 `patch` 配方。不要解压到游戏目录，不需要重装汉化。
3. 想测时再用原有启动器。两位玩家分别拿到不同分数，然后双方倒地选「重试」，检查分数是否分别保留；再拿分重试一次，检查是否继续累积。

12 项离线原生用例通过，实际游戏内重试尚待验证。解压本 ZIP 不会启动 Steam 或游戏。
要退回 v0.8.1，请先用测试补丁文件夹里的 `Remove-v08.cmd` 移除测试程序，再从原 v0.8.1 补丁包重新生成。不需要卸载汉化。
'''


def changes(before, after):
    assert len(before) <= len(after)
    pos = 0
    while pos < len(before):
        if before[pos] == after[pos]:
            pos += 1
            continue
        start = pos
        while pos < len(before) and before[pos] != after[pos]:
            pos += 1
        yield dict(offset=start, before=before[start:pos].hex(), after=after[start:pos].hex())


def members():
    dump = lambda value: (json.dumps(value, indent=2) + '\n').encode()
    content = {'README-分数保留测试版.md': README.encode()}
    previous = json.loads((BASE / 'previous-baselines.json').read_text())
    for mode in ('keyboard', 'pads'):
        for lang in ('en', 'chs'):
            name = f'{mode}-{lang}-addon.json'
            recipe = json.loads((BASE / name).read_text())
            previous[mode].append(recipe['output_sha256'])
            suffix = '-chs' if lang == 'chs' else ''
            base = (HERE.parent / 'story-coop-v05/final' / f'shank2-coop-v05-{mode}{suffix}.exe').read_bytes()
            assert len(base) == recipe['source_size']
            assert hashlib.sha256(base).hexdigest() == recipe['input_sha256']
            rebuilt = bytearray(base)
            for p in recipe['patches']:
                a = bytes.fromhex(p['before'])
                i = p['offset']
                assert rebuilt[i:i+len(a)] == a
                rebuilt[i:i+len(a)] = bytes.fromhex(p['after'])
            rebuilt.extend(base64.b64decode(recipe['append']))
            assert hashlib.sha256(rebuilt).hexdigest() == recipe['output_sha256']
            target = (HERE / 'dev' / f'{mode}-{lang}.exe').read_bytes()
            recipe.update(output_sha256=hashlib.sha256(target).hexdigest(), target_size=len(target),
                          patches=list(changes(base, target)), append=base64.b64encode(target[len(base):]).decode())
            content['patch/' + name] = dump(recipe)
    content['patch/previous-baselines.json'] = dump(previous)
    return content


def package():
    content = members()
    with zipfile.ZipFile(ARCHIVE, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(content.items()):
            z.writestr(name, data)
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None
        assert {name: z.read(name) for name in z.namelist()} == content
    print(f'{ARCHIVE}: {ARCHIVE.stat().st_size} bytes, {len(content)} files')


if __name__ == '__main__':
    package()
