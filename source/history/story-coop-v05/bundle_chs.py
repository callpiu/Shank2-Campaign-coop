"""Bundle tested v0.5 recipes with the immutable repaired Chinese payload."""
from pathlib import Path
import shutil,json,hashlib,zipfile,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
MOD=ROOT/'outputs/Shank2-StoryCoop-v0.5-Test'
CHS=ROOT/'outputs/Shank2-StoryCoop-v0.4-CHS'
OUT=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def prepare():
    runtime=OUT/'patch';runtime.mkdir(parents=True,exist_ok=True)
    # Only authored runtime files; never copy user settings from a played folder.
    for name in ['Coop-Launcher.ps1','Manage-Coop.ps1','Portraits.ps1','Launcher-Strings.ps1','Launcher-Preferences.ps1','Game-Paths.ps1','Start-Coop.ps1','Remove-Coop.ps1','catalog.json','keyboard-recipe.json','pads-recipe.json','keyboard-chs-recipe.json','pads-chs-recipe.json','ui-recipe.json','ui-chs-recipe.json','pause-en-recipe.json','pause-chs-recipe.json','equip-en-recipe.json','equip-chs-recipe.json']:
        shutil.copy2(MOD/name,runtime/name)
    text=(HERE.parent/'chs-compat/Coop-Localization.ps1').read_text(encoding='utf-8-sig')
    assert text.count('patch\\manifest.json')==1 and text.count('patch\\payload\\')==3
    text=text.replace('patch\\manifest.json','manifest.json').replace('patch\\payload\\','payload\\')
    (runtime/'Coop-Localization.ps1').write_text(text,encoding='utf-8-sig')
    (runtime/'Localization-Manager.ps1').write_text((HERE/'Localization-Manager.ps1').read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
    shutil.copy2(CHS/'patch/manifest.json',runtime/'manifest.json')
    manifest=json.loads((runtime/'manifest.json').read_text())
    for entry in manifest['files']:
        src=CHS/'patch/payload'/entry['path'];dest=runtime/'payload'/entry['path']
        assert src.stat().st_size==entry['size'] and sha(src)==entry['sha256']
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists() or sha(dest)!=entry['sha256']:shutil.copy2(src,dest)
    prefix=['@echo off','setlocal',r'set "coopPs=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"']
    commands={
        'Launch-Coop.cmd':('Start-Coop.ps1','',True),
        'Install-CHS.cmd':('Coop-Localization.ps1',' -Action Install',False),
        '一键安装汉化.cmd':('Coop-Localization.ps1',' -Action Install',False),
        'Remove-CHS.cmd':('Coop-Localization.ps1',' -Action Remove',False),
        '一键卸载汉化.cmd':('Coop-Localization.ps1',' -Action Remove',False),
        '检查汉化安装.cmd':('Coop-Localization.ps1',' -Action Verify',False),
        'Remove-v05.cmd':('Remove-Coop.ps1','',False),
        '启动中文补丁管理器.cmd':('Localization-Manager.ps1','',True)}
    for name,(script,args,hidden) in commands.items():
        call=('start "" /b ' if hidden else '')+'"%coopPs%" -NoProfile -STA -ExecutionPolicy Bypass '+('-WindowStyle Hidden ' if hidden else '')+'-File "%~dp0patch\\'+script+'"'+args+' %*'
        ending=[] if hidden else ['set "coopResult=%errorlevel%"','pause','exit /b %coopResult%']
        (OUT/name).write_bytes(('\r\n'.join(prefix+[call]+ending)+'\r\n').encode('ascii'))
    (OUT/'README.md').write_text('''# Shank 2 故事双人 v0.5 · 汉化完整测试包

本包包含最新版双人 MOD、修复后的文字／字体汉化、27 个中文字幕过场视频，无需另外下载 v0.4-CHS。完整解压到可写文件夹，保持 Steam 运行。

1. 关闭游戏，双击 **一键安装汉化.cmd**（或 **Install-CHS.cmd**），选取自己的 Steam 原版 Shank 2 游戏目录。也可用 **启动中文补丁管理器.cmd** 安装、校验或卸载。
2. 双击 **Launch-Coop.cmd**，选择同一个游戏目录，配置两人的角色与初始装备并启动；游戏内进入故事模式。
3. 首次启动器默认英文，切换中文后会记住；游戏的分辨率、全屏、画质和音量沿用已有设置。

支持的原版 bin/shank2.exe SHA256：`3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3`。需要 Windows PowerShell 5.1 和游戏正常运行环境，不需要 Python 或 Codex。包内没有游戏 EXE、DLL、存档、个人配装或作者电脑路径。

如果曾用原始3DM安装器覆盖程序，请先用 Steam 验证游戏文件；本包只安装汉化资源，保留 Steam 原版 EXE／DLL。已安装**修复字体版本的 v0.4-CHS**可以直接使用本包，同样的汉化资源会跳过；更早的字体版本需先用旧包卸载汉化，再安装新版。

## 已验证的功能

两人独立操作、血条与装备、角色头像与选择、实体手柄操作；双向救援、双方倒地才重试、地形死亡回到队友附近等待救援；暂停菜单“1P 装备／2P 装备”按战役解锁筛选，实际攻击与所选武器对应；关卡前装备选择正常；回车暂停／确认与防长按误触；同一进程重试后两人及所选武器保留。中文菜单、血条、过场字幕和教程按键图标已获用户实测确认。

这是测试版：自然推进到另一关后的配装保留、完整故事流程、长期稳定性、真实新 Steam 成就仍待验证。对方 Win11 4K 屏幕的裁切问题尚未确认修复。保留成就接口不等于已验证真实解锁；本包不强制解锁或修改 Steam 统计。

## 按键

共用键盘时开启 NumLock：1P WASD／空格，2P 方向键／小键盘0；轻攻击 J／小键盘1，装备近战 K／小键盘2，远程及互动 L／小键盘3，RT O／小键盘6。回车暂停或确认；F6 手动召回2P。正常救援请靠近倒地伙伴按互动键。启动器可选择两个 XInput 手柄。

## 卸载

先关闭游戏。**Remove-CHS.cmd／一键卸载汉化.cmd**只卸载文字和字幕、恢复备份原资源；**Remove-v05.cmd**只移除本版双人 MOD。要完整移除，先卸载汉化、再移除 MOD。游戏内 `.storycoop-chs` 是原资源备份，请勿手动删除。仅移除汉化后，再从本包启动即可生成英文版双人界面。原版和 v0.4 MOD 保留。

内部脚本和资源在 patch 文件夹，配置与语言偏好也保存在该文件夹；分享请发送干净 ZIP。汉化与过场视频来自用户提供的3DM汉化包；保留原作者署名。教程图标编号修复、Steam兼容与双人 MOD 由本项目适配。体积主要来自字幕视频，每份只存一遍。

## English quick start

Extract everything. Close the game and run **Install-CHS.cmd** to install the included repaired Chinese text and 27 subtitled movies. Then open **Launch-Coop.cmd**, select the same compatible Steam game folder and choose CAMPAIGN MODE. The launcher defaults to English and remembers later language selection. Use **Remove-CHS.cmd** to restore the original assets and **Remove-v05.cmd** to remove this co-op version. Existing v0.4 and original Steam components remain. This is a test build; full campaign and real new Steam achievements are not fully validated.
''',encoding='utf8')
    (OUT/'FONT-LICENSE.txt').write_text('Font textures and bitmap font metadata originate from the user-supplied 3DMGAME-Shank.2.CHS.Patch.V1.0 package. Original authors retain their rights and attribution. No separate font license file was present in the selected resource payload; this notice does not grant a new font license. The compatibility fix changes reserved glyph identifiers and matching decoder behavior; original textures are retained.\n汉化字体图像及字库来自用户提供的3DM汉化包，原作者权利和署名保留。本说明不构成新的字体授权。\n',encoding='utf8')
    report=json.loads((MOD/'VALIDATION.json').read_text())
    report.update(package='0.5-CHS-complete-test',managed_text_files=69,managed_movie_files=27,localization_payload='byte-identical to repaired v0.4-CHS',tutorial_input_icons_user_confirmed=True,original_steam_components_preserved=True)
    if (HERE/'analysis/bundle-installer.json').exists():
        checks=json.loads((HERE/'analysis/bundle-installer.json').read_text())
        report['combined_package_transaction_checks']=checks['checks']
    if (HERE/'analysis/bundle-manager.json').exists():
        gui=json.loads((HERE/'analysis/bundle-manager.json').read_text(encoding='utf-8-sig'))
        report['combined_package_manager_checks']=len(gui['checks'])
        report['combined_package_manager_labels_fit']=gui['localized_labels_fit']
    if (HERE/'analysis/bundle-command-tests.json').exists():
        cli=json.loads((HERE/'analysis/bundle-command-tests.json').read_text())
        report['combined_package_command_checks']=len(cli['checks'])
        report['combined_package_command_errors_propagated']=cli['failure_exit_code_propagated']
    if (HERE/'analysis/bundle-launcher.json').exists():
        report['combined_package_launcher_smoke']=json.loads((HERE/'analysis/bundle-launcher.json').read_text())
    (runtime/'VALIDATION.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'prepared':str(OUT),'payload_files':len(manifest['files']),'payload_bytes':sum(e['size'] for e in manifest['files'])}))

def package():
    files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    assert not any(p.suffix.lower() in ('.exe','.dll') for p in files)
    assert not any(p.name in ['loadouts.json','launcher-settings.json','startup-error.log'] for p in files)
    (OUT/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(OUT).as_posix()+'\n' for p in files),encoding='utf8')
    archive=OUT.parent/(OUT.name+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    result={'zip':str(archive),'bytes':archive.stat().st_size,'files':len(files)+1,'sha256':sha(archive)}
    (HERE/'bundle-release.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':
    if '--archive' in sys.argv:package()
    else:prepare()
