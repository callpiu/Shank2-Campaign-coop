"""Build three independent v0.10.0 packages from frozen assets and clean code."""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import struct
import sys
import zipfile

HERE=Path(__file__).resolve().parent;WORK=HERE.parent;ROOT=HERE.parents[1]
BASE=ROOT/'outputs/Shank2-StoryCoop-v0.9.1-CHS.zip'
BASE_SHA='64a5e0a18dc0dc11261dcd2c856fbe316797cefa9725ed9efb3d93bf44672753'
ORIGINAL=WORK/'story-coop-v09-fixes/upgrade-fixture'
STOCK=ORIGINAL/'bin/shank2.exe'
PROFILES={'MOD-EN':('Shank2-v0.10.0-MOD-EN',True,False),
    'CHS':('Shank2-v0.10.0-CHS',False,True),
    'MOD-CHS':('Shank2-v0.10.0-MOD-CHS',True,True)}
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def delta(source,target):
    assert len(target)>=len(source);patches=[];i=0
    while i<len(source):
        if source[i]==target[i]:i+=1;continue
        start=i
        while i<len(source) and source[i]!=target[i]:i+=1
        patches.append(dict(offset=start,before=source[start:i].hex(),after=target[start:i].hex()))
    return dict(format=1,input_sha256=sha(source),output_sha256=sha(target),source_size=len(source),
        target_size=len(target),patches=patches,append=base64.b64encode(target[len(source):]).decode())


def rebuild(source,r):
    assert sha(source)==r['input_sha256'];out=bytearray(source)
    if r['format']==2:
        out=bytearray().join(source[c['copy']:c['copy']+c['length']] if 'copy'in c else base64.b64decode(c['literal']) for c in r['chunks'])
    else:
        for p in r['patches']:
            before=bytes.fromhex(p['before']);after=bytes.fromhex(p['after']);a=p['offset']
            assert out[a:a+len(before)]==before;out[a:a+len(after)]=after
        for c in r.get('append',[]):
            out.extend(source[c['copy']:c['copy']+c['length']] if 'copy'in c else base64.b64decode(c['literal']))
    assert sha(out)==r['output_sha256'];return bytes(out)


def standalone_chs(stock):
    sys.path.insert(0,str(WORK/'chs-compat'))
    compat=module('standalone_steam_chs',WORK/'chs-compat/build_compat.py')
    raw,_,mapped,decoder=compat.patch_exe(stock,compat.translated_slots())
    pe=compat.pefile.PE(data=raw);out=bytearray(raw)
    rva=compat.align(pe.OPTIONAL_HEADER.SizeOfImage,0x1000);ptr=compat.align(len(raw),512);va=0x400000+rva
    header=pe.sections[-1].get_file_offset()+40
    assert raw[header:header+40]==bytes(40)
    out[header:header+40]=struct.pack('<8sIIIIIIHHI',b'.chsaud',0x3000,rva,0x3000,ptr,0,0,0,0,0xe0000060)
    struct.pack_into('<H',out,pe.FILE_HEADER.get_field_absolute_offset('NumberOfSections'),len(pe.sections)+1)
    struct.pack_into('<I',out,pe.OPTIONAL_HEADER.get_field_absolute_offset('SizeOfImage'),rva+0x3000)
    out.extend(bytes(ptr-len(out)));out.extend(b'\xcc'*0x1000+bytes(0x2000))
    dev=HERE/'dev';dev.mkdir(exist_ok=True);source=dev/'chs-renderer.exe';source.write_bytes(out)
    audio=module('standalone_movie_paths',WORK/'story-coop-v07-dialogue/build_audio.py')
    target=dev/'shank2-localization.exe'
    audio_report=audio.build(source,target,'../data/movies',code_address=va,data_address=va+0x1000)
    result=target.read_bytes();p=compat.pefile.PE(data=result)
    assert p.OPTIONAL_HEADER.AddressOfEntryPoint==compat.pefile.PE(data=stock).OPTIONAL_HEADER.AddressOfEntryPoint
    sections=[s.Name.rstrip(b'\0').decode() for s in p.sections]
    assert not any(x in sections for x in ('.coop','.direct','.precoop','.camx'))
    assert p.DIRECTORY_ENTRY_IMPORT[0].dll==b'steam_api.dll'
    for a,n in ((0x4ee3b0,7),(0x6655ce,6),(0x68d1c0,5),(0x68e148,5)):
        old=compat.pefile.PE(data=stock);o=old.get_offset_from_rva(a-0x400000);i=p.get_offset_from_rva(a-0x400000)
        assert result[i:i+n]==stock[o:o+n]
    save(HERE/'standalone-chs-validation.json',dict(passed=True,sha256=sha(result),sections=sections,
        native_gameplay_and_entry_unchanged=True,mapped_strings=len(mapped),decoder=decoder,movie_redirect=audio_report))
    return result


