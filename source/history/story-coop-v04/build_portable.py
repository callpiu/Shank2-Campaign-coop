"""Build a clean, path-independent end-user package from authored scripts/recipes."""
from pathlib import Path
import hashlib,json,zipfile

here=Path(__file__).resolve().parent
output=here.parents[1]/'outputs/Shank2-StoryCoop-v0.4-Portable'
recipes=here.parents[1]/'outputs/Shank2-StoryCoop-v0.4'
output.mkdir(exist_ok=True)
runtime=['Coop-Launcher.ps1','Manage-Coop.ps1','Portraits.ps1','Launcher-Strings.ps1',
         'Launcher-Preferences.ps1','Game-Paths.ps1','Start-Coop.ps1','Remove-Coop.ps1']
for name in runtime:(output/name).write_text((here/name).read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
for name in ['catalog.json','keyboard-recipe.json','pads-recipe.json','ui-recipe.json']:
    (output/name).write_bytes((recipes/name).read_bytes())
cmd_prefix=('\r\n'.join(['@echo off','setlocal',r'set "coopPs=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"',
    'if not exist "%coopPs%" (','  echo Windows PowerShell 5.1 is required.','  pause','  exit /b 1',')'])+'\r\n').encode('ascii')
(output/'Launch-Coop.cmd').write_bytes(cmd_prefix+b'start "" /b "%coopPs%" -NoProfile -STA -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0Start-Coop.ps1"\r\n')
(output/'Remove-v04.cmd').write_bytes(cmd_prefix+b'"%coopPs%" -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0Remove-Coop.ps1"\r\n')
(output/'README.md').write_text('''# Shank 2 Story Co-op v0.4 — Portable Mod

## Quick start

1. Install the Steam version of Shank 2 and make sure the original game starts normally. Keep Steam running.
2. Extract the **entire ZIP** into a writable folder. Do not run files from inside the ZIP.
3. Double-click **Launch-Coop.cmd**. The launcher searches your saved location and Steam libraries. If needed, click **Browse** and select the game folder containing `bin` and `data-pc`.
4. Choose each player's character and weapons, then click **Save and launch**. Select **CAMPAIGN MODE** in the game.

The first launch uses English. Select 简体中文 in the Language menu to switch; your choice is saved automatically for next time. Character portraits are read from your own installed game. Default loadouts are Shank and Corina, using a shared keyboard.

## Requirements and compatibility

- Windows with Windows PowerShell **5.1**, .NET Framework/System.Drawing and the game's normal prerequisites. Tested on the developer's Windows PC; no second physical PC has been tested.
- Your own compatible Steam game installation. Supported original `bin/shank2.exe` SHA256: `3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3`.
- The installer checks the EXE and original UI automatically. Other builds or modified original files are rejected before writing mod files.
- Python, Codex and the developer's project folders are **not required to run this package**. No game executable, textures, save files or personal settings are included.

The mod uses your existing in-game resolution, fullscreen/windowed, graphics and audio settings. It does not force a display mode or rewrite `users/graphics.ini`.

## Controls

Enable NumLock for Player 2's numeric keypad.

| Input | Player 1 | Player 2 |
|---|---|---|
| Move | WASD | Arrow keys |
| Jump | Space | Numpad 0 |
| Light melee | J | Numpad 1 |
| Equipped melee | K | Numpad 2 |
| Ranged / contextual interaction | L | Numpad 3 |
| RB / LB | U / I | Numpad 4 / 5 |
| LT / RT | Q / O | Numpad 7 / 6 |
| Pause | Enter | Enter |
| Recall Player 2 | F6 | F6 |

A downed player can be revived by the living teammate. Retry starts when both players are down. Use the interaction prompt near your teammate for normal revival. F6 recalls Player 2's position; full revival-effect cleanup via F6 has not been verified. Two XInput controllers are also selectable; that mode has not been tested with two physical controllers.

## Remove or move

Close the mod game, then double-click **Remove-v04.cmd**. It uses your saved game location or asks you to choose it. Only recognized v0.4 mod files are removed. Original game files and older mod programs remain. The shared UI stays when v0.3 still needs it.

Settings are stored beside the launcher (`loadouts.json` and `launcher-settings.json`) on the recipient's own computer. To share the mod, send this clean ZIP rather than a folder containing your personal settings.

## Prototype limits

The first story level, two-way revival, both-down retry and independent melee/ranged attacks have been tested by the original user. Full-story progression, checkpoints, all outfits in combat and long-session stability need more testing. Normal play can update Steam save progress. This is local co-op; it does not add online play.

---

## 中文说明

1. 对方需要自行安装**兼容版本的 Steam 原版 Shank 2**，先确认原版能正常启动，并保持 Steam 运行。
2. **完整解压 ZIP** 到可写文件夹，不能直接在压缩包内运行。
3. 双击 **Launch-Coop.cmd**。启动器会查找对方电脑的 Steam 库；未找到时点 **Browse／浏览**，选择含 `bin` 和 `data-pc` 的游戏目录。
4. 选择两人的角色、装备和输入方式，点 **Save and launch／保存并启动**，游戏里进入 **CAMPAIGN MODE**。

游戏分辨率、全屏／窗口、画质和音量沿用用户已有设置，不强制显示模式或重写 `users/graphics.ini`。

首次默认英文，右上角可切换简体中文，并立即记住语言。角色头像从对方本机游戏读取。无需安装 Python 或 Codex，也不依赖作者的盘符或项目目录。包内不含游戏本体、图片、存档或作者的个人设置。

单人倒地可由伙伴互动救起，双方倒地才重试；F6 手动召回2P。默认共用键盘，2P需要独立数字小键盘并开启NumLock。按键见上表。双实体手柄、全故事流程和长期稳定性仍未完成实测。

移除时先关闭游戏，再双击 **Remove-v04.cmd**；会使用这台电脑保存的游戏路径，必要时让使用者选择目录。原版与旧版程序保留。此包只支持上述原版EXE哈希，不匹配的版本会拒绝安装。\n''',encoding='utf-8')
def archive():
    # Whitelist distribution files; never include saved paths, language prefs or logs.
    names=runtime+['catalog.json','keyboard-recipe.json','pads-recipe.json','ui-recipe.json',
                   'Launch-Coop.cmd','Remove-v04.cmd','README.md']
    if (output/'PORTABLE-VALIDATION.json').exists():names.append('PORTABLE-VALIDATION.json')
    sums=''.join(hashlib.sha256((output/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in sorted(names))
    (output/'SHA256SUMS.txt').write_text(sums,encoding='ascii');names.append('SHA256SUMS.txt')
    target=output.parent/(output.name+'.zip')
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:z.write(output/name,Path(output.name)/name)
    with zipfile.ZipFile(target) as z:assert z.testzip() is None and len(z.infolist())==len(names)
    return {'zip':str(target),'files':len(names),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
if __name__=='__main__':print(json.dumps(archive(),indent=2))
