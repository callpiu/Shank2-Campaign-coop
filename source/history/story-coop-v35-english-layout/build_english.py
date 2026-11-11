"""Build the English-only v0.10.1 release without changing the frozen CHS packages."""
import json
from pathlib import Path
import re
import zipfile
import sys

HERE=Path(__file__).resolve().parent;WORK=HERE.parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(WORK/'story-coop-v34-release'))
from build_release import sha,save
SOURCE=ROOT/'outputs/Shank2-v0.10.0-MOD-EN.zip'
SOURCE_SHA='a868d8a2042f62c454119f8e606ddc0361089b5d9c20d30934f3a18f883f4d38'
DEST=ROOT/'outputs/Shank2-v0.10.1-MOD-EN'
CJK=re.compile(r'[\u3400-\u9fff\uf900-\ufaff]')


def english_controls(text):
    text=text.lstrip('\ufeff')
    # Keep the established key serialization/save logic and existing defaults.
    # Project every bilingual T call to its English string, then remove the
    # unused Chinese label table and hide language selection in this edition.
    text=re.sub(r"\bT ('(?:[^']|'')*') '(?:[^']|'')*'",lambda m:'T '+m[1]+' '+m[1],text)
    text=re.sub(r"\$zh = @\([\s\S]*?\)\r?\nfunction T",'$zh = $en\nfunction T',text,count=1)
    text=text.replace("'简体中文'","'English'")
    text=text.replace("$langBox.SelectedIndex = [int]($script:language -eq 'zh')", "$script:language='en'\n$langBox.SelectedIndex=0\n$langBox.Visible=$false")
    replacements={'键位设置':'Co-op Controls','切换双人镜头':'Toggle co-op camera',
        '向左闪避（右摇杆）':'Dodge left (right stick)','向右闪避（右摇杆）':'Dodge right (right stick)'}
    for before,after in replacements.items():text=text.replace(before,after)
    text=text.replace('→','->')
    assert not CJK.search(text),'Untranslated string in English controls.'
    return text


def english_manager(text):
    lines=[]
    for line in text.splitlines():
        if line.startswith('$managerHint.Text='):
            line='$managerHint.Text="Close the game before installing/removing. Launch normally from Steam after installation.`r`nOriginal files are backed up under .shank2-patch in the game directory."'
        # All remaining bilingual captions use an English / Chinese pair.
        line=re.sub(r"'([^'\r\n]*[\u3400-\u9fff][^'\r\n]*)'",lambda m:"'"+m[1].split(' /')[0]+"'",line)
        lines.append(line.replace('v0.10.0','v0.10.1').replace('—','-'))
    result='\n'.join(lines)+'\n';assert not CJK.search(result)
    return result


README='''# Shank 2 Story Co-op MOD v0.10.1

Local two-player campaign for the Steam version of Shank 2. This English-only
package contains no Chinese localization, replacement fonts or movie assets.
All package filenames, instructions, installer and controls UI are in English.

## Install and play

1. Extract the entire archive to a new folder. Exit the game.
2. Run Start-Installer.cmd, select the Shank 2 folder containing bin and data-pc,
   and click Install. Alternatively, run Install.cmd.
3. Launch Shank 2 normally from Steam. Select Campaign Mode > Local Co-op.
4. Run Coop-Key-Settings.cmd in the GAME folder to change bindings or select two
   XInput controllers. Save before restarting the game to apply new bindings.

Use Verify.cmd to check the installation. Uninstall.cmd restores original files.
Keep the .shank2-patch backup folder until uninstall. Saves, display settings and
custom key files are preserved. The mod uses the game's saved resolution and
fullscreen settings. No separate launcher is needed to enable co-op.

To update v0.10.0 English MOD, exit the game and install this package into the
same folder; original backups and personal bindings are retained. To switch from
another package/profile, uninstall it with its own package first. Restore older
mods and localizations using their original tools, or use a clean English game
folder. Unknown modified files are refused. Steam file verification may restore
the original executable; rerun Install to repair the mod afterward.

## Co-op features

- Independent controls, health, equipment, consumables and scores.
- Both players choose character and equipment before each campaign level.
- All 17 characters are available, with applicable Survival health/damage traits.
  Weapons still follow campaign unlocks. Character names, traits and biographies
  now use separate areas in the English selection panel.
- Either player can revive the other; retry only after both players are down.
  Retry retains individual scores. Terrain deaths return downed players nearby.
- Pause-menu equipment selection for each player. Character changes there apply
  on retry or the next level.
- Shared camera with smooth zoom, manual P2 recall, and the previously confirmed
  boss-grab, cutscene-transition, recovery-overlay and selection UI fixes.

## Default keyboard controls

Enable NumLock for P2.

| Action | P1 | P2 |
| --- | --- | --- |
| Move | WASD | Arrow keys |
| Jump / Confirm | Space | Numpad 0 |
| Light attack | J | Numpad 1 |
| Heavy weapon | K | Numpad 2 |
| Ranged attack | L | Numpad 3 |
| Grapple | O | Numpad 6 |
| Dodge left / right | Z / C | Numpad 8 / 9 |

Enter pauses/resumes and confirms menus. F6 recalls P2. F7 toggles the shared
camera. Other actions and custom bindings are available in the controls tool.
Two physical XInput controllers are also supported.

## Requirements and validation

Windows PowerShell 5.1 and a working Steam installation of Shank 2 are required.
Supported original bin/shank2.exe SHA-256:
3cd7aeb0d9f135dc82c4bba491463ecb85fec9aa33b9189ab2cee5160dd045d3

The installer reconstructs the modified executable from your own verified copy.
No complete game EXE/DLL, save, personal settings, invincibility, one-hit-kill
assist or diagnostic tool is distributed. Original Steam and Bink DLLs remain
unchanged. Steam APIs are retained; achievement conditions are not bypassed.

Many co-op features were confirmed by the user in the Chinese edition. The user
also confirmed that Classic, Boogie and Sunshine display complete names, traits
and biographies without overlap in this English update. All 17 English layouts
passed static checks; full-campaign coverage remains incomplete.
'''


