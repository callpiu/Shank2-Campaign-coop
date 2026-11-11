00671d10  55                   push     ebp
00671d11  8bec                 mov      ebp, esp
00671d13  6aff                 push     -1
00671d15  68707f6c00           push     0x6c7f70
00671d1a  64a100000000         mov      eax, dword ptr fs:[0]
00671d20  50                   push     eax
00671d21  81ec50010000         sub      esp, 0x150
00671d27  a108957c00           mov      eax, dword ptr [0x7c9508]
00671d2c  33c5                 xor      eax, ebp
00671d2e  8945f0               mov      dword ptr [ebp - 0x10], eax
00671d31  56                   push     esi
00671d32  50                   push     eax
00671d33  8d45f4               lea      eax, [ebp - 0xc]
00671d36  64a300000000         mov      dword ptr fs:[0], eax
00671d3c  898dd4feffff         mov      dword ptr [ebp - 0x12c], ecx
00671d42  8b85d4feffff         mov      eax, dword ptr [ebp - 0x12c]
00671d48  50                   push     eax
00671d49  8b4d0c               mov      ecx, dword ptr [ebp + 0xc]
00671d4c  8b4508               mov      eax, dword ptr [ebp + 8]
00671d4f  e8ac20f7ff           call     0x5e3e00
00671d54  8d8d64ffffff         lea      ecx, [ebp - 0x9c]
00671d5a  51                   push     ecx
00671d5b  8b95d4feffff         mov      edx, dword ptr [ebp - 0x12c]
00671d61  52                   push     edx
00671d62  e89922f7ff           call     0x5e4000
00671d67  8985d0feffff         mov      dword ptr [ebp - 0x130], eax
00671d6d  8b85d0feffff         mov      eax, dword ptr [ebp - 0x130]
00671d73  8985ccfeffff         mov      dword ptr [ebp - 0x134], eax
00671d79  c745fc00000000       mov      dword ptr [ebp - 4], 0
00671d80  8b8dccfeffff         mov      ecx, dword ptr [ebp - 0x134]
00671d86  51                   push     ecx
00671d87  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00671d8d  81c114010000         add      ecx, 0x114
00671d93  e858e6d9ff           call     0x4103f0
00671d98  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
00671d9f  8d8d64ffffff         lea      ecx, [ebp - 0x9c]
00671da5  e866a3dbff           call     0x42c110
00671daa  8b95d4feffff         mov      edx, dword ptr [ebp - 0x12c]
00671db0  81c214010000         add      edx, 0x114
00671db6  52                   push     edx
00671db7  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00671dbd  81c11c010000         add      ecx, 0x11c
00671dc3  e828e6d9ff           call     0x4103f0
00671dc8  8b85d4feffff         mov      eax, dword ptr [ebp - 0x12c]
00671dce  f30f5a801c010000     cvtss2sd xmm0, dword ptr [eax + 0x11c]
00671dd6  f20f5c05402d7600     subsd    xmm0, qword ptr [0x762d40]
00671dde  f20f5ac0             cvtsd2ss xmm0, xmm0
00671de2  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00671de8  f30f11811c010000     movss    dword ptr [ecx + 0x11c], xmm0
00671df0  8b550c               mov      edx, dword ptr [ebp + 0xc]
00671df3  52                   push     edx
00671df4  8d4dd4               lea      ecx, [ebp - 0x2c]
00671df7  e84414d9ff           call     0x403240
00671dfc  c745fc01000000       mov      dword ptr [ebp - 4], 1
00671e03  680c5f7500           push     0x755f0c
00671e08  8d45d4               lea      eax, [ebp - 0x2c]
00671e0b  50                   push     eax
00671e0c  8d8d48ffffff         lea      ecx, [ebp - 0xb8]
00671e12  51                   push     ecx
00671e13  e8986adaff           call     0x4188b0
00671e18  83c40c               add      esp, 0xc
00671e1b  8985c8feffff         mov      dword ptr [ebp - 0x138], eax
00671e21  8b95c8feffff         mov      edx, dword ptr [ebp - 0x138]
00671e27  8995c4feffff         mov      dword ptr [ebp - 0x13c], edx
00671e2d  c645fc02             mov      byte ptr [ebp - 4], 2
00671e31  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
00671e37  e88415d9ff           call     0x4033c0
00671e3c  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00671e42  83c118               add      ecx, 0x18
00671e45  51                   push     ecx
00671e46  8bc8                 mov      ecx, eax
00671e48  8b4508               mov      eax, dword ptr [ebp + 8]
00671e4b  e8b01ff7ff           call     0x5e3e00
00671e50  c645fc01             mov      byte ptr [ebp - 4], 1
00671e54  8d8d48ffffff         lea      ecx, [ebp - 0xb8]
00671e5a  e80116d9ff           call     0x403460
00671e5f  68185f7500           push     0x755f18
00671e64  8d55d4               lea      edx, [ebp - 0x2c]
00671e67  52                   push     edx
00671e68  8d852cffffff         lea      eax, [ebp - 0xd4]
00671e6e  50                   push     eax
00671e6f  e83c6adaff           call     0x4188b0
00671e74  83c40c               add      esp, 0xc
00671e77  8985c0feffff         mov      dword ptr [ebp - 0x140], eax
00671e7d  8b8dc0feffff         mov      ecx, dword ptr [ebp - 0x140]
00671e83  898dbcfeffff         mov      dword ptr [ebp - 0x144], ecx
00671e89  c645fc03             mov      byte ptr [ebp - 4], 3
00671e8d  8b8dbcfeffff         mov      ecx, dword ptr [ebp - 0x144]
00671e93  e82815d9ff           call     0x4033c0
00671e98  8b95d4feffff         mov      edx, dword ptr [ebp - 0x12c]
00671e9e  83c234               add      edx, 0x34
00671ea1  52                   push     edx
00671ea2  8bc8                 mov      ecx, eax
00671ea4  8b4508               mov      eax, dword ptr [ebp + 8]
00671ea7  e8541ff7ff           call     0x5e3e00
00671eac  c645fc01             mov      byte ptr [ebp - 4], 1
00671eb0  8d8d2cffffff         lea      ecx, [ebp - 0xd4]
00671eb6  e8a515d9ff           call     0x403460
00671ebb  68205f7500           push     0x755f20
00671ec0  8d45d4               lea      eax, [ebp - 0x2c]
00671ec3  50                   push     eax
00671ec4  8d8d10ffffff         lea      ecx, [ebp - 0xf0]
00671eca  51                   push     ecx
00671ecb  e8e069daff           call     0x4188b0
00671ed0  83c40c               add      esp, 0xc
00671ed3  8985b8feffff         mov      dword ptr [ebp - 0x148], eax
00671ed9  8b95b8feffff         mov      edx, dword ptr [ebp - 0x148]
00671edf  8995b4feffff         mov      dword ptr [ebp - 0x14c], edx
00671ee5  c645fc04             mov      byte ptr [ebp - 4], 4
00671ee9  8b8db4feffff         mov      ecx, dword ptr [ebp - 0x14c]
00671eef  e8cc14d9ff           call     0x4033c0
00671ef4  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00671efa  83c150               add      ecx, 0x50
00671efd  51                   push     ecx
00671efe  8bc8                 mov      ecx, eax
00671f00  8b4508               mov      eax, dword ptr [ebp + 8]
00671f03  e8f81ef7ff           call     0x5e3e00
00671f08  c645fc01             mov      byte ptr [ebp - 4], 1
00671f0c  8d8d10ffffff         lea      ecx, [ebp - 0xf0]
00671f12  e84915d9ff           call     0x403460
00671f17  68285f7500           push     0x755f28
00671f1c  8d55d4               lea      edx, [ebp - 0x2c]
00671f1f  52                   push     edx
00671f20  8d85f4feffff         lea      eax, [ebp - 0x10c]
00671f26  50                   push     eax
00671f27  e88469daff           call     0x4188b0
00671f2c  83c40c               add      esp, 0xc
00671f2f  8985b0feffff         mov      dword ptr [ebp - 0x150], eax
00671f35  8b8db0feffff         mov      ecx, dword ptr [ebp - 0x150]
00671f3b  898dacfeffff         mov      dword ptr [ebp - 0x154], ecx
00671f41  c645fc05             mov      byte ptr [ebp - 4], 5
00671f45  8b8dacfeffff         mov      ecx, dword ptr [ebp - 0x154]
00671f4b  e87014d9ff           call     0x4033c0
00671f50  8b95d4feffff         mov      edx, dword ptr [ebp - 0x12c]
00671f56  81c2f8000000         add      edx, 0xf8
00671f5c  52                   push     edx
00671f5d  8bc8                 mov      ecx, eax
00671f5f  8b4508               mov      eax, dword ptr [ebp + 8]
00671f62  e8991ef7ff           call     0x5e3e00
00671f67  c645fc01             mov      byte ptr [ebp - 4], 1
00671f6b  8d8df4feffff         lea      ecx, [ebp - 0x10c]
00671f71  e8ea14d9ff           call     0x403460
00671f76  68305f7500           push     0x755f30
00671f7b  8d45d4               lea      eax, [ebp - 0x2c]
00671f7e  50                   push     eax
00671f7f  8d8dd8feffff         lea      ecx, [ebp - 0x128]
00671f85  51                   push     ecx
00671f86  e82569daff           call     0x4188b0
00671f8b  83c40c               add      esp, 0xc
00671f8e  8985a8feffff         mov      dword ptr [ebp - 0x158], eax
00671f94  8b95a8feffff         mov      edx, dword ptr [ebp - 0x158]
00671f9a  8995a4feffff         mov      dword ptr [ebp - 0x15c], edx
00671fa0  c645fc06             mov      byte ptr [ebp - 4], 6
00671fa4  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
00671faa  e81114d9ff           call     0x4033c0
00671faf  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00671fb5  81c19c010000         add      ecx, 0x19c
00671fbb  51                   push     ecx
00671fbc  8bc8                 mov      ecx, eax
00671fbe  8b4508               mov      eax, dword ptr [ebp + 8]
00671fc1  e83a1ef7ff           call     0x5e3e00
00671fc6  c645fc01             mov      byte ptr [ebp - 4], 1
00671fca  8d8dd8feffff         lea      ecx, [ebp - 0x128]
00671fd0  e88b14d9ff           call     0x403460
00671fd5  8b85d4feffff         mov      eax, dword ptr [ebp - 0x12c]
00671fdb  05f8000000           add      eax, 0xf8
00671fe0  e8fb26f7ff           call     0x5e46e0
00671fe5  8b95d4feffff         mov      edx, dword ptr [ebp - 0x12c]
00671feb  d99a38010000         fstp     dword ptr [edx + 0x138]
00671ff1  c745d000000000       mov      dword ptr [ebp - 0x30], 0
00671ff8  eb09                 jmp      0x672003
00671ffa  8b45d0               mov      eax, dword ptr [ebp - 0x30]
00671ffd  83c001               add      eax, 1
00672000  8945d0               mov      dword ptr [ebp - 0x30], eax
00672003  837dd005             cmp      dword ptr [ebp - 0x30], 5
00672007  7d42                 jge      0x67204b
00672009  8b4dd0               mov      ecx, dword ptr [ebp - 0x30]
0067200c  83c101               add      ecx, 1
0067200f  51                   push     ecx
00672010  8b550c               mov      edx, dword ptr [ebp + 0xc]
00672013  52                   push     edx
00672014  683c5f7500           push     0x755f3c
00672019  6a5a                 push     0x5a
0067201b  8d856cffffff         lea      eax, [ebp - 0x94]
00672021  50                   push     eax
00672022  e87800fdff           call     0x64209f
00672027  83c414               add      esp, 0x14
0067202a  8b4dd0               mov      ecx, dword ptr [ebp - 0x30]
0067202d  6bc91c               imul     ecx, ecx, 0x1c
00672030  8b95d4feffff         mov      edx, dword ptr [ebp - 0x12c]
00672036  8d440a6c             lea      eax, [edx + ecx + 0x6c]
0067203a  50                   push     eax
0067203b  8d8d6cffffff         lea      ecx, [ebp - 0x94]
00672041  8b4508               mov      eax, dword ptr [ebp + 8]
00672044  e8b71df7ff           call     0x5e3e00
00672049  ebaf                 jmp      0x671ffa
0067204b  684c5f7500           push     0x755f4c
00672050  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00672056  81c13c010000         add      ecx, 0x13c
0067205c  51                   push     ecx
0067205d  b804007500           mov      eax, 0x750004
00672062  8b4d08               mov      ecx, dword ptr [ebp + 8]
00672065  e8761ef7ff           call     0x5e3ee0
0067206a  0fb6d0               movzx    edx, al
0067206d  85d2                 test     edx, edx
0067206f  7444                 je       0x6720b5
00672071  8bb5d4feffff         mov      esi, dword ptr [ebp - 0x12c]
00672077  81c63c010000         add      esi, 0x13c
0067207d  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
00672083  81c170010000         add      ecx, 0x170
00672089  b8a8207500           mov      eax, 0x7520a8
0067208e  e82d1df7ff           call     0x5e3dc0
00672093  8bb5d4feffff         mov      esi, dword ptr [ebp - 0x12c]
00672099  81c63c010000         add      esi, 0x13c
0067209f  8b8dd4feffff         mov      ecx, dword ptr [ebp - 0x12c]
006720a5  81c154010000         add      ecx, 0x154
006720ab  b8a0207500           mov      eax, 0x7520a0
006720b0  e80b1df7ff           call     0x5e3dc0
006720b5  8b85d4feffff         mov      eax, dword ptr [ebp - 0x12c]
006720bb  053c010000           add      eax, 0x13c
006720c0  32d2                 xor      dl, dl
006720c2  e8b920f7ff           call     0x5e4180
006720c7  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006720ce  8d4dd4               lea      ecx, [ebp - 0x2c]
006720d1  e88a13d9ff           call     0x403460
006720d6  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006720d9  64890d00000000       mov      dword ptr fs:[0], ecx
006720e0  59                   pop      ecx
006720e1  5e                   pop      esi
006720e2  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006720e5  33cd                 xor      ecx, ebp
006720e7  e8b9effcff           call     0x6410a5
006720ec  8be5                 mov      esp, ebp
006720ee  5d                   pop      ebp
006720ef  c20800               ret      8
006720f2  cc                   int3     
006720f3  cc                   int3     
006720f4  cc                   int3     
006720f5  cc                   int3     
006720f6  cc                   int3     
006720f7  cc                   int3     
006720f8  cc                   int3     
006720f9  cc                   int3     
006720fa  cc                   int3     
006720fb  cc                   int3     
006720fc  cc                   int3     
006720fd  cc                   int3     
006720fe  cc                   int3     
006720ff  cc                   int3     
00672100  55                   push     ebp
00672101  8bec                 mov      ebp, esp
00672103  6aff                 push     -1
00672105  68d97f6c00           push     0x6c7fd9
0067210a  64a100000000         mov      eax, dword ptr fs:[0]
00672110  50                   push     eax
00672111  81ecb0000000         sub      esp, 0xb0
00672117  a108957c00           mov      eax, dword ptr [0x7c9508]
0067211c  33c5                 xor      eax, ebp
0067211e  8945cc               mov      dword ptr [ebp - 0x34], eax
00672121  56                   push     esi
00672122  50                   push     eax
00672123  8d45f4               lea      eax, [ebp - 0xc]
00672126  64a300000000         mov      dword ptr fs:[0], eax
0067212c  898d64ffffff         mov      dword ptr [ebp - 0x9c], ecx
00672132  837d0c00             cmp      dword ptr [ebp + 0xc], 0
00672136  7505                 jne      0x67213d
00672138  e923030000           jmp      0x672460
0067213d  8b4d0c               mov      ecx, dword ptr [ebp + 0xc]
00672140  e81bb6d9ff           call     0x40d760
00672145  8945f0               mov      dword ptr [ebp - 0x10], eax
00672148  837df000             cmp      dword ptr [ebp - 0x10], 0
0067214c  7505                 jne      0x672153
0067214e  e90d030000           jmp      0x672460
00672153  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00672156  e80554e6ff           call     0x4d7560
0067215b  0fb6c0               movzx    eax, al
0067215e  85c0                 test     eax, eax
00672160  0f8495020000         je       0x6723fb
00672166  8b8d64ffffff         mov      ecx, dword ptr [ebp - 0x9c]
0067216c  83b9900a000000       cmp      dword ptr [ecx + 0xa90], 0
00672173  0f85a0000000         jne      0x672219
00672179  6a34                 push     0x34
0067217b  e8e08f0300           call     0x6ab160
00672180  83c404               add      esp, 4
00672183  894584               mov      dword ptr [ebp - 0x7c], eax
00672186  c745fc00000000       mov      dword ptr [ebp - 4], 0
0067218d  837d8400             cmp      dword ptr [ebp - 0x7c], 0
00672191  7410                 je       0x6721a3
00672193  8b4d84               mov      ecx, dword ptr [ebp - 0x7c]
00672196  e8e52de0ff           call     0x474f80
0067219b  898560ffffff         mov      dword ptr [ebp - 0xa0], eax
006721a1  eb0a                 jmp      0x6721ad
006721a3  c78560ffffff00000000 mov      dword ptr [ebp - 0xa0], 0
006721ad  8b9560ffffff         mov      edx, dword ptr [ebp - 0xa0]
006721b3  895588               mov      dword ptr [ebp - 0x78], edx
006721b6  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006721bd  8b8564ffffff         mov      eax, dword ptr [ebp - 0x9c]
006721c3  8b4d88               mov      ecx, dword ptr [ebp - 0x78]
006721c6  8988900a0000         mov      dword ptr [eax + 0xa90], ecx
006721cc  68d05d7500           push     0x755dd0
006721d1  8b9564ffffff         mov      edx, dword ptr [ebp - 0x9c]
006721d7  8b82900a0000         mov      eax, dword ptr [edx + 0xa90]
006721dd  50                   push     eax
006721de  b804007500           mov      eax, 0x750004
006721e3  8b8d64ffffff         mov      ecx, dword ptr [ebp - 0x9c]
006721e9  8b898c0a0000         mov      ecx, dword ptr [ecx + 0xa8c]
006721ef  e8ec1cf7ff           call     0x5e3ee0
006721f4  8b9564ffffff         mov      edx, dword ptr [ebp - 0x9c]
006721fa  8b8a900a0000         mov      ecx, dword ptr [edx + 0xa90]
00672200  83c118               add      ecx, 0x18
00672203  b8d85d7500           mov      eax, 0x755dd8
00672208  8b9564ffffff         mov      edx, dword ptr [ebp - 0x9c]
0067220e  8bb2900a0000         mov      esi, dword ptr [edx + 0xa90]
00672214  e8a71bf7ff           call     0x5e3dc0
00672219  8b45f0               mov      eax, dword ptr [ebp - 0x10]
0067221c  e81f49e6ff           call     0x4d6b40
00672221  8945d8               mov      dword ptr [ebp - 0x28], eax
00672224  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00672227  e8b448e6ff           call     0x4d6ae0
0067222c  8945ec               mov      dword ptr [ebp - 0x14], eax
0067222f  837dd800             cmp      dword ptr [ebp - 0x28], 0
00672233  0f86a0000000         jbe      0x6722d9
00672239  8b45f0               mov      eax, dword ptr [ebp - 0x10]
0067223c  e89f48e6ff           call     0x4d6ae0
00672241  50                   push     eax
00672242  683c1e7500           push     0x751e3c
00672247  6a40                 push     0x40
00672249  8d458c               lea      eax, [ebp - 0x74]
0067224c  50                   push     eax
0067224d  e84dfefcff           call     0x64209f
00672252  83c410               add      esp, 0x10
00672255  c645cb00             mov      byte ptr [ebp - 0x35], 0
00672259  8b8d64ffffff         mov      ecx, dword ptr [ebp - 0x9c]
0067225f  8b81900a0000         mov      eax, dword ptr [ecx + 0xa90]
00672265  83c018               add      eax, 0x18
00672268  8d4d8c               lea      ecx, [ebp - 0x74]
0067226b  e83023f7ff           call     0x5e45a0
00672270  8b55d8               mov      edx, dword ptr [ebp - 0x28]
00672273  52                   push     edx
00672274  8b45ec               mov      eax, dword ptr [ebp - 0x14]
00672277  50                   push     eax
00672278  8d4dd0               lea      ecx, [ebp - 0x30]
0067227b  51                   push     ecx
0067227c  e8afc9ffff           call     0x66ec30
00672281  83c40c               add      esp, 0xc
00672284  c745fc01000000       mov      dword ptr [ebp - 4], 1
0067228b  83ec08               sub      esp, 8
0067228e  8bcc                 mov      ecx, esp
00672290  896580               mov      dword ptr [ebp - 0x80], esp
00672293  8d55d0               lea      edx, [ebp - 0x30]
00672296  52                   push     edx
00672297  e8d4e3dcff           call     0x440670
0067229c  89855cffffff         mov      dword ptr [ebp - 0xa4], eax
006722a2  8b855cffffff         mov      eax, dword ptr [ebp - 0xa4]
006722a8  898558ffffff         mov      dword ptr [ebp - 0xa8], eax
006722ae  c645fc02             mov      byte ptr [ebp - 4], 2
006722b2  8b8d64ffffff         mov      ecx, dword ptr [ebp - 0x9c]
006722b8  8bb1900a0000         mov      esi, dword ptr [ecx + 0xa90]
006722be  83c618               add      esi, 0x18
006722c1  c645fc01             mov      byte ptr [ebp - 4], 1
006722c5  e80623f7ff           call     0x5e45d0
006722ca  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006722d1  8d4dd0               lea      ecx, [ebp - 0x30]
006722d4  e8b713dcff           call     0x433690
006722d9  f30f5a05c8f47400     cvtss2sd xmm0, dword ptr [0x74f4c8]
006722e1  f20f590558297600     mulsd    xmm0, qword ptr [0x762958]
006722e9  f20f5ac0             cvtsd2ss xmm0, xmm0
006722ed  51                   push     ecx
006722ee  f30f110424           movss    dword ptr [esp], xmm0
006722f3  51                   push     ecx
006722f4  d9ee                 fldz     
006722f6  d91c24               fstp     dword ptr [esp]
006722f9  8d8d78ffffff         lea      ecx, [ebp - 0x88]
006722ff  e80c6ae0ff           call     0x478d10
00672304  898554ffffff         mov      dword ptr [ebp - 0xac], eax
0067230a  8b9554ffffff         mov      edx, dword ptr [ebp - 0xac]
00672310  899550ffffff         mov      dword ptr [ebp - 0xb0], edx
00672316  c745fc03000000       mov      dword ptr [ebp - 4], 3
0067231d  8b8550ffffff         mov      eax, dword ptr [ebp - 0xb0]
00672323  50                   push     eax
00672324  8b4d0c               mov      ecx, dword ptr [ebp + 0xc]
00672327  e86471daff           call     0x419490
0067232c  e8af83e7ff           call     0x4ea6e0
00672331  50                   push     eax
00672332  8d8d70ffffff         lea      ecx, [ebp - 0x90]
00672338  51                   push     ecx
00672339  e8a20cdcff           call     0x432fe0
0067233e  83c40c               add      esp, 0xc
00672341  89854cffffff         mov      dword ptr [ebp - 0xb4], eax
00672347  8b954cffffff         mov      edx, dword ptr [ebp - 0xb4]
0067234d  899548ffffff         mov      dword ptr [ebp - 0xb8], edx
00672353  c645fc04             mov      byte ptr [ebp - 4], 4
00672357  8b8548ffffff         mov      eax, dword ptr [ebp - 0xb8]
0067235d  50                   push     eax
0067235e  8d4de4               lea      ecx, [ebp - 0x1c]
00672361  51                   push     ecx
00672362  8b4d10               mov      ecx, dword ptr [ebp + 0x10]
00672365  e876dedbff           call     0x4301e0
0067236a  c645fc06             mov      byte ptr [ebp - 4], 6
0067236e  8d8d70ffffff         lea      ecx, [ebp - 0x90]
00672374  e8979ddbff           call     0x42c110
00672379  c645fc07             mov      byte ptr [ebp - 4], 7
0067237d  8d8d78ffffff         lea      ecx, [ebp - 0x88]
00672383  e8889ddbff           call     0x42c110
00672388  f30f5a45e8           cvtss2sd xmm0, dword ptr [ebp - 0x18]
0067238d  f30f5a0d7c9d7d00     cvtss2sd xmm1, dword ptr [0x7d9d7c]
00672395  f20f5ec1             divsd    xmm0, xmm1
00672399  f20f5ac0             cvtsd2ss xmm0, xmm0
0067239d  51                   push     ecx
0067239e  f30f110424           movss    dword ptr [esp], xmm0
006723a3  f30f5a45e4           cvtss2sd xmm0, dword ptr [ebp - 0x1c]
006723a8  f30f5a0d809d7d00     cvtss2sd xmm1, dword ptr [0x7d9d80]
006723b0  f20f5ec1             divsd    xmm0, xmm1
006723b4  f20f5ac0             cvtsd2ss xmm0, xmm0
006723b8  51                   push     ecx
006723b9  f30f110424           movss    dword ptr [esp], xmm0
006723be  8d4ddc               lea      ecx, [ebp - 0x24]
006723c1  e84a69e0ff           call     0x478d10
006723c6  c645fc08             mov      byte ptr [ebp - 4], 8
006723ca  8d4ddc               lea      ecx, [ebp - 0x24]
006723cd  8b9564ffffff         mov      edx, dword ptr [ebp - 0x9c]
006723d3  8b82900a0000         mov      eax, dword ptr [edx + 0xa90]
006723d9  e8e21cf7ff           call     0x5e40c0
006723de  c645fc07             mov      byte ptr [ebp - 4], 7
006723e2  8d4ddc               lea      ecx, [ebp - 0x24]
006723e5  e8269ddbff           call     0x42c110
006723ea  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006723f1  8d4de4               lea      ecx, [ebp - 0x1c]
006723f4  e8179ddbff           call     0x42c110
006723f9  eb65                 jmp      0x672460
006723fb  8b8564ffffff         mov      eax, dword ptr [ebp - 0x9c]
00672401  83b8900a000000       cmp      dword ptr [eax + 0xa90], 0
00672408  7456                 je       0x672460
0067240a  8b8d64ffffff         mov      ecx, dword ptr [ebp - 0x9c]
00672410  8b91900a0000         mov      edx, dword ptr [ecx + 0xa90]
