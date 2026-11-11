CALLS 0x6a8b40
FUNC 0x6a9850
006a9850  55                   push     ebp
006a9851  8bec                 mov      ebp, esp
006a9853  6aff                 push     -1
006a9855  683fca6c00           push     0x6cca3f
006a985a  64a100000000         mov      eax, dword ptr fs:[0]
006a9860  50                   push     eax
006a9861  81ecd8010000         sub      esp, 0x1d8
006a9867  a108957c00           mov      eax, dword ptr [0x7c9508]
006a986c  33c5                 xor      eax, ebp
006a986e  50                   push     eax
006a986f  8d45f4               lea      eax, [ebp - 0xc]
006a9872  64a300000000         mov      dword ptr fs:[0], eax
006a9878  898da4feffff         mov      dword ptr [ebp - 0x15c], ecx
006a987e  8b85a4feffff         mov      eax, dword ptr [ebp - 0x15c]
006a9884  50                   push     eax
006a9885  e83624e0ff           call     0x4abcc0
006a988a  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a9890  e84bcdd5ff           call     0x4065e0
006a9895  8945ec               mov      dword ptr [ebp - 0x14], eax
006a9898  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a989e  8b11                 mov      edx, dword ptr [ecx]
006a98a0  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a98a6  8b4238               mov      eax, dword ptr [edx + 0x38]
006a98a9  ffd0                 call     eax
006a98ab  8845eb               mov      byte ptr [ebp - 0x15], al
006a98ae  c745b800000000       mov      dword ptr [ebp - 0x48], 0
006a98b5  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a98bb  8b9150010000         mov      edx, dword ptr [ecx + 0x150]
006a98c1  8b8264010000         mov      eax, dword ptr [edx + 0x164]
006a98c7  8985a0feffff         mov      dword ptr [ebp - 0x160], eax
006a98cd  83bda0feffff00       cmp      dword ptr [ebp - 0x160], 0
006a98d4  7474                 je       0x6a994a
006a98d6  83bda0feffff01       cmp      dword ptr [ebp - 0x160], 1
006a98dd  7412                 je       0x6a98f1
006a98df  83bda0feffff02       cmp      dword ptr [ebp - 0x160], 2
006a98e6  0f84b1000000         je       0x6a999d
006a98ec  e900010000           jmp      0x6a99f1
006a98f1  68d0000000           push     0xd0
006a98f6  e865180000           call     0x6ab160
006a98fb  83c404               add      esp, 4
006a98fe  8945a8               mov      dword ptr [ebp - 0x58], eax
006a9901  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a9908  837da800             cmp      dword ptr [ebp - 0x58], 0
006a990c  7417                 je       0x6a9925
006a990e  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a9914  51                   push     ecx
006a9915  8b4da8               mov      ecx, dword ptr [ebp - 0x58]
006a9918  e823f2ffff           call     0x6a8b40
006a991d  89859cfeffff         mov      dword ptr [ebp - 0x164], eax
006a9923  eb0a                 jmp      0x6a992f
006a9925  c7859cfeffff00000000 mov      dword ptr [ebp - 0x164], 0
006a992f  8b959cfeffff         mov      edx, dword ptr [ebp - 0x164]
006a9935  8955ac               mov      dword ptr [ebp - 0x54], edx
006a9938  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a993f  8b45ac               mov      eax, dword ptr [ebp - 0x54]
006a9942  8945b8               mov      dword ptr [ebp - 0x48], eax
006a9945  e9a7000000           jmp      0x6a99f1
006a994a  6a3c                 push     0x3c
006a994c  e80f180000           call     0x6ab160
006a9951  83c404               add      esp, 4
006a9954  8945a0               mov      dword ptr [ebp - 0x60], eax
006a9957  c745fc01000000       mov      dword ptr [ebp - 4], 1
006a995e  837da000             cmp      dword ptr [ebp - 0x60], 0
006a9962  7417                 je       0x6a997b
006a9964  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a996a  51                   push     ecx
006a996b  8b4da0               mov      ecx, dword ptr [ebp - 0x60]
CALLS 0x6a5ac0
FUNC 0x6a9850
006a9850  55                   push     ebp
006a9851  8bec                 mov      ebp, esp
006a9853  6aff                 push     -1
006a9855  683fca6c00           push     0x6cca3f
006a985a  64a100000000         mov      eax, dword ptr fs:[0]
006a9860  50                   push     eax
006a9861  81ecd8010000         sub      esp, 0x1d8
006a9867  a108957c00           mov      eax, dword ptr [0x7c9508]
006a986c  33c5                 xor      eax, ebp
006a986e  50                   push     eax
006a986f  8d45f4               lea      eax, [ebp - 0xc]
006a9872  64a300000000         mov      dword ptr fs:[0], eax
006a9878  898da4feffff         mov      dword ptr [ebp - 0x15c], ecx
006a987e  8b85a4feffff         mov      eax, dword ptr [ebp - 0x15c]
006a9884  50                   push     eax
006a9885  e83624e0ff           call     0x4abcc0
006a988a  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a9890  e84bcdd5ff           call     0x4065e0
006a9895  8945ec               mov      dword ptr [ebp - 0x14], eax
006a9898  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a989e  8b11                 mov      edx, dword ptr [ecx]
006a98a0  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a98a6  8b4238               mov      eax, dword ptr [edx + 0x38]
006a98a9  ffd0                 call     eax
006a98ab  8845eb               mov      byte ptr [ebp - 0x15], al
006a98ae  c745b800000000       mov      dword ptr [ebp - 0x48], 0
006a98b5  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a98bb  8b9150010000         mov      edx, dword ptr [ecx + 0x150]
006a98c1  8b8264010000         mov      eax, dword ptr [edx + 0x164]
006a98c7  8985a0feffff         mov      dword ptr [ebp - 0x160], eax
006a98cd  83bda0feffff00       cmp      dword ptr [ebp - 0x160], 0
006a98d4  7474                 je       0x6a994a
006a98d6  83bda0feffff01       cmp      dword ptr [ebp - 0x160], 1
006a98dd  7412                 je       0x6a98f1
006a98df  83bda0feffff02       cmp      dword ptr [ebp - 0x160], 2
006a98e6  0f84b1000000         je       0x6a999d
006a98ec  e900010000           jmp      0x6a99f1
006a98f1  68d0000000           push     0xd0
006a98f6  e865180000           call     0x6ab160
006a98fb  83c404               add      esp, 4
006a98fe  8945a8               mov      dword ptr [ebp - 0x58], eax
006a9901  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a9908  837da800             cmp      dword ptr [ebp - 0x58], 0
006a990c  7417                 je       0x6a9925
006a990e  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a9914  51                   push     ecx
006a9915  8b4da8               mov      ecx, dword ptr [ebp - 0x58]
006a9918  e823f2ffff           call     0x6a8b40
006a991d  89859cfeffff         mov      dword ptr [ebp - 0x164], eax
006a9923  eb0a                 jmp      0x6a992f
006a9925  c7859cfeffff00000000 mov      dword ptr [ebp - 0x164], 0
006a992f  8b959cfeffff         mov      edx, dword ptr [ebp - 0x164]
006a9935  8955ac               mov      dword ptr [ebp - 0x54], edx
006a9938  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a993f  8b45ac               mov      eax, dword ptr [ebp - 0x54]
006a9942  8945b8               mov      dword ptr [ebp - 0x48], eax
006a9945  e9a7000000           jmp      0x6a99f1
006a994a  6a3c                 push     0x3c
006a994c  e80f180000           call     0x6ab160
006a9951  83c404               add      esp, 4
006a9954  8945a0               mov      dword ptr [ebp - 0x60], eax
006a9957  c745fc01000000       mov      dword ptr [ebp - 4], 1
006a995e  837da000             cmp      dword ptr [ebp - 0x60], 0
006a9962  7417                 je       0x6a997b
006a9964  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a996a  51                   push     ecx
006a996b  8b4da0               mov      ecx, dword ptr [ebp - 0x60]
006a996e  e8fdd6ffff           call     0x6a7070
006a9973  898598feffff         mov      dword ptr [ebp - 0x168], eax
006a9979  eb0a                 jmp      0x6a9985
006a997b  c78598feffff00000000 mov      dword ptr [ebp - 0x168], 0
006a9985  8b9598feffff         mov      edx, dword ptr [ebp - 0x168]
006a998b  8955a4               mov      dword ptr [ebp - 0x5c], edx
006a998e  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a9995  8b45a4               mov      eax, dword ptr [ebp - 0x5c]
006a9998  8945b8               mov      dword ptr [ebp - 0x48], eax
006a999b  eb54                 jmp      0x6a99f1
006a999d  68ec000000           push     0xec
006a99a2  e8b9170000           call     0x6ab160
006a99a7  83c404               add      esp, 4
006a99aa  894598               mov      dword ptr [ebp - 0x68], eax
006a99ad  c745fc02000000       mov      dword ptr [ebp - 4], 2
006a99b4  837d9800             cmp      dword ptr [ebp - 0x68], 0
006a99b8  7417                 je       0x6a99d1
006a99ba  8b8da4feffff         mov      ecx, dword ptr [ebp - 0x15c]
006a99c0  51                   push     ecx
006a99c1  8b4d98               mov      ecx, dword ptr [ebp - 0x68]
006a99c4  e8f7c0ffff           call     0x6a5ac0
006a99c9  898594feffff         mov      dword ptr [ebp - 0x16c], eax
006a99cf  eb0a                 jmp      0x6a99db
006a99d1  c78594feffff00000000 mov      dword ptr [ebp - 0x16c], 0
006a99db  8b9594feffff         mov      edx, dword ptr [ebp - 0x16c]
006a99e1  89559c               mov      dword ptr [ebp - 0x64], edx
006a99e4  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a99eb  8b459c               mov      eax, dword ptr [ebp - 0x64]
006a99ee  8945b8               mov      dword ptr [ebp - 0x48], eax
006a99f1  6a08                 push     8
006a99f3  e868170000           call     0x6ab160
006a99f8  83c404               add      esp, 4
006a99fb  894590               mov      dword ptr [ebp - 0x70], eax
006a99fe  c745fc03000000       mov      dword ptr [ebp - 4], 3
006a9a05  837d9000             cmp      dword ptr [ebp - 0x70], 0
006a9a09  7418                 je       0x6a9a23
006a9a0b  8b4db8               mov      ecx, dword ptr [ebp - 0x48]
006a9a0e  51                   push     ecx
006a9a0f  8b55ec               mov      edx, dword ptr [ebp - 0x14]
006a9a12  52                   push     edx
006a9a13  8b4d90               mov      ecx, dword ptr [ebp - 0x70]
006a9a16  e8c5cad5ff           call     0x4064e0