def wrappers(dest,mod,chs):
    def cmd(name,script):
        text='@echo off\r\n"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0'+script+'" %*\r\nset "result=%errorlevel%"\r\nif not "%result%"=="0" pause\r\nexit /b %result%\r\n'
        (dest/name).write_bytes(text.encode('ascii'))
    for filename,action in (('Install.ps1','Install'),('Test-Patch.ps1','Verify'),('Uninstall.ps1','Remove')):
        text="param([string]$GamePath,[switch]$NoUI)\n$ErrorActionPreference='Stop'\ntry { & (Join-Path $PSScriptRoot 'patch\\Install-Patch.ps1') -Action '"+action+"' -GamePath $GamePath -NoUI:$NoUI } catch { Write-Error $_; exit 1 }\n"
        (dest/filename).write_text(text,encoding='utf-8-sig')
    (dest/'PatchManager.ps1').write_text("param([string]$GamePath)\n& (Join-Path $PSScriptRoot 'patch\\PatchManager.ps1') -GamePath $GamePath\n",encoding='utf-8-sig')
    for name,script in (('Install.cmd','Install.ps1'),('Verify.cmd','Test-Patch.ps1'),('Uninstall.cmd','Uninstall.ps1'),('Start-Installer.cmd','PatchManager.ps1')):cmd(name,script)
    if chs:
        for name,script in (('一键安装汉化.cmd','Install.ps1'),('检查汉化安装.cmd','Test-Patch.ps1'),('一键卸载汉化.cmd','Uninstall.ps1'),('启动中文补丁管理器.cmd','PatchManager.ps1')):cmd(name,script)
    if mod:
        for name,script in (('安装MOD.cmd','Install.ps1'),('卸载MOD.cmd','Uninstall.ps1')):cmd(name,script)


