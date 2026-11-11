"""Consolidate frozen, user-tested v0.8.3 into a clean full Chinese bundle."""
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = ROOT/'outputs/Shank2-StoryCoop-v0.8.3-CHS'
BASE = ROOT/'outputs/Shank2-StoryCoop-v0.8.1-CHS-Test.zip'
OVERLAY = ROOT/'outputs/Shank2-StoryCoop-v0.8.3-Character-Test.zip'
EXPECTED_BASE = 'e6fb69880e0cecedfab9affc2f692d1815c811e47f62213263487625f9091673'
EXPECTED_OVERLAY = '07066f9d97344db47959944f59b026573bb3edc969613391037c23cf0af81efa'

README = '''# Shank 2 故事模式本地双人 v0.8.3 · 完整汉化整合包

包含故事双人 MOD、修复后的文字／字体汉化和 27 段中文字幕过场（增强对白、压低背景音乐）。无需再叠加旧升级包。

## 安装与升级

1. 完整解压。首次安装先运行“一键安装汉化.cmd”或 `Install-CHS.cmd`，选择 Shank 2 游戏目录。资源未安装时，仅打开双人启动器会被过场校验拦住。
2. 运行 `Launch-Coop.cmd`，选择同一游戏目录，设置角色、初始装备及输入方式，再保存并启动。游戏内进入 CAMPAIGN MODE。
3. 已使用 v0.8／v0.8.1／v0.8.2／v0.8.3 小升级包：解压本包到新的文件夹，选回原游戏目录即可；汉化资源相同，不需重装。若要保留启动器设置，可复制旧包 `patch/loadouts.json` 和 `patch/launcher-settings.json` 到新包同一位置。
4. 已装 v0.4／v0.5 旧汉化：先用旧包卸载汉化，再安装本包。不要删除游戏里的 `.storycoop-chs` 原件备份。

启动器首次默认英文，切换中文后记住。游戏分辨率、全屏等沿用原版保存设置，Win11 4K／150% 裁切已获用户确认解决。

## 双人功能

- 独立输入、血条、装备与投掷物。一人倒地可由队友救起，双方倒地才重试；地形死亡会移回存活队友附近等待救援。
- 暂停菜单中分别打开“1P 装备／2P 装备”，武器仅列战役已解锁项，进入关卡后可独立换武器。
- 角色栏对两人开放全部 17 个角色。选择在下一关或双方倒地重试时生效；同类保留武器，跨 Shank／Corina 类型改用新类型默认近战与远程，投掷物保持。游戏内选择在当前进程内保留；重启游戏仍采用启动器配装。
- 重试保留两人各自的分数，可继续累积。
- 双人镜头按距离平滑拉远；F7 可关闭／重开。F6 手动把 2P 召回 1P 附近，倒地召回后仍可救援。
- 增强过场对白并压低背景音乐；Jungle 和 Human Cargo 子弹时间后的虚焦清理已获用户确认。

键盘模式请开启 NumLock：1P WASD／空格，2P 方向键／小键盘0；轻攻击 J／小键盘1，装备近战 K／小键盘2，远程或互动 L／小键盘3，RT O／小键盘6。回车暂停／恢复及菜单确认。也支持两个 XInput 手柄。

## 已知限制与验证范围

**启动器配装会覆盖关卡开始前的配装选择；进入关卡后可以正常从暂停菜单切换。** 启动器有红字提示，该问题按用户要求保留。

角色切换、重试保分、救援、装备独立、实体手柄等已获用户实测确认。独眼巨人处决这次实测正常扣血（756→516）；原版处决扣一定血量，并非必杀，没有为此修改伤害。用户导入通关存档后 Steam 实际解锁全部成就，确认当前兼容版本同步有效；未单独验证每项正常游玩触发。

完整战役长期稳定性、所有自然跨关组合尚未全面验证。本包不包含诊断代码、测试无敌、游戏 EXE/DLL、用户存档或个人配置。原始 Steam EXE、Steam 接口和 Bink DLL 保留。

## 卸载与回退

关闭游戏，运行 `Remove-v08.cmd` 移除本系列 MOD 程序（为兼容旧版，命令名沿用 v08）；再运行“一键卸载汉化.cmd”或 `Remove-CHS.cmd` 恢复资源。只回退 MOD 时无需卸载汉化，移除本版 MOD 后从保留的旧补丁包重新生成即可。

仅支持 Steam 原版 `bin/shank2.exe` SHA256 `3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3`。本包只从本机原版重建，不分发完整游戏。汉化与字幕源自用户提供的 3DM 汉化包，原作者权利与署名保留。

English: extract the full bundle. For a first install, run Install-CHS.cmd before Launch-Coop.cmd. Existing v0.8+ localization does not need reinstalling. Both players may select any of 17 characters in the pause equipment menu; changes apply at the next level/retry. Retry keeps individual scores. F6 recalls P2; F7 toggles the shared camera. Use Remove-v08.cmd to remove the mod and Remove-CHS.cmd to restore localization. No test invincibility or personal files are included.
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    assert sha(BASE) == EXPECTED_BASE and sha(OVERLAY) == EXPECTED_OVERLAY
    assert not OUTPUT.exists(), 'Refusing to overwrite an existing release directory'
    OUTPUT.mkdir()
    for archive in (BASE, OVERLAY):
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for info in z.infolist():
                relative = Path(info.filename)
                assert not relative.is_absolute() and '..' not in relative.parts
                assert relative.name not in ('loadouts.json','launcher-settings.json','features.json')
                if info.is_dir() or relative.name.startswith('README-') or relative.name.endswith('SHA256SUMS.txt'):
                    continue
                target = OUTPUT/relative
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(z.read(info))
    (OUTPUT/'README.md').write_text(README,encoding='utf-8')
    patch = OUTPUT/'patch'
    for name in ('Launcher-Strings.ps1','Localization-Manager.ps1','Remove-Coop.ps1','Manage-Coop.ps1'):
        p = patch/name
        text = p.read_text(encoding='utf-8-sig').replace('v0.8.1','v0.8.3').replace('v0.8 ', 'v0.8.3 ')
        if name == 'Manage-Coop.ps1':
            text = text.replace("'. Restore the matching movie resources before launching.'",
                                "'. Run Install-CHS.cmd from the complete bundle for this game folder first / 请先用完整包安装对应游戏目录的汉化和增强过场。'")
        p.write_text(text,encoding='utf-8-sig')
    validation = json.loads((patch/'VALIDATION.json').read_text())
    validation.update(version='0.8.3-CHS', character_switch_user_confirmed=True,
                      retry_score_user_confirmed=dict(p1_before=65,p1_after=65,p2_before=160,p2_after=160),
                      high_dpi_user_confirmed='resolved by retaining native saved display settings',
                      steam_achievements_user_confirmed='unlocked after completed-save import; natural triggers not individually tested',
                      cyclops_test='native damage 240, HP756 to516; user confirmed no visual refill; damage unchanged',
                      includes_test_invincibility=False, includes_boss_probe=False,
                      bullet_time_blur_fix_remote_gameplay=True,
                      bullet_time_blur_status='user confirmed fixed on affected PC',
                      full_campaign_verified=False, exact_bundle_runtime_verified=False)
    (patch/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(f'Prepared clean release: {OUTPUT}')


def package():
    assert sha(BASE)==EXPECTED_BASE and sha(OVERLAY)==EXPECTED_OVERLAY
    validation_path=OUTPUT/'patch/VALIDATION.json'
    validation=json.loads(validation_path.read_text())
    checks=json.loads((HERE/'validation.json').read_text())
    assert all(checks[key] for key in ('four_variants_exact','no_godmode_or_probe',
                                      'restores_all_96_originals','launcher_smoke'))
    validation.update(bullet_time_blur_fix_remote_gameplay=True,
                      bullet_time_blur_status='user confirmed fixed on affected PC',
                      upgrade='v0.8+ localization unchanged; v0.4/v0.5 uninstall using old package before installing',
                      consolidated_bundle_installer_operations=checks['operations'],
                      consolidated_bundle_gui_operations=checks['gui_operations'],
                      consolidated_bundle_command_checks=len(checks['command_checks']),
                      consolidated_bundle_four_binaries_exact=checks['four_variants_exact'],
                      consolidated_bundle_launcher_smoke=checks['launcher_smoke'])
    validation_path.write_text(json.dumps(validation,indent=2)+'\n')
    files=sorted(p for p in OUTPUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    assert sum(p.suffix.lower()=='.bik' for p in files)==27
    assert not any(p.suffix.lower() in ('.exe','.dll') or p.name in ('loadouts.json','launcher-settings.json','features.json') for p in files)
    (OUTPUT/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(OUTPUT).as_posix()+'\n' for p in files),encoding='utf-8')
    archive=OUTPUT.with_name(OUTPUT.name+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(OUTPUT.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(OUTPUT).as_posix())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    report=dict(archive=str(archive),bytes=archive.stat().st_size,sha256=sha(archive),files=len(files)+1)
    (HERE/'release.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    import sys
    package() if '--archive' in sys.argv else prepare()
