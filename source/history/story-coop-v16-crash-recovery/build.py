"""Isolated four-variant build; no changes to release archives or user install."""
import hashlib
import json
from pose3 import HERE, routine
from build_teleport import Ks, KS_ARCH_X86, KS_MODE_32, pefile

CODE, TRAMPOLINE, NATIVE, METRICS = 0x7fcc00, 0x7fcf80, 0x511460, 0x7ffa00
ORIGINAL = bytes.fromhex('558bec83e4f8')

def build(source, target, pose_anchor=None):
    raw=source.read_bytes();pe=pefile.PE(data=raw)
    off=lambda a:pe.get_offset_from_rva(a-0x400000)
    ks=Ks(KS_ARCH_X86,KS_MODE_32);asm=lambda s,a:bytes(ks.asm(s,a)[0])
    assert raw[off(NATIVE):off(NATIVE)+6]==ORIGINAL
    assert raw[off(CODE):off(CODE)+0x400]==b'\xcc'*0x400
    assert raw[off(METRICS):off(METRICS)+16]==bytes(16)
    blob=routine(asm,CODE,native=TRAMPOLINE,metrics=METRICS,anchor=pose_anchor)
    trampoline=asm('push ebp;mov ebp,esp;and esp,-8;jmp 0x511466',TRAMPOLINE)
    assert len(blob)<TRAMPOLINE-CODE
    out=bytearray(raw)
    changes=[(NATIVE,asm(f'jmp {CODE};nop',NATIVE)),(CODE,blob),(TRAMPOLINE,trampoline)]
    for address,data in changes:out[off(address):off(address)+len(data)]=data
    allowed=set()
    for address,data in changes:allowed.update(range(off(address),off(address)+len(data)))
    assert all(i in allowed for i,(a,b) in enumerate(zip(raw,out)) if a!=b)
    for address,size in ((0x4ee3b0,0x80),(0x504920,0x100),(0x505000,0xba0),(0x7ff800,128)):
        assert out[off(address):off(address)+size]==raw[off(address):off(address)+size]
    target.write_bytes(out)
    return dict(name=target.name,sha256=hashlib.sha256(out).hexdigest(),
        base_sha256=hashlib.sha256(raw).hexdigest(),hook_size=len(blob),
        trampoline=hex(TRAMPOLINE),metrics=hex(METRICS),grapple_damage_config_unchanged=True,
        pose_anchor=pose_anchor,gameplay_verified=False)

if __name__=='__main__':
    checks=json.loads((HERE/'deferred-validation.json').read_text(encoding='utf-8-sig'))
    assert checks['passed'] and checks['old_implementation_escaped_stack_pointers']==2
    dest=HERE/'dev';dest.mkdir(exist_ok=True)
    rows=[build(p,dest/p.name) for p in sorted((HERE.parent/'story-coop-v15-boss-transitions/dev').glob('*.exe'))]
    assert len(rows)==4
    (HERE/'build-validation.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print('Built 4 isolated variants with native deferred-packet lifetimes preserved.')
