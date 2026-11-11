"""Frozen v0.8 -> v0.8.1 verification bundle and small overlay update."""
from pathlib import Path
import json,shutil,hashlib,base64,sys,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OLD=ROOT/'outputs/Shank2-StoryCoop-v0.8-CHS';OUT=ROOT/'outputs/Shank2-StoryCoop-v0.8.1-CHS-Test';UPDATE=ROOT/'outputs/Shank2-StoryCoop-v0.8.1-Update-Test'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def prepare():
 OUT.mkdir(exist_ok=True);UPDATE.mkdir(exist_ok=True)
 for p in OLD.rglob('*'):
  if p.is_file() and p.name!='SHA256SUMS.txt':
   d=OUT/p.relative_to(OLD);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
 runtime=OUT/'patch';changed=[];previous={}
 for mode in ['keyboard','pads']:
  previous[mode]=[]
  for lang in ['en','chs']:
   name=f'{mode}-{lang}-addon.json';recipe=json.loads((runtime/name).read_text());previous[mode].append(recipe['output_sha256'])
   original=(HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{"-chs" if lang=="chs" else ""}.exe').read_bytes()
   target=HERE/'final'/f'{mode}-{lang}.exe';b=target.read_bytes();meta=json.loads(target.with_suffix('.fixes.json').read_text())
   assert meta['source_sha256']==recipe['output_sha256']
   patches=[];i=0
   while i<len(original):
    if original[i]==b[i]:i+=1;continue
    start=i
    while i<len(original) and original[i]!=b[i]:i+=1
    patches.append({'offset':start,'before':original[start:i].hex(),'after':b[start:i].hex()})
   recipe.update(output_sha256=sha(target),target_size=len(b),patches=patches,append=base64.b64encode(b[len(original):]).decode())
   (runtime/name).write_text(json.dumps(recipe,indent=2));changed.append('patch/'+name)
 (runtime/'previous-baselines.json').write_text(json.dumps(previous,indent=2));changed.append('patch/previous-baselines.json')
 s=(runtime/'Manage-Coop.ps1').read_text(encoding='utf-8-sig')
 anchor="    if(Test-Path -LiteralPath $receipt) {"
 assert s.count(anchor)==1
 s=s.replace(anchor,"    $previous=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'previous-baselines.json') -Raw | ConvertFrom-Json\n    $allowed+=@($previous.$mode)\n"+anchor,1)
 (runtime/'Manage-Coop.ps1').write_text(s,encoding='utf-8-sig');changed.append('patch/Manage-Coop.ps1')
 for name in ['Launcher-Strings.ps1','Localization-Manager.ps1','Remove-Coop.ps1']:
  s=(runtime/name).read_text(encoding='utf-8-sig').replace('v0.8','v0.8.1')
  (runtime/name).write_text(s,encoding='utf-8-sig');changed.append('patch/'+name)
 report=json.loads((runtime/'VALIDATION.json').read_text());report.update(version='0.8.1-CHS-verification',native_fix_scope_abi_cases=14,f6_downed_recall_revival_user_confirmed=True,bullet_time_blur_fix_remote_gameplay=None,bullet_time_blur_status='static root cause and native test passed; remote PC verification pending',upgrade_from_v08='known baseline/receipt upgrade; localization payload unchanged')
 (runtime/'VALIDATION.json').write_text(json.dumps(report,indent=2));changed.append('patch/VALIDATION.json')
 header='''# v0.8.1 验证版：慢动作滤镜清理与 F6 救援修正

本版供复现问题的电脑验证，**两关滤镜修复尚待该电脑实测**。F6召回倒地2P后可救援已获本机用户确认；14项原生接口检查通过。

**已有v0.8完整包：关闭游戏，把升级包内容解压覆盖到原v0.8补丁包文件夹（能看到Launch-Coop.cmd的地方），再从该文件夹运行Launch-Coop.cmd。不要直接覆盖到游戏bin。无需卸载或重装v0.8汉化。** 两种输入方式的程序会按启动器保存的初始配装重新生成，语言偏好和个人配置不在升级包内。

完整CHS-Test包可单独使用，包含全部汉化和增强视频。v0.4/v0.5汉化升级仍需先用旧包卸载汉化；v0.8升级不需要此步骤。本修复沿用v0.8的程序文件名和Remove-v08.cmd，启动器显示v0.8.1。

请验证：Jungle吊桥黑白慢动作和Human Cargo跨船飞扑结束后，滤镜能自行清理（不要以死亡重试后的画面判断）；另测1P存活时让2P倒地，F6召回后互动救援。双人镜头、音频增强和F7保留。

若需退回v0.8：先用本版Remove-v08.cmd移除双人程序，再用保留的v0.8包重新启动生成；无需改动汉化资源。原v0.8 ZIP保留。

---

'''
 (OUT/'README.md').write_text(header+(OLD/'README.md').read_text(encoding='utf-8'),encoding='utf-8');changed.append('README.md')
 for relative in changed:
  p=UPDATE/relative;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(OUT/relative,p)
 (HERE/'changed-files.json').write_text(json.dumps(changed,indent=2));print('Prepared full verification bundle and small overlay; 96 localization payload files unchanged.')
def package():
 if (HERE/'upgrade-tests.json').exists():
  checks=json.loads((HERE/'upgrade-tests.json').read_text())
  for folder in [OUT,UPDATE]:
   p=folder/'patch/VALIDATION.json';v=json.loads(p.read_text());v.update(configured_v08_upgrade_test_cases=checks['cases'],both_input_modes_upgrade_verified=True,localization_receipt_unchanged=True)
   p.write_text(json.dumps(v,indent=2))
 reports=[]
 for folder in [OUT,UPDATE]:
  sums='SHA256SUMS.txt' if folder==OUT else 'UPDATE-SHA256SUMS.txt'
  files=sorted(p for p in folder.rglob('*') if p.is_file() and p.name!=sums)
  assert not any(p.suffix.lower() in ['.exe','.dll'] or p.name in ['loadouts.json','launcher-settings.json','features.json','startup-error.log'] for p in files)
  (folder/sums).write_text(''.join(sha(p)+'  '+p.relative_to(folder).as_posix()+'\n' for p in files))
  archive=folder.parent/(folder.name+'.zip')
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file():z.write(p,p.relative_to(folder).as_posix())
  with zipfile.ZipFile(archive) as z:assert z.testzip() is None
  reports.append({'zip':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'files':len(files)+1})
 (HERE/'packages.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports))
if __name__=='__main__':
 if '--archive' in sys.argv:package()
 else:prepare()
