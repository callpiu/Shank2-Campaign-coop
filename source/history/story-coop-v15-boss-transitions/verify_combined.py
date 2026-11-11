"""Assert the combined builds change only the two reviewed hook paths."""
import hashlib
import json
from build_teleport import HERE,pefile,CODE as TELEPORT,routine as tele_routine,Ks,KS_ARCH_X86,KS_MODE_32
from build_pose import CODE,TRAMPOLINE,NATIVE,PROLOGUE,routine
ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
records=[]
for source in sorted((HERE.parent/'story-coop-v12-live-character/dev').glob('*.exe')):
    original=source.read_bytes();image=(HERE/'combined'/source.name).read_bytes()
    assert len(original)==len(image)
    pe=pefile.PE(data=original);off=lambda a:pe.get_offset_from_rva(a-0x400000)
    spans=((off(TELEPORT),len(tele_routine(asm))),(off(0x75ae04),4),(off(CODE),len(routine(asm))),
           (off(TRAMPOLINE),14),(off(NATIVE),len(PROLOGUE)))
    allowed={n for start,length in spans for n in range(start,start+length)}
    diffs={i for i,(a,b) in enumerate(zip(original,image)) if a!=b}
    assert diffs and diffs<=allowed
    for address,size in ((0x4ee3b0,0x300),(0x504920,0x5d2),(0x505000,0xba0),(0x7ff800,128)):
        assert image[off(address):off(address)+size]==original[off(address):off(address)+size]
    records.append(dict(name=source.name,changed_bytes=len(diffs),only_reviewed_spans=True,
                        damage_grab_release_config_unchanged=True,sha256=hashlib.sha256(image).hexdigest()))
(HERE/'combined-validation.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
print('PASS: four combined builds; only two reviewed hooks/caves differ; damage, grapple, release and 128-byte loadouts unchanged.')