def prepare():
    assert sha(BASE.read_bytes())==BASE_SHA
    stock=STOCK.read_bytes();assert sha(stock)=='3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3'
    pure_chs=standalone_chs(stock)
    modrows={r['language']:r for r in json.loads((WORK/'story-coop-v33-dodge/builds.json').read_text(encoding='utf-8-sig'))}
    reports=[]
    with zipfile.ZipFile(BASE) as z:
        oldmanifest=json.loads(z.read('patch/manifest.json'))
        for profile,(name,mod,chs) in PROFILES.items():
            dest=ROOT/'outputs'/name
            assert not dest.exists() and not (dest.parent/(dest.name+'.zip')).exists(),'Do not overwrite frozen releases.'
            patch=dest/'patch';patch.mkdir(parents=True);files=[]
            def payload(path,data,original=None):
                p=patch/'payload'/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
                files.append(dict(path=path,targetRelative=path,relative='payload/'+path,size=len(data),sha256=sha(data),original_sha256=original))
            if chs:
                for r in oldmanifest['files']:
                    data=z.read('patch/payload/'+r['path']);assert sha(data)==r['sha256']
                    payload(r['path'],data,r['original_sha256'])
            lang='chs' if chs else 'en'
            if mod:
                row=modrows[lang];exe=(WORK/'story-coop-v33-dodge/dev'/f'shank2-story-coop-{lang}.exe').read_bytes()
                assert sha(exe)==row['sha256'] and not row['test_assists']
                for asset in row['ui_assets']:payload('data-pc/ui/'+asset,(WORK/'story-coop-v33-dodge/dev'/asset).read_bytes())
                for asset,folder in ((f'campaigncoopv20{lang}.chui','story-coop-v20-prelevel-layout'),(f'coopsolo26hud{lang}.chui','story-coop-v26-direct')):
                    payload('data-pc/ui/'+asset,(WORK/folder/'dev'/asset).read_bytes())
                for stem,native,target in (('pause','pausedialog.chui','pausecoopv05.chui'),('equip','singleplayerloadoutscreen.chui','equipcoopv05.chui')):
                    source=z.read('patch/payload/data-pc/ui/'+native) if chs else (ORIGINAL/'data-pc/ui'/native).read_bytes()
                    recipe=json.loads(z.read(f'patch/{stem}-{lang}-recipe.json'))
                    payload('data-pc/ui/'+target,rebuild(source,recipe))
                payload('patch/Coop-Key-Settings.ps1',(WORK/'story-coop-v26-direct/Coop-Key-Settings.ps1').read_bytes())
                payload('Coop-Key-Settings.cmd',(WORK/'story-coop-v26-direct/Coop-Key-Settings.cmd').read_bytes())
                (patch/'Coop-Key-Settings.ps1').write_bytes((WORK/'story-coop-v26-direct/Coop-Key-Settings.ps1').read_bytes())
            else:exe=pure_chs
            save(patch/'exe-recipe.json',delta(stock,exe))
            for path in (['bin/shank2.exe','bin/shank2-story-coop.exe'] if mod else ['bin/shank2.exe']):
                files.append(dict(path=path,targetRelative=path,recipe='exe-recipe.json',size=len(exe),sha256=sha(exe),original_sha256=sha(stock) if path=='bin/shank2.exe' else None))
            manifest=dict(format=1,version='0.10.0',profile=profile,display_name={'MOD-EN':'Story Co-op MOD (English)','CHS':'优化汉化补丁','MOD-CHS':'双人 MOD + 优化汉化'}[profile],
                includes_mod=mod,includes_localization=chs,original_exe_sha256=sha(stock),
                guards={k:v for k,v in oldmanifest['guards'].items() if k!='bin/shank2.exe'},files=files)
            if not chs:manifest['guards']['data-pc/ui/campaignscreen.chui']=sha((ORIGINAL/'data-pc/ui/campaignscreen.chui').read_bytes())
            save(patch/'manifest.json',manifest)
            for script in ('Install-Patch.ps1','PatchManager.ps1'):(patch/script).write_bytes((HERE/script).read_text(encoding='utf8').encode('utf-8-sig'))
            (patch/'Game-Paths.ps1').write_bytes(z.read('patch/Game-Paths.ps1'))
            wrappers(dest,mod,chs)
            (dest/'README.md').write_text(readme(profile,manifest),encoding='utf8')
            if chs:
                (dest/'FONT-LICENSE.txt').write_text('字体、汉化文本及中文字幕视频来自用户提供的 3DM Shank 2 汉化补丁与过场汉化包。原作者权利与署名保留；本项目不授予额外字体授权。\n本项目增加 Steam 兼容渲染、教程图标修复与过场混音优化。发行包不含分轨模型。\n',encoding='utf8')
            save(patch/'VALIDATION.json',dict(source_builds_verified=True,test_assists=False,
                gameplay_user_confirmed_chs_mod=bool(mod and chs),english_mod_gameplay_pending=bool(mod and not chs),
                standalone_chs_runtime_pending=bool(chs and not mod),full_campaign_exhaustive=False))
            reports.append(dict(profile=profile,directory=str(dest),exe_sha256=sha(exe),payload_files=len(files)))
    save(HERE/'prepared.json',reports);print(json.dumps(reports,ensure_ascii=False))


