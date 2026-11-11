"""Ensure the existing MOD updater commits and rolls back the Steam entry too."""
import json
from pathlib import Path
import sys
import tempfile

from prepare import HERE,WORK,GAME,prepare
sys.path.insert(0,str(WORK/'story-coop-v28-trait-descriptions'))
from build_descriptions import sha
# The build modules modify sys.path: bind this exact updater by its path.
import importlib.util
spec=importlib.util.spec_from_file_location('description_updater_with_steam',WORK/'story-coop-v28-trait-descriptions/deploy_local.py')
updater=importlib.util.module_from_spec(spec);spec.loader.exec_module(updater)


def main():
    stock=(GAME/'bin/shank2.exe').read_bytes()
    if sha(stock)!=updater.STOCK:stock=(GAME/'.storycoop-steam/shank2.original.exe').read_bytes()
    assert sha(stock)==updater.STOCK
    results=[]
    for lang in ('en','chs'):
        with tempfile.TemporaryDirectory(prefix='steam-sync-',dir=HERE) as folder:
            root=Path(folder);(root/'bin').mkdir();(root/'data-pc/ui').mkdir(parents=True);(root/'.storycoop-steam').mkdir()
            prepare(root/'patch')
            previous=(WORK/'story-coop-v27-traits/dev'/f'shank2-story-coop-{lang}.exe').read_bytes()
            (root/'bin/shank2.exe').write_bytes(previous);(root/'bin/shank2-story-coop.exe').write_bytes(previous)
            (root/'.storycoop-steam/shank2.original.exe').write_bytes(stock)
            state=dict(Version=1,Enabled=True,AppID=102840,OriginalSHA256=updater.STOCK,ActiveModSHA256=sha(previous),Language=lang,TestAssists=False)
            state_bytes=json.dumps(state).encode();(root/'.storycoop-steam/state.json').write_bytes(state_bytes)
            receipt=updater.install(root,lang,save_receipt=False)
            after=(WORK/'story-coop-v28-trait-descriptions/dev'/f'shank2-story-coop-{lang}.exe').read_bytes()
            assert (root/'bin/shank2.exe').read_bytes()==(root/'bin/shank2-story-coop.exe').read_bytes()==after
            assert (root/'.storycoop-steam/shank2.original.exe').read_bytes()==stock
            assert updater.install(root,lang,save_receipt=False)['steam_entry_synced']
            updater.rollback(receipt)
            assert (root/'bin/shank2.exe').read_bytes()==(root/'bin/shank2-story-coop.exe').read_bytes()==previous
            assert (root/'.storycoop-steam/state.json').read_bytes()==state_bytes
            assert (root/'.storycoop-steam/shank2.original.exe').read_bytes()==stock
            results.append(dict(language=lang,automatic_sync=True,idempotent_sync=True,rollback_restores_both_entries=True,original_backup_unchanged=True))
    (HERE/'sync-validation.json').write_text(json.dumps(dict(passed=True,cases=results),indent=2)+'\n')
    print('EN/CHS updater synchronization and exact rollback of both launch entries passed.')


if __name__=='__main__':main()
