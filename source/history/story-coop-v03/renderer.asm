0069d110  55                   push     ebp
0069d111  8bec                 mov      ebp, esp
0069d113  51                   push     ecx
0069d114  894dfc               mov      dword ptr [ebp - 4], ecx
0069d117  e874d80000           call     0x6aa990
0069d11c  8b45fc               mov      eax, dword ptr [ebp - 4]
0069d11f  8b88f4600000         mov      ecx, dword ptr [eax + 0x60f4]
0069d125  51                   push     ecx
0069d126  e875ceffff           call     0x699fa0
0069d12b  8bc8                 mov      ecx, eax
0069d12d  e84e35d9ff           call     0x430680
0069d132  8b55fc               mov      edx, dword ptr [ebp - 4]
0069d135  c782f460000000000000 mov      dword ptr [edx + 0x60f4], 0
0069d13f  8be5                 mov      esp, ebp
0069d141  5d                   pop      ebp
0069d142  c3                   ret      
0069d143  cc                   int3     
0069d144  cc                   int3     
0069d145  cc                   int3     
0069d146  cc                   int3     
0069d147  cc                   int3     
0069d148  cc                   int3     
0069d149  cc                   int3     
0069d14a  cc                   int3     
0069d14b  cc                   int3     
0069d14c  cc                   int3     
0069d14d  cc                   int3     
0069d14e  cc                   int3     
0069d14f  cc                   int3     
0069d150  55                   push     ebp
0069d151  8bec                 mov      ebp, esp
0069d153  6aff                 push     -1
0069d155  6835786c00           push     0x6c7835
0069d15a  64a100000000         mov      eax, dword ptr fs:[0]
0069d160  50                   push     eax
0069d161  81ecc4010000         sub      esp, 0x1c4
0069d167  56                   push     esi
0069d168  a108957c00           mov      eax, dword ptr [0x7c9508]
0069d16d  33c5                 xor      eax, ebp
0069d16f  50                   push     eax
0069d170  8d45f4               lea      eax, [ebp - 0xc]
0069d173  64a300000000         mov      dword ptr fs:[0], eax
0069d179  898d58feffff         mov      dword ptr [ebp - 0x1a8], ecx
0069d17f  f30f100520297600     movss    xmm0, dword ptr [0x762920]
0069d187  f30f1145f0           movss    dword ptr [ebp - 0x10], xmm0
0069d18c  8b8558feffff         mov      eax, dword ptr [ebp - 0x1a8]
0069d192  83b86061000000       cmp      dword ptr [eax + 0x6160], 0
0069d199  7f13                 jg       0x69d1ae
0069d19b  8b8d58feffff         mov      ecx, dword ptr [ebp - 0x1a8]
0069d1a1  83b93c61000000       cmp      dword ptr [ecx + 0x613c], 0
0069d1a8  0f841c010000         je       0x69d2ca
0069d1ae  8bb558feffff         mov      esi, dword ptr [ebp - 0x1a8]
0069d1b4  81c640610000         add      esi, 0x6140
0069d1ba  e871f7f0ff           call     0x5ac930
0069d1bf  d99d54feffff         fstp     dword ptr [ebp - 0x1ac]
0069d1c5  d98554feffff         fld      dword ptr [ebp - 0x1ac]
0069d1cb  dc0d002a7600         fmul     qword ptr [0x762a00]
0069d1d1  d99d50feffff         fstp     dword ptr [ebp - 0x1b0]
0069d1d7  d98550feffff         fld      dword ptr [ebp - 0x1b0]
0069d1dd  51                   push     ecx
0069d1de  d91c24               fstp     dword ptr [esp]
0069d1e1  e85a61d9ff           call     0x433340
0069d1e6  83c404               add      esp, 4
0069d1e9  dc35002a7600         fdiv     qword ptr [0x762a00]
0069d1ef  dc05d02c7600         fadd     qword ptr [0x762cd0]
0069d1f5  d95df0               fstp     dword ptr [ebp - 0x10]
0069d1f8  8b9558feffff         mov      edx, dword ptr [ebp - 0x1a8]
0069d1fe  8b823c610000         mov      eax, dword ptr [edx + 0x613c]
0069d204  89854cfeffff         mov      dword ptr [ebp - 0x1b4], eax
0069d20a  83bd4cfeffff00       cmp      dword ptr [ebp - 0x1b4], 0
0069d211  7417                 je       0x69d22a
0069d213  83bd4cfeffff01       cmp      dword ptr [ebp - 0x1b4], 1
0069d21a  741e                 je       0x69d23a
0069d21c  83bd4cfeffff02       cmp      dword ptr [ebp - 0x1b4], 2
0069d223  7467                 je       0x69d28c
0069d225  e9a0000000           jmp      0x69d2ca
0069d22a  8b8d58feffff         mov      ecx, dword ptr [ebp - 0x1a8]
0069d230  c7813c61000001000000 mov      dword ptr [ecx + 0x613c], 1
0069d23a  8bb558feffff         mov      esi, dword ptr [ebp - 0x1a8]
0069d240  81c640610000         add      esi, 0x6140
0069d246  e8e5f6f0ff           call     0x5ac930
0069d24b  dd05c82c7600         fld      qword ptr [0x762cc8]
0069d251  d9c9                 fxch     st(1)
0069d253  dff1                 fcompi   st(1)
0069d255  ddd8                 fstp     st(0)
0069d257  7631                 jbe      0x69d28a
0069d259  8b9558feffff         mov      edx, dword ptr [ebp - 0x1a8]
0069d25f  83ba6061000000       cmp      dword ptr [edx + 0x6160], 0
0069d266  7512                 jne      0x69d27a
0069d268  8b8558feffff         mov      eax, dword ptr [ebp - 0x1a8]
0069d26e  c7803c61000000000000 mov      dword ptr [eax + 0x613c], 0
0069d278  eb10                 jmp      0x69d28a
0069d27a  8b8d58feffff         mov      ecx, dword ptr [ebp - 0x1a8]
0069d280  c7813c61000002000000 mov      dword ptr [ecx + 0x613c], 2
0069d28a  eb3e                 jmp      0x69d2ca
0069d28c  8bb558feffff         mov      esi, dword ptr [ebp - 0x1a8]
0069d292  81c640610000         add      esi, 0x6140
0069d298  e893f6f0ff           call     0x5ac930
0069d29d  dd0558297600         fld      qword ptr [0x762958]
0069d2a3  d9c9                 fxch     st(1)
0069d2a5  dff1                 fcompi   st(1)
0069d2a7  ddd8                 fstp     st(0)
0069d2a9  761f                 jbe      0x69d2ca
0069d2ab  8b9558feffff         mov      edx, dword ptr [ebp - 0x1a8]
0069d2b1  83ba6061000000       cmp      dword ptr [edx + 0x6160], 0
0069d2b8  7510                 jne      0x69d2ca
0069d2ba  8b8558feffff         mov      eax, dword ptr [ebp - 0x1a8]
0069d2c0  c7803c61000000000000 mov      dword ptr [eax + 0x613c], 0
0069d2ca  be01000000           mov      esi, 1
0069d2cf  e89cccdeff           call     0x489f70
0069d2d4  f30f5a45f0           cvtss2sd xmm0, dword ptr [ebp - 0x10]
0069d2d9  660f2f0518297600     comisd   xmm0, xmmword ptr [0x762918]
0069d2e1  0f86b2010000         jbe      0x69d499
0069d2e7  8d8d44ffffff         lea      ecx, [ebp - 0xbc]
0069d2ed  e8fe60d9ff           call     0x4333f0
0069d2f2  c745fc00000000       mov      dword ptr [ebp - 4], 0
0069d2f9  8d4d8c               lea      ecx, [ebp - 0x74]
0069d2fc  e8ef60d9ff           call     0x4333f0
0069d301  c645fc01             mov      byte ptr [ebp - 4], 1
0069d305  51                   push     ecx
0069d306  d9ee                 fldz     
0069d308  d91c24               fstp     dword ptr [esp]
0069d30b  f30f5a05248d7d00     cvtss2sd xmm0, dword ptr [0x7d8d24]
0069d313  f20f5905f8297600     mulsd    xmm0, qword ptr [0x7629f8]
0069d31b  f20f5ac0             cvtsd2ss xmm0, xmm0
0069d31f  51                   push     ecx
0069d320  f30f110424           movss    dword ptr [esp], xmm0
0069d325  f30f5a05288d7d00     cvtss2sd xmm0, dword ptr [0x7d8d28]
0069d32d  f20f5905f8297600     mulsd    xmm0, qword ptr [0x7629f8]
0069d335  f20f5ac0             cvtsd2ss xmm0, xmm0
0069d339  51                   push     ecx
0069d33a  f30f110424           movss    dword ptr [esp], xmm0
0069d33f  8d4ddc               lea      ecx, [ebp - 0x24]
0069d342  e8895fd9ff           call     0x4332d0
0069d347  c645fc02             mov      byte ptr [ebp - 4], 2
0069d34b  8d4ddc               lea      ecx, [ebp - 0x24]
0069d34e  51                   push     ecx
0069d34f  8d4d8c               lea      ecx, [ebp - 0x74]
0069d352  e8e95ed9ff           call     0x433240
0069d357  8d9544ffffff         lea      edx, [ebp - 0xbc]
0069d35d  b802000000           mov      eax, 2
0069d362  e8692adfff           call     0x48fdd0
0069d367  8d558c               lea      edx, [ebp - 0x74]
0069d36a  b801000000           mov      eax, 1
0069d36f  e85c2adfff           call     0x48fdd0
0069d374  51                   push     ecx
0069d375  d905c02c7600         fld      dword ptr [0x762cc0]
0069d37b  d91c24               fstp     dword ptr [esp]
0069d37e  51                   push     ecx
0069d37f  d90528ef7400         fld      dword ptr [0x74ef28]
0069d385  d91c24               fstp     dword ptr [esp]
0069d388  8d4dd0               lea      ecx, [ebp - 0x30]
0069d38b  e880b9ddff           call     0x478d10
0069d390  c645fc03             mov      byte ptr [ebp - 4], 3
0069d394  51                   push     ecx
0069d395  d905bc2c7600         fld      dword ptr [0x762cbc]
0069d39b  d91c24               fstp     dword ptr [esp]
0069d39e  51                   push     ecx
0069d39f  d90528ef7400         fld      dword ptr [0x74ef28]
0069d3a5  d91c24               fstp     dword ptr [esp]
0069d3a8  8d8d94feffff         lea      ecx, [ebp - 0x16c]
0069d3ae  e85db9ddff           call     0x478d10
0069d3b3  898548feffff         mov      dword ptr [ebp - 0x1b8], eax
0069d3b9  8b9548feffff         mov      edx, dword ptr [ebp - 0x1b8]
0069d3bf  899544feffff         mov      dword ptr [ebp - 0x1bc], edx
0069d3c5  c645fc04             mov      byte ptr [ebp - 4], 4
0069d3c9  8b8544feffff         mov      eax, dword ptr [ebp - 0x1bc]
0069d3cf  50                   push     eax
0069d3d0  8d4d84               lea      ecx, [ebp - 0x7c]
0069d3d3  51                   push     ecx
0069d3d4  8d4dd0               lea      ecx, [ebp - 0x30]
0069d3d7  e8742fd7ff           call     0x410350
0069d3dc  c645fc06             mov      byte ptr [ebp - 4], 6
0069d3e0  8d8d94feffff         lea      ecx, [ebp - 0x16c]
0069d3e6  e825edd8ff           call     0x42c110
0069d3eb  c745d8f01148f9       mov      dword ptr [ebp - 0x28], 0xf94811f0
0069d3f2  c745e8befc22e6       mov      dword ptr [ebp - 0x18], 0xe622fcbe
0069d3f9  51                   push     ecx
0069d3fa  8bcc                 mov      ecx, esp
0069d3fc  89a590feffff         mov      dword ptr [ebp - 0x170], esp
0069d402  8b55e8               mov      edx, dword ptr [ebp - 0x18]
0069d405  52                   push     edx
0069d406  e86505d7ff           call     0x40d970
0069d40b  51                   push     ecx
0069d40c  8bcc                 mov      ecx, esp
0069d40e  89a58cfeffff         mov      dword ptr [ebp - 0x174], esp
0069d414  8b45d8               mov      eax, dword ptr [ebp - 0x28]
0069d417  50                   push     eax
0069d418  e85305d7ff           call     0x40d970
0069d41d  51                   push     ecx
0069d41e  d945f0               fld      dword ptr [ebp - 0x10]
0069d421  d91c24               fstp     dword ptr [esp]
0069d424  51                   push     ecx
0069d425  d9e8                 fld1     
0069d427  d91c24               fstp     dword ptr [esp]
0069d42a  51                   push     ecx
0069d42b  d9e8                 fld1     
0069d42d  d91c24               fstp     dword ptr [esp]
0069d430  51                   push     ecx
0069d431  d9e8                 fld1     
0069d433  d91c24               fstp     dword ptr [esp]
0069d436  8d8d7cfeffff         lea      ecx, [ebp - 0x184]
0069d43c  e87f5cd9ff           call     0x4330c0
0069d441  50                   push     eax
0069d442  8d4d84               lea      ecx, [ebp - 0x7c]
0069d445  51                   push     ecx
0069d446  8d55d0               lea      edx, [ebp - 0x30]
0069d449  52                   push     edx
0069d44a  e80137dfff           call     0x490b50
0069d44f  83c414               add      esp, 0x14
0069d452  e8692edfff           call     0x4902c0
0069d457  c645fc03             mov      byte ptr [ebp - 4], 3
0069d45b  8d4d84               lea      ecx, [ebp - 0x7c]
0069d45e  e8adecd8ff           call     0x42c110
0069d463  c645fc02             mov      byte ptr [ebp - 4], 2
0069d467  8d4dd0               lea      ecx, [ebp - 0x30]
0069d46a  e8a1ecd8ff           call     0x42c110
0069d46f  c645fc01             mov      byte ptr [ebp - 4], 1
0069d473  8d4ddc               lea      ecx, [ebp - 0x24]
0069d476  e895ecd8ff           call     0x42c110
0069d47b  c645fc00             mov      byte ptr [ebp - 4], 0
0069d47f  8d4d8c               lea      ecx, [ebp - 0x74]
0069d482  e889ecd8ff           call     0x42c110
0069d487  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069d48e  8d8d44ffffff         lea      ecx, [ebp - 0xbc]
0069d494  e877ecd8ff           call     0x42c110
0069d499  f30f100520297600     movss    xmm0, dword ptr [0x762920]
0069d4a1  f30f1145ec           movss    dword ptr [ebp - 0x14], xmm0
0069d4a6  8b8558feffff         mov      eax, dword ptr [ebp - 0x1a8]
0069d4ac  83b88861000000       cmp      dword ptr [eax + 0x6188], 0
0069d4b3  7f13                 jg       0x69d4c8
0069d4b5  8b8d58feffff         mov      ecx, dword ptr [ebp - 0x1a8]
0069d4bb  83b96461000000       cmp      dword ptr [ecx + 0x6164], 0
0069d4c2  0f8418010000         je       0x69d5e0
0069d4c8  8bb558feffff         mov      esi, dword ptr [ebp - 0x1a8]
0069d4ce  81c668610000         add      esi, 0x6168
0069d4d4  e857f4f0ff           call     0x5ac930
0069d4d9  d99d40feffff         fstp     dword ptr [ebp - 0x1c0]
0069d4df  d98540feffff         fld      dword ptr [ebp - 0x1c0]
0069d4e5  dc0d002a7600         fmul     qword ptr [0x762a00]
0069d4eb  d99d3cfeffff         fstp     dword ptr [ebp - 0x1c4]
0069d4f1  d9853cfeffff         fld      dword ptr [ebp - 0x1c4]
0069d4f7  51                   push     ecx
0069d4f8  d91c24               fstp     dword ptr [esp]
0069d4fb  e8405ed9ff           call     0x433340
0069d500  83c404               add      esp, 4
0069d503  dc35002a7600         fdiv     qword ptr [0x762a00]
0069d509  dc05d02c7600         fadd     qword ptr [0x762cd0]
0069d50f  d95dec               fstp     dword ptr [ebp - 0x14]
0069d512  8b9558feffff         mov      edx, dword ptr [ebp - 0x1a8]
0069d518  8b8264610000         mov      eax, dword ptr [edx + 0x6164]
0069d51e  898538feffff         mov      dword ptr [ebp - 0x1c8], eax
0069d524  83bd38feffff00       cmp      dword ptr [ebp - 0x1c8], 0
0069d52b  7417                 je       0x69d544
0069d52d  83bd38feffff01       cmp      dword ptr [ebp - 0x1c8], 1
0069d534  741e                 je       0x69d554
0069d536  83bd38feffff02       cmp      dword ptr [ebp - 0x1c8], 2
0069d53d  7463                 je       0x69d5a2
0069d53f  e99c000000           jmp      0x69d5e0
0069d544  8b8d58feffff         mov      ecx, dword ptr [ebp - 0x1a8]
0069d54a  c7816461000001000000 mov      dword ptr [ecx + 0x6164], 1
0069d554  8bb558feffff         mov      esi, dword ptr [ebp - 0x1a8]
0069d55a  81c668610000         add      esi, 0x6168
0069d560  e8cbf3f0ff           call     0x5ac930
0069d565  d9e8                 fld1     
0069d567  d9c9                 fxch     st(1)
0069d569  dff1                 fcompi   st(1)
0069d56b  ddd8                 fstp     st(0)
0069d56d  7631                 jbe      0x69d5a0
0069d56f  8b9558feffff         mov      edx, dword ptr [ebp - 0x1a8]
0069d575  83ba8861000000       cmp      dword ptr [edx + 0x6188], 0
0069d57c  7512                 jne      0x69d590
0069d57e  8b8558feffff         mov      eax, dword ptr [ebp - 0x1a8]
0069d584  c7806461000000000000 mov      dword ptr [eax + 0x6164], 0
0069d58e  eb10                 jmp      0x69d5a0
0069d590  8b8d58feffff         mov      ecx, dword ptr [ebp - 0x1a8]
0069d596  c7816461000002000000 mov      dword ptr [ecx + 0x6164], 2
0069d5a0  eb3e                 jmp      0x69d5e0
0069d5a2  8bb558feffff         mov      esi, dword ptr [ebp - 0x1a8]
0069d5a8  81c668610000         add      esi, 0x6168
0069d5ae  e87df3f0ff           call     0x5ac930
0069d5b3  dd0558297600         fld      qword ptr [0x762958]
0069d5b9  d9c9                 fxch     st(1)
0069d5bb  dff1                 fcompi   st(1)
0069d5bd  ddd8                 fstp     st(0)
0069d5bf  761f                 jbe      0x69d5e0
0069d5c1  8b9558feffff         mov      edx, dword ptr [ebp - 0x1a8]
0069d5c7  83ba8861000000       cmp      dword ptr [edx + 0x6188], 0
0069d5ce  7510                 jne      0x69d5e0
0069d5d0  8b8558feffff         mov      eax, dword ptr [ebp - 0x1a8]
0069d5d6  c7806461000000000000 mov      dword ptr [eax + 0x6164], 0
0069d5e0  f30f5a45ec           cvtss2sd xmm0, dword ptr [ebp - 0x14]
0069d5e5  660f2f0518297600     comisd   xmm0, xmmword ptr [0x762918]
0069d5ed  0f86ff010000         jbe      0x69d7f2
0069d5f3  f30f5a45f0           cvtss2sd xmm0, dword ptr [ebp - 0x10]
0069d5f8  f20f100d18297600     movsd    xmm1, qword ptr [0x762918]
0069d600  660f2fc8             comisd   xmm1, xmm0
0069d604  0f82e8010000         jb       0x69d7f2
0069d60a  8d8d9cfeffff         lea      ecx, [ebp - 0x164]
0069d610  e8db5dd9ff           call     0x4333f0
0069d615  c745fc07000000       mov      dword ptr [ebp - 4], 7
0069d61c  8d8de4feffff         lea      ecx, [ebp - 0x11c]
0069d622  e8c95dd9ff           call     0x4333f0
0069d627  c645fc08             mov      byte ptr [ebp - 4], 8
0069d62b  51                   push     ecx
0069d62c  d9ee                 fldz     
0069d62e  d91c24               fstp     dword ptr [esp]
0069d631  f30f5a05248d7d00     cvtss2sd xmm0, dword ptr [0x7d8d24]
0069d639  f20f5905f8297600     mulsd    xmm0, qword ptr [0x7629f8]
0069d641  f20f5ac0             cvtsd2ss xmm0, xmm0
0069d645  51                   push     ecx
0069d646  f30f110424           movss    dword ptr [esp], xmm0
0069d64b  f30f5a05288d7d00     cvtss2sd xmm0, dword ptr [0x7d8d28]
0069d653  f20f5905f8297600     mulsd    xmm0, qword ptr [0x7629f8]
0069d65b  f20f5ac0             cvtsd2ss xmm0, xmm0
0069d65f  51                   push     ecx
0069d660  f30f110424           movss    dword ptr [esp], xmm0
0069d665  8d8d34ffffff         lea      ecx, [ebp - 0xcc]
0069d66b  e8605cd9ff           call     0x4332d0
0069d670  c645fc09             mov      byte ptr [ebp - 4], 9
0069d674  8d8d34ffffff         lea      ecx, [ebp - 0xcc]
0069d67a  51                   push     ecx
0069d67b  8d8de4feffff         lea      ecx, [ebp - 0x11c]
0069d681  e8ba5bd9ff           call     0x433240
0069d686  8d959cfeffff         lea      edx, [ebp - 0x164]
0069d68c  b802000000           mov      eax, 2
0069d691  e83a27dfff           call     0x48fdd0
0069d696  8d95e4feffff         lea      edx, [ebp - 0x11c]
0069d69c  b801000000           mov      eax, 1
0069d6a1  e82a27dfff           call     0x48fdd0
0069d6a6  51                   push     ecx
0069d6a7  d905c02c7600         fld      dword ptr [0x762cc0]
0069d6ad  d91c24               fstp     dword ptr [esp]
0069d6b0  51                   push     ecx
0069d6b1  d90528ef7400         fld      dword ptr [0x74ef28]
0069d6b7  d91c24               fstp     dword ptr [esp]
0069d6ba  8d8d28ffffff         lea      ecx, [ebp - 0xd8]
0069d6c0  e84bb6ddff           call     0x478d10
0069d6c5  c645fc0a             mov      byte ptr [ebp - 4], 0xa
0069d6c9  51                   push     ecx
0069d6ca  d905bc2c7600         fld      dword ptr [0x762cbc]
0069d6d0  d91c24               fstp     dword ptr [esp]
0069d6d3  51                   push     ecx
0069d6d4  d905b82c7600         fld      dword ptr [0x762cb8]
0069d6da  d91c24               fstp     dword ptr [esp]
0069d6dd  8d8d74feffff         lea      ecx, [ebp - 0x18c]
0069d6e3  e828b6ddff           call     0x478d10
0069d6e8  898534feffff         mov      dword ptr [ebp - 0x1cc], eax
0069d6ee  8b9534feffff         mov      edx, dword ptr [ebp - 0x1cc]
0069d6f4  899530feffff         mov      dword ptr [ebp - 0x1d0], edx
0069d6fa  c645fc0b             mov      byte ptr [ebp - 4], 0xb
0069d6fe  8b8530feffff         mov      eax, dword ptr [ebp - 0x1d0]
0069d704  50                   push     eax
0069d705  8d8ddcfeffff         lea      ecx, [ebp - 0x124]
0069d70b  51                   push     ecx
0069d70c  8d8d28ffffff         lea      ecx, [ebp - 0xd8]
0069d712  e8392cd7ff           call     0x410350
0069d717  c645fc0d             mov      byte ptr [ebp - 4], 0xd
0069d71b  8d8d74feffff         lea      ecx, [ebp - 0x18c]
0069d721  e8eae9d8ff           call     0x42c110
0069d726  c78530fffffff01148f9 mov      dword ptr [ebp - 0xd0], 0xf94811f0
0069d730  c78540ffffff3c5392fb mov      dword ptr [ebp - 0xc0], 0xfb92533c
0069d73a  51                   push     ecx
0069d73b  8bcc                 mov      ecx, esp
0069d73d  89a570feffff         mov      dword ptr [ebp - 0x190], esp
0069d743  8b9540ffffff         mov      edx, dword ptr [ebp - 0xc0]
0069d749  52                   push     edx
0069d74a  e82102d7ff           call     0x40d970
0069d74f  51                   push     ecx
0069d750  8bcc                 mov      ecx, esp
0069d752  89a56cfeffff         mov      dword ptr [ebp - 0x194], esp
0069d758  8b8530ffffff         mov      eax, dword ptr [ebp - 0xd0]
0069d75e  50                   push     eax
0069d75f  e80c02d7ff           call     0x40d970
0069d764  51                   push     ecx
0069d765  d945ec               fld      dword ptr [ebp - 0x14]
0069d768  d91c24               fstp     dword ptr [esp]
0069d76b  51                   push     ecx
0069d76c  d9e8                 fld1     
0069d76e  d91c24               fstp     dword ptr [esp]
0069d771  51                   push     ecx
0069d772  d9e8                 fld1     
0069d774  d91c24               fstp     dword ptr [esp]
0069d777  51                   push     ecx
0069d778  d9e8                 fld1     
0069d77a  d91c24               fstp     dword ptr [esp]
0069d77d  8d8d5cfeffff         lea      ecx, [ebp - 0x1a4]
0069d783  e83859d9ff           call     0x4330c0
0069d788  50                   push     eax
0069d789  8d8ddcfeffff         lea      ecx, [ebp - 0x124]
0069d78f  51                   push     ecx
0069d790  8d9528ffffff         lea      edx, [ebp - 0xd8]
0069d796  52                   push     edx
0069d797  e8b433dfff           call     0x490b50
0069d79c  83c414               add      esp, 0x14
0069d79f  e81c2bdfff           call     0x4902c0
0069d7a4  c645fc0a             mov      byte ptr [ebp - 4], 0xa
0069d7a8  8d8ddcfeffff         lea      ecx, [ebp - 0x124]
0069d7ae  e85de9d8ff           call     0x42c110
0069d7b3  c645fc09             mov      byte ptr [ebp - 4], 9
0069d7b7  8d8d28ffffff         lea      ecx, [ebp - 0xd8]
0069d7bd  e84ee9d8ff           call     0x42c110
0069d7c2  c645fc08             mov      byte ptr [ebp - 4], 8
0069d7c6  8d8d34ffffff         lea      ecx, [ebp - 0xcc]
0069d7cc  e83fe9d8ff           call     0x42c110
0069d7d1  c645fc07             mov      byte ptr [ebp - 4], 7
0069d7d5  8d8de4feffff         lea      ecx, [ebp - 0x11c]
0069d7db  e830e9d8ff           call     0x42c110
0069d7e0  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069d7e7  8d8d9cfeffff         lea      ecx, [ebp - 0x164]
0069d7ed  e81ee9d8ff           call     0x42c110
0069d7f2  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
0069d7f5  64890d00000000       mov      dword ptr fs:[0], ecx
0069d7fc  59                   pop      ecx
0069d7fd  5e                   pop      esi
0069d7fe  8be5                 mov      esp, ebp
0069d800  5d                   pop      ebp
0069d801  c3                   ret      
0069d802  cc                   int3     
0069d803  cc                   int3     
0069d804  cc                   int3     
0069d805  cc                   int3     
0069d806  cc                   int3     
0069d807  cc                   int3     
0069d808  cc                   int3     
0069d809  cc                   int3     
0069d80a  cc                   int3     
0069d80b  cc                   int3     
0069d80c  cc                   int3     
0069d80d  cc                   int3     
0069d80e  cc                   int3     
0069d80f  cc                   int3     
0069d810  55                   push     ebp
0069d811  8bec                 mov      ebp, esp
0069d813  6aff                 push     -1
0069d815  6898946c00           push     0x6c9498
0069d81a  64a100000000         mov      eax, dword ptr fs:[0]
0069d820  50                   push     eax
0069d821  81ec5c010000         sub      esp, 0x15c
0069d827  56                   push     esi
0069d828  a108957c00           mov      eax, dword ptr [0x7c9508]
0069d82d  33c5                 xor      eax, ebp
0069d82f  50                   push     eax
0069d830  8d45f4               lea      eax, [ebp - 0xc]
0069d833  64a300000000         mov      dword ptr fs:[0], eax
0069d839  898dc4feffff         mov      dword ptr [ebp - 0x13c], ecx
0069d83f  f30f1005902c7600     movss    xmm0, dword ptr [0x762c90]
0069d847  f30f1145f0           movss    dword ptr [ebp - 0x10], xmm0
0069d84c  8b4508               mov      eax, dword ptr [ebp + 8]
0069d84f  8b4804               mov      ecx, dword ptr [eax + 4]
0069d852  898dc0feffff         mov      dword ptr [ebp - 0x140], ecx
0069d858  8b95c0feffff         mov      edx, dword ptr [ebp - 0x140]
0069d85e  83ea10               sub      edx, 0x10
0069d861  8995c0feffff         mov      dword ptr [ebp - 0x140], edx
0069d867  83bdc0feffff22       cmp      dword ptr [ebp - 0x140], 0x22
0069d86e  0f87360d0000         ja       0x69e5aa
0069d874  8b85c0feffff         mov      eax, dword ptr [ebp - 0x140]
0069d87a  0fb68818e66900       movzx    ecx, byte ptr [eax + 0x69e618]
0069d881  ff248dbce56900       jmp      dword ptr [ecx*4 + 0x69e5bc]
0069d888  8bb5c4feffff         mov      esi, dword ptr [ebp - 0x13c]
0069d88e  81c640610000         add      esi, 0x6140
0069d894  e847f1f0ff           call     0x5ac9e0
0069d899  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d89f  8b8260610000         mov      eax, dword ptr [edx + 0x6160]
0069d8a5  83c001               add      eax, 1
0069d8a8  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069d8ae  898160610000         mov      dword ptr [ecx + 0x6160], eax
0069d8b4  e9f10c0000           jmp      0x69e5aa
0069d8b9  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d8bf  8b8260610000         mov      eax, dword ptr [edx + 0x6160]
0069d8c5  83e801               sub      eax, 1
0069d8c8  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069d8ce  898160610000         mov      dword ptr [ecx + 0x6160], eax
0069d8d4  e9d10c0000           jmp      0x69e5aa
0069d8d9  8bb5c4feffff         mov      esi, dword ptr [ebp - 0x13c]
0069d8df  81c668610000         add      esi, 0x6168
0069d8e5  e8f6f0f0ff           call     0x5ac9e0
0069d8ea  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d8f0  8b8288610000         mov      eax, dword ptr [edx + 0x6188]
0069d8f6  83c001               add      eax, 1
0069d8f9  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069d8ff  898188610000         mov      dword ptr [ecx + 0x6188], eax
0069d905  e9a00c0000           jmp      0x69e5aa
0069d90a  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d910  8b8288610000         mov      eax, dword ptr [edx + 0x6188]
0069d916  83e801               sub      eax, 1
0069d919  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069d91f  898188610000         mov      dword ptr [ecx + 0x6188], eax
0069d925  e9800c0000           jmp      0x69e5aa
0069d92a  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d930  8b420c               mov      eax, dword ptr [edx + 0xc]
0069d933  50                   push     eax
0069d934  6a26                 push     0x26
0069d936  8d8d10ffffff         lea      ecx, [ebp - 0xf0]
0069d93c  e8af2bd9ff           call     0x4304f0
0069d941  8985bcfeffff         mov      dword ptr [ebp - 0x144], eax
0069d947  8b8dbcfeffff         mov      ecx, dword ptr [ebp - 0x144]
0069d94d  898db8feffff         mov      dword ptr [ebp - 0x148], ecx
0069d953  c745fc00000000       mov      dword ptr [ebp - 4], 0
0069d95a  8b95b8feffff         mov      edx, dword ptr [ebp - 0x148]
0069d960  52                   push     edx
0069d961  e83ac6ffff           call     0x699fa0
0069d966  8bc8                 mov      ecx, eax
0069d968  e8332dd9ff           call     0x4306a0
0069d96d  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069d974  8d8d10ffffff         lea      ecx, [ebp - 0xf0]
0069d97a  e8212cd9ff           call     0x4305a0
0069d97f  e9260c0000           jmp      0x69e5aa
0069d984  f30f5a45f0           cvtss2sd xmm0, dword ptr [ebp - 0x10]
0069d989  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069d98f  f30f5a8820610000     cvtss2sd xmm1, dword ptr [eax + 0x6120]
0069d997  f20f5ec1             divsd    xmm0, xmm1
0069d99b  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069d9a1  f30f5a891c610000     cvtss2sd xmm1, dword ptr [ecx + 0x611c]
0069d9a9  f20f58c8             addsd    xmm1, xmm0
0069d9ad  f20f5ac1             cvtsd2ss xmm0, xmm1
0069d9b1  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d9b7  f30f11821c610000     movss    dword ptr [edx + 0x611c], xmm0
0069d9bf  e9e60b0000           jmp      0x69e5aa
0069d9c4  f30f5a45f0           cvtss2sd xmm0, dword ptr [ebp - 0x10]
0069d9c9  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069d9cf  f30f5a8820610000     cvtss2sd xmm1, dword ptr [eax + 0x6120]
0069d9d7  f20f5ec1             divsd    xmm0, xmm1
0069d9db  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069d9e1  f30f5a891c610000     cvtss2sd xmm1, dword ptr [ecx + 0x611c]
0069d9e9  f20f5cc8             subsd    xmm1, xmm0
0069d9ed  f20f5ac1             cvtsd2ss xmm0, xmm1
0069d9f1  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069d9f7  f30f11821c610000     movss    dword ptr [edx + 0x611c], xmm0
0069d9ff  e9a60b0000           jmp      0x69e5aa
0069da04  f30f5a45f0           cvtss2sd xmm0, dword ptr [ebp - 0x10]
0069da09  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069da0f  f30f5a8820610000     cvtss2sd xmm1, dword ptr [eax + 0x6120]
0069da17  f20f5ec1             divsd    xmm0, xmm1
0069da1b  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069da21  f30f5a8918610000     cvtss2sd xmm1, dword ptr [ecx + 0x6118]
0069da29  f20f5cc8             subsd    xmm1, xmm0
0069da2d  f20f5ac1             cvtsd2ss xmm0, xmm1
0069da31  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069da37  f30f118218610000     movss    dword ptr [edx + 0x6118], xmm0
0069da3f  e9660b0000           jmp      0x69e5aa
0069da44  f30f5a45f0           cvtss2sd xmm0, dword ptr [ebp - 0x10]
0069da49  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069da4f  f30f5a8820610000     cvtss2sd xmm1, dword ptr [eax + 0x6120]
0069da57  f20f5ec1             divsd    xmm0, xmm1
0069da5b  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069da61  f30f5a8918610000     cvtss2sd xmm1, dword ptr [ecx + 0x6118]
0069da69  f20f58c8             addsd    xmm1, xmm0
0069da6d  f20f5ac1             cvtsd2ss xmm0, xmm1
0069da71  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069da77  f30f118218610000     movss    dword ptr [edx + 0x6118], xmm0
0069da7f  e9260b0000           jmp      0x69e5aa
0069da84  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069da8a  f30f5a8020610000     cvtss2sd xmm0, dword ptr [eax + 0x6120]
0069da92  660f2f05202b7600     comisd   xmm0, xmmword ptr [0x762b20]
0069da9a  0f86cb000000         jbe      0x69db6b
0069daa0  51                   push     ecx
0069daa1  d945f0               fld      dword ptr [ebp - 0x10]
0069daa4  d91c24               fstp     dword ptr [esp]
0069daa7  51                   push     ecx
0069daa8  d945f0               fld      dword ptr [ebp - 0x10]
0069daab  d91c24               fstp     dword ptr [esp]
0069daae  8d8d08ffffff         lea      ecx, [ebp - 0xf8]
0069dab4  e857b2ddff           call     0x478d10
0069dab9  8985b4feffff         mov      dword ptr [ebp - 0x14c], eax
0069dabf  8b8db4feffff         mov      ecx, dword ptr [ebp - 0x14c]
0069dac5  898db0feffff         mov      dword ptr [ebp - 0x150], ecx
0069dacb  c745fc01000000       mov      dword ptr [ebp - 4], 1
0069dad2  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dad8  51                   push     ecx
0069dad9  d98220610000         fld      dword ptr [edx + 0x6120]
0069dadf  d91c24               fstp     dword ptr [esp]
0069dae2  8d8500ffffff         lea      eax, [ebp - 0x100]
0069dae8  50                   push     eax
0069dae9  8b8db0feffff         mov      ecx, dword ptr [ebp - 0x150]
0069daef  e86c58d9ff           call     0x433360
0069daf4  8985acfeffff         mov      dword ptr [ebp - 0x154], eax
0069dafa  8b8dacfeffff         mov      ecx, dword ptr [ebp - 0x154]
0069db00  898da8feffff         mov      dword ptr [ebp - 0x158], ecx
0069db06  c645fc02             mov      byte ptr [ebp - 4], 2
0069db0a  8b95a8feffff         mov      edx, dword ptr [ebp - 0x158]
0069db10  52                   push     edx
0069db11  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069db17  81c118610000         add      ecx, 0x6118
0069db1d  e8de22d9ff           call     0x42fe00
0069db22  c645fc01             mov      byte ptr [ebp - 4], 1
0069db26  8d8d00ffffff         lea      ecx, [ebp - 0x100]
0069db2c  e8dfe5d8ff           call     0x42c110
0069db31  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069db38  8d8d08ffffff         lea      ecx, [ebp - 0xf8]
0069db3e  e8cde5d8ff           call     0x42c110
0069db43  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069db49  f30f5a8020610000     cvtss2sd xmm0, dword ptr [eax + 0x6120]
0069db51  f20f5c05202b7600     subsd    xmm0, qword ptr [0x762b20]
0069db59  f20f5ac0             cvtsd2ss xmm0, xmm0
0069db5d  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069db63  f30f118120610000     movss    dword ptr [ecx + 0x6120], xmm0
0069db6b  e93a0a0000           jmp      0x69e5aa
0069db70  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069db76  f30f5a8220610000     cvtss2sd xmm0, dword ptr [edx + 0x6120]
0069db7e  f20f100dd0297600     movsd    xmm1, qword ptr [0x7629d0]
0069db86  660f2fc8             comisd   xmm1, xmm0
0069db8a  0f86cb000000         jbe      0x69dc5b
0069db90  51                   push     ecx
0069db91  d945f0               fld      dword ptr [ebp - 0x10]
0069db94  d91c24               fstp     dword ptr [esp]
0069db97  51                   push     ecx
0069db98  d945f0               fld      dword ptr [ebp - 0x10]
0069db9b  d91c24               fstp     dword ptr [esp]
0069db9e  8d8df8feffff         lea      ecx, [ebp - 0x108]
0069dba4  e867b1ddff           call     0x478d10
0069dba9  8985a4feffff         mov      dword ptr [ebp - 0x15c], eax
0069dbaf  8b85a4feffff         mov      eax, dword ptr [ebp - 0x15c]
0069dbb5  8985a0feffff         mov      dword ptr [ebp - 0x160], eax
0069dbbb  c745fc03000000       mov      dword ptr [ebp - 4], 3
0069dbc2  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dbc8  51                   push     ecx
0069dbc9  d98120610000         fld      dword ptr [ecx + 0x6120]
0069dbcf  d91c24               fstp     dword ptr [esp]
0069dbd2  8d95f0feffff         lea      edx, [ebp - 0x110]
0069dbd8  52                   push     edx
0069dbd9  8b8da0feffff         mov      ecx, dword ptr [ebp - 0x160]
0069dbdf  e87c57d9ff           call     0x433360
0069dbe4  89859cfeffff         mov      dword ptr [ebp - 0x164], eax
0069dbea  8b859cfeffff         mov      eax, dword ptr [ebp - 0x164]
0069dbf0  898598feffff         mov      dword ptr [ebp - 0x168], eax
0069dbf6  c645fc04             mov      byte ptr [ebp - 4], 4
0069dbfa  8b8d98feffff         mov      ecx, dword ptr [ebp - 0x168]
0069dc00  51                   push     ecx
0069dc01  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dc07  81c118610000         add      ecx, 0x6118
0069dc0d  e83e22d9ff           call     0x42fe50
0069dc12  c645fc03             mov      byte ptr [ebp - 4], 3
0069dc16  8d8df0feffff         lea      ecx, [ebp - 0x110]
0069dc1c  e8efe4d8ff           call     0x42c110
0069dc21  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069dc28  8d8df8feffff         lea      ecx, [ebp - 0x108]
0069dc2e  e8dde4d8ff           call     0x42c110
0069dc33  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dc39  f30f5a8220610000     cvtss2sd xmm0, dword ptr [edx + 0x6120]
0069dc41  f20f5805202b7600     addsd    xmm0, qword ptr [0x762b20]
0069dc49  f20f5ac0             cvtsd2ss xmm0, xmm0
0069dc4d  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dc53  f30f118020610000     movss    dword ptr [eax + 0x6120], xmm0
0069dc5b  e94a090000           jmp      0x69e5aa
0069dc60  68f09e7d00           push     0x7d9ef0
0069dc65  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dc6b  81c118610000         add      ecx, 0x6118
0069dc71  e87a27d7ff           call     0x4103f0
0069dc76  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dc7c  f30f1005c8e87400     movss    xmm0, dword ptr [0x74e8c8]
0069dc84  f30f118120610000     movss    dword ptr [ecx + 0x6120], xmm0
0069dc8c  e919090000           jmp      0x69e5aa
0069dc91  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dc97  8b4508               mov      eax, dword ptr [ebp + 8]
0069dc9a  8b4818               mov      ecx, dword ptr [eax + 0x18]
0069dc9d  894a0c               mov      dword ptr [edx + 0xc], ecx
0069dca0  e905090000           jmp      0x69e5aa
0069dca5  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dcab  0fb6828d610000       movzx    eax, byte ptr [edx + 0x618d]
0069dcb2  f7d8                 neg      eax
0069dcb4  1bc0                 sbb      eax, eax
0069dcb6  83c001               add      eax, 1
0069dcb9  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dcbf  88818d610000         mov      byte ptr [ecx + 0x618d], al
0069dcc5  e9e0080000           jmp      0x69e5aa
0069dcca  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dcd0  0fb6828c610000       movzx    eax, byte ptr [edx + 0x618c]
0069dcd7  f7d8                 neg      eax
0069dcd9  1bc0                 sbb      eax, eax
0069dcdb  83c001               add      eax, 1
0069dcde  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dce4  88818c610000         mov      byte ptr [ecx + 0x618c], al
0069dcea  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dcf0  0fb6828c610000       movzx    eax, byte ptr [edx + 0x618c]
0069dcf7  85c0                 test     eax, eax
0069dcf9  7512                 jne      0x69dd0d
0069dcfb  ff151ce07200         call     dword ptr [0x72e01c]
0069dd01  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dd07  898190610000         mov      dword ptr [ecx + 0x6190], eax
0069dd0d  e998080000           jmp      0x69e5aa
0069dd12  8b5508               mov      edx, dword ptr [ebp + 8]
0069dd15  837a1800             cmp      dword ptr [edx + 0x18], 0
0069dd19  0f95c0               setne    al
0069dd1c  0fb6c8               movzx    ecx, al
0069dd1f  51                   push     ecx
0069dd20  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dd26  e8251ce7ff           call     0x50f950
0069dd2b  e97a080000           jmp      0x69e5aa
0069dd30  8b5508               mov      edx, dword ptr [ebp + 8]
0069dd33  837a1802             cmp      dword ptr [edx + 0x18], 2
0069dd37  7422                 je       0x69dd5b
0069dd39  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dd3f  0fb6888e610000       movzx    ecx, byte ptr [eax + 0x618e]
0069dd46  f7d9                 neg      ecx
0069dd48  1bc9                 sbb      ecx, ecx
0069dd4a  83c101               add      ecx, 1
0069dd4d  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069dd53  888a8e610000         mov      byte ptr [edx + 0x618e], cl
0069dd59  eb0d                 jmp      0x69dd68
0069dd5b  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dd61  c6808e61000001       mov      byte ptr [eax + 0x618e], 1
0069dd68  e93d080000           jmp      0x69e5aa
0069dd6d  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dd73  0fb65104             movzx    edx, byte ptr [ecx + 4]
0069dd77  f7da                 neg      edx
0069dd79  1bd2                 sbb      edx, edx
0069dd7b  83c201               add      edx, 1
0069dd7e  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dd84  885004               mov      byte ptr [eax + 4], dl
0069dd87  e91e080000           jmp      0x69e5aa
0069dd8c  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dd92  81c1f8600000         add      ecx, 0x60f8
0069dd98  e873cfd8ff           call     0x42ad10
0069dd9d  0fb6c8               movzx    ecx, al
0069dda0  85c9                 test     ecx, ecx
0069dda2  7412                 je       0x69ddb6
0069dda4  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069ddaa  c7420cffffffff       mov      dword ptr [edx + 0xc], 0xffffffff
0069ddb1  e9db000000           jmp      0x69de91
0069ddb6  8d45e8               lea      eax, [ebp - 0x18]
0069ddb9  50                   push     eax
0069ddba  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069ddc0  81c1f8600000         add      ecx, 0x60f8
0069ddc6  e8952ad9ff           call     0x430860
0069ddcb  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
0069ddce  894dec               mov      dword ptr [ebp - 0x14], ecx
0069ddd1  8d55e4               lea      edx, [ebp - 0x1c]
0069ddd4  52                   push     edx
0069ddd5  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dddb  81c1f8600000         add      ecx, 0x60f8
0069dde1  e8aa2ad9ff           call     0x430890
0069dde6  eb08                 jmp      0x69ddf0
0069dde8  8d4dec               lea      ecx, [ebp - 0x14]
0069ddeb  e8102bd9ff           call     0x430900
0069ddf0  8d45e4               lea      eax, [ebp - 0x1c]
0069ddf3  50                   push     eax
0069ddf4  8d4dec               lea      ecx, [ebp - 0x14]
0069ddf7  51                   push     ecx
0069ddf8  e8632fd9ff           call     0x430d60
0069ddfd  83c408               add      esp, 8
0069de00  0fb6d0               movzx    edx, al
0069de03  85d2                 test     edx, edx
0069de05  7460                 je       0x69de67
0069de07  8d4dec               lea      ecx, [ebp - 0x14]
0069de0a  e8312bd9ff           call     0x430940
0069de0f  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069de15  8b10                 mov      edx, dword ptr [eax]
0069de17  3b510c               cmp      edx, dword ptr [ecx + 0xc]
0069de1a  7549                 jne      0x69de65
0069de1c  8d4dec               lea      ecx, [ebp - 0x14]
0069de1f  e8dc2ad9ff           call     0x430900
0069de24  8d45e4               lea      eax, [ebp - 0x1c]
0069de27  50                   push     eax
0069de28  8d4dec               lea      ecx, [ebp - 0x14]
0069de2b  51                   push     ecx
0069de2c  e84f2fd9ff           call     0x430d80
0069de31  83c408               add      esp, 8
0069de34  0fb6d0               movzx    edx, al
0069de37  85d2                 test     edx, edx
0069de39  7415                 je       0x69de50
0069de3b  8d4de8               lea      ecx, [ebp - 0x18]
0069de3e  e8fd2ad9ff           call     0x430940
0069de43  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069de49  8b10                 mov      edx, dword ptr [eax]
0069de4b  89510c               mov      dword ptr [ecx + 0xc], edx
0069de4e  eb13                 jmp      0x69de63
0069de50  8d4dec               lea      ecx, [ebp - 0x14]
0069de53  e8e82ad9ff           call     0x430940
0069de58  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069de5e  8b10                 mov      edx, dword ptr [eax]
0069de60  89510c               mov      dword ptr [ecx + 0xc], edx
0069de63  eb02                 jmp      0x69de67
0069de65  eb81                 jmp      0x69dde8
0069de67  8d45e4               lea      eax, [ebp - 0x1c]
0069de6a  50                   push     eax
0069de6b  8d4dec               lea      ecx, [ebp - 0x14]
0069de6e  51                   push     ecx
0069de6f  e80c2fd9ff           call     0x430d80
0069de74  83c408               add      esp, 8
0069de77  0fb6d0               movzx    edx, al
0069de7a  85d2                 test     edx, edx
0069de7c  7413                 je       0x69de91
0069de7e  8d4de8               lea      ecx, [ebp - 0x18]
0069de81  e8ba2ad9ff           call     0x430940
0069de86  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069de8c  8b10                 mov      edx, dword ptr [eax]
0069de8e  89510c               mov      dword ptr [ecx + 0xc], edx
0069de91  e914070000           jmp      0x69e5aa
0069de96  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069de9c  81c1f8600000         add      ecx, 0x60f8
0069dea2  e869ced8ff           call     0x42ad10
0069dea7  0fb6c0               movzx    eax, al
0069deaa  85c0                 test     eax, eax
0069deac  7412                 je       0x69dec0
0069deae  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069deb4  c7410cffffffff       mov      dword ptr [ecx + 0xc], 0xffffffff
0069debb  e9cf000000           jmp      0x69df8f
0069dec0  8d55dc               lea      edx, [ebp - 0x24]
0069dec3  52                   push     edx
0069dec4  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069deca  81c1f8600000         add      ecx, 0x60f8
0069ded0  e86bbcd7ff           call     0x419b40
0069ded5  8b45dc               mov      eax, dword ptr [ebp - 0x24]
0069ded8  8945e0               mov      dword ptr [ebp - 0x20], eax
0069dedb  8d4dd8               lea      ecx, [ebp - 0x28]
0069dede  51                   push     ecx
0069dedf  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dee5  81c1f8600000         add      ecx, 0x60f8
0069deeb  e8a0abd9ff           call     0x438a90
0069def0  eb08                 jmp      0x69defa
0069def2  8d4de0               lea      ecx, [ebp - 0x20]
0069def5  e8262ad9ff           call     0x430920
0069defa  8d55d8               lea      edx, [ebp - 0x28]
0069defd  52                   push     edx
0069defe  8d4de0               lea      ecx, [ebp - 0x20]
0069df01  e8ca70d7ff           call     0x414fd0
0069df06  0fb6c0               movzx    eax, al
0069df09  85c0                 test     eax, eax
0069df0b  745c                 je       0x69df69
0069df0d  8d4de0               lea      ecx, [ebp - 0x20]
0069df10  e89bacd9ff           call     0x438bb0
0069df15  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069df1b  8b10                 mov      edx, dword ptr [eax]
0069df1d  3b510c               cmp      edx, dword ptr [ecx + 0xc]
0069df20  7545                 jne      0x69df67
0069df22  8d4de0               lea      ecx, [ebp - 0x20]
0069df25  e8f629d9ff           call     0x430920
0069df2a  8d45d8               lea      eax, [ebp - 0x28]
0069df2d  50                   push     eax
0069df2e  8d4de0               lea      ecx, [ebp - 0x20]
0069df31  e80a33d9ff           call     0x431240
0069df36  0fb6c8               movzx    ecx, al
0069df39  85c9                 test     ecx, ecx
0069df3b  7415                 je       0x69df52
0069df3d  8d4ddc               lea      ecx, [ebp - 0x24]
0069df40  e86bacd9ff           call     0x438bb0
0069df45  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069df4b  8b00                 mov      eax, dword ptr [eax]
0069df4d  89420c               mov      dword ptr [edx + 0xc], eax
0069df50  eb13                 jmp      0x69df65
0069df52  8d4de0               lea      ecx, [ebp - 0x20]
0069df55  e856acd9ff           call     0x438bb0
0069df5a  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069df60  8b10                 mov      edx, dword ptr [eax]
0069df62  89510c               mov      dword ptr [ecx + 0xc], edx
0069df65  eb02                 jmp      0x69df69
0069df67  eb89                 jmp      0x69def2
0069df69  8d45d8               lea      eax, [ebp - 0x28]
0069df6c  50                   push     eax
0069df6d  8d4de0               lea      ecx, [ebp - 0x20]
0069df70  e8cb32d9ff           call     0x431240
0069df75  0fb6c8               movzx    ecx, al
0069df78  85c9                 test     ecx, ecx
0069df7a  7413                 je       0x69df8f
0069df7c  8d4ddc               lea      ecx, [ebp - 0x24]
0069df7f  e82cacd9ff           call     0x438bb0
0069df84  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069df8a  8b00                 mov      eax, dword ptr [eax]
0069df8c  89420c               mov      dword ptr [edx + 0xc], eax
0069df8f  e916060000           jmp      0x69e5aa
0069df94  8b4508               mov      eax, dword ptr [ebp + 8]
0069df97  83c028               add      eax, 0x28
0069df9a  e8312af1ff           call     0x5b09d0
0069df9f  0fb6c8               movzx    ecx, al
0069dfa2  85c9                 test     ecx, ecx
0069dfa4  0f84de050000         je       0x69e588
0069dfaa  8b5508               mov      edx, dword ptr [ebp + 8]
0069dfad  837a280a             cmp      dword ptr [edx + 0x28], 0xa
0069dfb1  754a                 jne      0x69dffd
0069dfb3  8b4508               mov      eax, dword ptr [ebp + 8]
0069dfb6  f30f5a4034           cvtss2sd xmm0, dword ptr [eax + 0x34]
0069dfbb  660f2f0518297600     comisd   xmm0, xmmword ptr [0x762918]
0069dfc3  761d                 jbe      0x69dfe2
0069dfc5  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dfcb  8b9124610000         mov      edx, dword ptr [ecx + 0x6124]
0069dfd1  83c201               add      edx, 1
0069dfd4  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dfda  899024610000         mov      dword ptr [eax + 0x6124], edx
0069dfe0  eb1b                 jmp      0x69dffd
0069dfe2  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069dfe8  8b9124610000         mov      edx, dword ptr [ecx + 0x6124]
0069dfee  83ea01               sub      edx, 1
0069dff1  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069dff7  899024610000         mov      dword ptr [eax + 0x6124], edx
0069dffd  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e003  8b9124610000         mov      edx, dword ptr [ecx + 0x6124]
0069e009  52                   push     edx
0069e00a  6a64                 push     0x64
0069e00c  6a00                 push     0
0069e00e  e88d2dd9ff           call     0x430da0
0069e013  83c40c               add      esp, 0xc
0069e016  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e01c  898124610000         mov      dword ptr [ecx + 0x6124], eax
0069e022  8b5508               mov      edx, dword ptr [ebp + 8]
0069e025  f30f2a4238           cvtsi2ss xmm0, dword ptr [edx + 0x38]
0069e02a  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069e030  f30f118094610000     movss    dword ptr [eax + 0x6194], xmm0
0069e038  8b4d08               mov      ecx, dword ptr [ebp + 8]
0069e03b  f30f2a413c           cvtsi2ss xmm0, dword ptr [ecx + 0x3c]
0069e040  f30f5a0d248d7d00     cvtss2sd xmm1, dword ptr [0x7d8d24]
0069e048  f30f5ac0             cvtss2sd xmm0, xmm0
0069e04c  f20f5cc8             subsd    xmm1, xmm0
0069e050  f20f5ac1             cvtsd2ss xmm0, xmm1
0069e054  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069e05a  f30f118298610000     movss    dword ptr [edx + 0x6198], xmm0
0069e062  8b4508               mov      eax, dword ptr [ebp + 8]
0069e065  83783001             cmp      dword ptr [eax + 0x30], 1
0069e069  0f857a020000         jne      0x69e2e9
0069e06f  8b4d08               mov      ecx, dword ptr [ebp + 8]
0069e072  83792807             cmp      dword ptr [ecx + 0x28], 7
0069e076  0f856d020000         jne      0x69e2e9
0069e07c  8b5508               mov      edx, dword ptr [ebp + 8]
0069e07f  f30f2a423c           cvtsi2ss xmm0, dword ptr [edx + 0x3c]
0069e084  f30f5a0d248d7d00     cvtss2sd xmm1, dword ptr [0x7d8d24]
0069e08c  f30f5ac0             cvtss2sd xmm0, xmm0
0069e090  f20f5cc8             subsd    xmm1, xmm0
0069e094  f20f5ac1             cvtsd2ss xmm0, xmm1
0069e098  51                   push     ecx
0069e099  f30f110424           movss    dword ptr [esp], xmm0
0069e09e  8b4508               mov      eax, dword ptr [ebp + 8]
0069e0a1  f30f2a4038           cvtsi2ss xmm0, dword ptr [eax + 0x38]
0069e0a6  51                   push     ecx
0069e0a7  f30f110424           movss    dword ptr [esp], xmm0
0069e0ac  8d4db4               lea      ecx, [ebp - 0x4c]
0069e0af  e85cacddff           call     0x478d10
0069e0b4  c745fc05000000       mov      dword ptr [ebp - 4], 5
0069e0bb  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e0c1  8b510c               mov      edx, dword ptr [ecx + 0xc]
0069e0c4  8955bc               mov      dword ptr [ebp - 0x44], edx
0069e0c7  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069e0cd  c7400cffffffff       mov      dword ptr [eax + 0xc], 0xffffffff
0069e0d4  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e0da  c74110ffffffff       mov      dword ptr [ecx + 0x10], 0xffffffff
0069e0e1  f30f100520297600     movss    xmm0, dword ptr [0x762920]
0069e0e9  f30f1145d0           movss    dword ptr [ebp - 0x30], xmm0
0069e0ee  8d4dc0               lea      ecx, [ebp - 0x40]
0069e0f1  e8ca26d7ff           call     0x4107c0
0069e0f6  c645fc06             mov      byte ptr [ebp - 4], 6
0069e0fa  8d55b0               lea      edx, [ebp - 0x50]
0069e0fd  52                   push     edx
0069e0fe  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e104  81c1f8600000         add      ecx, 0x60f8
0069e10a  e831bad7ff           call     0x419b40
0069e10f  8d45ac               lea      eax, [ebp - 0x54]
0069e112  50                   push     eax
0069e113  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e119  81c1f8600000         add      ecx, 0x60f8
0069e11f  e86ca9d9ff           call     0x438a90
0069e124  eb08                 jmp      0x69e12e
0069e126  8d4db0               lea      ecx, [ebp - 0x50]
0069e129  e8f227d9ff           call     0x430920
0069e12e  8d4dac               lea      ecx, [ebp - 0x54]
0069e131  51                   push     ecx
0069e132  8d4db0               lea      ecx, [ebp - 0x50]
0069e135  e8966ed7ff           call     0x414fd0
0069e13a  0fb6d0               movzx    edx, al
0069e13d  85d2                 test     edx, edx
0069e13f  0f84bb000000         je       0x69e200
0069e145  8d45b4               lea      eax, [ebp - 0x4c]
0069e148  50                   push     eax
0069e149  8d4db0               lea      ecx, [ebp - 0x50]
0069e14c  e85faad9ff           call     0x438bb0
0069e151  83c004               add      eax, 4
0069e154  8bc8                 mov      ecx, eax
0069e156  e8551cd9ff           call     0x42fdb0
0069e15b  d95da8               fstp     dword ptr [ebp - 0x58]
0069e15e  f30f5a45a8           cvtss2sd xmm0, dword ptr [ebp - 0x58]
0069e163  f20f100d902d7600     movsd    xmm1, qword ptr [0x762d90]
0069e16b  660f2fc8             comisd   xmm1, xmm0
0069e16f  0f8686000000         jbe      0x69e1fb
0069e175  8d4dc0               lea      ecx, [ebp - 0x40]
0069e178  e843ebdcff           call     0x46ccc0
0069e17d  0fb6c8               movzx    ecx, al
0069e180  85c9                 test     ecx, ecx
0069e182  7527                 jne      0x69e1ab
0069e184  51                   push     ecx
0069e185  d90584f97400         fld      dword ptr [0x74f984]
0069e18b  d91c24               fstp     dword ptr [esp]
0069e18e  51                   push     ecx
0069e18f  d945a8               fld      dword ptr [ebp - 0x58]
0069e192  d91c24               fstp     dword ptr [esp]
0069e195  51                   push     ecx
0069e196  d945d0               fld      dword ptr [ebp - 0x30]
0069e199  d91c24               fstp     dword ptr [esp]
0069e19c  e87ff9d6ff           call     0x40db20
0069e1a1  83c40c               add      esp, 0xc
0069e1a4  0fb6d0               movzx    edx, al
0069e1a7  85d2                 test     edx, edx
0069e1a9  741d                 je       0x69e1c8
0069e1ab  f30f1045a8           movss    xmm0, dword ptr [ebp - 0x58]
0069e1b0  f30f1145d0           movss    dword ptr [ebp - 0x30], xmm0
0069e1b5  8d4db0               lea      ecx, [ebp - 0x50]
0069e1b8  e8f3a9d9ff           call     0x438bb0
0069e1bd  50                   push     eax
0069e1be  8d4dc0               lea      ecx, [ebp - 0x40]
0069e1c1  e89ab9d7ff           call     0x419b60
0069e1c6  eb33                 jmp      0x69e1fb
0069e1c8  f30f5a45a8           cvtss2sd xmm0, dword ptr [ebp - 0x58]
0069e1cd  f30f5a4dd0           cvtss2sd xmm1, dword ptr [ebp - 0x30]
0069e1d2  660f2fc8             comisd   xmm1, xmm0
0069e1d6  7623                 jbe      0x69e1fb
0069e1d8  f30f1045a8           movss    xmm0, dword ptr [ebp - 0x58]
0069e1dd  f30f1145d0           movss    dword ptr [ebp - 0x30], xmm0
0069e1e2  8d4dc0               lea      ecx, [ebp - 0x40]
0069e1e5  e87673ddff           call     0x475560
0069e1ea  8d4db0               lea      ecx, [ebp - 0x50]
0069e1ed  e8bea9d9ff           call     0x438bb0
0069e1f2  50                   push     eax
0069e1f3  8d4dc0               lea      ecx, [ebp - 0x40]
0069e1f6  e865b9d7ff           call     0x419b60
0069e1fb  e926ffffff           jmp      0x69e126
0069e200  8d45bc               lea      eax, [ebp - 0x44]
0069e203  50                   push     eax
0069e204  8d8decfeffff         lea      ecx, [ebp - 0x114]
0069e20a  51                   push     ecx
0069e20b  8d4dc0               lea      ecx, [ebp - 0x40]
0069e20e  e87da8d9ff           call     0x438a90
0069e213  8b10                 mov      edx, dword ptr [eax]
0069e215  52                   push     edx
0069e216  8d85e8feffff         lea      eax, [ebp - 0x118]
0069e21c  50                   push     eax
0069e21d  8d4dc0               lea      ecx, [ebp - 0x40]
0069e220  e81bb9d7ff           call     0x419b40
0069e225  8b08                 mov      ecx, dword ptr [eax]
0069e227  51                   push     ecx
0069e228  8d55d4               lea      edx, [ebp - 0x2c]
0069e22b  52                   push     edx
0069e22c  e89f2bd9ff           call     0x430dd0
0069e231  83c410               add      esp, 0x10
0069e234  8d85e4feffff         lea      eax, [ebp - 0x11c]
0069e23a  50                   push     eax
0069e23b  8d4dc0               lea      ecx, [ebp - 0x40]
0069e23e  e84da8d9ff           call     0x438a90
0069e243  50                   push     eax
0069e244  8d4dd4               lea      ecx, [ebp - 0x2c]
0069e247  e8846dd7ff           call     0x414fd0
0069e24c  0fb6c8               movzx    ecx, al
0069e24f  85c9                 test     ecx, ecx
0069e251  7408                 je       0x69e25b
0069e253  8d4dd4               lea      ecx, [ebp - 0x2c]
0069e256  e85511d8ff           call     0x41f3b0
0069e25b  8d95e0feffff         lea      edx, [ebp - 0x120]
0069e261  52                   push     edx
0069e262  8d4dc0               lea      ecx, [ebp - 0x40]
0069e265  e826a8d9ff           call     0x438a90
0069e26a  50                   push     eax
0069e26b  8d4dd4               lea      ecx, [ebp - 0x2c]
0069e26e  e85d6dd7ff           call     0x414fd0
0069e273  0fb6c0               movzx    eax, al
0069e276  85c0                 test     eax, eax
0069e278  7415                 je       0x69e28f
0069e27a  8d4dd4               lea      ecx, [ebp - 0x2c]
0069e27d  e81e1cddff           call     0x46fea0
0069e282  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e288  8b10                 mov      edx, dword ptr [eax]
0069e28a  89510c               mov      dword ptr [ecx + 0xc], edx
0069e28d  eb3f                 jmp      0x69e2ce
0069e28f  8d4dc0               lea      ecx, [ebp - 0x40]
0069e292  e829eadcff           call     0x46ccc0
0069e297  0fb6c0               movzx    eax, al
0069e29a  85c0                 test     eax, eax
0069e29c  7523                 jne      0x69e2c1
0069e29e  8d8ddcfeffff         lea      ecx, [ebp - 0x124]
0069e2a4  51                   push     ecx
0069e2a5  8d4dc0               lea      ecx, [ebp - 0x40]
0069e2a8  e893b8d7ff           call     0x419b40
0069e2ad  8bc8                 mov      ecx, eax
0069e2af  e8ec1bddff           call     0x46fea0
0069e2b4  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069e2ba  8b00                 mov      eax, dword ptr [eax]
0069e2bc  89420c               mov      dword ptr [edx + 0xc], eax
0069e2bf  eb0d                 jmp      0x69e2ce
0069e2c1  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e2c7  c7410cffffffff       mov      dword ptr [ecx + 0xc], 0xffffffff
0069e2ce  c645fc05             mov      byte ptr [ebp - 4], 5
0069e2d2  8d4dc0               lea      ecx, [ebp - 0x40]
0069e2d5  e8766ed9ff           call     0x435150
0069e2da  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069e2e1  8d4db4               lea      ecx, [ebp - 0x4c]
0069e2e4  e827ded8ff           call     0x42c110
0069e2e9  8b5508               mov      edx, dword ptr [ebp + 8]
0069e2ec  837a3003             cmp      dword ptr [edx + 0x30], 3
0069e2f0  0f8592020000         jne      0x69e588
0069e2f6  8b4508               mov      eax, dword ptr [ebp + 8]
0069e2f9  83782807             cmp      dword ptr [eax + 0x28], 7
0069e2fd  0f8585020000         jne      0x69e588
0069e303  8b4d08               mov      ecx, dword ptr [ebp + 8]
0069e306  f30f2a413c           cvtsi2ss xmm0, dword ptr [ecx + 0x3c]
0069e30b  f30f5a0d248d7d00     cvtss2sd xmm1, dword ptr [0x7d8d24]
0069e313  f30f5ac0             cvtss2sd xmm0, xmm0
0069e317  f20f5cc8             subsd    xmm1, xmm0
0069e31b  f20f5ac1             cvtsd2ss xmm0, xmm1
0069e31f  51                   push     ecx
0069e320  f30f110424           movss    dword ptr [esp], xmm0
0069e325  8b5508               mov      edx, dword ptr [ebp + 8]
0069e328  f30f2a4238           cvtsi2ss xmm0, dword ptr [edx + 0x38]
0069e32d  51                   push     ecx
0069e32e  f30f110424           movss    dword ptr [esp], xmm0
0069e333  8d4d84               lea      ecx, [ebp - 0x7c]
0069e336  e8d5a9ddff           call     0x478d10
0069e33b  c745fc07000000       mov      dword ptr [ebp - 4], 7
0069e342  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069e348  8b4810               mov      ecx, dword ptr [eax + 0x10]
0069e34b  894d8c               mov      dword ptr [ebp - 0x74], ecx
0069e34e  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069e354  c7420cffffffff       mov      dword ptr [edx + 0xc], 0xffffffff
0069e35b  8b85c4feffff         mov      eax, dword ptr [ebp - 0x13c]
0069e361  c74010ffffffff       mov      dword ptr [eax + 0x10], 0xffffffff
0069e368  f30f100520297600     movss    xmm0, dword ptr [0x762920]
0069e370  f30f1145a0           movss    dword ptr [ebp - 0x60], xmm0
0069e375  8d4d90               lea      ecx, [ebp - 0x70]
0069e378  e84324d7ff           call     0x4107c0
0069e37d  c645fc08             mov      byte ptr [ebp - 4], 8
0069e381  8d4d80               lea      ecx, [ebp - 0x80]
0069e384  51                   push     ecx
0069e385  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e38b  81c108610000         add      ecx, 0x6108
0069e391  e8aab7d7ff           call     0x419b40
0069e396  8d957cffffff         lea      edx, [ebp - 0x84]
0069e39c  52                   push     edx
0069e39d  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e3a3  81c108610000         add      ecx, 0x6108
0069e3a9  e8e2a6d9ff           call     0x438a90
0069e3ae  eb08                 jmp      0x69e3b8
0069e3b0  8d4d80               lea      ecx, [ebp - 0x80]
0069e3b3  e86825d9ff           call     0x430920
0069e3b8  8d857cffffff         lea      eax, [ebp - 0x84]
0069e3be  50                   push     eax
0069e3bf  8d4d80               lea      ecx, [ebp - 0x80]
0069e3c2  e8096cd7ff           call     0x414fd0
0069e3c7  0fb6c8               movzx    ecx, al
0069e3ca  85c9                 test     ecx, ecx
0069e3cc  0f84cd000000         je       0x69e49f
0069e3d2  8d5584               lea      edx, [ebp - 0x7c]
0069e3d5  52                   push     edx
0069e3d6  8d4d80               lea      ecx, [ebp - 0x80]
0069e3d9  e8d2a7d9ff           call     0x438bb0
0069e3de  83c004               add      eax, 4
0069e3e1  8bc8                 mov      ecx, eax
0069e3e3  e8c819d9ff           call     0x42fdb0
0069e3e8  d99d78ffffff         fstp     dword ptr [ebp - 0x88]
0069e3ee  f30f5a8578ffffff     cvtss2sd xmm0, dword ptr [ebp - 0x88]
0069e3f6  f20f100d902d7600     movsd    xmm1, qword ptr [0x762d90]
0069e3fe  660f2fc8             comisd   xmm1, xmm0
0069e402  0f8692000000         jbe      0x69e49a
0069e408  8d4d90               lea      ecx, [ebp - 0x70]
0069e40b  e8b0e8dcff           call     0x46ccc0
0069e410  0fb6c0               movzx    eax, al
0069e413  85c0                 test     eax, eax
0069e415  752a                 jne      0x69e441
0069e417  51                   push     ecx
0069e418  d90584f97400         fld      dword ptr [0x74f984]
0069e41e  d91c24               fstp     dword ptr [esp]
0069e421  51                   push     ecx
0069e422  d98578ffffff         fld      dword ptr [ebp - 0x88]
0069e428  d91c24               fstp     dword ptr [esp]
0069e42b  51                   push     ecx
0069e42c  d945a0               fld      dword ptr [ebp - 0x60]
0069e42f  d91c24               fstp     dword ptr [esp]
0069e432  e8e9f6d6ff           call     0x40db20
0069e437  83c40c               add      esp, 0xc
0069e43a  0fb6c8               movzx    ecx, al
0069e43d  85c9                 test     ecx, ecx
0069e43f  7420                 je       0x69e461
0069e441  f30f108578ffffff     movss    xmm0, dword ptr [ebp - 0x88]
0069e449  f30f1145a0           movss    dword ptr [ebp - 0x60], xmm0
0069e44e  8d4d80               lea      ecx, [ebp - 0x80]
0069e451  e85aa7d9ff           call     0x438bb0
0069e456  50                   push     eax
0069e457  8d4d90               lea      ecx, [ebp - 0x70]
0069e45a  e801b7d7ff           call     0x419b60
0069e45f  eb39                 jmp      0x69e49a
0069e461  f30f5a8578ffffff     cvtss2sd xmm0, dword ptr [ebp - 0x88]
0069e469  f30f5a4da0           cvtss2sd xmm1, dword ptr [ebp - 0x60]
0069e46e  660f2fc8             comisd   xmm1, xmm0
0069e472  7626                 jbe      0x69e49a
0069e474  f30f108578ffffff     movss    xmm0, dword ptr [ebp - 0x88]
0069e47c  f30f1145a0           movss    dword ptr [ebp - 0x60], xmm0
0069e481  8d4d90               lea      ecx, [ebp - 0x70]
0069e484  e8d770ddff           call     0x475560
0069e489  8d4d80               lea      ecx, [ebp - 0x80]
0069e48c  e81fa7d9ff           call     0x438bb0
0069e491  50                   push     eax
0069e492  8d4d90               lea      ecx, [ebp - 0x70]
0069e495  e8c6b6d7ff           call     0x419b60
0069e49a  e911ffffff           jmp      0x69e3b0
0069e49f  8d558c               lea      edx, [ebp - 0x74]
0069e4a2  52                   push     edx
0069e4a3  8d85d8feffff         lea      eax, [ebp - 0x128]
0069e4a9  50                   push     eax
0069e4aa  8d4d90               lea      ecx, [ebp - 0x70]
0069e4ad  e8dea5d9ff           call     0x438a90
0069e4b2  8b08                 mov      ecx, dword ptr [eax]
0069e4b4  51                   push     ecx
0069e4b5  8d95d4feffff         lea      edx, [ebp - 0x12c]
0069e4bb  52                   push     edx
0069e4bc  8d4d90               lea      ecx, [ebp - 0x70]
0069e4bf  e87cb6d7ff           call     0x419b40
0069e4c4  8b00                 mov      eax, dword ptr [eax]
0069e4c6  50                   push     eax
0069e4c7  8d4da4               lea      ecx, [ebp - 0x5c]
0069e4ca  51                   push     ecx
0069e4cb  e80029d9ff           call     0x430dd0
0069e4d0  83c410               add      esp, 0x10
0069e4d3  8d95d0feffff         lea      edx, [ebp - 0x130]
0069e4d9  52                   push     edx
0069e4da  8d4d90               lea      ecx, [ebp - 0x70]
0069e4dd  e8aea5d9ff           call     0x438a90
0069e4e2  50                   push     eax
0069e4e3  8d4da4               lea      ecx, [ebp - 0x5c]
0069e4e6  e8e56ad7ff           call     0x414fd0
0069e4eb  0fb6c0               movzx    eax, al
0069e4ee  85c0                 test     eax, eax
0069e4f0  7408                 je       0x69e4fa
0069e4f2  8d4da4               lea      ecx, [ebp - 0x5c]
0069e4f5  e8b60ed8ff           call     0x41f3b0
0069e4fa  8d8dccfeffff         lea      ecx, [ebp - 0x134]
0069e500  51                   push     ecx
0069e501  8d4d90               lea      ecx, [ebp - 0x70]
0069e504  e887a5d9ff           call     0x438a90
0069e509  50                   push     eax
0069e50a  8d4da4               lea      ecx, [ebp - 0x5c]
0069e50d  e8be6ad7ff           call     0x414fd0
0069e512  0fb6d0               movzx    edx, al
0069e515  85d2                 test     edx, edx
0069e517  7415                 je       0x69e52e
0069e519  8d4da4               lea      ecx, [ebp - 0x5c]
0069e51c  e87f19ddff           call     0x46fea0
0069e521  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e527  8b10                 mov      edx, dword ptr [eax]
0069e529  895110               mov      dword ptr [ecx + 0x10], edx
0069e52c  eb3f                 jmp      0x69e56d
0069e52e  8d4d90               lea      ecx, [ebp - 0x70]
0069e531  e88ae7dcff           call     0x46ccc0
0069e536  0fb6c0               movzx    eax, al
0069e539  85c0                 test     eax, eax
0069e53b  7523                 jne      0x69e560
0069e53d  8d8dc8feffff         lea      ecx, [ebp - 0x138]
0069e543  51                   push     ecx
0069e544  8d4d90               lea      ecx, [ebp - 0x70]
0069e547  e8f4b5d7ff           call     0x419b40
0069e54c  8bc8                 mov      ecx, eax
0069e54e  e84d19ddff           call     0x46fea0
0069e553  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069e559  8b00                 mov      eax, dword ptr [eax]
0069e55b  894210               mov      dword ptr [edx + 0x10], eax
0069e55e  eb0d                 jmp      0x69e56d
0069e560  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e566  c74110ffffffff       mov      dword ptr [ecx + 0x10], 0xffffffff
0069e56d  c645fc07             mov      byte ptr [ebp - 4], 7
0069e571  8d4d90               lea      ecx, [ebp - 0x70]
0069e574  e8d76bd9ff           call     0x435150
0069e579  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069e580  8d4d84               lea      ecx, [ebp - 0x7c]
0069e583  e888dbd8ff           call     0x42c110
0069e588  eb20                 jmp      0x69e5aa
0069e58a  8b95c4feffff         mov      edx, dword ptr [ebp - 0x13c]
0069e590  0fb6828f610000       movzx    eax, byte ptr [edx + 0x618f]
0069e597  f7d8                 neg      eax
0069e599  1bc0                 sbb      eax, eax
0069e59b  83c001               add      eax, 1
0069e59e  8b8dc4feffff         mov      ecx, dword ptr [ebp - 0x13c]
0069e5a4  88818f610000         mov      byte ptr [ecx + 0x618f], al
0069e5aa  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
0069e5ad  64890d00000000       mov      dword ptr fs:[0], ecx
0069e5b4  59                   pop      ecx
0069e5b5  5e                   pop      esi
0069e5b6  8be5                 mov      esp, ebp
0069e5b8  5d                   pop      ebp
0069e5b9  c20400               ret      4
0069e5bc  88d8                 mov      al, bl
0069e5be  6900b9d86900         imul     eax, dword ptr [eax], 0x69d8b9
0069e5c4  d9d8                 fstpnce  st(0), st(0)
0069e5c6  69000ad96900         imul     eax, dword ptr [eax], 0x69d90a
0069e5cc  84d9                 test     cl, bl
0069e5ce  6900c4d96900         imul     eax, dword ptr [eax], 0x69d9c4
0069e5d4  04da                 add      al, 0xda
0069e5d6  690044da6900         imul     eax, dword ptr [eax], 0x69da44
0069e5dc  84da                 test     dl, bl
0069e5de  690070db6900         imul     eax, dword ptr [eax], 0x69db70
0069e5e4  60                   pushal   
0069e5e5  dc6900               fsubr    qword ptr [ecx]
0069e5e8  6d                   insd     dword ptr es:[edi], dx