def readme(profile,m):
    mod,chs=m['includes_mod'],m['includes_localization']
    description={'MOD-EN':'纯 MOD：保留英文界面、原版英文文本和原版音视频，不包含汉化字体、中文字幕或音频优化资源。',
        'CHS':'纯优化汉化：69 项汉化文字／字库／界面与 27 段中文字幕过场，含中文渲染、教程按键图标修复；对白约 ×1.8、背景音乐约 ×0.3，原画面帧和字幕保留。没有战役双人、角色全解锁、MOD 镜头或 MOD 改键逻辑。',
        'MOD-CHS':'整合包：最新双人 MOD + 优化汉化，包含 69 项文字／字体／界面和 27 段中文字幕优化过场。'}[profile]
    common=f'''# Shank 2 v0.10.0 — {m['display_name']}

{description}

## 安装

1. 完整解压到新文件夹，退出这份游戏。运行 `Start-Installer.cmd` 打开管理器，选择包含 bin 和 data-pc 的 Shank 2 Steam 游戏目录，点安装。也可运行 `Install.cmd`。
2. 安装后直接从 Steam 启动 Shank 2；无需启动器。沿用已有分辨率、全屏和存档。
3. `Verify.cmd` 校验，`Uninstall.cmd` 卸载并还原安装前文件。请保留游戏内 `.shank2-patch` 备份。

三个包分别面向干净的 Steam 原版，不必叠加。切换包前先用已安装包卸载。已有旧版汉化先用其旧包卸载；旧 Steam MOD 入口先运行原目录 `Restore-Steam-Original.cmd`，再安装本包。不要手动删除原件备份。Steam 验证文件可能还原程序，届时可重新运行安装修复，或卸载还原。原件／本包之外的未知改动会被拒绝覆盖。

支持原版 bin/shank2.exe SHA256：`{m['original_exe_sha256']}`。若原 3DM 安装器替换过 EXE/DLL，请先用 Steam 验证恢复。安装器在本机用配方重建，保持原 Steam 接口与 Bink DLL。无需 Python、Codex 或开发目录。需要 Windows PowerShell 5.1 和游戏自身运行环境。

本包不包含完整游戏 EXE/DLL、存档、个人键位、测试无敌、一击必杀或诊断器。安装／卸载不会更改个人存档、显示设置或自定义键位；卸载后保留个人键位文件。不要覆盖混装其他未知补丁。
'''
    if mod:common+='''
## 双人玩法与键位

游戏内选择「战役 → 本地双人」（英文 Campaign Mode → Local Co-op）。每关先依次完成 1P 选人／装备、2P 选人／装备；武器按战役进度，17 角色全开放，适用的生命／伤害属性沿用生存模式。选人显示人物介绍与属性；暂停页可独立配装。独立血条／投掷物／分数，互动救援，双方倒地才重试，重试保分，地形倒地回到队友身边。默认双人镜头，F6 召回 2P，F7 切换镜头。

运行游戏目录的 `Coop-Key-Settings.cmd` 修改键盘或选择两只 XInput 手柄；保存后下次启动生效。设置页首次英文，切换中文后记忆。

默认 1P WASD／空格，2P 方向键／小键盘 0。轻攻击 J／小键盘 1，重武器 K／小键盘 2，远程攻击 L／小键盘 3，抓取 O／小键盘 6，左右闪避 Z、C／小键盘 8、9。NumLock 开启。回车暂停／恢复与确认。其余键位见设置页。

包含已确认的女性角色 Boss 抓取显示、第二关过场双人传送、重试保分、恢复血量红边、角色介绍与首屏属性显示、左右闪避等修正。连击负数与双人同时处决 Boss 血条修正保留，但未穷尽所有触发组合。
'''
    common+='''
## 验证范围与署名

中文双人版本的上述主要功能已由用户实测；纯英文 MOD 将由用户随后实测，纯汉化的独立程序组合还需游戏内核对。不把配方、安装器及字体检查当成完整战役测试。成就方面，用户在此前整合环境导入通关存档后正常同步；本版保留 Steam API，未逐项验证自然游玩触发。

原汉化文本、字体和字幕来自用户提供的 3DM 汉化与过场汉化补丁，原作者权利与署名保留。过场音频使用 TIGER-DnR 本地估算分轨后重混，音效／残余成分保留并限幅；不分发模型，实际比例随分离误差变化。

English: Extract everything. Run Start-Installer.cmd, choose the Steam Shank 2 folder, then Install. You can use Install.cmd / Verify.cmd / Uninstall.cmd instead. Exit the game before changes. Launch normally from Steam afterward. The three profiles are standalone alternatives; uninstall the installed profile before switching. Restore older mods/localizations with their original uninstallers first. Original files are backed up under .shank2-patch; keep it until uninstall. Saves, display settings and custom keys are preserved. Only the known Steam executable is supported; no full EXE/DLL, cheats or personal data is distributed. English co-op gameplay and standalone Chinese runtime still await user verification.
'''
    return common


def refresh_tools():
    for report in json.loads((HERE/'prepared.json').read_text(encoding='utf-8-sig')):
        dest=Path(report['directory']);assert dest.parent==ROOT/'outputs'
        assert not (dest.parent/(dest.name+'.zip')).exists(),'Do not modify a frozen archive directory.'
        patch=dest/'patch';m=json.loads((patch/'manifest.json').read_text(encoding='utf-8-sig'))
        assert m['profile']==report['profile'] and m['version']=='0.10.0'
        for script in ('Install-Patch.ps1','PatchManager.ps1'):(patch/script).write_bytes((HERE/script).read_text(encoding='utf8').encode('utf-8-sig'))
        (dest/'README.md').write_text(readme(m['profile'],m),encoding='utf8')
    print('Refreshed canonical installer tools and documentation before archiving.')


if __name__=='__main__':refresh_tools() if '--refresh-tools' in sys.argv else prepare()
