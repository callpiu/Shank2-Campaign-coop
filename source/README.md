# Source and build notes

This directory contains the development source and release patch data for Shank 2 Campaign Co-op v0.10.3.

- `release-v0.10.3-mod/patch/`: the actual English MOD release's installer and controls PowerShell scripts, executable patch recipe, manifests, and patched UI resources. These files match the published MOD archive.
- `history/story-coop-prototype/` and `history/story-coop-v02` through `story-coop-v37-simple-packages/`: development builders, native hook and interface work, packaging scripts, and tests, preserved by milestone. Later milestones build on earlier work; this is not one independent project per directory.
- `story-coop-v27-traits/build_traits.py`, `story-coop-v28-trait-descriptions/build_descriptions.py`, `story-coop-v33-dodge/build_dodge.py`, and `story-coop-v34-release/build_release.py` cover recent gameplay, selection UI, dodge and release work. v35–v37 contain later English layout, control shortcut and package changes.

## Build limitations

These are historical development scripts, not a self-contained one-command build. Some contain paths specific to the development machine, depend on earlier intermediate archives or local tools, or expect an original game executable and resources. Generated intermediates, original game files, commercial movies and fonts, personal settings, saves, crash dumps and test executables are not included in this source tree. Some historical diagnostic scripts attach to or modify running processes; review them before use. Temporary invincibility and one-hit test helpers are not included in the released MOD.

To install the tested release, use the [release packages](https://github.com/callpiu/Shank2-Campaign-coop/releases/tag/v0.10.3), which reconstruct the executable from a supported Steam installation.

---

# 源码与构建说明

本目录包含 Shank 2 战役双人 MOD v0.10.3 的开发源码及发行版补丁数据。

- `release-v0.10.3-mod/patch/`：英文 MOD 发行包实际使用的安装器、键位设置脚本、程序补丁配方、清单及界面资源，与发布包一致。
- `history/story-coop-prototype/` 和 `history/story-coop-v02` 至 `story-coop-v37-simple-packages/`：按里程碑保存的玩法、原生补丁、界面、打包脚本与测试。后续版本基于早期工作，并非彼此独立的项目。
- v27 属性、v28 选人说明、v33 闪避和 v34 发行包目录中分别保存了对应构建脚本；v35 至 v37 包含英文布局、键位入口及打包更新。

## 构建限制

这些是历史开发脚本，并非可以直接一键构建的完整工程。部分脚本包含开发机器路径，依赖早期中间包、本地工具或用户自备的原版游戏程序和资源。本源码目录不包含生成的中间产物、原版游戏文件、商业过场视频与字体、个人设置、存档、崩溃转储及测试程序。部分历史诊断脚本会连接或修改运行中的进程，使用前请先阅读。正式 MOD 不包含临时无敌或一击必杀测试辅助。

需要安装已测试版本时，请使用 [发行包](https://github.com/callpiu/Shank2-Campaign-coop/releases/tag/v0.10.3)，安装器会根据受支持的 Steam 版游戏重建程序。
