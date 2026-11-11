FUNCTION 0x6a9290
006a9290  55                   push     ebp
006a9291  8bec                 mov      ebp, esp
006a9293  6aff                 push     -1
006a9295  68ecd36c00           push     0x6cd3ec
006a929a  64a100000000         mov      eax, dword ptr fs:[0]
006a92a0  50                   push     eax
006a92a1  83ec50               sub      esp, 0x50
006a92a4  53                   push     ebx
006a92a5  56                   push     esi
006a92a6  57                   push     edi
006a92a7  a108957c00           mov      eax, dword ptr [0x7c9508]
006a92ac  33c5                 xor      eax, ebp
006a92ae  50                   push     eax
006a92af  8d45f4               lea      eax, [ebp - 0xc]
006a92b2  64a300000000         mov      dword ptr fs:[0], eax
006a92b8  894dac               mov      dword ptr [ebp - 0x54], ecx
006a92bb  8b45ac               mov      eax, dword ptr [ebp - 0x54]
006a92be  8b4808               mov      ecx, dword ptr [eax + 8]
006a92c1  e8cab6d5ff           call     0x404990
006a92c6  8945dc               mov      dword ptr [ebp - 0x24], eax
006a92c9  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a92cc  81c120010000         add      ecx, 0x120
006a92d2  e8e9a0d5ff           call     0x4033c0
006a92d7  50                   push     eax
006a92d8  8b4dac               mov      ecx, dword ptr [ebp - 0x54]
006a92db  8b4908               mov      ecx, dword ptr [ecx + 8]
006a92de  e83d28d6ff           call     0x40bb20
006a92e3  8bc8                 mov      ecx, eax
006a92e5  e8661ed6ff           call     0x40b150
006a92ea  50                   push     eax
006a92eb  e860bde3ff           call     0x4e5050
006a92f0  8945d8               mov      dword ptr [ebp - 0x28], eax
006a92f3  837dd800             cmp      dword ptr [ebp - 0x28], 0
006a92f7  751a                 jne      0x6a9313
006a92f9  8b55ac               mov      edx, dword ptr [ebp - 0x54]
006a92fc  8b4a08               mov      ecx, dword ptr [edx + 8]
006a92ff  e81c28d6ff           call     0x40bb20
006a9304  8bc8                 mov      ecx, eax
006a9306  e8451ed6ff           call     0x40b150
006a930b  e810bde3ff           call     0x4e5020
006a9310  8945d8               mov      dword ptr [ebp - 0x28], eax
006a9313  8b45d8               mov      eax, dword ptr [ebp - 0x28]
006a9316  e865c9e3ff           call     0x4e5c80
006a931b  8945cc               mov      dword ptr [ebp - 0x34], eax
006a931e  8d4dd0               lea      ecx, [ebp - 0x30]
006a9321  e82a1dd6ff           call     0x40b050
006a9326  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a932d  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a9330  e82bb6d5ff           call     0x404960
006a9335  83c020               add      eax, 0x20
006a9338  51                   push     ecx
006a9339  8bf4                 mov      esi, esp
006a933b  8965c4               mov      dword ptr [ebp - 0x3c], esp
006a933e  8bc8                 mov      ecx, eax
006a9340  e87bfedcff           call     0x4791c0
006a9345  8b45ac               mov      eax, dword ptr [ebp - 0x54]
006a9348  8b4808               mov      ecx, dword ptr [eax + 8]
006a934b  e81031d6ff           call     0x40c460
006a9350  50                   push     eax
006a9351  e8ea16e2ff           call     0x4caa40
006a9356  8945e0               mov      dword ptr [ebp - 0x20], eax
006a9359  6a00                 push     0
006a935b  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a935e  e8fdb5d5ff           call     0x404960
006a9363  8b4860               mov      ecx, dword ptr [eax + 0x60]
006a9366  51                   push     ecx
006a9367  8b55e0               mov      edx, dword ptr [ebp - 0x20]
006a936a  52                   push     edx
006a936b  8b45ac               mov      eax, dword ptr [ebp - 0x54]
006a936e  8b4808               mov      ecx, dword ptr [eax + 8]
006a9371  8b55ac               mov      edx, dword ptr [ebp - 0x54]
006a9374  8b4208               mov      eax, dword ptr [edx + 8]
006a9377  8b11                 mov      edx, dword ptr [ecx]
006a9379  8bc8                 mov      ecx, eax
006a937b  8b4224               mov      eax, dword ptr [edx + 0x24]
006a937e  ffd0                 call     eax
006a9380  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a9383  e8d8b5d5ff           call     0x404960
006a9388  8b7064               mov      esi, dword ptr [eax + 0x64]
006a938b  8b7de0               mov      edi, dword ptr [ebp - 0x20]
006a938e  e8fd8de2ff           call     0x4d2190
006a9393  6a00                 push     0
006a9395  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006a9398  e80328d6ff           call     0x40bba0
006a939d  8b45d8               mov      eax, dword ptr [ebp - 0x28]
006a93a0  e8cbc8e3ff           call     0x4e5c70
006a93a5  8ad8                 mov      bl, al
006a93a7  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006a93aa  e89127d6ff           call     0x40bb40
006a93af  8ad3                 mov      dl, bl
006a93b1  e87ae5e3ff           call     0x4e7930
006a93b6  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a93b9  e8a2b5d5ff           call     0x404960
006a93be  8b703c               mov      esi, dword ptr [eax + 0x3c]
006a93c1  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006a93c4  e857d2d5ff           call     0x406620
006a93c9  89b004010000         mov      dword ptr [eax + 0x104], esi
006a93cf  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006a93d2  51                   push     ecx
006a93d3  e89889e2ff           call     0x4d1d70
006a93d8  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006a93db  e8e043d6ff           call     0x40d7c0
006a93e0  8945c8               mov      dword ptr [ebp - 0x38], eax
006a93e3  837dc800             cmp      dword ptr [ebp - 0x38], 0
006a93e7  0f84a8000000         je       0x6a9495
006a93ed  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a93f0  e86bb5d5ff           call     0x404960
006a93f5  83c040               add      eax, 0x40
006a93f8  51                   push     ecx
006a93f9  8bcc                 mov      ecx, esp
006a93fb  8965c0               mov      dword ptr [ebp - 0x40], esp
006a93fe  50                   push     eax
006a93ff  e83ca0d5ff           call     0x403440
006a9404  8b4dc8               mov      ecx, dword ptr [ebp - 0x38]
006a9407  e85428d6ff           call     0x40bc60
006a940c  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a940f  e84cb5d5ff           call     0x404960
006a9414  83c044               add      eax, 0x44
006a9417  51                   push     ecx
006a9418  8bcc                 mov      ecx, esp
006a941a  8965bc               mov      dword ptr [ebp - 0x44], esp
006a941d  50                   push     eax
006a941e  e81da0d5ff           call     0x403440
006a9423  8b4dc8               mov      ecx, dword ptr [ebp - 0x38]
006a9426  e80528d6ff           call     0x40bc30
006a942b  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a942e  e82db5d5ff           call     0x404960
006a9433  83c048               add      eax, 0x48
006a9436  51                   push     ecx
006a9437  8bcc                 mov      ecx, esp
006a9439  8965b8               mov      dword ptr [ebp - 0x48], esp
006a943c  50                   push     eax
006a943d  e8fe9fd5ff           call     0x403440
006a9442  8b4dc8               mov      ecx, dword ptr [ebp - 0x38]
006a9445  e84628d6ff           call     0x40bc90
006a944a  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a944d  e80eb5d5ff           call     0x404960
006a9452  8b5058               mov      edx, dword ptr [eax + 0x58]
006a9455  52                   push     edx
006a9456  8b4dc8               mov      ecx, dword ptr [ebp - 0x38]
006a9459  e86228d6ff           call     0x40bcc0
006a945e  83ec08               sub      esp, 8
006a9461  8bcc                 mov      ecx, esp
006a9463  8965b4               mov      dword ptr [ebp - 0x4c], esp
006a9466  e8e51bd6ff           call     0x40b050
006a946b  8945a8               mov      dword ptr [ebp - 0x58], eax
006a946e  8b45a8               mov      eax, dword ptr [ebp - 0x58]
006a9471  8945a4               mov      dword ptr [ebp - 0x5c], eax
006a9474  c645fc01             mov      byte ptr [ebp - 4], 1
006a9478  51                   push     ecx
006a9479  d9ee                 fldz     
006a947b  d91c24               fstp     dword ptr [esp]
006a947e  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a9481  e8dab4d5ff           call     0x404960
006a9486  c645fc00             mov      byte ptr [ebp - 4], 0
006a948a  8b485c               mov      ecx, dword ptr [eax + 0x5c]
006a948d  8b75c8               mov      esi, dword ptr [ebp - 0x38]
006a9490  e84bcfe2ff           call     0x4d63e0
006a9495  68009f7d00           push     0x7d9f00
006a949a  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006a949d  81c15c010000         add      ecx, 0x15c
006a94a3  e8a845d6ff           call     0x40da50
006a94a8  0fb6c8               movzx    ecx, al
006a94ab  85c9                 test     ecx, ecx
006a94ad  7414                 je       0x6a94c3
006a94af  8b55dc               mov      edx, dword ptr [ebp - 0x24]
006a94b2  81c25c010000         add      edx, 0x15c
006a94b8  52                   push     edx
006a94b9  8d4dd0               lea      ecx, [ebp - 0x30]
006a94bc  e82f6fd6ff           call     0x4103f0
006a94c1  eb40                 jmp      0x6a9503
006a94c3  8b4dcc               mov      ecx, dword ptr [ebp - 0x34]
006a94c6  e8852cd6ff           call     0x40c150
006a94cb  0fb6c0               movzx    eax, al
006a94ce  85c0                 test     eax, eax
006a94d0  7515                 jne      0x6a94e7
006a94d2  6a00                 push     0
006a94d4  8b4dcc               mov      ecx, dword ptr [ebp - 0x34]
006a94d7  e8d472dbff           call     0x4607b0
006a94dc  50                   push     eax
006a94dd  8d4dd0               lea      ecx, [ebp - 0x30]
006a94e0  e80b6fd6ff           call     0x4103f0
006a94e5  eb1c                 jmp      0x6a9503
006a94e7  68f0017500           push     0x7501f0
006a94ec  6a02                 push     2
006a94ee  8b0d20f47400         mov      ecx, dword ptr [0x74f420]
006a94f4  51                   push     ecx
006a94f5  e8b629d6ff           call     0x40beb0
006a94fa  50                   push     eax
006a94fb  e8f042ddff           call     0x47d7f0
006a9500  83c410               add      esp, 0x10
006a9503  51                   push     ecx
006a9504  8bcc                 mov      ecx, esp
006a9506  8965b0               mov      dword ptr [ebp - 0x50], esp
006a9509  68b4c7f546           push     0x46f5c7b4
006a950e  e85d44d6ff           call     0x40d970
006a9513  8d55d0               lea      edx, [ebp - 0x30]
006a9516  52                   push     edx
006a9517  8b45e0               mov      eax, dword ptr [ebp - 0x20]
006a951a  e8c190e2ff           call     0x4d25e0
006a951f  8b45ac               mov      eax, dword ptr [ebp - 0x54]
006a9522  8b4808               mov      ecx, dword ptr [eax + 8]
006a9525  8d45e4               lea      eax, [ebp - 0x1c]
006a9528  e89331e4ff           call     0x4ec6c0
006a952d  6a01                 push     1
006a952f  8d75e4               lea      esi, [ebp - 0x1c]
006a9532  8b7dd8               mov      edi, dword ptr [ebp - 0x28]
006a9535  e8d6c5e3ff           call     0x4e5b10
006a953a  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a9541  8d4dd0               lea      ecx, [ebp - 0x30]
006a9544  e8c72bd8ff           call     0x42c110
006a9549  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006a954c  64890d00000000       mov      dword ptr fs:[0], ecx
006a9553  59                   pop      ecx
006a9554  5f                   pop      edi
006a9555  5e                   pop      esi
006a9556  5b                   pop      ebx
006a9557  8be5                 mov      esp, ebp
006a9559  5d                   pop      ebp
006a955a  c3                   ret      
006a955b  cc                   int3     
006a955c  cc                   int3     
006a955d  cc                   int3     
006a955e  cc                   int3     
006a955f  cc                   int3     
006a9560  55                   push     ebp
006a9561  8bec                 mov      ebp, esp
006a9563  51                   push     ecx
006a9564  894dfc               mov      dword ptr [ebp - 4], ecx
006a9567  8b45fc               mov      eax, dword ptr [ebp - 4]
006a956a  8b8850010000         mov      ecx, dword ptr [eax + 0x150]
006a9570  83b96401000002       cmp      dword ptr [ecx + 0x164], 2
006a9577  7507                 jne      0x6a9580
006a9579  b802000000           mov      eax, 2
006a957e  eb05                 jmp      0x6a9585
006a9580  b801000000           mov      eax, 1
006a9585  8be5                 mov      esp, ebp
006a9587  5d                   pop      ebp
006a9588  c3                   ret      
006a9589  cc                   int3     
006a958a  cc                   int3     
006a958b  cc                   int3     
006a958c  cc                   int3     
006a958d  cc                   int3     
006a958e  cc                   int3     
006a958f  cc                   int3     
006a9590  55                   push     ebp
006a9591  8bec                 mov      ebp, esp
006a9593  51                   push     ecx
006a9594  894dfc               mov      dword ptr [ebp - 4], ecx
006a9597  8b4dfc               mov      ecx, dword ptr [ebp - 4]
006a959a  81c154010000         add      ecx, 0x154
006a95a0  e8bb2ed6ff           call     0x40c460
006a95a5  8be5                 mov      esp, ebp
006a95a7  5d                   pop      ebp
006a95a8  c3                   ret      
006a95a9  cc                   int3     
006a95aa  cc                   int3     
006a95ab  cc                   int3     
006a95ac  cc                   int3     
006a95ad  cc                   int3     
006a95ae  cc                   int3     
006a95af  cc                   int3     
006a95b0  55                   push     ebp
006a95b1  8bec                 mov      ebp, esp
006a95b3  51                   push     ecx
006a95b4  894dfc               mov      dword ptr [ebp - 4], ecx
006a95b7  8b45fc               mov      eax, dword ptr [ebp - 4]
006a95ba  8b8850010000         mov      ecx, dword ptr [eax + 0x150]
006a95c0  33c0                 xor      eax, eax
006a95c2  83b96801000001       cmp      dword ptr [ecx + 0x168], 1
006a95c9  0f94c0               sete     al
006a95cc  8be5                 mov      esp, ebp
006a95ce  5d                   pop      ebp
006a95cf  c3                   ret      
006a95d0  55                   push     ebp
006a95d1  8bec                 mov      ebp, esp
006a95d3  51                   push     ecx
006a95d4  894dfc               mov      dword ptr [ebp - 4], ecx
006a95d7  8b45fc               mov      eax, dword ptr [ebp - 4]
006a95da  8b8850010000         mov      ecx, dword ptr [eax + 0x150]
006a95e0  33c0                 xor      eax, eax
006a95e2  83b96401000002       cmp      dword ptr [ecx + 0x164], 2
006a95e9  0f94c0               sete     al
006a95ec  8be5                 mov      esp, ebp
006a95ee  5d                   pop      ebp
006a95ef  c3                   ret      
006a95f0  55                   push     ebp
006a95f1  8bec                 mov      ebp, esp
006a95f3  83ec0c               sub      esp, 0xc
006a95f6  894df8               mov      dword ptr [ebp - 8], ecx
006a95f9  8b4df8               mov      ecx, dword ptr [ebp - 8]
006a95fc  e83fcddaff           call     0x456340
006a9601  8945fc               mov      dword ptr [ebp - 4], eax
006a9604  837dfc00             cmp      dword ptr [ebp - 4], 0
006a9608  741d                 je       0x6a9627
006a960a  8b45fc               mov      eax, dword ptr [ebp - 4]
006a960d  8b10                 mov      edx, dword ptr [eax]
006a960f  8b4dfc               mov      ecx, dword ptr [ebp - 4]
006a9612  8b4258               mov      eax, dword ptr [edx + 0x58]
006a9615  ffd0                 call     eax
006a9617  0fb6c8               movzx    ecx, al
006a961a  85c9                 test     ecx, ecx
006a961c  7409                 je       0x6a9627
006a961e  c745f401000000       mov      dword ptr [ebp - 0xc], 1
006a9625  eb07                 jmp      0x6a962e
006a9627  c745f400000000       mov      dword ptr [ebp - 0xc], 0
006a962e  8a45f4               mov      al, byte ptr [ebp - 0xc]
006a9631  8be5                 mov      esp, ebp
006a9633  5d                   pop      ebp
006a9634  c3                   ret      
006a9635  cc                   int3     
006a9636  cc                   int3     
006a9637  cc                   int3     
006a9638  cc                   int3     
006a9639  cc                   int3     
006a963a  cc                   int3     
006a963b  cc                   int3     
006a963c  cc                   int3     
006a963d  cc                   int3     
006a963e  cc                   int3     
006a963f  cc                   int3     
006a9640  55                   push     ebp
006a9641  8bec                 mov      ebp, esp
006a9643  83ec08               sub      esp, 8
006a9646  56                   push     esi
006a9647  57                   push     edi
006a9648  894df8               mov      dword ptr [ebp - 8], ecx
006a964b  8d45fc               lea      eax, [ebp - 4]
006a964e  50                   push     eax
006a964f  8b4df8               mov      ecx, dword ptr [ebp - 8]
006a9652  81c154010000         add      ecx, 0x154
006a9658  e8a328d9ff           call     0x43bf00
006a965d  8b4df8               mov      ecx, dword ptr [ebp - 8]
006a9660  81c154010000         add      ecx, 0x154
006a9666  e8f52dd6ff           call     0x40c460
006a966b  3b4508               cmp      eax, dword ptr [ebp + 8]
006a966e  762d                 jbe      0x6a969d
006a9670  8b4d08               mov      ecx, dword ptr [ebp + 8]
006a9673  51                   push     ecx
006a9674  8d55fc               lea      edx, [ebp - 4]
006a9677  52                   push     edx
006a9678  e803f1d5ff           call     0x408780
006a967d  83c408               add      esp, 8
006a9680  8d4dfc               lea      ecx, [ebp - 4]
006a9683  e8c849d8ff           call     0x42e050
006a9688  8bf0                 mov      esi, eax
006a968a  8b4df8               mov      ecx, dword ptr [ebp - 8]
006a968d  e8ce2dd6ff           call     0x40c460
006a9692  50                   push     eax
006a9693  8b7e04               mov      edi, dword ptr [esi + 4]
006a9696  e82526e2ff           call     0x4cbcc0
006a969b  eb02                 jmp      0x6a969f
006a969d  33c0                 xor      eax, eax
006a969f  5f                   pop      edi
006a96a0  5e                   pop      esi
006a96a1  8be5                 mov      esp, ebp
006a96a3  5d                   pop      ebp
006a96a4  c20400               ret      4
006a96a7  cc                   int3     
006a96a8  cc                   int3     
006a96a9  cc                   int3     
006a96aa  cc                   int3     
006a96ab  cc                   int3     
006a96ac  cc                   int3     
006a96ad  cc                   int3     
006a96ae  cc                   int3     
006a96af  cc                   int3     
006a96b0  55                   push     ebp
006a96b1  8bec                 mov      ebp, esp
006a96b3  83ec0c               sub      esp, 0xc
006a96b6  56                   push     esi
006a96b7  57                   push     edi
006a96b8  894df4               mov      dword ptr [ebp - 0xc], ecx
006a96bb  8d4508               lea      eax, [ebp + 8]
006a96be  50                   push     eax
006a96bf  8d4dfc               lea      ecx, [ebp - 4]
006a96c2  51                   push     ecx
006a96c3  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006a96c6  81c154010000         add      ecx, 0x154
006a96cc  e8cfd2d5ff           call     0x4069a0
006a96d1  8d55f8               lea      edx, [ebp - 8]
006a96d4  52                   push     edx
006a96d5  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006a96d8  81c154010000         add      ecx, 0x154
006a96de  e82dc2d8ff           call     0x435910
006a96e3  50                   push     eax
006a96e4  8d4dfc               lea      ecx, [ebp - 4]
006a96e7  e8547bd8ff           call     0x431240
006a96ec  0fb6c0               movzx    eax, al
006a96ef  85c0                 test     eax, eax
006a96f1  7404                 je       0x6a96f7
006a96f3  33c0                 xor      eax, eax
006a96f5  eb1b                 jmp      0x6a9712
006a96f7  8d4dfc               lea      ecx, [ebp - 4]
006a96fa  e85149d8ff           call     0x42e050
006a96ff  8bf0                 mov      esi, eax
006a9701  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006a9704  e8572dd6ff           call     0x40c460
006a9709  50                   push     eax
006a970a  8b7e04               mov      edi, dword ptr [esi + 4]
006a970d  e8ae25e2ff           call     0x4cbcc0
006a9712  5f                   pop      edi
006a9713  5e                   pop      esi
006a9714  8be5                 mov      esp, ebp
006a9716  5d                   pop      ebp
006a9717  c20400               ret      4
006a971a  cc                   int3     
006a971b  cc                   int3     
006a971c  cc                   int3     
006a971d  cc                   int3     
006a971e  cc                   int3     
006a971f  cc                   int3     
006a9720  55                   push     ebp
006a9721  8bec                 mov      ebp, esp
006a9723  51                   push     ecx
006a9724  56                   push     esi
006a9725  894dfc               mov      dword ptr [ebp - 4], ecx
006a9728  8b450c               mov      eax, dword ptr [ebp + 0xc]
006a972b  50                   push     eax
006a972c  8b4d08               mov      ecx, dword ptr [ebp + 8]
006a972f  e89c8ae2ff           call     0x4d21d0
006a9734  837d0cff             cmp      dword ptr [ebp + 0xc], -1
006a9738  741e                 je       0x6a9758
006a973a  8b4d08               mov      ecx, dword ptr [ebp + 8]
006a973d  e81ecfd5ff           call     0x406660
006a9742  8bf0                 mov      esi, eax
006a9744  8d4d0c               lea      ecx, [ebp + 0xc]
006a9747  51                   push     ecx
006a9748  8b4dfc               mov      ecx, dword ptr [ebp - 4]
006a974b  81c154010000         add      ecx, 0x154
006a9751  e8aad1d5ff           call     0x406900
006a9756  8930                 mov      dword ptr [eax], esi
006a9758  5e                   pop      esi
006a9759  8be5                 mov      esp, ebp
006a975b  5d                   pop      ebp
006a975c  c20c00               ret      0xc
006a975f  cc                   int3     
006a9760  55                   push     ebp
006a9761  8bec                 mov      ebp, esp
006a9763  51                   push     ecx
006a9764  894dfc               mov      dword ptr [ebp - 4], ecx
006a9767  8b4dfc               mov      ecx, dword ptr [ebp - 4]
006a976a  e8a134e0ff           call     0x4acc10
006a976f  8be5                 mov      esp, ebp
006a9771  5d                   pop      ebp
006a9772  c3                   ret      
006a9773  cc                   int3     
006a9774  cc                   int3     
006a9775  cc                   int3     
006a9776  cc                   int3     
006a9777  cc                   int3     
006a9778  cc                   int3     
006a9779  cc                   int3     
006a977a  cc                   int3     
006a977b  cc                   int3     
006a977c  cc                   int3     
006a977d  cc                   int3     
006a977e  cc                   int3     
006a977f  cc                   int3     
006a9780  55                   push     ebp
006a9781  8bec                 mov      ebp, esp
006a9783  83ec08               sub      esp, 8
006a9786  894df8               mov      dword ptr [ebp - 8], ecx
006a9789  6a00                 push     0
006a978b  8b45f8               mov      eax, dword ptr [ebp - 8]
006a978e  8b10                 mov      edx, dword ptr [eax]
006a9790  8b4df8               mov      ecx, dword ptr [ebp - 8]
006a9793  8b422c               mov      eax, dword ptr [edx + 0x2c]
006a9796  ffd0                 call     eax
006a9798  8945fc               mov      dword ptr [ebp - 4], eax
006a979b  837dfc00             cmp      dword ptr [ebp - 4], 0
006a979f  741a                 je       0x6a97bb
006a97a1  8b4dfc               mov      ecx, dword ptr [ebp - 4]
006a97a4  e877ced5ff           call     0x406620
006a97a9  8b4d08               mov      ecx, dword ptr [ebp + 8]
006a97ac  898804010000         mov      dword ptr [eax + 0x104], ecx
006a97b2  8b55fc               mov      edx, dword ptr [ebp - 4]
006a97b5  52                   push     edx
006a97b6  e8b585e2ff           call     0x4d1d70
006a97bb  8be5                 mov      esp, ebp
006a97bd  5d                   pop      ebp
006a97be  c20400               ret      4
006a97c1  cc                   int3     
006a97c2  cc                   int3     
006a97c3  cc                   int3     
006a97c4  cc                   int3     
006a97c5  cc                   int3     
006a97c6  cc                   int3     
006a97c7  cc                   int3     
006a97c8  cc                   int3     
006a97c9  cc                   int3     
006a97ca  cc                   int3     
006a97cb  cc                   int3     
006a97cc  cc                   int3     
006a97cd  cc                   int3     
006a97ce  cc                   int3     
006a97cf  cc                   int3     
006a97d0  55                   push     ebp
006a97d1  8bec                 mov      ebp, esp
006a97d3  6aff                 push     -1
006a97d5  6868c86c00           push     0x6cc868
006a97da  64a100000000         mov      eax, dword ptr fs:[0]
006a97e0  50                   push     eax
006a97e1  83ec10               sub      esp, 0x10
006a97e4  a108957c00           mov      eax, dword ptr [0x7c9508]
006a97e9  33c5                 xor      eax, ebp
006a97eb  50                   push     eax
006a97ec  8d45f4               lea      eax, [ebp - 0xc]
006a97ef  64a300000000         mov      dword ptr fs:[0], eax
006a97f5  894de8               mov      dword ptr [ebp - 0x18], ecx
006a97f8  68c0010000           push     0x1c0
006a97fd  e85e190000           call     0x6ab160
006a9802  83c404               add      esp, 4
006a9805  8945ec               mov      dword ptr [ebp - 0x14], eax
006a9808  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a980f  837dec00             cmp      dword ptr [ebp - 0x14], 0
006a9813  7413                 je       0x6a9828
006a9815  6aff                 push     -1
006a9817  8b45e8               mov      eax, dword ptr [ebp - 0x18]
006a981a  50                   push     eax
006a981b  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a981e  e8ad57ffff           call     0x69efd0
006a9823  8945e4               mov      dword ptr [ebp - 0x1c], eax
006a9826  eb07                 jmp      0x6a982f
006a9828  c745e400000000       mov      dword ptr [ebp - 0x1c], 0
006a982f  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a9832  894df0               mov      dword ptr [ebp - 0x10], ecx
006a9835  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a983c  8b45f0               mov      eax, dword ptr [ebp - 0x10]
006a983f  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006a9842  64890d00000000       mov      dword ptr fs:[0], ecx
006a9849  59                   pop      ecx
006a984a  8be5                 mov      esp, ebp
006a984c  5d                   pop      ebp
006a984d  c3                   ret      
006a984e  cc                   int3     
006a984f  cc                   int3     
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
FUNCTION 0x6a7ee0
006a7ee0  55                   push     ebp
006a7ee1  8bec                 mov      ebp, esp
006a7ee3  6aff                 push     -1
006a7ee5  6818d36c00           push     0x6cd318
006a7eea  64a100000000         mov      eax, dword ptr fs:[0]
006a7ef0  50                   push     eax
006a7ef1  83ec70               sub      esp, 0x70
006a7ef4  56                   push     esi
006a7ef5  57                   push     edi
006a7ef6  a108957c00           mov      eax, dword ptr [0x7c9508]
006a7efb  33c5                 xor      eax, ebp
006a7efd  50                   push     eax
006a7efe  8d45f4               lea      eax, [ebp - 0xc]
006a7f01  64a300000000         mov      dword ptr fs:[0], eax
006a7f07  894d8c               mov      dword ptr [ebp - 0x74], ecx
006a7f0a  8b458c               mov      eax, dword ptr [ebp - 0x74]
006a7f0d  8b4808               mov      ecx, dword ptr [eax + 8]
006a7f10  e87bcad5ff           call     0x404990
006a7f15  8945ec               mov      dword ptr [ebp - 0x14], eax
006a7f18  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a7f1b  e840cad5ff           call     0x404960
006a7f20  85c0                 test     eax, eax
006a7f22  7415                 je       0x6a7f39
006a7f24  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a7f27  e8440ed6ff           call     0x408d70
006a7f2c  85c0                 test     eax, eax
006a7f2e  7409                 je       0x6a7f39
006a7f30  c7458801000000       mov      dword ptr [ebp - 0x78], 1
006a7f37  eb07                 jmp      0x6a7f40
006a7f39  c7458800000000       mov      dword ptr [ebp - 0x78], 0
006a7f40  8a4d88               mov      cl, byte ptr [ebp - 0x78]
006a7f43  884df3               mov      byte ptr [ebp - 0xd], cl
006a7f46  8d4dd4               lea      ecx, [ebp - 0x2c]
006a7f49  e86266d6ff           call     0x40e5b0
006a7f4e  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a7f55  8d55d4               lea      edx, [ebp - 0x2c]
006a7f58  52                   push     edx
006a7f59  0fb645f3             movzx    eax, byte ptr [ebp - 0xd]
006a7f5d  f7d8                 neg      eax
006a7f5f  1bc0                 sbb      eax, eax
006a7f61  f7d8                 neg      eax
006a7f63  83c001               add      eax, 1
006a7f66  50                   push     eax
006a7f67  8b4d8c               mov      ecx, dword ptr [ebp - 0x74]
006a7f6a  8b4908               mov      ecx, dword ptr [ecx + 8]
006a7f6d  e8ae6fd6ff           call     0x40ef20
006a7f72  8bc8                 mov      ecx, eax
006a7f74  e887930100           call     0x6c1300
006a7f79  8d4dd4               lea      ecx, [ebp - 0x2c]
006a7f7c  e8cf41d6ff           call     0x40c150
006a7f81  0fb6d0               movzx    edx, al
006a7f84  85d2                 test     edx, edx
006a7f86  742f                 je       0x6a7fb7
006a7f88  6810037500           push     0x750310
006a7f8d  6a02                 push     2
006a7f8f  a120f47400           mov      eax, dword ptr [0x74f420]
006a7f94  50                   push     eax
006a7f95  e8163fd6ff           call     0x40beb0
006a7f9a  50                   push     eax
006a7f9b  e85058ddff           call     0x47d7f0
006a7fa0  83c410               add      esp, 0x10
006a7fa3  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a7faa  8d4dd4               lea      ecx, [ebp - 0x2c]
006a7fad  e86e66d6ff           call     0x40e620
006a7fb2  e9b7040000           jmp      0x6a846e
006a7fb7  6a01                 push     1
006a7fb9  8d4dd4               lea      ecx, [ebp - 0x2c]
006a7fbc  e8ef87dbff           call     0x4607b0
006a7fc1  f30f5a4004           cvtss2sd xmm0, dword ptr [eax + 4]
006a7fc6  83ec08               sub      esp, 8
006a7fc9  f20f110424           movsd    qword ptr [esp], xmm0
006a7fce  6a01                 push     1
006a7fd0  8d4dd4               lea      ecx, [ebp - 0x2c]
006a7fd3  e8d887dbff           call     0x4607b0
006a7fd8  f30f5a00             cvtss2sd xmm0, dword ptr [eax]
006a7fdc  83ec08               sub      esp, 8
006a7fdf  f20f110424           movsd    qword ptr [esp], xmm0
006a7fe4  6a00                 push     0
006a7fe6  8d4dd4               lea      ecx, [ebp - 0x2c]
006a7fe9  e8c287dbff           call     0x4607b0
006a7fee  f30f5a4004           cvtss2sd xmm0, dword ptr [eax + 4]
006a7ff3  83ec08               sub      esp, 8
006a7ff6  f20f110424           movsd    qword ptr [esp], xmm0
006a7ffb  6a00                 push     0
006a7ffd  8d4dd4               lea      ecx, [ebp - 0x2c]
006a8000  e8ab87dbff           call     0x4607b0
006a8005  f30f5a00             cvtss2sd xmm0, dword ptr [eax]
006a8009  83ec08               sub      esp, 8
006a800c  f20f110424           movsd    qword ptr [esp], xmm0
006a8011  0fb64df3             movzx    ecx, byte ptr [ebp - 0xd]
006a8015  51                   push     ecx
006a8016  683c037500           push     0x75033c
006a801b  6a02                 push     2
006a801d  8b1520f47400         mov      edx, dword ptr [0x74f420]
006a8023  52                   push     edx
006a8024  e8873ed6ff           call     0x40beb0
006a8029  50                   push     eax
006a802a  e8c157ddff           call     0x47d7f0
006a802f  83c434               add      esp, 0x34
006a8032  0fb645f3             movzx    eax, byte ptr [ebp - 0xd]
006a8036  85c0                 test     eax, eax
006a8038  0f84bc000000         je       0x6a80fa
006a803e  6a00                 push     0
006a8040  8d4dd4               lea      ecx, [ebp - 0x2c]
006a8043  e86887dbff           call     0x4607b0
006a8048  8bf0                 mov      esi, eax
006a804a  6a01                 push     1
006a804c  8d4dd4               lea      ecx, [ebp - 0x2c]
006a804f  e85c87dbff           call     0x4607b0
006a8054  f30f5a06             cvtss2sd xmm0, dword ptr [esi]
006a8058  f30f5a08             cvtss2sd xmm1, dword ptr [eax]
006a805c  660f2fc1             comisd   xmm0, xmm1
006a8060  0f8694000000         jbe      0x6a80fa
006a8066  6a01                 push     1
006a8068  8d4dd4               lea      ecx, [ebp - 0x2c]
006a806b  e84087dbff           call     0x4607b0
006a8070  50                   push     eax
006a8071  6a00                 push     0
006a8073  8d4dd4               lea      ecx, [ebp - 0x2c]
006a8076  e83587dbff           call     0x4607b0
006a807b  50                   push     eax
006a807c  e80f6fd6ff           call     0x40ef90
006a8081  83c408               add      esp, 8
006a8084  6a01                 push     1
006a8086  8d4dd4               lea      ecx, [ebp - 0x2c]
006a8089  e82287dbff           call     0x4607b0
006a808e  f30f5a4004           cvtss2sd xmm0, dword ptr [eax + 4]
006a8093  83ec08               sub      esp, 8
006a8096  f20f110424           movsd    qword ptr [esp], xmm0
006a809b  6a01                 push     1
006a809d  8d4dd4               lea      ecx, [ebp - 0x2c]
006a80a0  e80b87dbff           call     0x4607b0
006a80a5  f30f5a00             cvtss2sd xmm0, dword ptr [eax]
006a80a9  83ec08               sub      esp, 8
006a80ac  f20f110424           movsd    qword ptr [esp], xmm0
006a80b1  6a00                 push     0
006a80b3  8d4dd4               lea      ecx, [ebp - 0x2c]
006a80b6  e8f586dbff           call     0x4607b0
006a80bb  f30f5a4004           cvtss2sd xmm0, dword ptr [eax + 4]
006a80c0  83ec08               sub      esp, 8
006a80c3  f20f110424           movsd    qword ptr [esp], xmm0
006a80c8  6a00                 push     0
006a80ca  8d4dd4               lea      ecx, [ebp - 0x2c]
006a80cd  e8de86dbff           call     0x4607b0
006a80d2  f30f5a00             cvtss2sd xmm0, dword ptr [eax]
006a80d6  83ec08               sub      esp, 8
006a80d9  f20f110424           movsd    qword ptr [esp], xmm0
006a80de  687c037500           push     0x75037c
006a80e3  6a02                 push     2
006a80e5  8b0d20f47400         mov      ecx, dword ptr [0x74f420]
006a80eb  51                   push     ecx
006a80ec  e8bf3dd6ff           call     0x40beb0
006a80f1  50                   push     eax
006a80f2  e8f956ddff           call     0x47d7f0
006a80f7  83c430               add      esp, 0x30
006a80fa  c745e400000000       mov      dword ptr [ebp - 0x1c], 0
006a8101  c745e800000000       mov      dword ptr [ebp - 0x18], 0
006a8108  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a810b  e850c8d5ff           call     0x404960
006a8110  85c0                 test     eax, eax
006a8112  0f8477010000         je       0x6a828f
006a8118  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a811b  e840c8d5ff           call     0x404960
006a8120  83c020               add      eax, 0x20
006a8123  51                   push     ecx
006a8124  8bf4                 mov      esi, esp
006a8126  8965c8               mov      dword ptr [ebp - 0x38], esp
006a8129  8bc8                 mov      ecx, eax
006a812b  e89010ddff           call     0x4791c0
006a8130  8b558c               mov      edx, dword ptr [ebp - 0x74]
006a8133  8b4a08               mov      ecx, dword ptr [edx + 8]
006a8136  e82543d6ff           call     0x40c460
006a813b  50                   push     eax
006a813c  e8ff28e2ff           call     0x4caa40
006a8141  8945e4               mov      dword ptr [ebp - 0x1c], eax
006a8144  6a01                 push     1
006a8146  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a8149  e812c8d5ff           call     0x404960
006a814e  8b4060               mov      eax, dword ptr [eax + 0x60]
006a8151  50                   push     eax
006a8152  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a8155  51                   push     ecx
006a8156  8b558c               mov      edx, dword ptr [ebp - 0x74]
006a8159  8b4208               mov      eax, dword ptr [edx + 8]
006a815c  8b4d8c               mov      ecx, dword ptr [ebp - 0x74]
006a815f  8b4908               mov      ecx, dword ptr [ecx + 8]
006a8162  8b10                 mov      edx, dword ptr [eax]
006a8164  8b4224               mov      eax, dword ptr [edx + 0x24]
006a8167  ffd0                 call     eax
006a8169  51                   push     ecx
006a816a  8bcc                 mov      ecx, esp
006a816c  8965c4               mov      dword ptr [ebp - 0x3c], esp
006a816f  68b4c7f546           push     0x46f5c7b4
006a8174  e8f757d6ff           call     0x40d970
006a8179  6a00                 push     0
006a817b  8d4dd4               lea      ecx, [ebp - 0x2c]
006a817e  e82d86dbff           call     0x4607b0
006a8183  50                   push     eax
006a8184  8b45e4               mov      eax, dword ptr [ebp - 0x1c]
006a8187  e854a4e2ff           call     0x4d25e0
006a818c  33f6                 xor      esi, esi
006a818e  8b7de4               mov      edi, dword ptr [ebp - 0x1c]
006a8191  e8fa9fe2ff           call     0x4d2190
006a8196  6a00                 push     0
006a8198  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a819b  e8003ad6ff           call     0x40bba0
006a81a0  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a81a3  51                   push     ecx
006a81a4  8b558c               mov      edx, dword ptr [ebp - 0x74]
006a81a7  8b02                 mov      eax, dword ptr [edx]
006a81a9  8b4d8c               mov      ecx, dword ptr [ebp - 0x74]
006a81ac  8b505c               mov      edx, dword ptr [eax + 0x5c]
006a81af  ffd2                 call     edx
006a81b1  51                   push     ecx
006a81b2  8bcc                 mov      ecx, esp
006a81b4  8965c0               mov      dword ptr [ebp - 0x40], esp
006a81b7  689c311472           push     0x7214319c
006a81bc  e8af57d6ff           call     0x40d970
006a81c1  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a81c4  e8c760d6ff           call     0x40e290
006a81c9  8bc8                 mov      ecx, eax
006a81cb  e8b018e3ff           call     0x4d9a80
006a81d0  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a81d3  e888c7d5ff           call     0x404960
006a81d8  83c03c               add      eax, 0x3c
006a81db  51                   push     ecx
006a81dc  8bcc                 mov      ecx, esp
006a81de  8965bc               mov      dword ptr [ebp - 0x44], esp
006a81e1  50                   push     eax
006a81e2  e859b2d5ff           call     0x403440
006a81e7  8b75e4               mov      esi, dword ptr [ebp - 0x1c]
006a81ea  e84197e2ff           call     0x4d1930
006a81ef  51                   push     ecx
006a81f0  d9e8                 fld1     
006a81f2  d91c24               fstp     dword ptr [esp]
006a81f5  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a81f8  e86339d6ff           call     0x40bb60
006a81fd  8bf0                 mov      esi, eax
006a81ff  e80c82e4ff           call     0x4f0410
006a8204  8b45e4               mov      eax, dword ptr [ebp - 0x1c]
006a8207  50                   push     eax
006a8208  e8639be2ff           call     0x4d1d70
006a820d  8b4de4               mov      ecx, dword ptr [ebp - 0x1c]
006a8210  e8ab55d6ff           call     0x40d7c0
006a8215  8945d0               mov      dword ptr [ebp - 0x30], eax
006a8218  837dd000             cmp      dword ptr [ebp - 0x30], 0
006a821c  7471                 je       0x6a828f
006a821e  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a8221  e83ac7d5ff           call     0x404960
006a8226  83c040               add      eax, 0x40
006a8229  51                   push     ecx
006a822a  8bcc                 mov      ecx, esp
006a822c  8965b8               mov      dword ptr [ebp - 0x48], esp
006a822f  50                   push     eax
006a8230  e80bb2d5ff           call     0x403440
006a8235  8b4dd0               mov      ecx, dword ptr [ebp - 0x30]
006a8238  e8233ad6ff           call     0x40bc60
006a823d  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a8240  e81bc7d5ff           call     0x404960
006a8245  83c044               add      eax, 0x44
006a8248  51                   push     ecx
006a8249  8bcc                 mov      ecx, esp
006a824b  8965b4               mov      dword ptr [ebp - 0x4c], esp
006a824e  50                   push     eax
006a824f  e8ecb1d5ff           call     0x403440
006a8254  8b4dd0               mov      ecx, dword ptr [ebp - 0x30]
006a8257  e8d439d6ff           call     0x40bc30
006a825c  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a825f  e8fcc6d5ff           call     0x404960
006a8264  83c048               add      eax, 0x48
006a8267  51                   push     ecx
006a8268  8bcc                 mov      ecx, esp
006a826a  8965b0               mov      dword ptr [ebp - 0x50], esp
006a826d  50                   push     eax
006a826e  e8cdb1d5ff           call     0x403440
006a8273  8b4dd0               mov      ecx, dword ptr [ebp - 0x30]
006a8276  e8153ad6ff           call     0x40bc90
006a827b  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a827e  e8ddc6d5ff           call     0x404960
006a8283  8b4858               mov      ecx, dword ptr [eax + 0x58]
006a8286  51                   push     ecx
006a8287  8b4dd0               mov      ecx, dword ptr [ebp - 0x30]
006a828a  e8313ad6ff           call     0x40bcc0
006a828f  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a8292  e8d90ad6ff           call     0x408d70
006a8297  85c0                 test     eax, eax
006a8299  0f84a2010000         je       0x6a8441
006a829f  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a82a2  e8c90ad6ff           call     0x408d70
006a82a7  83c020               add      eax, 0x20
006a82aa  51                   push     ecx
006a82ab  8bf4                 mov      esi, esp
006a82ad  8965ac               mov      dword ptr [ebp - 0x54], esp
006a82b0  8bc8                 mov      ecx, eax
006a82b2  e8090fddff           call     0x4791c0
006a82b7  8b558c               mov      edx, dword ptr [ebp - 0x74]
006a82ba  8b4a08               mov      ecx, dword ptr [edx + 8]
006a82bd  e89e41d6ff           call     0x40c460
006a82c2  50                   push     eax
006a82c3  e87827e2ff           call     0x4caa40
006a82c8  8945e8               mov      dword ptr [ebp - 0x18], eax
006a82cb  6a00                 push     0
006a82cd  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a82d0  e89b0ad6ff           call     0x408d70
006a82d5  8b4060               mov      eax, dword ptr [eax + 0x60]
006a82d8  50                   push     eax
006a82d9  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a82dc  51                   push     ecx
006a82dd  8b558c               mov      edx, dword ptr [ebp - 0x74]
006a82e0  8b4208               mov      eax, dword ptr [edx + 8]
006a82e3  8b4d8c               mov      ecx, dword ptr [ebp - 0x74]
006a82e6  8b4908               mov      ecx, dword ptr [ecx + 8]
006a82e9  8b10                 mov      edx, dword ptr [eax]
006a82eb  8b4224               mov      eax, dword ptr [edx + 0x24]
006a82ee  ffd0                 call     eax
006a82f0  8d4dd4               lea      ecx, [ebp - 0x2c]
006a82f3  e8e896d7ff           call     0x4219e0
006a82f8  83f801               cmp      eax, 1
006a82fb  760f                 jbe      0x6a830c
006a82fd  6a01                 push     1
006a82ff  8d4dd4               lea      ecx, [ebp - 0x2c]
006a8302  e8a984dbff           call     0x4607b0
006a8307  894584               mov      dword ptr [ebp - 0x7c], eax
006a830a  eb0d                 jmp      0x6a8319
006a830c  6a00                 push     0
006a830e  8d4dd4               lea      ecx, [ebp - 0x2c]
006a8311  e89a84dbff           call     0x4607b0
006a8316  894584               mov      dword ptr [ebp - 0x7c], eax
006a8319  8b4d84               mov      ecx, dword ptr [ebp - 0x7c]
006a831c  894da4               mov      dword ptr [ebp - 0x5c], ecx
006a831f  51                   push     ecx
006a8320  8bcc                 mov      ecx, esp
006a8322  8965a8               mov      dword ptr [ebp - 0x58], esp
006a8325  68b4c7f546           push     0x46f5c7b4
006a832a  e84156d6ff           call     0x40d970
006a832f  8b55a4               mov      edx, dword ptr [ebp - 0x5c]
006a8332  52                   push     edx
006a8333  8b45e8               mov      eax, dword ptr [ebp - 0x18]
006a8336  e8a5a2e2ff           call     0x4d25e0
006a833b  be01000000           mov      esi, 1
006a8340  8b7de8               mov      edi, dword ptr [ebp - 0x18]
006a8343  e8489ee2ff           call     0x4d2190
006a8348  6a00                 push     0
006a834a  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a834d  e84e38d6ff           call     0x40bba0
006a8352  8b45e8               mov      eax, dword ptr [ebp - 0x18]
006a8355  50                   push     eax
006a8356  8b4d8c               mov      ecx, dword ptr [ebp - 0x74]
006a8359  8b11                 mov      edx, dword ptr [ecx]
006a835b  8b4d8c               mov      ecx, dword ptr [ebp - 0x74]
006a835e  8b425c               mov      eax, dword ptr [edx + 0x5c]
006a8361  ffd0                 call     eax
006a8363  51                   push     ecx
006a8364  8bcc                 mov      ecx, esp
006a8366  8965a0               mov      dword ptr [ebp - 0x60], esp
006a8369  689c311472           push     0x7214319c
006a836e  e8fd55d6ff           call     0x40d970
006a8373  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a8376  e8155fd6ff           call     0x40e290
006a837b  8bc8                 mov      ecx, eax
006a837d  e8fe16e3ff           call     0x4d9a80
006a8382  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a8385  e8e609d6ff           call     0x408d70
006a838a  83c03c               add      eax, 0x3c
006a838d  51                   push     ecx
006a838e  8bcc                 mov      ecx, esp
006a8390  89659c               mov      dword ptr [ebp - 0x64], esp
006a8393  50                   push     eax
006a8394  e8a7b0d5ff           call     0x403440
006a8399  8b75e8               mov      esi, dword ptr [ebp - 0x18]
006a839c  e88f95e2ff           call     0x4d1930
006a83a1  51                   push     ecx
006a83a2  d9e8                 fld1     
006a83a4  d91c24               fstp     dword ptr [esp]
006a83a7  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a83aa  e8b137d6ff           call     0x40bb60
006a83af  8bf0                 mov      esi, eax
006a83b1  e85a80e4ff           call     0x4f0410
006a83b6  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a83b9  51                   push     ecx
006a83ba  e8b199e2ff           call     0x4d1d70
006a83bf  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a83c2  e8f953d6ff           call     0x40d7c0
006a83c7  8945cc               mov      dword ptr [ebp - 0x34], eax
006a83ca  837dcc00             cmp      dword ptr [ebp - 0x34], 0
006a83ce  7471                 je       0x6a8441
006a83d0  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a83d3  e89809d6ff           call     0x408d70
006a83d8  83c040               add      eax, 0x40
006a83db  51                   push     ecx
006a83dc  8bcc                 mov      ecx, esp
006a83de  896598               mov      dword ptr [ebp - 0x68], esp
006a83e1  50                   push     eax
006a83e2  e859b0d5ff           call     0x403440
006a83e7  8b4dcc               mov      ecx, dword ptr [ebp - 0x34]
006a83ea  e87138d6ff           call     0x40bc60
006a83ef  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a83f2  e87909d6ff           call     0x408d70
006a83f7  83c044               add      eax, 0x44
006a83fa  51                   push     ecx
006a83fb  8bcc                 mov      ecx, esp
