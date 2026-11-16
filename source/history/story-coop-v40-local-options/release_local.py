"""Finalize only the local HUD and mixed-input changes for v0.10.7."""

import argparse
import json
from pathlib import Path

from build_options import BASELINES, create, load_build, sha

VERSION = '0.10.7'

EN = '''## Co-op controls and health bars

Open `Coop-Key-Settings.cmd` in the installed game folder. Select **1P keyboard / mouse + 2P controller** to use the keyboard and mouse for player 1 and the first connected XInput controller for player 2. Choose **Restore defaults** in that mode to set left click to light attack and right click to ranged attack / interact; you can also rebind them individually. Shared keyboard and two controllers are still supported.

Choose **Side by side** (the default) or **Stacked** under **HUD layout**. In Side by side, player 2's status sits just to the right of player 1, leaving room for the boss bar. Save and restart the game to apply changes.
'''

CHS = '''## 双人键位与血条布局

运行游戏目录中的 `Coop-Key-Settings.cmd`。选择「1P 键鼠 + 2P 手柄」后，1P 使用键盘和鼠标，2P 使用第一个可用的 XInput 手柄。该模式下点「恢复默认」可将鼠标左键设为轻攻击、右键设为远程攻击／互动，也可以单独改绑。共用键盘和双手柄仍可用。

在「血条布局」中选择「左右并排」（默认）或「上下排列」。并排时，2P 状态栏位于 1P 右侧，为 Boss 血条留出空间。保存后重启游戏生效。
'''


def stage(lang, source, destination):
    files = create((source/'bin/shank2.exe').read_bytes(), lang)
    manifest = json.loads(files['patch/manifest.json'])
    previous = manifest['version']
    manifest['version'] = VERSION
    if lang == 'en':
        manifest['display_name'] = 'Campaign Co-op MOD (Original Game)'
    files['patch/manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
    files['patch/VALIDATION.json'] = (json.dumps(dict(
        version=VERSION, base_release=previous, online_campaign=False,
        scope='Local campaign: selectable health bar layout and keyboard/mouse plus controller',
    ),indent=2)+'\n').encode()
    readme = 'README.md' if lang == 'en' else '说明.md'
    readme_text = files[readme].decode('utf-8-sig').replace(previous, VERSION)
    files[readme] = (readme_text.rstrip()+'\n\n'+(EN if lang=='en' else CHS)).encode()
    del files['patch/SHA256SUMS.txt']
    files['patch/SHA256SUMS.txt'] = ''.join(
        f'{sha(data)}  {path}\n' for path,data in sorted(files.items())).encode()
    builder=load_build()
    builder.verify_game(source,manifest,json.loads(files['patch/exe-recipe.json']))
    name = f'Shank2-v{VERSION}-MOD'+('-CHS' if lang=='chs' else '')
    builder.package(destination, name, files)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lang', choices=BASELINES, required=True)
    p.add_argument('--game-dir', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a=p.parse_args()
    stage(a.lang,a.game_dir,a.out)
