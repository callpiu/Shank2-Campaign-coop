# Source and build notes

This directory contains the development source and release patch data for Shank 2 Campaign Co-op v0.10.4.

- `release-v0.10.4-mod/patch/`: the installer, controls scripts, executable patch recipe, install manifest, and patched UI resources for the original-game MOD.
- `package-inputs/MOD/`: the public install and uninstall commands and the package readme. The builder combines these with the manifest-selected patch files and regenerates `patch/SHA256SUMS.txt`.
- `history/story-coop-prototype/` and `history/story-coop-v02` through `story-coop-v37-simple-packages/`: development builders, native hook and interface work, packaging scripts, and tests, preserved by milestone. Later milestones build on earlier work; this is not one independent project per directory.
- `story-coop-v27-traits/build_traits.py`, `story-coop-v28-trait-descriptions/build_descriptions.py`, `story-coop-v33-dodge/build_dodge.py`, and `story-coop-v34-release/build_release.py` cover recent gameplay, selection UI, dodge and release work. v35–v37 contain later English layout, control shortcut and package changes.

## What the build reproduces

[The root build command](../README.md#build-the-mod-for-the-original-game) reconstructs the MOD executable from the committed patch recipe and a supported Steam copy, then packages the verified runtime inputs. The recipe and UI files are the build inputs; regenerating them from the historical gameplay and UI generators is a separate task. Some of those scripts still depend on old paths, intermediate files and local tools. The Chinese localization and combined packages are outside the new build's scope.

Reference build: Python 3.12.10 with zlib 1.3.1 produced ZIP SHA-256 `643c68d1374d11aca75b4c915146ad2193aa6d816d30b65a8cd86a27c8830ed7`. The release was built using this workflow: `Shank2-v0.10.4-MOD.zip`. The build contains no Steam EXE, DLLs, saves, or gameplay test assists.

To install the tested release, use the [release packages](https://github.com/callpiu/Shank2-Campaign-coop/releases/tag/v0.10.4), which reconstruct the executable from a supported Steam installation.

---

# 源码与构建说明

本目录包含 Shank 2 战役双人 MOD v0.10.4 的开发源码及发行版补丁数据。

- `release-v0.10.4-mod/patch/`：原版 MOD 的安装器、键位设置脚本、程序补丁配方、安装清单及界面资源。
- `package-inputs/MOD/`：安装、卸载入口及包内说明。构建脚本将其与清单指定的补丁文件一起打包，并重新生成 `patch/SHA256SUMS.txt`。
- `history/story-coop-prototype/` 和 `history/story-coop-v02` 至 `story-coop-v37-simple-packages/`：按里程碑保存的玩法、原生补丁、界面、打包脚本与测试。后续版本基于早期工作，并非彼此独立的项目。
- v27 属性、v28 选人说明、v33 闪避和 v34 发行包目录中分别保存了对应构建脚本；v35 至 v37 包含英文布局、键位入口及打包更新。

## 构建可复现的范围

[仓库根目录的构建命令](../README.md#构建原版-mod)使用已提交的补丁配方和受支持的 Steam 副本重建原版 MOD 程序，再打包校验过的运行资源。补丁配方和界面文件是本流程的输入；从历史玩法和界面生成器重新生成这些文件是另一项工作，部分旧脚本仍依赖原机器路径、中间产物和本地工具。汉化包和整合包不在这次构建范围内。

参考环境为 Python 3.12.10 和 zlib 1.3.1，输出 ZIP 的 SHA-256 为 `643c68d1374d11aca75b4c915146ad2193aa6d816d30b65a8cd86a27c8830ed7`。发行包使用此流程生成。包内不含 Steam 原版 EXE、DLL、存档或玩法测试辅助。

需要安装已测试版本时，请使用 [发行包](https://github.com/callpiu/Shank2-Campaign-coop/releases/tag/v0.10.4)，安装器会根据受支持的 Steam 版游戏重建程序。
