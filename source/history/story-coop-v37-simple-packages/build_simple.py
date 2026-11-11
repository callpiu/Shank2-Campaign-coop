"""Produce one install and one uninstall entry for each independent package."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
VERSION='0.10.3'
SOURCES=[('MOD-EN','Shank2-v0.10.2-MOD-EN','ed337e9f3c46f57331a817636b899372ce32d48dabfa7b00724cb4ba75cfbb24'),
    ('CHS','Shank2-v0.10.0-CHS','293c70d0ebae04433d22db5956faddbee1a11324043a76dac0fc4fdc1bb71674'),
    ('MOD-CHS','Shank2-v0.10.1-MOD-CHS','fc4c7c204f5378d58241fd0aa3e773694d406c94711f0e95fa108bb5265e6753')]
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def command(script,args=''):
    return ('@echo off\r\n"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0patch\\'+script+'" '+args+' %*\r\nset "result=%errorlevel%"\r\nif not "%result%"=="0" pause\r\nexit /b %result%\r\n').encode('ascii')


def main():
    reports=[]
    for profile,source_name,digest in SOURCES:
        source=ROOT/'outputs'/(source_name+'.zip')
        with source.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==digest
        dest=ROOT/'outputs'/f'Shank2-v{VERSION}-{profile}'
        refresh='--refresh' in sys.argv
        assert (not dest.exists() or refresh) and not (dest.parent/(dest.name+'.zip')).exists();dest.mkdir(exist_ok=refresh)
        english=profile=='MOD-EN'
        with zipfile.ZipFile(source) as z:
            for entry in z.infolist():
                if entry.is_dir():continue
                relative=Path(entry.filename);assert not relative.is_absolute() and '..' not in relative.parts
                if relative.parts[0]!='patch' and relative.name!='FONT-LICENSE.txt':continue
                target=dest/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(entry))
            previous_readme=z.read('README.md').decode('utf8').replace('\r\n','\n')
        patch=dest/'patch';m=json.loads((patch/'manifest.json').read_text(encoding='utf8'));old=m['version'];m['version']=VERSION
        save(patch/'manifest.json',m)
        p=patch/'Install-Patch.ps1';text=p.read_text(encoding='utf-8-sig')
        old_case="    if ($Action -eq 'Install' -and $state -and $allCurrent) { Write-Output 'Already installed and verified.'; return }"
        new_case="    if ($Action -eq 'Install' -and $state -and $allCurrent) {\n        if ($state.version -ne $manifest.version) { $state.version=$manifest.version; Write-Json $statePath $state }\n        Write-Output 'Already installed and verified.'; return\n    }"
        assert text.count(old_case)==1
        p.write_text(text.replace(old_case,new_case),encoding='utf-8-sig')
        p=patch/'PatchManager.ps1';p.write_text(p.read_text(encoding='utf-8-sig').replace('v'+old,'v'+VERSION),encoding='utf-8-sig')
        install='Install.cmd' if english else '安装.cmd';uninstall='Uninstall.cmd' if english else '卸载.cmd'
        (dest/install).write_bytes(command('PatchManager.ps1'))
        (dest/uninstall).write_bytes(command('Install-Patch.ps1','-Action Remove'))
        if english:
            intro=f'''# Shank 2 Story Co-op MOD v{VERSION}

This package has two shortcuts:

- Install.cmd: open the manager, select the game folder, then choose Install,
  Verify or Remove. The manager also opens the controls tool.
- Uninstall.cmd: restore the previous files directly.

Extract the full archive and keep the patch folder beside these shortcuts.
Exit the game before installing/removing. Launch normally from Steam afterward.
To update the English MOD, install into the same game folder; original backups,
saves, display settings and custom bindings are retained. Uninstall the previous
profile before switching between MOD-only and localized packages.

Coop-Key-Settings.cmd is installed in the GAME folder. Use it to edit bindings;
settings apply the next time the game starts. All package filenames and text are
English. Technical scripts, manifests and checksums are inside patch.

'''
            tail=previous_readme[previous_readme.index('## Co-op features'):]
            text=intro+tail;readme='README.md'
        else:
            description=previous_readme.split('## 安装')[0].split('\n\n',1)[1].strip()
            tail=previous_readme[previous_readme.index('## 双人玩法与键位' if m['includes_mod'] else '## 验证范围与署名'):]
            tail=tail.split('\nEnglish:')[0]
            text=f'''# Shank 2 v{VERSION} · {m['display_name']}

{description}

## 使用方法

1. 完整解压，保留旁边的 `patch` 文件夹。
2. 退出游戏，打开 `安装.cmd`，选择含 bin、data-pc 的游戏目录，然后在管理器内点「安装」。需要检查时点「校验」。
3. 安装后直接从 Steam 启动游戏；原分辨率、全屏和存档保留。
4. 卸载时退出游戏，打开 `卸载.cmd`；也可以在管理器内卸载。

同一类型的旧包可直接更新，保留原件备份与个人设置。三个包独立安装，切换类型前用已安装包卸载。更早的汉化／开发版需先用其原工具恢复，未知改动会被拒绝覆盖。请保留游戏中的 `.shank2-patch` 备份。

根目录只保留安装、卸载、说明及字体署名；内部脚本和校验清单统一放在 `patch`。MOD 的键位设置仍在游戏目录的 `Coop-Key-Settings.cmd`，或管理器的「键位」按钮内打开。纯汉化包不含该功能。

'''+tail+'\n'
            readme='说明.md'
        (dest/readme).write_text(text,encoding='utf8')
        v=json.loads((patch/'VALIDATION.json').read_text(encoding='utf8'));v.update(version=VERSION,simplified_entries=True,game_payload_unchanged=True);save(patch/'VALIDATION.json',v)
        for f in m['files']:
            if f.get('relative'):assert sha((patch/f['relative']).read_bytes())==f['sha256']
        if english:
            for p in dest.rglob('*'):
                assert p.relative_to(dest).as_posix().isascii()
                if p.is_file() and p.suffix.lower() in ('.ps1','.cmd','.md','.json','.txt'):assert not re.search(r'[\u3400-\u9fff\uf900-\ufaff]',p.read_text(encoding='utf-8-sig'))
        reports.append(dict(profile=profile,directory=str(dest),source_directory=str(ROOT/'outputs'/source_name),
            install_entry=install,uninstall_entry=uninstall,readme=readme))
    save(HERE/'prepared.json',reports)
    print('Prepared three v0.10.3 packages with two CMD entries each; game payloads unchanged.')


if __name__=='__main__':main()