def main():
    assert sha(SOURCE.read_bytes())==SOURCE_SHA
    refresh='--refresh' in sys.argv
    assert (not DEST.exists() or refresh) and not (DEST.parent/(DEST.name+'.zip')).exists()
    DEST.mkdir(exist_ok=refresh)
    with zipfile.ZipFile(SOURCE) as z:
        for entry in z.infolist():
            if entry.is_dir() or entry.filename=='SHA256SUMS.txt' or not entry.filename.isascii():continue
            relative=Path(entry.filename);assert not relative.is_absolute() and '..' not in relative.parts
            target=DEST/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(entry))
    patch=DEST/'patch'
    (patch/'payload/Coop-Key-Settings.cmd').write_bytes((WORK/'story-coop-v26-direct/Coop-Key-Settings.cmd').read_bytes())
    manifest=json.loads((patch/'manifest.json').read_text(encoding='utf8'));manifest['version']='0.10.1'
    row=next(r for r in json.loads((WORK/'story-coop-v33-dodge/builds.json').read_text(encoding='utf8')) if r['language']=='en')
    for name,digest in row['ui_assets'].items():
        data=(WORK/'story-coop-v33-dodge/dev'/name).read_bytes();assert sha(data)==digest
        (patch/'payload/data-pc/ui'/name).write_bytes(data)
    for p in (patch/'Coop-Key-Settings.ps1',patch/'payload/patch/Coop-Key-Settings.ps1'):
        p.write_text(english_controls((WORK/'story-coop-v26-direct/Coop-Key-Settings.ps1').read_text(encoding='utf-8-sig')),encoding='utf-8-sig')
    for name in ('Install-Patch.ps1','PatchManager.ps1'):
        p=patch/name;p.write_text(english_manager(p.read_text(encoding='utf-8-sig')),encoding='utf-8-sig')
    for f in manifest['files']:
        if f.get('relative'):
            data=(patch/f['relative']).read_bytes();f.update(size=len(data),sha256=sha(data))
    save(patch/'manifest.json',manifest)
    confirmed=(HERE/'user-validation.json').exists()
    save(patch/'VALIDATION.json',dict(version='0.10.1',english_only=True,layout_visual_pending=not confirmed,
        user_confirmed_characters=['Classic','Boogie','Sunshine'] if confirmed else [],
        native_mod_exe_unchanged=True,test_assists=False))
    (DEST/'README.md').write_text(README,encoding='utf8')
    for p in DEST.rglob('*'):
        assert p.relative_to(DEST).as_posix().isascii()
        if p.is_file() and p.suffix.lower() in ('.md','.ps1','.cmd','.json','.txt'):
            assert not CJK.search(p.read_text(encoding='utf-8-sig')),p
    save(HERE/'prepared.json',dict(directory=str(DEST),profile='MOD-EN',version='0.10.1',exe_sha256=row['sha256']))
    print('Prepared English-only v0.10.1 with separate title, traits and biography bands.')


if __name__=='__main__':main()
