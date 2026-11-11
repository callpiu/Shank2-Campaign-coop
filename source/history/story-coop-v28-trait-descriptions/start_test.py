"""Start one isolated bilingual UI test, preserving any running Shank game."""
import argparse
import json
import os
import subprocess
import sys

from build_descriptions import HERE, WORK, sha, pefile, BASE, Ks, KS_ARCH_X86, KS_MODE_32


def main():
    args=argparse.ArgumentParser()
    args.add_argument('--language',choices=('en','chs'),default='chs')
    options=args.parse_args()
    check=subprocess.run(['powershell.exe','-NoProfile','-Command',
        "if (Get-CimInstance Win32_Process -Filter \"Name LIKE 'shank2%'\") {exit 9}"],check=False)
    if check.returncode:raise RuntimeError('Preserve running Shank game; do not restart it.')
    assert json.loads((HERE/'validation.json').read_text())['passed']
    row=next(x for x in json.loads((HERE/'builds.json').read_text()) if x['language']==options.language)
    game=WORK/'story-coop-v14-transitions/game'
    for name,digest in row['ui_assets'].items():
        asset=HERE/'dev'/name
        assert sha(asset.read_bytes())==digest
        (game/'data-pc/ui'/name).write_bytes(asset.read_bytes())
    source=HERE/'dev'/f'shank2-story-coop-{options.language}.exe'
    assert sha(source.read_bytes())==row['sha256']
    target=game/'bin'/f'shank2-story-coop-v28-{options.language}-test.exe'
    # Test-only loader observation. Record the actual resource string used
    # by the native constructor, including selectors created before co-op
    # mode was chosen. No gameplay or normal-install code is changed.
    raw=bytearray(source.read_bytes());pe=pefile.PE(data=raw,fast_load=True)
    off=lambda a:pe.get_offset_from_rva(a-BASE)
    c,d=int(row['code'],16),int(row['data'],16)
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    routine=bytes(ks.asm(f'''pushfd;pushad;mov eax,[esp+48]
        mov [{d+0x5a0}],eax;mov eax,[{d+4}];mov [{d+0x5a4}],eax
        inc dword ptr [{d+0x5a8}];popad;popfd;jmp 0x5e3170''',c+0x1e00)[0])
    assert raw[off(c+0x1e00):off(c+0x1e00)+len(routine)]==b'\xcc'*len(routine)
    raw[off(c+0x1e00):off(c+0x1e00)+len(routine)]=routine
    at=0x68e15a
    assert raw[off(at):off(at)+5]==bytes(ks.asm('call 0x5e3170',at)[0])
    raw[off(at):off(at)+5]=bytes(ks.asm(f'call {c+0x1e00}',at)[0])
    target.write_bytes(raw)
    env={k:v for k,v in os.environ.items() if k.casefold() not in {'steamappid','steamgameid'}}
    process=subprocess.Popen([str(target)],cwd=game,env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP|subprocess.DETACHED_PROCESS)
    report=dict(pid=process.pid,path=str(target),sha256=sha(raw),canonical_sha256=row['sha256'],language=options.language,
        loader_observation=hex(d+0x5a0),ui_assets=row['ui_assets'],
        assists_enabled=False,reason='User requested continuing tests with invincibility and one-hit kills disabled.',
        asset=str(game/'data-pc/ui'/row['description_asset']),asset_sha256=row['ui_assets'][row['description_asset']])
    (HERE/'current-test.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
