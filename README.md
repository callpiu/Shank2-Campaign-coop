# Shank 2 Campaign Co-op

Play the campaign locally with two players on the same screen. The mod adds a **Local Co-op** entry under Campaign Mode while retaining the single-player and Survival menus. It supports two XInput controllers or a shared keyboard.

## Downloads

Download one package from the [unified latest release](https://github.com/callpiu/Shank2-Campaign-coop/releases/latest). The three packages retain their own version numbers.

| Package | Contents |
| --- | --- |
| `Shank2-v0.10.4-MOD.zip` | Campaign co-op MOD for the original game, without Chinese localization |
| `Shank2-v0.10.3-CHS.zip` | Simplified Chinese localization and optimized cutscenes, without the co-op mod |
| `Shank2-v0.10.5-MOD-CHS.zip` | Co-op mod and optimized Simplified Chinese localization; includes the checkpoint retry fix |

## Features

- Separate controls, health, equipment, consumables and scores for each player.
- Choose characters and unlocked weapons for both players before campaign levels; change equipment from the pause menu.
- All 17 characters available, with applicable Survival health and damage traits shown on the selection screen.
- Revive either player; retry when both are down. Scores are retained on retry, and terrain deaths bring the downed player near their teammate.
- In v0.10.4, choose **Restart Checkpoint** from the pause menu, or confirm a different character to restart the checkpoint and apply the change immediately. Throwables refill on retry and when starting a new level.
- Shared camera with smooth zoom; F6 recalls player 2 and F7 toggles the shared camera.
- The Chinese packages include localized cutscenes with enhanced dialogue and reduced background music.

## Installation

1. Install the Steam version of Shank 2 and exit the game.
2. Extract one complete package, keeping its `patch` folder next to the installer.
3. Run `Install.cmd` (or `安装.cmd` in the Chinese packages), choose the game folder containing `bin` and `data-pc`, and select Install. The manager also offers verification and removal.
4. Start the game normally through Steam. With either co-op package, choose **Campaign Mode → Local Co-op**.

To switch package types, uninstall the installed package first. Keep the `.shank2-patch` backup in the game folder. The installer checks the original executable and reconstructs the modified version from your own game; it does not include the full game executable or Steam DLLs. Windows PowerShell 5.1 is required.

## Controls

Run `Coop-Key-Settings.cmd` in the game folder to change bindings; restart the game to apply changes. The default shared-keyboard layout uses WASD / arrow keys to move, Space / Numpad 0 to jump, J / Numpad 1 for light attack, K / Numpad 2 for heavy weapon, L / Numpad 3 for ranged attack, O / Numpad 6 for grapple, and Z / C or Numpad 8 / 9 to dodge left / right. Enable NumLock for player 2. Enter pauses or resumes.

## Source code

The [source directory](source/) contains the shipped installer, patch recipe and UI resources for the original-game MOD, plus the gameplay, interface, tools and packaging scripts used throughout development. See [source/README.md](source/README.md) for the layout and build limitations.

## Build the MOD for the original game

From the repository root, run this with Python 3.12 and a supported, unmodified Steam installation or copy:

```powershell
py -3.12 build.py --game-dir 'C:\SteamLibrary\steamapps\common\Shank 2'
```

The build verifies the Steam files, reconstructs the patched executable in memory and checks its SHA-256. It writes the release directory and `Shank2-v0.10.4-MOD.zip` to `dist/`, without changing the game directory. Use `--out` to choose a new output directory for subsequent builds. No previous release ZIP or extra Python packages are required.

To package the committed inputs without verifying a game copy, run `py -3.12 build.py --package-only`. With the same Python and zlib versions, repeat builds produce identical ZIP bytes. See [source/README.md](source/README.md) for the build inputs and scope.

## Notes

The original Steam executable supported by the installer has SHA-256 `3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3`. Many features have been tested in play, but complete campaign and character coverage is not yet verified. Steam integration is retained; achievements are not bypassed.

The Chinese localization and cutscene subtitles are based on the 3DM patches supplied for this project. Cutscene audio was processed using TIGER-DnR source separation; results vary by scene.

---

# Shank 2 战役双人合作 MOD

在同一屏幕上双人游玩战役。MOD 在战役菜单中增加「本地双人」入口，保留单人战役和生存模式，支持两个 XInput 手柄或共用键盘。

## 下载

从[统一下载页](https://github.com/callpiu/Shank2-Campaign-coop/releases/latest)选择一个包下载。三个包各自保留原来的版本号。

| 文件 | 内容 |
| --- | --- |
| `Shank2-v0.10.4-MOD.zip` | 原版战役双人 MOD，不含汉化 |
| `Shank2-v0.10.3-CHS.zip` | 优化后的简体中文汉化及过场，不含双人 MOD |
| `Shank2-v0.10.5-MOD-CHS.zip` | 双人 MOD 与优化汉化整合包，已修复汉化下的检查点重试 |

## 功能

- 两人拥有独立操作、血量、装备、消耗品和分数。
- 每关开始前分别选择角色及已解锁武器，关卡中可从暂停菜单更换装备。
- 开放 17 名角色，并在选人界面显示适用的生存模式生命和伤害属性。
- 双方均可救援队友，双方倒地后进入重试；重试保留分数，地形击倒会将角色送回队友附近。
- v0.10.4 可从暂停菜单选择 **Restart Checkpoint（从检查点重试）**。确认换成不同角色也会自动重试当前检查点，让新角色立即生效。重试和进入新关卡时会补满投掷物。
- 双人镜头平滑缩放；F6 召回 2P，F7 切换双人镜头。
- 汉化包包含中文字幕过场，对白经过增强，背景音乐经过压低。

## 安装

1. 安装 Steam 版 Shank 2，退出游戏。
2. 完整解压一个发行包，保持 `patch` 文件夹与安装脚本在一起。
3. 运行 `安装.cmd`，选择包含 `bin` 和 `data-pc` 的游戏目录，在管理器中选择安装；管理器也提供校验和卸载。
4. 从 Steam 正常启动游戏；安装双人 MOD 或整合包后，选择「战役模式 → 本地双人」。

切换不同类型的包前，请先卸载当前包。保留游戏目录下的 `.shank2-patch` 备份。安装器会校验并基于用户自己的游戏文件重建程序，不包含完整游戏 EXE 或 Steam DLL；需要 Windows PowerShell 5.1。

## 按键

运行游戏目录中的 `Coop-Key-Settings.cmd` 可修改键位，重启游戏后生效。默认共用键盘：1P 使用 WASD 移动，2P 使用方向键；跳跃分别为空格和小键盘 0，轻攻击为 J 和小键盘 1，重武器为 K 和小键盘 2，远程攻击为 L 和小键盘 3，抓取为 O 和小键盘 6，左右闪避为 Z／C 和小键盘 8／9。2P 请开启 NumLock。回车暂停或恢复。

## 源码

[源码目录](source/)包含原版 MOD 发行包的安装器、补丁配方和界面资源，以及开发过程中使用的玩法、界面、工具和打包脚本。目录结构和构建限制见 [源码说明](source/README.md)。

## 构建原版 MOD

在仓库根目录执行以下命令。需要 Python 3.12 和受支持、未修改的 Steam 游戏目录或副本：

```powershell
py -3.12 build.py --game-dir 'C:\SteamLibrary\steamapps\common\Shank 2'
```

构建脚本会校验 Steam 文件，在内存中重建补丁程序并核对 SHA-256，再将发行目录和 `Shank2-v0.10.4-MOD.zip` 写入 `dist/`，不会修改游戏目录。重复构建时可用 `--out` 指定新的输出目录。无需旧版 ZIP 或额外的 Python 包。

只打包、不核对原版游戏时，可执行 `py -3.12 build.py --package-only`。使用相同的 Python 和 zlib 版本，重复构建的 ZIP 字节一致。构建输入和范围见[源码说明](source/README.md)。

## 说明

支持的 Steam 原版程序 SHA-256 为 `3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3`。多项功能已经实机测试，全部关卡和角色的完整覆盖仍待验证。MOD 保留 Steam 接口，不绕过成就条件。

中文文本和过场字幕基于本项目使用的 3DM 汉化补丁。过场音频使用 TIGER-DnR 分离并重混，实际效果因场景而异。
