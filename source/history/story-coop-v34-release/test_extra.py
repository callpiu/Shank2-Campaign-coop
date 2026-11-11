"""Check public CMD routing, safe paths, Steam repair, and installed manifests."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from build_release import HERE,ROOT,PROFILES,save
from test_release import PS,fixture,snapshot,run,installed


def main():
    results=[]
    with tempfile.TemporaryDirectory(prefix='additional-检查 空格-',dir=HERE) as name:
        temp=Path(name)
        for profile,(folder,mod,chs) in PROFILES.items():
            package=ROOT/'outputs'/folder;m=json.loads((package/'patch/manifest.json').read_text(encoding='utf-8-sig'))
            game=temp/profile;before=fixture(game,m)
            run(package,game,'Install');installed(game,m)
            subprocess.run([sys.executable,r'G:\DeepSeekData\.codex\skills\localize-game-text\scripts\verify_overlay_manifest.py',
                '--manifest',str(package/'patch/manifest.json'),'--root',str(game),'--json',str(HERE/(profile+'-installed-manifest.json'))],check=True,stdout=subprocess.DEVNULL)
            # Simulate Steam restoring the original entry: Verify rejects stale
            # installation; Install repairs it without losing original backups.
            original=(game/'.shank2-patch/backups/bin/shank2.exe').read_bytes();(game/'bin/shank2.exe').write_bytes(original)
            run(package,game,'Verify',True);run(package,game,'Install');installed(game,m)
            (game/'bin/shank2.exe').write_bytes(original);run(package,game,'Remove');assert snapshot(game)==before
            results.append(dict(profile=profile,installed_manifest=True,steam_repair=True,uninstall_after_steam_restore=True))
        # Test ASCII and Chinese CMD wrappers from a path containing spaces.
        for profile,(folder,mod,chs) in PROFILES.items():
            source=ROOT/'outputs'/folder;stub=temp/('入口 测试 '+profile);(stub/'patch').mkdir(parents=True)
            for p in source.glob('*.cmd'):shutil.copyfile(p,stub/p.name)
            for p in source.glob('*.ps1'):shutil.copyfile(p,stub/p.name)
            marker=stub/'marker.txt'
            (stub/'patch/Install-Patch.ps1').write_text("param([string]$Action,[string]$GamePath,[switch]$NoUI)\n[IO.File]::WriteAllText((Join-Path (Split-Path -Parent $PSScriptRoot) 'marker.txt'),($Action+'|'+$GamePath))\n",encoding='utf-8-sig')
            (stub/'patch/PatchManager.ps1').write_text("param([string]$GamePath)\n[IO.File]::WriteAllText((Join-Path (Split-Path -Parent $PSScriptRoot) 'marker.txt'),('GUI|'+$GamePath))\n",encoding='utf-8-sig')
            checks=[]
            for p in stub.glob('*.cmd'):
                action='GUI' if 'Installer' in p.name or '管理器' in p.name else ('Remove' if 'Uninstall' in p.name or '卸载' in p.name else ('Verify' if 'Verify' in p.name or '检查' in p.name else 'Install'))
                game=Path('G:/样例 游戏 目录')
                command='cmd.exe /d /s /c "'+subprocess.list2cmdline([str(p),'-GamePath',str(game)])+'"'
                result=subprocess.run(command,input='',capture_output=True,text=True,encoding='utf8',errors='replace',timeout=20)
                assert result.returncode==0,(p.name,result.stdout,result.stderr)
                actual=marker.read_text(encoding='utf8')
                assert actual==action+'|'+str(game),(p.name,actual)
                checks.append(p.name)
            results.append(dict(profile=profile,public_cmd_routes=checks,unicode_space_paths=True))
        # Unsafe manifest paths fail before writes.
        source=ROOT/'outputs'/PROFILES['MOD-EN'][0];m=json.loads((source/'patch/manifest.json').read_text(encoding='utf-8-sig'))
        game=temp/'path-guards';before=fixture(game,m)
        bad=temp/'bad-path';(bad/'patch').mkdir(parents=True)
        for p in ('Install-Patch.ps1','Game-Paths.ps1'):shutil.copyfile(source/'patch'/p,bad/'patch'/p)
        m['files'][0]['path']='../escape.bin';save(bad/'patch/manifest.json',m)
        run(bad,game,'Install',True);assert snapshot(game)==before and not (temp/'escape.bin').exists()
        junction=temp/'game-junction'
        script="New-Item -ItemType Junction -Path $args[0] -Target $args[1] | Out-Null"
        helper=temp/'junction.ps1';helper.write_text(script)
        subprocess.run([str(PS),'-NoProfile','-File',str(helper),str(junction),str(game)],check=True)
        try:run(source,junction,'Install',True);assert snapshot(game)==before
        finally:junction.rmdir()
        ui=game/'data-pc/ui';held=game/'data-pc/ui-original';ui.rename(held)
        outside=temp/'outside-ui';shutil.copytree(held,outside)
        subprocess.run([str(PS),'-NoProfile','-File',str(helper),str(ui),str(outside)],check=True)
        try:run(source,game,'Install',True);assert not (outside/'coopsolo28selen.chui').exists()
        finally:ui.rmdir();held.rename(ui)
        assert snapshot(game)==before
        results.append(dict(unsafe_manifest_refused=True,reparse_root_refused=True,reparse_payload_parent_refused=True))
    save(HERE/'extra-validation.json',dict(passed=True,checks=results))
    print('Three installed manifests, Steam repair, 24 public CMD routes and traversal/junction guards passed.')


if __name__=='__main__':main()
