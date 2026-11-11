"""Run the exact new image in the isolated game with process-only assists."""
import json
import argparse
import os
import subprocess
import sys
from build_traits import HERE, PREVIOUS, sha

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--no-assists',action='store_true',help='Current trait-damage verification explicitly requires native damage.')
    options=parser.parse_args()
    root=HERE.parent/'story-coop-v14-transitions/game'
    query=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }"],check=False)
    if query.returncode: raise RuntimeError('A Shank 2 window is open. Keep its progress.')
    row=next(row for row in json.loads((HERE/'builds.json').read_text()) if row['language']=='chs')
    asset_folder=root/'data-pc/ui'
    for filename,info in row['solo_assets'].items():
        assert sha((asset_folder/filename).read_bytes())==info['sha256']
    src=(HERE/'dev/shank2-story-coop-chs.exe').read_bytes()
    assert sha(src)==row['sha256']
    target=root/'bin/shank2-story-coop-v27-test.exe'
    target.write_bytes(src)
    manifest=HERE/'assist-build.json'
    manifest.write_text(json.dumps([dict(row,name='keyboard-chs.exe')]),encoding='ascii')
    sys.path.insert(0,str(HERE.parent/'story-coop-v15-boss-transitions'))
    from test_assist import install
    env={k:v for k,v in os.environ.items() if k.casefold() not in {'steamappid','steamgameid'}}
    game=subprocess.Popen([str(target)],cwd=root,env=env,
                          creationflags=subprocess.CREATE_NEW_PROCESS_GROUP|subprocess.DETACHED_PROCESS)
    if not options.no_assists:
        install(game.pid,expected_path=target,manifest_path=manifest,report_dir=HERE)
    (HERE/'current-test.json').write_text(json.dumps(dict(pid=game.pid,path=str(target),
        sha256=row['sha256'],assists_requested=not options.no_assists,
        purpose='Survival traits: original projectile gate, no target replacement'),indent=2)+'\n',encoding='utf8')
    print('Trait test PID:',game.pid,flush=True)
