"""Reproduce the v0.9 release from the frozen v0.8.3 bundle and clean v20 builds."""
import base64
import difflib
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT/'outputs/Shank2-StoryCoop-v0.8.3-CHS.zip'
OUTPUT = ROOT/'outputs/Shank2-StoryCoop-v0.9-CHS'
DEV = HERE.parent/'story-coop-v20-prelevel-layout'
BASE_SHA = 'bf3a45e932685c69cf0897cf3989a0d206b73080927d95bb304829f9d971a3d4'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(b): return hashlib.sha256(b).hexdigest()
def save(p, data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def recipe(source, target):
    chunks=[]
    for tag,a,b,c,d in difflib.SequenceMatcher(None,source,target,autojunk=False).get_opcodes():
        if tag=='equal': chunks.append(dict(copy=a,length=b-a))
        elif c!=d: chunks.append(dict(literal=base64.b64encode(target[c:d]).decode()))
    result=dict(format=2,input_sha256=digest(source),output_sha256=digest(target),
                source_size=len(source),target_size=len(target),chunks=chunks)
    rebuilt=b''.join(source[r['copy']:r['copy']+r['length']] if 'copy'in r else base64.b64decode(r['literal']) for r in chunks)
    assert rebuilt==target
    return result

def addon(source,target,old):
    assert len(target)>=len(source)
    patches=[];i=0
    while i<len(source):
        if source[i]==target[i]: i+=1;continue
        start=i
        while i<len(source) and source[i]!=target[i]:i+=1
        patches.append(dict(offset=start,before=source[start:i].hex(),after=target[start:i].hex()))
    return dict(old,format=1,input_sha256=digest(source),output_sha256=digest(target),
        source_size=len(source),target_size=len(target),patches=patches,
        append=base64.b64encode(target[len(source):]).decode())

README='''# Shank 2 故事模式本地双人 v0.9 · 完整汉化整合包

包含双人 MOD、修复后的文字／字体汉化，以及 27 段增强对白、压低背景音乐的中文字幕过场。无需叠加旧版升级包。

## 安装与升级

1. 完整解压到一个新文件夹。首次安装运行“一键安装汉化.cmd”或 Install-CHS.cmd，选择包含 bin、data-pc 的 Shank 2 游戏目录。
2. 运行 Launch-Coop.cmd，选择同一游戏目录，设置输入方式和初始角色／装备，保存并启动。进入 CAMPAIGN MODE。
3. 已使用 v0.8 系列完整汉化：汉化与视频资源未变，无需重装。关闭游戏，用本包启动器选回原游戏目录，即可升级 MOD。需要保留启动器设置时，可复制旧包 patch/loadouts.json、patch/launcher-settings.json 到本包同一位置。
4. v0.4／v0.5 旧汉化先用旧包卸载，再安装本包。保留游戏目录中的 .storycoop-chs 原件备份。

启动器首次默认英文，切换中文后记住。分辨率、全屏等沿用原版保存设置。

## 本版新增与修复

- 进入故事关卡以及正常通关进入下一关前，依次为 1P 选角色、选装备，再为 2P 选角色、选装备，最后进入关卡。两人完成后统一应用，角色与装备在即将进入的关卡立即生效。
- 双方开放全部 17 个角色，支持跨 Shank／Corina 类型切换；武器仍按战役进度筛选。跨类型时先刷新兼容装备，再由玩家选择。
- 修复“邪恶”角色的选人小图、大图和游戏内血条头像；恢复人物介绍和三格武器图标。
- 修复第一关 Boss 抓取女性角色时身体错乱和位置偏高，保留抓取伤害、脱身和队友打断流程。
- 修复第二关 Boss 前过场结束后只有一人传送、另一人留在场外倒地的问题。
- 启动器配装现在只作为初始值，关卡前界面的选择可以正常覆盖它。

## 保留的双人功能

独立输入、血条、装备、投掷物和分数；队友互动救援，双方倒地才重试，重试保留各自分数；地形倒地自动送回存活队友附近。暂停菜单“1P 装备／2P 装备”可独立更换已解锁武器，暂停菜单选的角色在下一关或重试生效。游戏内选择在当前进程保留，重新启动采用启动器初始设置。

F6 手动召回 2P，倒地后召回仍可救援。双人镜头默认开启、平滑拉远，F7 可临时关闭／开启。过场默认使用增强对白、降低背景的版本，保留中文字幕和音画同步。Jungle／Human Cargo 子弹时间虚焦残留修复保留。

共用键盘需开启 NumLock：1P WASD／空格，2P 方向键／小键盘0；轻攻击 J／小键盘1，装备近战 K／小键盘2，远程或互动 L／小键盘3，RT O／小键盘6。回车暂停／恢复和菜单确认。也支持两个 XInput 手柄。

## 验证范围

用户已实测确认双人关前配装、正常跨关、跨角色类型切换、邪恶图片／介绍／武器图标／血条头像、两项 Boss 修复，以及先前双人救援、分数保留、实体手柄等功能。完整战役、所有角色与 Boss 组合尚未穷尽测试。独眼巨人处决按原版扣固定血量，不是必杀，未修改 Boss 伤害。用户导入通关存档后 Steam 成就同步成功，未逐项验证自然游玩触发。

发行包不含测试无敌、普通敌人一击必杀、诊断工具、游戏 EXE／DLL、存档或个人设置。测试辅助只用于开发测试进程。原始 Steam EXE、Steam 接口和 Bink DLL 保留。

## 卸载与回退

关闭游戏，运行 Remove-v08.cmd 移除 MOD（名称为兼容升级而保留）；需恢复汉化／视频时，再运行“一键卸载汉化.cmd”或 Remove-CHS.cmd。仅回退 MOD 时无需卸载汉化，移除后用保留的旧包重新生成。旧包不要直接覆盖本版的 MOD 程序。

仅支持 Steam 原版 bin/shank2.exe SHA-256：3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3。本包在本机原版上重建 MOD，不分发完整游戏。汉化与字幕源自用户提供的 3DM 汉化包，原作者权利与署名保留。

English: Run Install-CHS.cmd for a first installation, then Launch-Coop.cmd. Existing v0.8+ Chinese/movie assets need no reinstall. Before each campaign level, select P1 character and equipment, then P2 character and equipment; both choices apply to that upcoming level. All 17 characters are available; weapons follow campaign unlocks. Pause-menu character changes still apply on next level/retry. F6 recalls P2; F7 toggles the camera. Remove-v08.cmd removes the mod. No test assists or personal files are shipped.
'''

def prepare():
    assert sha(BASE)==BASE_SHA
    assert not OUTPUT.exists(), 'Do not overwrite a release'
    OUTPUT.mkdir()
    with zipfile.ZipFile(BASE) as z:
        for info in z.infolist():
            p=Path(info.filename)
            assert not p.is_absolute() and '..' not in p.parts
            if info.is_dir() or p.name=='SHA256SUMS.txt':continue
            target=OUTPUT/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(info))
    patch=OUTPUT/'patch'
    previous=json.loads((patch/'previous-baselines.json').read_text())
    for mode in ('keyboard','pads'):
        for lang in ('en','chs'):
            p=patch/f'{mode}-{lang}-addon.json';old=json.loads(p.read_text())
            previous[mode]=list(dict.fromkeys(previous[mode]+[old['output_sha256']]))
            suffix='-chs' if lang=='chs' else ''
            source=(HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{suffix}.exe').read_bytes()
            target=(DEV/'dev'/f'{mode}-{lang}.exe').read_bytes()
            save(p,addon(source,target,old))
    save(patch/'previous-baselines.json',previous)
    fixture=HERE.parent/'story-coop-v09-fixes/upgrade-fixture/data-pc/ui'
    for lang in ('en','chs'):
        source_dir=fixture if lang=='en' else patch/'payload/data-pc/ui'
        for stem,native,filename in [('prelevel','singleplayerloadoutscreen.chui',f'cooppreselv20{lang}.chui'),
                                     ('hud20','campaignscreen.chui',f'campaigncoopv20{lang}.chui')]:
            save(patch/f'{stem}-{lang}-recipe.json',recipe((source_dir/native).read_bytes(),(DEV/'dev'/filename).read_bytes()))
    p=patch/'Manage-Coop.ps1';text=p.read_text(encoding='utf-8-sig').replace('v0.8.3','v0.9')
    text=text.replace("chs='equip-chs-recipe.json'}", "chs='equip-chs-recipe.json'},\n    @{source='singleplayerloadoutscreen.chui';target='cooppreselv20{lang}.chui';en='prelevel-en-recipe.json';chs='prelevel-chs-recipe.json'},\n    @{source='campaignscreen.chui';target='campaigncoopv20{lang}.chui';en='hud20-en-recipe.json';chs='hud20-chs-recipe.json'}")
    start=text.index('function Assert-Ui($Entry)');end=text.index('function New-Config',start)
    text=text[:start]+'''function Ui-Targets($Entry) {
    @('en','chs') | ForEach-Object {$Entry.target.Replace('{lang}',$_)} | Select-Object -Unique
}
function Assert-Ui($Entry) {
    $allowed=@()
    foreach($language in @('en','chs')) {
        $r=Get-Content (Join-Path $PSScriptRoot $Entry.$language) -Raw | ConvertFrom-Json
        $allowed+=@($r.output_sha256)
    }
    foreach($name in (Ui-Targets $Entry)) {
        $path=Join-Path $root ('data-pc\\ui\\'+$name)
        if((Test-Path -LiteralPath $path) -and (Hash-Bytes ([IO.File]::ReadAllBytes($path))) -notin $allowed) {throw ('Unrecognized custom UI: '+$name)}
    }
}
''' +text[end:]
    text=text.replace("foreach($e in $uiFiles) {$p=Join-Path $root ('data-pc\\ui\\'+$e.target);if(Test-Path -LiteralPath $p) {Remove-Item -LiteralPath $p}}",
        "foreach($e in $uiFiles) {foreach($name in (Ui-Targets $e)) {$p=Join-Path $root ('data-pc\\ui\\'+$name);if(Test-Path -LiteralPath $p) {Remove-Item -LiteralPath $p}}}")
    text=text.replace("('data-pc\\ui\\'+$e.target));bytes=", "('data-pc\\ui\\'+$e.target.Replace('{lang}',$selectedLanguage)));bytes=")
    text=text.replace('all three UI reconstructions','all five UI reconstructions')
    assert text.count('cooppreselv20')==1 and "target.Replace('{lang}',$selectedLanguage)" in text
    p.write_text(text,encoding='utf-8-sig')
    for name in ('Launcher-Strings.ps1','Localization-Manager.ps1','Remove-Coop.ps1'):
        p=patch/name;t=p.read_text(encoding='utf-8-sig').replace('v0.8.3','v0.9')
        if name=='Launcher-Strings.ps1':
            t=t.replace('Launcher loadouts override pre-level selections. Change weapons normally from the in-game pause menu.',
                'Starting defaults only. Before each level: P1 character and gear, then P2 character and gear.')
            t=t.replace('启动器配装会覆盖关卡开始前的配装；进入关卡后可在暂停菜单正常换装。',
                '此处仅设初始配装；关卡前依次选择 1P 角色／装备、2P 角色／装备，即将进入的关卡立即生效。')
        p.write_text(t,encoding='utf-8-sig')
    (OUTPUT/'README.md').write_text(README,encoding='utf-8')
    v=json.loads((patch/'VALIDATION.json').read_text())
    v.update(version='0.9-CHS',clean_builds={r['name']:r['sha256'] for r in json.loads((DEV/'builds.json').read_text())},
        prelevel_order='P1 character, P1 equipment, P2 character, P2 equipment, spawn',
        prelevel_and_natural_transition_user_confirmed=True,cross_family_user_confirmed=True,
        evil_preview_description_icons_hud_user_confirmed=True,
        female_first_boss_grab_user_confirmed=True,slums_boss_teleport_user_confirmed=True,
        launcher_no_longer_overrides_prelevel=True,includes_test_invincibility=False,
        includes_one_hit_kills=False,exact_bundle_runtime_verified=False,full_campaign_verified=False)
    save(patch/'VALIDATION.json',v)
    print('Prepared',OUTPUT)

def package():
    assert sha(BASE)==BASE_SHA
    checks=json.loads((HERE/'validation.json').read_text())
    assert all(checks[k] for k in ('four_variants_exact','no_godmode_or_probe','restores_all_96_originals','launcher_smoke','new_ui_exact','ui_removal','custom_ui_rejected'))
    recovery=json.loads((HERE/'recovery-validation.json').read_text());assert recovery['passed']
    p=OUTPUT/'patch/VALIDATION.json';v=json.loads(p.read_text())
    v['v09_installer_checks']={k:value for k,value in checks.items() if k not in ('checks','command_checks')}
    v['v09_recovery_cases']=len(recovery['cases']);save(p,v)
    files=sorted(p for p in OUTPUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    assert sum(p.suffix.lower()=='.bik' for p in files)==27
    assert not any(p.suffix.lower() in ('.exe','.dll') or p.name in ('loadouts.json','launcher-settings.json','features.json') for p in files)
    (OUTPUT/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(OUTPUT).as_posix()+'\n' for p in files),encoding='utf-8')
    archive=OUTPUT.parent/(OUTPUT.name+'.zip')
    assert not archive.exists(), 'Do not overwrite a frozen archive'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(OUTPUT.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(OUTPUT).as_posix())
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    report=dict(archive=str(archive),bytes=archive.stat().st_size,sha256=sha(archive),files=len(files)+1)
    save(HERE/'release.json',report);print(json.dumps(report))

if __name__=='__main__':
    import sys
    package() if '--archive' in sys.argv else prepare()
