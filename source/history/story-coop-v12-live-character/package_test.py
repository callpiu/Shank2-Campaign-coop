"""Build a reversible small character-test overlay, based on the frozen score ZIP."""
import base64
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'outputs'
PREVIOUS = OUT / 'Shank2-StoryCoop-v0.8.2-RetryScore-Test.zip'
NEW = OUT / 'Shank2-StoryCoop-v0.8.3-Character-Test.zip'
README = '''# Shank 2 v0.8.3 双人角色选择测试版

暂停后打开「1P 装备」或「2P 装备」，在原生角色栏里选角色并确认。双人战役中两位玩家各自都可选全部 17 个角色。
选择会在进入下一关或双方倒地后选择「重试」时生效。换人不会自动重开关卡。同类角色保留武器，跨到另一类角色时，近战和远程换为新角色的默认武器。投掷物保留，武器仍按战役进度解锁。
v0.8.2 的双方重试保分仍包含在内。

将本 ZIP 解压覆盖到已使用的 v0.8.2 补丁包文件夹（有 `Launch-Coop.cmd` 的位置），不要解压到游戏 `bin`。已安装完整汉化与增强过场的电脑不需要重装；首次使用须从完整包运行 `Install-CHS.cmd`。

游戏内验证待做：暂停菜单为 1P 选 Corina 类角色、为 2P 选 Shank 类角色；确认两人的当前角色没有被替换。让两人各拿分后倒地重试，观察两人是否分别换成所选角色、装备可用且分数保留。另测自然进入下一关。请不要在仍有 Steam 登录问题时使用在线会话做测试。

回退：用本测试包文件夹里的 `Remove-v08.cmd` 先移除测试程序，再从保留的 v0.8.2 补丁包重新生成。不需要卸载汉化。解压本 ZIP 不会启动 Steam 或游戏。
'''


def recipe_for(old, baseline, target):
    assert hashlib.sha256(baseline).hexdigest() == old['input_sha256']
    old_image = bytearray(baseline)
    for p in old['patches']:
        a, b = bytes.fromhex(p['before']), bytes.fromhex(p['after'])
        i = p['offset']
        assert old_image[i:i+len(a)] == a
        old_image[i:i+len(a)] = b
    old_image.extend(base64.b64decode(old['append']))
    assert hashlib.sha256(old_image).hexdigest() == old['output_sha256']
    changes = []
    i = 0
    while i < len(baseline):
        if baseline[i] == target[i]:
            i += 1
            continue
        start = i
        while i < len(baseline) and baseline[i] != target[i]:
            i += 1
        changes.append(dict(offset=start, before=baseline[start:i].hex(), after=target[start:i].hex()))
    return {**old, 'patches': changes, 'append': base64.b64encode(target[len(baseline):]).decode(),
            'output_sha256': hashlib.sha256(target).hexdigest(), 'target_size': len(target)}


def main():
    dump = lambda value: (json.dumps(value, indent=2)+'\n').encode()
    content = {'README-角色选择测试版.md': README.encode()}
    builds = {row['name']: row for row in json.loads((HERE/'builds.json').read_text())}
    with zipfile.ZipFile(PREVIOUS) as z:
        previous = json.loads(z.read('patch/previous-baselines.json'))
        for mode in ('keyboard', 'pads'):
            for lang in ('en', 'chs'):
                variant = f'{mode}-{lang}'
                name = f'patch/{variant}-addon.json'
                old = json.loads(z.read(name))
                previous[mode].append(old['output_sha256'])
                assert old['output_sha256'] == builds[variant+'.exe']['baseline_sha256']
                suffix = '-chs' if lang == 'chs' else ''
                baseline = (HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{suffix}.exe').read_bytes()
                target = (HERE/'dev'/f'{variant}.exe').read_bytes()
                recipe = recipe_for(old, baseline, target)
                assert recipe['output_sha256'] == builds[variant+'.exe']['sha256']
                content[name] = dump(recipe)
    content['patch/previous-baselines.json'] = dump(previous)
    with zipfile.ZipFile(NEW, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(content.items()):
            z.writestr(name, data)
    with zipfile.ZipFile(NEW) as z:
        assert z.testzip() is None
        assert {n: z.read(n) for n in z.namelist()} == content
    print(f'{NEW}: {NEW.stat().st_size} bytes; {len(content)} files; {hashlib.sha256(NEW.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    main()
