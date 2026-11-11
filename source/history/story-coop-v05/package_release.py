"""Package only authored scripts/recipes; Chinese assets stay in the v0.4 pack."""
from pathlib import Path
import json,hashlib,zipfile
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'outputs/Shank2-StoryCoop-v0.5-Test'
sha=lambda b:hashlib.sha256(b).hexdigest()

def build():
    (OUT/'README.md').write_text('''# Shank 2 Story Co-op v0.5 — Test build

Extract the entire ZIP, keep Steam running, then open **Launch-Coop.cmd**.
Select your own compatible Steam game folder and choose **CAMPAIGN MODE**.
Supported original EXE SHA256: `3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3`.
Windows PowerShell 5.1 and the normal game prerequisites are required; Python is not required.

## Changes

- Enter pauses during play and confirms Continue in the pause menu. Hold protection prevents repeated toggling or a jump on resume. Confirmed in actual play.
- Pause menu has separate **P1 LOADOUT / P2 LOADOUT** buttons. Each player's melee, ranged and throwable choices are independent. The launcher supplies starting equipment; it does not force that equipment every frame.
- In-level selections are synchronized to subsequent level initialization. Both players retained their weapons after both-down retry in the same game process, confirmed by the user and recreated actor inventories. Natural progression into a different story level is still awaiting play confirmation.
- The new weapon row filter uses the game's native campaign weapon unlock check and keeps a visible-to-source selection map. Its 24 native visibility/index and pre-level bypass tests pass. The user confirmed both players' lists, selected weapons and independent attacks. Pre-level equipment uses the original native UI; its display, selection and Continue were also user-confirmed after the fix.
- Terrain-killed players move beside their surviving teammate while remaining downed and needing revival. Confirmed in actual play. Both down still opens retry.
- Existing resolution, fullscreen/windowed, graphics and audio settings are inherited. No forced display parameters or graphics.ini rewrite.

## Input

Enable NumLock for Player 2. P1: WASD, Space; P2: arrows, Numpad 0.
P1 light/heavy/ranged: J/K/L; P2 light/heavy/ranged: Numpad 1/2/3. Grapple: O / Numpad 6. Interaction/revive: L / Numpad 3.
Enter: pause / confirm. F6: manually recall P2. Two XInput controllers can be selected in the launcher. The user has confirmed normal operation with physical controllers; this does not establish full-campaign coverage.

First launch is English; switching language is remembered. Character selection and portraits are in the launcher. Costume selection is hidden in the in-game weapon menu.

## Chinese localization and coexistence

This small package supports the repaired localization from **Shank2-StoryCoop-v0.4-CHS** already installed in the selected game. It verifies its text/font assets before enabling the Chinese renderer. To add or remove the localization itself, use that package's Install-CHS.cmd / Remove-CHS.cmd with all games closed. This ZIP contains no localization payload, movies, game executable, save data or personal settings. Do not run the original 3DM installer over the Steam EXE/DLL.

v0.5 uses separate executable and UI names and preserves v0.4. To remove only v0.5, close its game and run **Remove-v05.cmd**. Both input modes are removed; original files, v0.4 and Chinese assets remain.

## Validation limits

43 actual installer checks cover English/Chinese reconstruction, both input modes, non-default equipment, repeated install, foreign-file refusal, locked-EXE rollback, removal ownership and preservation of originals/settings/older mod files. Four additional old-test upgrade cases pass for English/Chinese and keyboard/controller builds. Enter has 16 native transition tests. This is a test build: full campaign, natural cross-level retention, long sessions and new Steam achievement unlocks are not yet fully verified. The separate Win11 4K cropping report remains unresolved.

---

完整解压后打开 **Launch-Coop.cmd**，选择游戏目录，游戏内进入故事模式。首次默认英文，切换中文后会记住选择。

本版修复回车暂停后无法“继续”：游戏中回车暂停，暂停及装备菜单中回车确认，并防止长按误触。关卡前配装恢复使用原生UI，用户确认装备显示、选择和进入关卡正常。暂停菜单新增“1P 装备／2P 装备”，用户确认只列已解锁武器、实际攻击对应所选武器、两人装备独立；启动器只提供初始配装。武器筛选24项原生测试、回车16项原生测试通过。同一进程双方倒地后重试，两人重新出现且保留武器，已获用户确认和重建角色库存记录支持；自然推进到不同关卡的保留仍待实际游玩确认。地形死亡回到存活队友身旁并等待救援也已获实测确认。

沿用已有分辨率、全屏、画质和音量设置。需要汉化时，先用已提供的 **v0.4-CHS** 包安装修复后的汉化；这个小包可自动识别并验证该汉化，不包含汉化资源或过场视频。勿用原始3DM安装器覆盖Steam EXE/DLL。

本版与v0.4并存。关闭v0.5游戏后双击 **Remove-v05.cmd** 可移除本版，两种输入模式均移除，原版、旧版MOD和汉化保留。用户已确认实体手柄操作正常；全关卡、长时间稳定性、真实新Steam成就仍未验证，Win11 4K裁切问题尚未确认修复。
''',encoding='utf8')
    public={'version':'0.5-test','installer_checks':43,'configured_previous_test_upgrade_cases':4,'native_enter_transitions':16,'native_weapon_visibility_and_selection':24,
            'user_confirmed':['Enter pause/resume and held-key protection','terrain recall remains revivable','separate player weapon menus and swaps','Chinese equipment labels','normal operation with physical controllers','pre-level equipment display, selection and Continue','corrected native weapon filter, corresponding attacks and player independence','same-process both-down retry retains weapons and recreates both players'],
            'pending':['natural transition to a different story level retains equipment','full campaign','long sessions','new Steam achievement unlock','Win11 4K cropping']}
    (OUT/'VALIDATION.json').write_text(json.dumps(public,indent=2))
    names=sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    assert all(p.endswith(('.ps1','.cmd','.json','.md')) for p in names)
    assert not any('settings.json' in p or 'loadouts.json' in p for p in names)
    (OUT/'SHA256SUMS.txt').write_text(''.join(sha((OUT/p).read_bytes())+'  '+p+'\n' for p in names),encoding='ascii');names.append('SHA256SUMS.txt')
    dest=OUT.parent/(OUT.name+'.zip')
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in names:z.write(OUT/p,OUT.name+'/'+p)
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        for p in names:assert z.read(OUT.name+'/'+p)==(OUT/p).read_bytes()
    result={'zip':str(dest),'files':len(names),'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'status':'test build; gameplay checks still pending'}
    (HERE/'archive-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':build()
