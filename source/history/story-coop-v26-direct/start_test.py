"""Start the isolated v26 EXE from a different working directory, without launcher environment."""
from pathlib import Path
import json
import os
import subprocess
import sys
from build import HERE, WORK, sha

if __name__ == '__main__':
    root=WORK/'story-coop-v14-transitions/game'
    query=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }"],check=False)
    if query.returncode: raise RuntimeError('Existing game is open; keeping it and its progress.')
    src=HERE/'dev/shank2-story-coop-chs.exe'
    record=next(row for row in json.loads((HERE/'builds.json').read_text()) if row['language']=='chs')
    assert sha(src.read_bytes())==record['sha256']
    for name, info in record['solo_assets'].items():
        ui=root/'data-pc/ui'
        assert sha((ui/info['native']).read_bytes())==info['native_sha256']
        asset=(HERE/'dev'/name).read_bytes()
        assert sha(asset)==info['sha256']
        (ui/name).write_bytes(asset)
    image=root/'bin/shank2-story-coop-v26-test.exe'
    image.write_bytes(src.read_bytes())
    manifest=HERE/'assist-build.json'
    manifest.write_text(json.dumps([dict(record,name='keyboard-chs.exe')]),encoding='ascii')
    sys.path.insert(0,str(WORK/'story-coop-v15-boss-transitions'))
    from test_assist import install
    env={k:v for k,v in os.environ.items() if k.casefold() not in {'steamappid','steamgameid'}}
    flags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    game=subprocess.Popen([str(image)],cwd=str(root),env=env,creationflags=flags)
    install(game.pid,expected_path=image,manifest_path=manifest,report_dir=HERE)
    print('Direct test PID:', game.pid, flush=True)

