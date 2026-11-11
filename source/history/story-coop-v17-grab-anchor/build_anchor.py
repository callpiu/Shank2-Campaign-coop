import json
import importlib.util
from anchor import HERE,load_anchor
spec=importlib.util.spec_from_file_location('boss_anchor_build16',HERE.parent/'story-coop-v16-crash-recovery/build.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
build=builder.build

if __name__=='__main__':
    assert json.loads((HERE/'anchor-validation.json').read_text(encoding='utf-8-sig'))['passed']
    anchor=load_anchor();target=HERE/'dev';target.mkdir(exist_ok=True)
    rows=[build(p,target/p.name,anchor['local_pelvis']) for p in sorted((HERE.parent/'story-coop-v15-boss-transitions/dev').glob('*.exe'))]
    assert len(rows)==4
    (HERE/'build-validation.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print('Built 4 isolated anchor-aligned variants; native damage, grapple and shadow unchanged.')
