"""Verify reversible installation for EN/CHS without touching live game files."""
import json
from pathlib import Path
import tempfile
import sys

from build_descriptions import HERE, PREVIOUS, sha
sys.path.insert(0,str(HERE))
from deploy_local import GAME, STOCK, install, rollback


def main():
    results=[]
    for language in ('en','chs'):
        with tempfile.TemporaryDirectory(prefix='trait-ui-install-',dir=HERE) as folder:
            root=Path(folder);(root/'bin').mkdir();(root/'data-pc/ui').mkdir(parents=True)
            stock=(GAME/'bin/shank2.exe').read_bytes()
            if sha(stock)!=STOCK:stock=(GAME/'.storycoop-steam/shank2.original.exe').read_bytes()
            assert sha(stock)==STOCK
            (root/'bin/shank2.exe').write_bytes(stock)
            old=(PREVIOUS/'dev'/f'shank2-story-coop-{language}.exe').read_bytes()
            (root/'bin/shank2-story-coop.exe').write_bytes(old)
            settings=root/'bin/Shank2-Coop-Keys.dat';settings.write_bytes(b'unchanged-control-settings')
            unrelated=root/'data-pc/ui/campaignscreen.chui';unrelated.write_bytes(b'unchanged HUD')
            for existing in (False,True):
                asset=root/'data-pc/ui'/f'cooppreselv28{language}.chui'
                solo=root/'data-pc/ui'/f'coopsolo28sel{language}.chui'
                if existing:
                    asset.write_bytes(b'old resource to restore')
                    solo.write_bytes(b'old solo resource to restore')
                receipt=install(root,language,save_receipt=False)
                assert settings.read_bytes()==b'unchanged-control-settings'
                assert unrelated.read_bytes()==b'unchanged HUD'
                assert install(root,language,save_receipt=False)['already_installed']
                rollback(receipt)
                assert (root/'bin/shank2-story-coop.exe').read_bytes()==old
                assert asset.read_bytes()==b'old resource to restore' if existing else not asset.exists()
                assert solo.read_bytes()==b'old solo resource to restore' if existing else not solo.exists()
                results.append(dict(language=language,existing_resource=existing,install=True,idempotent=True,rollback=True,settings_preserved=True))
    (HERE/'install-validation.json').write_text(json.dumps(dict(passed=True,cases=results),indent=2)+'\n')
    print('EN/CHS fresh/existing resource install, repeat install, exact rollback and settings preservation passed.')


if __name__=='__main__':main()
