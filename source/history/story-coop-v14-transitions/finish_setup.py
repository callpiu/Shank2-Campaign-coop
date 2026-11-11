"""Preserve the copied legacy executable rejected by the guard; finish new setup."""
import hashlib
import json
from prepare import GAME, HERE, PATCH, ROOT, run

archive=HERE/'copied-legacy-binaries'
archive.mkdir(exist_ok=True)
for name in ('shank2-coop-v08-keyboard.exe','shank2-coop-v08-keyboard.exe.coop-install.json'):
    source=GAME/'bin'/name;target=archive/name
    assert source.parent.resolve()==(HERE/'game/bin').resolve() and not target.exists()
    source.rename(target)
run(PATCH,'Manage-Coop.ps1','Install','-InputMode','Keyboard')
run(PATCH,'Manage-Coop.ps1','Verify','-InputMode','Keyboard')
image=GAME/'bin/shank2-coop-v08-keyboard.exe'
expected=ROOT/'work/story-coop-v12-live-character/dev/keyboard-chs.exe'
assert image.read_bytes()==expected.read_bytes()
(HERE/'setup.json').write_text(json.dumps(dict(game=str(GAME),sha256=hashlib.sha256(image.read_bytes()).hexdigest(),
    release_exact=True,localization='96 files verified by release installer',live_game_started=False),indent=2)+'\n',encoding='utf-8')
