import sys
from read_dump import Dump,HERE
sys.path.insert(0,str(HERE.parent/'story-coop-v05'))
from native import Cs,CS_ARCH_X86,CS_MODE_32,dis
d=Dump()
md=Cs(CS_ARCH_X86,CS_MODE_32)
print('REMOTE CODE')
sys.path.insert(0,str(HERE.parent/'story-coop-v15-boss-transitions'))
from pose2 import routine
from build_teleport import Ks,KS_ARCH_X86,KS_MODE_32
ks=Ks(KS_ARCH_X86,KS_MODE_32)
code=routine(lambda s,a:bytes(ks.asm(s,a)[0]),0x9b0000)
for i in md.disasm(code,0x9b0000):print(hex(i.address),i.mnemonic,i.op_str)
print('CANDIDATE PACKETS')
for a in (0x19f29c,0x19f34c,0x19f364,0x19f6c4,0x1a3ff8):
    print(hex(a),d.read(a,40).hex(), 'count20c', d.u32(a+0x20c))
print(dis(0x574070,100));print(dis(0x5735f0,75))
