"""Local development packager. Reconstructs from an owned Steam installation."""
from pathlib import Path
import subprocess,sys,shutil,json
root=Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common')
here=Path(__file__).resolve().parent;out=root/'outputs/Shank2-StoryCoop-v0.3';out.mkdir(exist_ok=True)
(out/'source').mkdir(exist_ok=True);(out/'validation').mkdir(exist_ok=True)
for name in ['build.py','extra_code.py','hud_code.py','loadout_code.py','death_code.py','revive_code.py','chui.py','make_ui.py','export_ui.py']:
 shutil.copy2(here/name,out/'source'/name)
for name in ['Manage-Coop.ps1','Coop-Launcher.ps1']:
 (out/name).write_text((here/name).read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
shutil.copy2(here/'catalog.json',out/'catalog.json')
for src,dest in [('README-v03.md','README.md'),('TECHNICAL-v03.md','TECHNICAL.md'),('VALIDATION-v03.md','VALIDATION.md')]:
 shutil.copy2(here/src,out/dest)
shutil.copy2(here/'revive-clean-effects.json',out/'validation/revive-clean-effects.json')
for mode in ['keyboard','pads']:
 target=here/f'final/shank2-coop-v03-{mode}.exe'
 # The earlier, verified recipe exporter includes only short authored literals
 # and references to source bytes, rather than shipping the game executable.
 subprocess.run([sys.executable,str(Path(r'G:\shank2\work\story-coop-v02\export.py')),str(target),str(out/f'{mode}-recipe.json')],check=True)
 if mode=='keyboard':
  recipe_path=out/f'{mode}-recipe.json';recipe=json.loads(recipe_path.read_text())
  # Exact previously installed builds only; never accept arbitrary receipt claims.
  recipe['allowed_previous_sha256']=['7958dca6be8bc2c8599bfcb79fb092eabe0f9bf53cd4bd38c18f07370c346a57','0206779180978b5bb35c68c0a00ecb520bd0076e9039069d63470fa2ff86ca20','820660e608b665f0cf3b5bac3dae582734e6b7b13558993f5c59216252bdc115']
  recipe_path.write_text(json.dumps(recipe,indent=2),encoding='utf-8')
subprocess.run([sys.executable,str(here/'export_ui.py'),r'E:\SteamLibrary\steamapps\common\Shank 2\data-pc\ui\campaignscreen.chui',str(root/'work/shank2-test/data-pc/ui/campaigncoop.chui'),str(out/'ui-recipe.json')],check=True)
(out/'Launch-Coop.cmd').write_bytes(b'@echo off\r\nstart "" /b powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0Coop-Launcher.ps1"\r\n')
(out/'Remove-v03.cmd').write_bytes(b'@echo off\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Manage-Coop.ps1" -Action Remove -InputMode Keyboard\r\nif errorlevel 1 goto done\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Manage-Coop.ps1" -Action Remove -InputMode Pads\r\n:done\r\npause\r\n')
(out/'source/requirements.txt').write_text('pefile==2024.8.26\ncapstone==5.0.9\nkeystone-engine==0.9.2\n',encoding='utf-8')
print(out)
