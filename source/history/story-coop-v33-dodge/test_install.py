"""Exercise EN/CHS managed Steam upgrades and exact rollback in temp roots."""
import json
from pathlib import Path
import tempfile
from build_dodge import HERE,SOURCE,sha
from deploy_local import GAME,updater,prepare


def main():
    module=updater();results=[]
    stock=(GAME/'.storycoop-steam/shank2.original.exe').read_bytes()
    assert sha(stock)==module.STOCK
    for row in json.loads((HERE/'builds.json').read_text()):
        lang=row['language']
        with tempfile.TemporaryDirectory(prefix='dodge-install-',dir=HERE) as name:
            root=Path(name);(root/'bin').mkdir();(root/'.storycoop-steam').mkdir();(root/'data-pc/ui').mkdir(parents=True)
            prepare(root/'patch')
            old=(SOURCE/'dev'/f'shank2-story-coop-{lang}.exe').read_bytes()
            for exe in ('shank2.exe','shank2-story-coop.exe'):(root/'bin'/exe).write_bytes(old)
            (root/'.storycoop-steam/shank2.original.exe').write_bytes(stock)
            state=json.dumps(dict(Version=1,Enabled=True,AppID=102840,OriginalSHA256=module.STOCK,
                ActiveModSHA256=sha(old),Language=lang,TestAssists=False)).encode()
            (root/'.storycoop-steam/state.json').write_bytes(state)
            keys=root/'bin/Shank2-Coop-Keys.dat';keys.write_bytes(b'existing user keys')
            dodge=root/'bin/Shank2-Coop-Dodge.dat';dodge.write_bytes(b'existing user dodge keys')
            for n in row['ui_assets']:(root/'data-pc/ui'/n).write_bytes((SOURCE/'dev'/n).read_bytes())
            receipt=module.install(root,lang,save_receipt=False)
            assert sha((root/'bin/shank2.exe').read_bytes())==row['sha256']
            assert (root/'bin/shank2.exe').read_bytes()==(root/'bin/shank2-story-coop.exe').read_bytes()
            assert module.install(root,lang,save_receipt=False)['already_installed']
            assert keys.read_bytes()==b'existing user keys' and dodge.read_bytes()==b'existing user dodge keys'
            module.rollback(receipt)
            assert (root/'bin/shank2.exe').read_bytes()==(root/'bin/shank2-story-coop.exe').read_bytes()==old
            assert (root/'.storycoop-steam/state.json').read_bytes()==state
            assert (root/'.storycoop-steam/shank2.original.exe').read_bytes()==stock
            results.append(dict(language=lang,upgrade=True,steam_sync=True,idempotent=True,
                exact_rollback=True,existing_keys_preserved=True))
    (HERE/'install-validation.json').write_text(json.dumps(dict(passed=True,cases=results),indent=2)+'\n')
    print('EN/CHS upgrade, Steam sync, repeat install, exact rollback and existing keys preservation passed.')


if __name__=='__main__':main()
