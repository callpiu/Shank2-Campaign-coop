"""Build v0.5 recipes without modifying stable v0.4 releases or game files."""
from pathlib import Path
import sys,json,hashlib,subprocess,shutil,difflib,base64
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path[:0]=[str(HERE),str(HERE.parent/'story-coop-v04'),str(HERE.parent/'chs-compat')]
from build_terrain import build as terrain
from build_menu import build as menu,ui,equipment_ui
from build_compat import patch_exe,translated_slots,reconstruct
sha=lambda b:hashlib.sha256(b).hexdigest()
GAME=Path(r'E:\SteamLibrary\steamapps\common\Shank 2')
OUT=ROOT/'outputs/Shank2-StoryCoop-v0.5-Test'
OUT.mkdir(exist_ok=True)
FINAL=HERE/'final';FINAL.mkdir(exist_ok=True)

def ui_recipe(source,target,path):
    a=source.read_bytes();b=target.read_bytes();chunks=[]
    for tag,i,j,u,v in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag=='equal':chunks.append({'copy':i,'length':j-i})
        elif v>u:chunks.append({'literal':base64.b64encode(b[u:v]).decode()})
    rebuilt=b''.join(a[c['copy']:c['copy']+c['length']] if 'copy' in c else base64.b64decode(c['literal']) for c in chunks)
    assert rebuilt==b
    r={'format':2,'input_sha256':sha(a),'output_sha256':sha(b),'source_size':len(a),'target_size':len(b),'chunks':chunks}
    path.write_text(json.dumps(r,indent=2));return r

def build():
    # Preserve native v0.4 keyboard/controller configurations. Only defaults are
    # exported: no live process state, account paths or personal loadout files.
    slots=translated_slots()
    original=(GAME/'bin/shank2.exe').read_bytes()
    for mode in ['keyboard','pads']:
        base=HERE.parent/'story-coop-v04/final'/f'shank2-coop-v04-{mode}.exe'
        middle=FINAL/f'{mode}-terrain.exe';target=FINAL/f'shank2-coop-v05-{mode}.exe'
        terrain(base,middle);menu(middle,target,versioned=True,write_ui=False)
        metadata=json.loads(base.with_suffix('.coop.json').read_text())
        metadata.update(version='0.5-test',output_sha256=sha(target.read_bytes()))
        target.with_suffix('.coop.json').write_text(json.dumps(metadata,indent=2))
        subprocess.run([sys.executable,str(HERE.parent/'story-coop-v02/export.py'),str(target),str(OUT/f'{mode}-recipe.json')],check=True)
        cn,recipe,_,_=patch_exe(target.read_bytes(),slots)
        assert reconstruct(target.read_bytes(),recipe)==cn
        (FINAL/f'shank2-coop-v05-{mode}-chs.exe').write_bytes(cn)
        (OUT/f'{mode}-chs-recipe.json').write_text(json.dumps(recipe,indent=2))
        # Original Steam API imports stay present in both native builds.
    cnroot=HERE.parent/'chs-compat/extracted/cn'
    for lang,source,english in [('en',GAME,True),('chs',cnroot,False)]:
        for stem,src,fn in [('pause','pausedialog.chui',ui),('equip','singleplayerloadoutscreen.chui',equipment_ui)]:
            target=FINAL/f'{stem}-{lang}.chui'
            if stem=='pause':fn(source/'data-pc/ui'/src,target,english=english)
            else:fn(source/'data-pc/ui'/src,target)
            ui_recipe(source/'data-pc/ui'/src,target,OUT/f'{stem}-{lang}-recipe.json')
    for name in ['catalog.json','ui-recipe.json','ui-chs-recipe.json']:
        shutil.copy2(ROOT/'outputs/Shank2-StoryCoop-v0.4-CHS'/name,OUT/name)
    for name in ['Coop-Launcher.ps1','Portraits.ps1','Launcher-Strings.ps1','Launcher-Preferences.ps1','Game-Paths.ps1','Start-Coop.ps1','Remove-Coop.ps1']:
        source=HERE/name if (HERE/name).exists() else HERE.parent/'story-coop-v04'/name
        text=source.read_text(encoding='utf-8-sig').replace('v0.4','v0.5')
        if name=='Launcher-Strings.ps1':
            text=text.replace('Choose a character and weapons for each player. Applied when you enter a level.','Choose starting equipment. Change weapons from the pause menu during play.')
            text=text.replace('分别选择角色和三格装备；进入关卡后采用这里保存的配装。','选择初始角色与装备；游戏中可从暂停菜单更换武器。')
        (OUT/name).write_text(text,encoding='utf-8-sig')
    (OUT/'Manage-Coop.ps1').write_text((HERE/'Manage-Coop.ps1').read_text(encoding='utf-8-sig'),encoding='utf-8-sig')
    shutil.copy2(HERE.parent/'chs-compat/Coop-Localization.ps1',OUT/'Coop-Localization.ps1')
    (OUT/'patch').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'outputs/Shank2-StoryCoop-v0.4-CHS/patch/manifest.json',OUT/'patch/manifest.json')
    for name in ['Launch-Coop.cmd','Remove-v04.cmd']:
        data=(ROOT/'outputs/Shank2-StoryCoop-v0.4-Portable'/name).read_bytes()
        (OUT/name.replace('v04','v05')).write_bytes(data)
    print(json.dumps({'output':str(OUT),'status':'recipes built; not yet packaged or released'}))

if __name__=='__main__':build()
