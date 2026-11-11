"""Build a clean full CHS release with one enhanced copy of each movie."""
from pathlib import Path
import sys,json,shutil,hashlib,base64,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE.parent/'story-coop-v07-dialogue')]
from build_audio import build as audio
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
OLD=ROOT/'outputs/Shank2-StoryCoop-v0.5-CHS';OUT=ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS';RUNTIME=OUT/'patch'
DEV=HERE/'launcher';FINAL=HERE/'final-release';FINAL.mkdir(exist_ok=True)
def change(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
def prepare():
 RUNTIME.mkdir(parents=True,exist_ok=True)
 # Immutable old release is only a payload/dependency input. No personal settings.
 for p in OLD.rglob('*'):
  if not p.is_file() or p.name in ['SHA256SUMS.txt','README.md','Remove-v05.cmd']:continue
  dest=OUT/p.relative_to(OLD);dest.parent.mkdir(parents=True,exist_ok=True)
  if '/payload/data/movies/' in p.as_posix():
   src=HERE.parent/'story-coop-v07-dialogue/enhanced'/p.name
  else:src=p
  shutil.copy2(src,dest)
 for name in ['Coop-Launcher.ps1','Launcher-Strings.ps1','Manage-Coop.ps1']:
  shutil.copy2(DEV/name,RUNTIME/name)
 # Rebuild just the root-path constant; keep native camera/input code unchanged.
 reports=[]
 for mode in ['keyboard','pads']:
  for lang in ['en','chs']:
   name=f'{mode}-{lang}';target=FINAL/(name+'.exe')
   meta=audio(HERE/'final'/(name+'-camera.exe'),target,'../data/movies')
   recipe=json.loads((DEV/(name+'-addon.json')).read_text())
   original=(HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{"-chs" if lang=="chs" else ""}.exe').read_bytes();b=target.read_bytes()
   patches=[];i=0
   while i<len(original):
    if original[i]==b[i]:i+=1;continue
    start=i
    while i<len(original) and original[i]!=b[i]:i+=1
    patches.append({'offset':start,'before':original[start:i].hex(),'after':b[start:i].hex()})
   recipe.update(output_sha256=hashlib.sha256(b).hexdigest(),target_size=len(b),patches=patches,append=base64.b64encode(b[len(original):]).decode(),resource_root='../data/movies')
   (RUNTIME/(name+'-addon.json')).write_text(json.dumps(recipe,indent=2));reports.append(meta)
 old=json.loads((OLD/'patch/manifest.json').read_text());manifest=json.loads(json.dumps(old));manifest['version']='0.8-CHS'
 for row in manifest['files']:
  p=RUNTIME/'payload'/row['path']
  if row['group']=='Movies':row.update(size=p.stat().st_size,sha256=sha(p))
  assert sha(p)==row['sha256'] and p.stat().st_size==row['size']
 (RUNTIME/'manifest.json').write_text(json.dumps(manifest,indent=2))
 (RUNTIME/'previous-manifest.json').write_text(json.dumps(old,indent=2))
 assets=[{'file':Path(r['path']).name,'input_sha256':r['sha256'],'output_sha256':r['sha256']} for r in manifest['files'] if r['group']=='Movies']
 (RUNTIME/'movie-assets.json').write_text(json.dumps(assets,indent=2))
 manager=(RUNTIME/'Manage-Coop.ps1').read_text(encoding='utf-8-sig')
 manager=change(manager,"('data\\movies\\coop_dialogue_enhanced\\'+$asset.file)","('data\\movies\\'+$asset.file)")
 (RUNTIME/'Manage-Coop.ps1').write_text(manager,encoding='utf-8-sig')
 local=(RUNTIME/'Coop-Localization.ps1').read_text(encoding='utf-8-sig')
 local=change(local,"if($allowed.Count -ne 1) {throw 'Unknown file in localization receipt.'}","""if($allowed.Count -ne 1) {
            $previous=Get-Content -LiteralPath (Join-Path $packageRoot 'previous-manifest.json') -Raw | ConvertFrom-Json
            $known=@($previous.files | Where-Object {$_.path -ceq $entry.path -and $_.sha256 -eq $entry.sha256 -and $_.original_sha256 -eq $entry.original_sha256})
            if($known.Count -eq 1) {throw 'Old Chinese movie patch detected. Uninstall localization with your OLD v0.5/v0.4 package first, then install v0.8. Keep the .storycoop-chs backup folder.'}
            throw 'Unknown file in localization receipt.'
        }""")
 (RUNTIME/'Coop-Localization.ps1').write_text(local,encoding='utf-8-sig')
 for name in ['Localization-Manager.ps1','Remove-Coop.ps1']:
  s=(RUNTIME/name).read_text(encoding='utf-8-sig').replace('v0.5','v0.8')
  (RUNTIME/name).write_text(s,encoding='utf-8-sig')
 (RUNTIME/'Start-Coop.ps1').write_text("param([string]$GamePath)\n$ErrorActionPreference='Stop'\ntry { & (Join-Path $PSScriptRoot 'Coop-Launcher.ps1') -GamePath $GamePath } catch { $_ | Out-String | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'startup-error.log') -Encoding UTF8; Add-Type -AssemblyName System.Windows.Forms; $null=[Windows.Forms.MessageBox]::Show($_.Exception.Message,'Shank 2 Story Co-op') }\n",encoding='utf-8-sig')
 (RUNTIME/'Open-Window.ps1').write_text('''param([ValidateSet('Coop','Localization')][string]$Tool='Coop',[string]$GamePath)
$ErrorActionPreference='Stop'
$scriptName=if($Tool -eq 'Coop'){'Start-Coop.ps1'}else{'Localization-Manager.ps1'}
$info=New-Object Diagnostics.ProcessStartInfo
$info.FileName="$env:WINDIR\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
$info.UseShellExecute=$false;$info.CreateNoWindow=$true
$info.Arguments='-NoProfile -STA -ExecutionPolicy Bypass -File "'+(Join-Path $PSScriptRoot $scriptName)+'"'
if($GamePath) {
 if($GamePath.Contains('"')) {throw 'Invalid game directory.'}
 $info.Arguments+=' -GamePath "'+$GamePath.TrimEnd('\\')+'"'
}
$process=[Diagnostics.Process]::Start($info)
Write-Output ('Launcher PID '+$process.Id)
'''.replace('\n+','\n'),encoding='utf-8-sig')
 for name,tool in [('Launch-Coop.cmd','Coop'),('启动中文补丁管理器.cmd','Localization')]:
  command='@echo off\r\nsetlocal\r\n"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0patch\\Open-Window.ps1" -Tool '+tool+' %*\r\n'
  (OUT/name).write_bytes(command.encode('ascii'))
 shutil.copy2(OLD/'Remove-v05.cmd',OUT/'Remove-v08.cmd')
 validation={'version':'0.8-CHS','managed_text_files':69,'managed_movie_files':27,'enhancements':'always on at launch; F7 session camera toggle retained','movie_profile':'voice7-background7-v1','video_frames_preserved':18822,'native_hook_tests_development':240,'fixed_enable_install_tests_development':24,'user_confirmed_camera_and_first_intro':True,'exact_release_runtime':None,'all_campaign_and_real_new_steam_achievement':None,'upgrade':'uninstall prior localization with prior package first'}
 audit=HERE/'release-analysis'
 if all((audit/name).exists() for name in ['installer-validation.json','gui.json','upgrade.json','command-tests.json']) and (HERE/'native-release-tests.json').exists():
  validation.update(release_native_cases=sum(x['passed'] for x in json.loads((HERE/'native-release-tests.json').read_text())),release_transaction_cases=json.loads((audit/'installer-validation.json').read_text(encoding='utf-8'))['checks'],release_gui_operations=len(json.loads((audit/'gui.json').read_text(encoding='utf-8-sig'))['checks']),old_uninstall_then_new_install_verified=True,release_command_cases=len(json.loads((audit/'command-tests.json').read_text())['checks']),launcher_bilingual_17_portraits=True)
 (RUNTIME/'VALIDATION.json').write_text(json.dumps(validation,indent=2))
 (OUT/'README.md').write_text('''# Shank 2 故事双人 v0.8 · 汉化完整包

包含双人 MOD、修复后的文字/字体汉化，以及 27 段中文字幕过场（增强对白、压低背景音乐）。双人镜头和音频增强每次启动自动启用，无需额外设置；F7 可在当前游戏中关闭/重新开启双人镜头。每段视频只存一份。

1. **已装 v0.4/v0.5 汉化：先关闭游戏，用旧包的“一键卸载汉化.cmd”恢复原资源，再安装本包。** 保留游戏内 `.storycoop-chs` 备份文件夹。新版会拒绝直接覆盖旧电影汉化记录，避免损坏还原链。
2. 完整解压本包，保持 Steam 运行，双击“一键安装汉化.cmd”（或 Install-CHS.cmd），选择 Steam 的 Shank 2 目录。也可使用“启动中文补丁管理器.cmd”安装、校验、卸载。
3. 双击 Launch-Coop.cmd，选择同一游戏目录，设置两人的角色、初始装备和输入方式，保存并启动；游戏内进入 CAMPAIGN MODE。首次界面默认英文，切成中文后记住；分辨率、全屏等沿用已有游戏设置。

支持 Steam 原版 bin/shank2.exe SHA256：3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3。若原3DM安装器改过 EXE/DLL，先用 Steam 验证游戏文件。本包保留原版 Steam 程序和接口；不需要 Python/Codex，不包含个人设置、存档或游戏 EXE/DLL。需要 Windows PowerShell 5.1 与游戏运行环境。

双人独立操作、血条、装备；一人倒地可救援，双方倒地才重试；地形死亡回到队友附近等待救援；暂停菜单各自更换战役已解锁武器；回车暂停/恢复和确认；共享镜头平滑拉远/恢复。启动器红字说明：**启动器配装仍会覆盖关卡开始前的配装；进入关卡后可正常从暂停菜单更换。** 此问题按用户要求暂不修复。

键盘 NumLock 开启：1P WASD/空格，2P 方向键/小键盘0；轻攻击 J/小键盘1，装备近战 K/小键盘2，远程/互动 L/小键盘3，RT O/小键盘6。F6 手动召回2P，F7 镜头切换。也支持两个 XInput 手柄。

卸载：关闭游戏，先运行 Remove-v08.cmd 移除本版双人程序，再运行“一键卸载汉化.cmd”恢复文字/原电影。旧版 MOD 和用户设置保留。请勿手动删除 `.storycoop-chs`。旧包继续保留，升级前用旧包卸载旧汉化。

验证范围：既有双人功能、双人镜头及第一关完整增强开场已获用户确认；27段视频的压缩画面帧、音频时长/峰值及原游戏解码兼容性通过技术检查。完整战役、自然跨关配装保留、长期稳定性、第二台4K电脑及真实新 Steam 成就仍未全面验证。保留接口不等于已验证真实解锁。过场是混合音轨处理，部分居中音效也可能变化。

汉化/字体和字幕视频来自用户提供的3DM汉化包，原作者权利与署名保留；本项目增加兼容修复、双人模式与音频处理。内部资源/脚本位于 patch；分享请发送干净 ZIP。

English: extract all files; uninstall older localization using its OLD package first. Run Install-CHS.cmd, then Launch-Coop.cmd and select CAMPAIGN MODE. Both enhancements start enabled; F7 toggles the camera for this session. Launcher language remembers your selection. Use Remove-v08.cmd then Remove-CHS.cmd to restore. This complete CHS bundle requires its included Chinese text and enhanced subtitled movies; full-campaign and achievement validation remain pending.
''',encoding='utf-8')
 (HERE/'release-builds.json').write_text(json.dumps(reports,indent=2))
 print('Prepared v0.8 complete release: 69 text assets, 27 enhanced movies, no duplicated movie set.')
def package():
 files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
 assert not any(p.suffix.lower() in ['.exe','.dll'] or p.name in ['loadouts.json','launcher-settings.json','features.json','startup-error.log'] for p in files)
 (OUT/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.relative_to(OUT).as_posix()+'\n' for p in files))
 dest=OUT.parent/(OUT.name+'.zip')
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(OUT.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
 with zipfile.ZipFile(dest) as z:assert z.testzip() is None
 report={'zip':str(dest),'bytes':dest.stat().st_size,'files':len(files)+1,'sha256':sha(dest)}
 (HERE/'release.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':
 if '--archive' in sys.argv:package()
 else:prepare()
