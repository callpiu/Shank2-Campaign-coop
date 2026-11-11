"""Exercise real PS5.1 installer in isolated English/Chinese fixtures."""
from pathlib import Path
import subprocess,json,hashlib,shutil,struct,ctypes,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PKG=ROOT/'outputs/Shank2-StoryCoop-v0.5-Test'
GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
PS=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
TESTROOT=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'installer-tests'
report=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def run(root,action,mode='Keyboard',settings=None,fail=False,script=None):
    cmd=[PS,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(script or PKG/'Manage-Coop.ps1'),'-Action',action,'-GamePath',str(root)]
    if not script:cmd+=['-InputMode',mode]
    else:cmd+=['-Group','Text','-NoUI']
    if settings:cmd+=['-LoadoutPath',str(settings)]
    p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace')
    assert (p.returncode!=0)==fail,(cmd,p.stdout,p.stderr)
    report.append({'language':root.name,'action':action,'mode':mode,'expected_failure':fail,'passed':True})

def build_fixture(lang):
    fixture=TESTROOT/lang
    fixture.mkdir(parents=True,exist_ok=True)
    # Stable unique fixture path; refuse reuse with any previous pending state.
    assert not (fixture/'bin/shank2-coop-v05-keyboard.exe').exists()
    files=['bin/shank2.exe','bin/steam_api.dll','bin/binkw32.dll','data-pc/ui/campaignscreen.chui','data-pc/ui/pausedialog.chui','data-pc/ui/singleplayerloadoutscreen.chui']
    if lang=='chs':
        manifest=json.loads((PKG/'patch/manifest.json').read_text())
        files+= [e['path'] for e in manifest['files'] if e['group']=='Text']
    for rel in set(files):
        dest=fixture/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(GAME/rel,dest)
    if lang=='chs':
        run(fixture,'Install',script=ROOT/'outputs/Shank2-StoryCoop-v0.4-CHS/Coop-Localization.ps1')
    (fixture/'users').mkdir(exist_ok=True)
    (fixture/'users/graphics.ini').write_bytes(b'Fullscreen = 1\r\nWidth = 3840\r\nHeight = 2160\r\n')
    for rel in ['bin/shank2-coop-v04-keyboard.exe','data-pc/ui/campaigncoop.chui']:(fixture/rel).write_bytes(b'PRESERVE OLDER MOD FIXTURE')
    protected={str(p.relative_to(fixture)):sha(p) for p in fixture.rglob('*') if p.is_file()}
    return fixture,protected

def test(lang):
    root,protected=build_fixture(lang)
    for mode in ['Keyboard','Pads']:
        run(root,'Verify',mode);run(root,'Install',mode);run(root,'Install',mode)
    custom={'players':[{'skin':'yakuza','melee':'saw','ranged':'shotgun','consumable':'weapon_mine'},{'skin':'sunshine','melee':'scythe','ranged':'uzi','consumable':'weapon_molotov'}]}
    settings=TESTROOT/f'{lang}-loadouts.json';settings.write_text(json.dumps(custom))
    run(root,'Install',settings=settings)
    target=root/'bin/shank2-coop-v05-keyboard.exe';original=target.read_bytes()
    recipe=json.loads((PKG/'keyboard-recipe.json').read_text());o=recipe['config_offset']
    default=(HERE/'final'/f'shank2-coop-v05-keyboard{ "-chs" if lang=="chs" else ""}.exe').read_bytes()
    assert original[:o]==default[:o] and original[o+128:]==default[o+128:]
    catalog=json.loads((PKG/'catalog.json').read_text())
    for i,e in enumerate(custom['players']):
        skin=next(s for s in catalog['skins'] if s['id']==e['skin'])
        expected=[skin['hash']]+[next(w['hash'] for w in catalog['weapons'][skin['family']][slot] if w['id']==e[slot]) for slot in ['melee','ranged','consumable']]+[3]
        assert list(struct.unpack_from('<5I',original,o+64*i+20))==expected
    report.append({'language':lang,'configured_equipment_matches_catalog':True,'config_only_difference':True})
    # Foreign file collision in each owned path must fail before any changes.
    owned=[target]+[root/'data-pc/ui'/s for s in ['campaigncoopv05.chui','pausecoopv05.chui','equipcoopv05.chui']]
    for collision in owned:
        saved=collision.read_bytes();collision.write_bytes(b'UNRELATED FILE')
        before={str(p):sha(p) for p in owned}
        run(root,'Install',fail=True);run(root,'Remove',fail=True)
        assert before=={str(p):sha(p) for p in owned}
        collision.write_bytes(saved)
    # A locked executable causes a real commit failure after UI stages; rollback
    # must retain every prior file and remove staging files.
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.CreateFileW.restype=ctypes.c_void_p
    handle=k.CreateFileW(str(target),0x80000000,1,None,3,0,None)
    assert handle not in (None,ctypes.c_void_p(-1).value)
    before={str(p):sha(p) for p in owned}
    try:run(root,'Install',fail=True)
    finally:k.CloseHandle(ctypes.c_void_p(handle))
    assert before=={str(p):sha(p) for p in owned}
    assert not list(root.rglob('*.tmp'))
    report.append({'language':lang,'locked_executable_rollback':True})
    # Per-mode removal keeps shared UI until the last v0.5 owner; earlier UI stays.
    run(root,'Remove');assert not target.exists() and all(p.exists() for p in owned[1:])
    run(root,'Remove','Pads');assert all(not p.exists() for p in owned)
    for rel,digest in protected.items():assert sha(root/rel)==digest,rel
    report.append({'language':lang,'original_files_settings_and_older_mod_preserved':True})

for language in ['en','chs']:test(language)
(HERE/'installer-tests.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'passed':len(report),'report':str(HERE/'installer-tests.json')}))
