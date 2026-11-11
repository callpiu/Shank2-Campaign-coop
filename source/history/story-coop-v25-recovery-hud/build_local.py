"""Clear the partner's stale full-screen blood effects on native recovery."""
import base64
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import uuid

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'story-coop-v24-boss-bar'
sys.path.insert(0, str(PREVIOUS))
from build_local import DIAG, Ks, KS_ARCH_X86, KS_MODE_32, pefile, sha, dump

spec = importlib.util.spec_from_file_location('boss_local_installer', PREVIOUS / 'deploy_local.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
from deploy_local import GAME, run, replace

SITE = 0x53f27c
BEFORE = bytes.fromhex('8bceffd05f')
CONTINUE = 0x53f281
RED_LOOP = 0x8ec3ab67
HIT_LOOP = 0xe824cec2
HIT = 0x748537b7


def routine(asm, address, diag, combat, continuation):
    return asm(f'''pushfd
        pushad
        cmp dword ptr [{diag+4:#x}],5
        jne original
        cmp dword ptr [esp+40],{RED_LOOP:#x}
        jne original
        cmp dword ptr [esp+44],2
        jne original
        mov eax,[esp+76]
        test eax,eax
        jz original
        mov ecx,[eax+8]
        test ecx,ecx
        jz original
        cmp ecx,[{diag+16:#x}]
        jne original
        cmp ecx,[{diag+12:#x}]
        je original
        mov eax,[ecx+0x20]
        test eax,eax
        jz original
        cmp eax,[{diag+36:#x}]
        jne original
        call {combat:#x}
        test eax,eax
        jz original
        cmp dword ptr [eax+0xa0],0
        jle original
        cmp dword ptr [eax+0x200],0
        jle original
        sub esp,36
        movdqu [esp],xmm0
        movdqu [esp+16],xmm1
        mov dword ptr [esp+32],0x3ea8f5c3
        movss xmm0,[eax+0xa0]
        movss xmm1,[eax+0x200]
        mulss xmm1,[esp+32]
        ucomiss xmm0,xmm1
        movdqu xmm0,[esp]
        movdqu xmm1,[esp+16]
        lea esp,[esp+36]
        jb original
        mov esi,[esp+4]
        mov edi,[esp+36]
        mov ebx,[esp+28]
        push 2
        push {HIT_LOOP:#x}
        push edi
        mov ecx,esi
        call ebx
        push 2
        push {HIT:#x}
        push edi
        mov ecx,esi
        call ebx
        original:
        popad
        popfd
        mov ecx,esi
        call eax
        pop edi
        jmp {continuation:#x}''', address)


def prepare():
    previous = PREVIOUS/'candidate/patch'
    previous_hashes = json.loads((previous/'previous-baselines.json').read_bytes())
    prepared = {'previous-baselines.json': None}
    targets = {}
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda source, address: bytes(ks.asm(source, address)[0])
    for row in json.loads((PREVIOUS/'builds.json').read_bytes()):
        mode, lang = row['mode'], row['lang']
        name = f'{mode}-{lang}-addon.json'
        recipe = json.loads((previous/name).read_bytes())
        assert recipe['output_sha256'] == row['sha256']
        suffix = '-chs' if lang == 'chs' else ''
        base = HERE.parent/'story-coop-v05/final'/f'shank2-coop-v05-{mode}{suffix}.exe'
        source = base.read_bytes()
        before = installer.reconstruct(recipe, source)
        image = pefile.PE(data=before)
        offset = lambda va: image.get_offset_from_rva(va-0x400000)
        code = int(row['code'],16)+0x100
        blob = routine(asm, code, DIAG, 0x40bb60, CONTINUE)
        assert len(blob) <= 0x100 and before[offset(code):offset(code)+len(blob)] == b'\xcc'*len(blob)
        assert before[offset(SITE):offset(SITE)+len(BEFORE)] == BEFORE
        jump = asm(f'jmp {code:#x}', SITE)
        assert len(jump) == len(BEFORE)
        after = bytearray(before)
        after[offset(SITE):offset(SITE)+len(jump)] = jump
        after[offset(code):offset(code)+len(blob)] = blob
        recipe['patches'].append(dict(offset=offset(SITE),before=BEFORE.hex(),after=jump.hex()))
        recipe['patches'].sort(key=lambda patch:patch['offset'])
        previous_hashes[mode].append(recipe['output_sha256'])
        recipe.update(output_sha256=sha(after),append=base64.b64encode(after[recipe['source_size']:]).decode('ascii'))
        assert installer.reconstruct(recipe,source) == after
        prepared[name] = dump(recipe)
        targets[mode,lang] = (before,bytes(after))
    prepared['previous-baselines.json'] = dump(previous_hashes)
    return prepared, targets


def deploy(prepared, targets):
    assert GAME.resolve() == GAME
    run('-Command', "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }")
    patch = GAME/'patch'
    files = {patch/name: data for name,data in prepared.items()}
    saved = {path:path.read_bytes() for path in files}
    assert all(data == (PREVIOUS/'candidate/patch'/path.name).read_bytes() for path,data in saved.items())
    keyboard = GAME/'bin/shank2-coop-v08-keyboard.exe'
    receipt = keyboard.with_name(keyboard.name+'.coop-install.json')
    receipt_bytes = receipt.read_bytes()
    installed = json.loads(receipt_bytes)
    current = keyboard.read_bytes()
    before, after = targets['keyboard','chs']
    assert sha(current) == installed['installed_sha256'] and sha(before) == installed['baseline_sha256']
    expected = bytearray(current)
    for offset,(old,new) in enumerate(zip(before,after)):
        if old != new:
            assert current[offset] == old
            expected[offset] = new
    manifest = json.loads((patch/'manifest.json').read_bytes())
    assert all(sha((GAME/name).read_bytes()) == digest for name,digest in manifest['guards'].items())
    saved.update({keyboard:current,receipt:receipt_bytes})
    backup = HERE/('local-backup-'+uuid.uuid4().hex[:8])
    for path,data in saved.items():
        destination = backup/path.relative_to(GAME)
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(data)
    args = ['-GamePath',str(GAME),'-InputMode','Keyboard','-LoadoutPath',str(backup/receipt.relative_to(GAME))]
    with tempfile.TemporaryDirectory(prefix='preflight-', dir=HERE) as temporary:
        stage = Path(temporary).resolve()
        assert stage.parent == HERE
        for path in patch.iterdir():
            if path.is_file() and path.name not in ('loadouts.json','launcher-settings.json'):
                (stage/path.name).write_bytes(files.get(path,path.read_bytes()))
        run('-File',str(stage/'Manage-Coop.ps1'),'-Action','Verify',*args)
    try:
        run('-Command', "if (Get-Process -Name 'shank2*' -ErrorAction SilentlyContinue) { exit 9 }")
        for path,data in files.items():
            replace(path,data)
        run('-File',str(patch/'Manage-Coop.ps1'),'-Action','Install',*args)
        assert keyboard.read_bytes() == expected
        run('-File',str(patch/'Manage-Coop.ps1'),'-Action','Verify',*args)
        assert all(sha((GAME/name).read_bytes()) == digest for name,digest in manifest['guards'].items())
    except BaseException:
        for path,data in saved.items():
            if path.read_bytes() != data:
                replace(path,data)
        raise
    report = dict(game=str(GAME),backup=str(backup),sha256=sha(expected),four_variants_exact=True,
                  combo_and_boss_fixes_preserved=True,game_started=False,gameplay_verified=False,archive_generated=False)
    (HERE/'local-install.json').write_bytes(dump(report))
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    import subprocess
    from test_recovery import test
    test(HERE, routine, Ks, KS_ARCH_X86, KS_MODE_32, RED_LOOP, HIT_LOOP, HIT)
    prepared, targets = prepare()
    candidate = HERE/'candidate/patch'
    candidate.mkdir(parents=True,exist_ok=True)
    for name,data in prepared.items():
        (candidate/name).write_bytes(data)
    if '--install' in sys.argv:
        try:
            deploy(prepared,targets)
        except subprocess.CalledProcessError as error:
            print(error.stdout or '',error.stderr or '',file=sys.stderr)
            raise
