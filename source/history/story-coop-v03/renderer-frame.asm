0069e8e0  55                   push     ebp
0069e8e1  8bec                 mov      ebp, esp
0069e8e3  83ec20               sub      esp, 0x20
0069e8e6  894de0               mov      dword ptr [ebp - 0x20], ecx
0069e8e9  83ec08               sub      esp, 8
0069e8ec  8bc4                 mov      eax, esp
0069e8ee  6810d86900           push     0x69d810
0069e8f3  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
0069e8f6  51                   push     ecx
0069e8f7  50                   push     eax
0069e8f8  e87316dcff           call     0x45ff70
0069e8fd  83c40c               add      esp, 0xc
0069e900  e89bb6ffff           call     0x699fa0
0069e905  8bc8                 mov      ecx, eax
0069e907  e8441dd9ff           call     0x430650
0069e90c  8b55e0               mov      edx, dword ptr [ebp - 0x20]
0069e90f  8982f4600000         mov      dword ptr [edx + 0x60f4], eax
0069e915  ff151ce07200         call     dword ptr [0x72e01c]
0069e91b  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
0069e91e  898190610000         mov      dword ptr [ecx + 0x6190], eax
0069e924  83ec08               sub      esp, 8
0069e927  8bcc                 mov      ecx, esp
0069e929  6850235100           push     0x512350
0069e92e  e89d1fd9ff           call     0x4308d0
0069e933  68c2a3b913           push     0x13b9a3c2
0069e938  8b55e0               mov      edx, dword ptr [ebp - 0x20]
0069e93b  52                   push     edx
0069e93c  e87ff6e6ff           call     0x50dfc0
0069e941  83ec08               sub      esp, 8
0069e944  8bcc                 mov      ecx, esp
0069e946  6860145100           push     0x511460
0069e94b  e8801fd9ff           call     0x4308d0
0069e950  680584594e           push     0x4e598405
0069e955  8b45e0               mov      eax, dword ptr [ebp - 0x20]
0069e958  50                   push     eax
0069e959  e862f6e6ff           call     0x50dfc0
0069e95e  83ec08               sub      esp, 8
0069e961  8bcc                 mov      ecx, esp
0069e963  6840245100           push     0x512440
0069e968  e8631fd9ff           call     0x4308d0
0069e96d  6892196600           push     0x661992
0069e972  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
0069e975  51                   push     ecx
0069e976  e845f6e6ff           call     0x50dfc0
0069e97b  83ec08               sub      esp, 8
0069e97e  8bcc                 mov      ecx, esp
0069e980  68b05b5000           push     0x505bb0
0069e985  e8162ad6ff           call     0x4013a0
0069e98a  680584594e           push     0x4e598405
0069e98f  8b55e0               mov      edx, dword ptr [ebp - 0x20]
0069e992  52                   push     edx
0069e993  e848f6e6ff           call     0x50dfe0
0069e998  83ec08               sub      esp, 8
0069e99b  8bcc                 mov      ecx, esp
0069e99d  68b05b5000           push     0x505bb0
0069e9a2  e8f929d6ff           call     0x4013a0
0069e9a7  6892196600           push     0x661992
0069e9ac  8b45e0               mov      eax, dword ptr [ebp - 0x20]
0069e9af  50                   push     eax
0069e9b0  e82bf6e6ff           call     0x50dfe0
0069e9b5  83ec08               sub      esp, 8
0069e9b8  8bcc                 mov      ecx, esp
0069e9ba  6890d06900           push     0x69d090
0069e9bf  8b55e0               mov      edx, dword ptr [ebp - 0x20]
0069e9c2  52                   push     edx
0069e9c3  51                   push     ecx
0069e9c4  e8a715dcff           call     0x45ff70
0069e9c9  83c40c               add      esp, 0xc
0069e9cc  e8cfbf0000           call     0x6aa9a0
0069e9d1  83c408               add      esp, 8
0069e9d4  8be5                 mov      esp, ebp
0069e9d6  5d                   pop      ebp
0069e9d7  c3                   ret      
0069e9d8  cc                   int3     
0069e9d9  cc                   int3     
0069e9da  cc                   int3     
0069e9db  cc                   int3     
0069e9dc  cc                   int3     
0069e9dd  cc                   int3     
0069e9de  cc                   int3     
0069e9df  cc                   int3     
0069e9e0  55                   push     ebp
0069e9e1  8bec                 mov      ebp, esp
0069e9e3  51                   push     ecx
0069e9e4  894dfc               mov      dword ptr [ebp - 4], ecx
0069e9e7  8be5                 mov      esp, ebp
0069e9e9  5d                   pop      ebp
0069e9ea  c3                   ret      
0069e9eb  cc                   int3     
0069e9ec  cc                   int3     
0069e9ed  cc                   int3     
0069e9ee  cc                   int3     
0069e9ef  cc                   int3     
0069e9f0  55                   push     ebp
0069e9f1  8bec                 mov      ebp, esp
0069e9f3  6aff                 push     -1
0069e9f5  6858b96c00           push     0x6cb958
0069e9fa  64a100000000         mov      eax, dword ptr fs:[0]
0069ea00  50                   push     eax
0069ea01  51                   push     ecx
0069ea02  a108957c00           mov      eax, dword ptr [0x7c9508]
0069ea07  33c5                 xor      eax, ebp
0069ea09  50                   push     eax
0069ea0a  8d45f4               lea      eax, [ebp - 0xc]
0069ea0d  64a300000000         mov      dword ptr fs:[0], eax
0069ea13  894df0               mov      dword ptr [ebp - 0x10], ecx
0069ea16  8b45f0               mov      eax, dword ptr [ebp - 0x10]
0069ea19  c700c40f7500         mov      dword ptr [eax], 0x750fc4
0069ea1f  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
0069ea22  c741042c107500       mov      dword ptr [ecx + 4], 0x75102c
0069ea29  c745fc00000000       mov      dword ptr [ebp - 4], 0
0069ea30  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069ea37  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
0069ea3a  e871f2e5ff           call     0x4fdcb0
0069ea3f  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
0069ea42  64890d00000000       mov      dword ptr fs:[0], ecx
0069ea49  59                   pop      ecx
0069ea4a  8be5                 mov      esp, ebp
0069ea4c  5d                   pop      ebp
0069ea4d  c3                   ret      
0069ea4e  cc                   int3     
0069ea4f  cc                   int3     
0069ea50  55                   push     ebp
0069ea51  8bec                 mov      ebp, esp
0069ea53  6aff                 push     -1
0069ea55  6843c46c00           push     0x6cc443
0069ea5a  64a100000000         mov      eax, dword ptr fs:[0]
0069ea60  50                   push     eax
0069ea61  51                   push     ecx
0069ea62  57                   push     edi
0069ea63  a108957c00           mov      eax, dword ptr [0x7c9508]
0069ea68  33c5                 xor      eax, ebp
0069ea6a  50                   push     eax
0069ea6b  8d45f4               lea      eax, [ebp - 0xc]
0069ea6e  64a300000000         mov      dword ptr fs:[0], eax
0069ea74  894df0               mov      dword ptr [ebp - 0x10], ecx
0069ea77  8b45f0               mov      eax, dword ptr [ebp - 0x10]
0069ea7a  50                   push     eax
0069ea7b  8b7d08               mov      edi, dword ptr [ebp + 8]
0069ea7e  e8cdede5ff           call     0x4fd850
0069ea83  c745fc00000000       mov      dword ptr [ebp - 4], 0
0069ea8a  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
0069ea8d  c701c40f7500         mov      dword ptr [ecx], 0x750fc4
0069ea93  8b55f0               mov      edx, dword ptr [ebp - 0x10]
0069ea96  c742042c107500       mov      dword ptr [edx + 4], 0x75102c
0069ea9d  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069eaa4  8b45f0               mov      eax, dword ptr [ebp - 0x10]
0069eaa7  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
0069eaaa  64890d00000000       mov      dword ptr fs:[0], ecx
0069eab1  59                   pop      ecx
0069eab2  5f                   pop      edi
0069eab3  8be5                 mov      esp, ebp
0069eab5  5d                   pop      ebp
0069eab6  c20400               ret      4
0069eab9  cc                   int3     
0069eaba  cc                   int3     
0069eabb  cc                   int3     
0069eabc  cc                   int3     
0069eabd  cc                   int3     
0069eabe  cc                   int3     
0069eabf  cc                   int3     
0069eac0  55                   push     ebp
0069eac1  8bec                 mov      ebp, esp
0069eac3  51                   push     ecx
0069eac4  894dfc               mov      dword ptr [ebp - 4], ecx
0069eac7  8be5                 mov      esp, ebp
0069eac9  5d                   pop      ebp
0069eaca  c20400               ret      4
0069eacd  cc                   int3     
0069eace  cc                   int3     
0069eacf  cc                   int3     
0069ead0  55                   push     ebp
0069ead1  8bec                 mov      ebp, esp
0069ead3  6aff                 push     -1
0069ead5  68da956c00           push     0x6c95da
0069eada  64a100000000         mov      eax, dword ptr fs:[0]
0069eae0  50                   push     eax
0069eae1  81ecd8000000         sub      esp, 0xd8
0069eae7  56                   push     esi
0069eae8  57                   push     edi
0069eae9  a108957c00           mov      eax, dword ptr [0x7c9508]
0069eaee  33c5                 xor      eax, ebp
0069eaf0  50                   push     eax
0069eaf1  8d45f4               lea      eax, [ebp - 0xc]
0069eaf4  64a300000000         mov      dword ptr fs:[0], eax
0069eafa  898d44ffffff         mov      dword ptr [ebp - 0xbc], ecx
0069eb00  8b8544ffffff         mov      eax, dword ptr [ebp - 0xbc]
0069eb06  8b4820               mov      ecx, dword ptr [eax + 0x20]
0069eb09  894de0               mov      dword ptr [ebp - 0x20], ecx
0069eb0c  8d4de4               lea      ecx, [ebp - 0x1c]
0069eb0f  e8cc6bdbff           call     0x4556e0
0069eb14  c745fc00000000       mov      dword ptr [ebp - 4], 0
0069eb1b  8d55e4               lea      edx, [ebp - 0x1c]
0069eb1e  52                   push     edx
0069eb1f  51                   push     ecx
0069eb20  8bcc                 mov      ecx, esp
0069eb22  8965c8               mov      dword ptr [ebp - 0x38], esp
0069eb25  8d4510               lea      eax, [ebp + 0x10]
0069eb28  50                   push     eax
0069eb29  e81249d6ff           call     0x403440
0069eb2e  51                   push     ecx
0069eb2f  8bcc                 mov      ecx, esp
0069eb31  8965c4               mov      dword ptr [ebp - 0x3c], esp
0069eb34  8d550c               lea      edx, [ebp + 0xc]
0069eb37  52                   push     edx
0069eb38  e80349d6ff           call     0x403440
0069eb3d  e88eecd8ff           call     0x42d7d0
0069eb42  8bc8                 mov      ecx, eax
0069eb44  e897210200           call     0x6c0ce0
0069eb49  8d45dc               lea      eax, [ebp - 0x24]
0069eb4c  50                   push     eax
0069eb4d  8d4de4               lea      ecx, [ebp - 0x1c]
0069eb50  e8ebafd7ff           call     0x419b40
0069eb55  eb08                 jmp      0x69eb5f
0069eb57  8d4ddc               lea      ecx, [ebp - 0x24]
0069eb5a  e85108d8ff           call     0x41f3b0
0069eb5f  8d4dc0               lea      ecx, [ebp - 0x40]
0069eb62  51                   push     ecx
0069eb63  8d4de4               lea      ecx, [ebp - 0x1c]
0069eb66  e8259fd9ff           call     0x438a90
0069eb6b  50                   push     eax
0069eb6c  8d4ddc               lea      ecx, [ebp - 0x24]
0069eb6f  e85c64d7ff           call     0x414fd0
0069eb74  0fb6d0               movzx    edx, al
0069eb77  85d2                 test     edx, edx
0069eb79  0f84ee020000         je       0x69ee6d
0069eb7f  8d4ddc               lea      ecx, [ebp - 0x24]
0069eb82  e81913ddff           call     0x46fea0
0069eb87  8b00                 mov      eax, dword ptr [eax]
0069eb89  8945d8               mov      dword ptr [ebp - 0x28], eax
0069eb8c  837dd800             cmp      dword ptr [ebp - 0x28], 0
0069eb90  0f84d2020000         je       0x69ee68
0069eb96  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069eb99  8b5514               mov      edx, dword ptr [ebp + 0x14]
0069eb9c  3b5140               cmp      edx, dword ptr [ecx + 0x40]
0069eb9f  0f8740020000         ja       0x69ede5
0069eba5  c645d700             mov      byte ptr [ebp - 0x29], 0
0069eba9  8b45d8               mov      eax, dword ptr [ebp - 0x28]
0069ebac  8b4870               mov      ecx, dword ptr [eax + 0x70]
0069ebaf  898d40ffffff         mov      dword ptr [ebp - 0xc0], ecx
0069ebb5  83bd40ffffff01       cmp      dword ptr [ebp - 0xc0], 1
0069ebbc  740b                 je       0x69ebc9
0069ebbe  83bd40ffffff02       cmp      dword ptr [ebp - 0xc0], 2
0069ebc5  745e                 je       0x69ec25
0069ebc7  eb06                 jmp      0x69ebcf
0069ebc9  c645d701             mov      byte ptr [ebp - 0x29], 1
0069ebcd  eb67                 jmp      0x69ec36
0069ebcf  8b55d8               mov      edx, dword ptr [ebp - 0x28]
0069ebd2  8b4240               mov      eax, dword ptr [edx + 0x40]
0069ebd5  2b4514               sub      eax, dword ptr [ebp + 0x14]
0069ebd8  83f805               cmp      eax, 5
0069ebdb  7306                 jae      0x69ebe3
0069ebdd  c645d701             mov      byte ptr [ebp - 0x29], 1
0069ebe1  eb40                 jmp      0x69ec23
0069ebe3  837d1401             cmp      dword ptr [ebp + 0x14], 1
0069ebe7  7506                 jne      0x69ebef
0069ebe9  c645d701             mov      byte ptr [ebp - 0x29], 1
0069ebed  eb34                 jmp      0x69ec23
0069ebef  837d1432             cmp      dword ptr [ebp + 0x14], 0x32
0069ebf3  7718                 ja       0x69ec0d
0069ebf5  8b4514               mov      eax, dword ptr [ebp + 0x14]
0069ebf8  33d2                 xor      edx, edx
0069ebfa  b90a000000           mov      ecx, 0xa
0069ebff  f7f1                 div      ecx
0069ec01  f7da                 neg      edx
0069ec03  1bd2                 sbb      edx, edx
0069ec05  83c201               add      edx, 1
0069ec08  8855d7               mov      byte ptr [ebp - 0x29], dl
0069ec0b  eb16                 jmp      0x69ec23
0069ec0d  8b4514               mov      eax, dword ptr [ebp + 0x14]
0069ec10  33d2                 xor      edx, edx
0069ec12  b919000000           mov      ecx, 0x19
0069ec17  f7f1                 div      ecx
0069ec19  f7da                 neg      edx
0069ec1b  1bd2                 sbb      edx, edx
0069ec1d  83c201               add      edx, 1
0069ec20  8855d7               mov      byte ptr [ebp - 0x29], dl
0069ec23  eb11                 jmp      0x69ec36
0069ec25  8b55d8               mov      edx, dword ptr [ebp - 0x28]
0069ec28  8b4514               mov      eax, dword ptr [ebp + 0x14]
0069ec2b  33c9                 xor      ecx, ecx
0069ec2d  3b4240               cmp      eax, dword ptr [edx + 0x40]
0069ec30  0f94c1               sete     cl
0069ec33  884dd7               mov      byte ptr [ebp - 0x29], cl
0069ec36  0fb655d7             movzx    edx, byte ptr [ebp - 0x29]
0069ec3a  85d2                 test     edx, edx
0069ec3c  0f840c010000         je       0x69ed4e
0069ec42  c745cc04007500       mov      dword ptr [ebp - 0x34], 0x750004
0069ec49  c745d004007500       mov      dword ptr [ebp - 0x30], 0x750004
0069ec50  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ec53  83c16c               add      ecx, 0x6c
0069ec56  e875eed6ff           call     0x40dad0
0069ec5b  0fb6c0               movzx    eax, al
0069ec5e  85c0                 test     eax, eax
0069ec60  752e                 jne      0x69ec90
0069ec62  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ec65  8b5514               mov      edx, dword ptr [ebp + 0x14]
0069ec68  3b5140               cmp      edx, dword ptr [ecx + 0x40]
0069ec6b  7223                 jb       0x69ec90
0069ec6d  8b45d8               mov      eax, dword ptr [ebp - 0x28]
0069ec70  83c06c               add      eax, 0x6c
0069ec73  51                   push     ecx
0069ec74  8bcc                 mov      ecx, esp
0069ec76  8965bc               mov      dword ptr [ebp - 0x44], esp
0069ec79  50                   push     eax
0069ec7a  e8c147d6ff           call     0x403440
0069ec7f  e81c1cd7ff           call     0x4108a0
0069ec84  8bf8                 mov      edi, eax
0069ec86  e8a57ce6ff           call     0x506930
0069ec8b  8945cc               mov      dword ptr [ebp - 0x34], eax
0069ec8e  eb1c                 jmp      0x69ecac
0069ec90  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ec93  83c108               add      ecx, 8
0069ec96  e82547d6ff           call     0x4033c0
0069ec9b  8945cc               mov      dword ptr [ebp - 0x34], eax
0069ec9e  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069eca1  83c124               add      ecx, 0x24
0069eca4  e81747d6ff           call     0x4033c0
0069eca9  8945d0               mov      dword ptr [ebp - 0x30], eax
0069ecac  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
0069ecaf  e81ca7d7ff           call     0x4193d0
0069ecb4  89853cffffff         mov      dword ptr [ebp - 0xc4], eax
0069ecba  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ecbd  83c16c               add      ecx, 0x6c
0069ecc0  51                   push     ecx
0069ecc1  8bd4                 mov      edx, esp
0069ecc3  89a568ffffff         mov      dword ptr [ebp - 0x98], esp
0069ecc9  51                   push     ecx
0069ecca  8bca                 mov      ecx, edx
0069eccc  e86f47d6ff           call     0x403440
0069ecd1  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ecd4  83c148               add      ecx, 0x48
0069ecd7  51                   push     ecx
0069ecd8  8bf4                 mov      esi, esp
0069ecda  89a564ffffff         mov      dword ptr [ebp - 0x9c], esp
0069ece0  e8dba4ddff           call     0x4791c0
0069ece5  8b45d8               mov      eax, dword ptr [ebp - 0x28]
0069ece8  8b4840               mov      ecx, dword ptr [eax + 0x40]
0069eceb  51                   push     ecx
0069ecec  8b5514               mov      edx, dword ptr [ebp + 0x14]
0069ecef  52                   push     edx
0069ecf0  8b45d0               mov      eax, dword ptr [ebp - 0x30]
0069ecf3  50                   push     eax
0069ecf4  8b4dcc               mov      ecx, dword ptr [ebp - 0x34]
0069ecf7  51                   push     ecx
0069ecf8  8b8d44ffffff         mov      ecx, dword ptr [ebp - 0xbc]
0069ecfe  e85d79d6ff           call     0x406660
0069ed03  50                   push     eax
0069ed04  8d8d6cffffff         lea      ecx, [ebp - 0x94]
0069ed0a  e851e1d8ff           call     0x42ce60
0069ed0f  898538ffffff         mov      dword ptr [ebp - 0xc8], eax
0069ed15  8b9538ffffff         mov      edx, dword ptr [ebp - 0xc8]
0069ed1b  899534ffffff         mov      dword ptr [ebp - 0xcc], edx
0069ed21  c645fc01             mov      byte ptr [ebp - 4], 1
0069ed25  8b8534ffffff         mov      eax, dword ptr [ebp - 0xcc]
0069ed2b  50                   push     eax
0069ed2c  8b8d3cffffff         mov      ecx, dword ptr [ebp - 0xc4]
0069ed32  8b11                 mov      edx, dword ptr [ecx]
0069ed34  8b8d3cffffff         mov      ecx, dword ptr [ebp - 0xc4]
0069ed3a  8b4234               mov      eax, dword ptr [edx + 0x34]
0069ed3d  ffd0                 call     eax
0069ed3f  c645fc00             mov      byte ptr [ebp - 4], 0
0069ed43  8d8d6cffffff         lea      ecx, [ebp - 0x94]
0069ed49  e8d2e1d8ff           call     0x42cf20
0069ed4e  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ed51  8b5514               mov      edx, dword ptr [ebp + 0x14]
0069ed54  3b5140               cmp      edx, dword ptr [ecx + 0x40]
0069ed57  0f8288000000         jb       0x69ede5
0069ed5d  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ed60  83c16c               add      ecx, 0x6c
0069ed63  e868edd6ff           call     0x40dad0
0069ed68  0fb6c0               movzx    eax, al
0069ed6b  85c0                 test     eax, eax
0069ed6d  7576                 jne      0x69ede5
0069ed6f  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
0069ed72  e859a6d7ff           call     0x4193d0
0069ed77  898530ffffff         mov      dword ptr [ebp - 0xd0], eax
0069ed7d  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ed80  83c16c               add      ecx, 0x6c
0069ed83  51                   push     ecx
0069ed84  8bd4                 mov      edx, esp
0069ed86  89a554ffffff         mov      dword ptr [ebp - 0xac], esp
0069ed8c  51                   push     ecx
0069ed8d  8bca                 mov      ecx, edx
0069ed8f  e8ac46d6ff           call     0x403440
0069ed94  8b4508               mov      eax, dword ptr [ebp + 8]
0069ed97  8b4864               mov      ecx, dword ptr [eax + 0x64]
0069ed9a  51                   push     ecx
0069ed9b  8d8d58ffffff         lea      ecx, [ebp - 0xa8]
0069eda1  e8faded8ff           call     0x42cca0
0069eda6  89852cffffff         mov      dword ptr [ebp - 0xd4], eax
0069edac  8b952cffffff         mov      edx, dword ptr [ebp - 0xd4]
0069edb2  899528ffffff         mov      dword ptr [ebp - 0xd8], edx
0069edb8  c645fc02             mov      byte ptr [ebp - 4], 2
0069edbc  8b8528ffffff         mov      eax, dword ptr [ebp - 0xd8]
0069edc2  50                   push     eax
0069edc3  8b8d30ffffff         mov      ecx, dword ptr [ebp - 0xd0]
0069edc9  8b11                 mov      edx, dword ptr [ecx]
0069edcb  8b8d30ffffff         mov      ecx, dword ptr [ebp - 0xd0]
0069edd1  8b4234               mov      eax, dword ptr [edx + 0x34]
0069edd4  ffd0                 call     eax
0069edd6  c645fc00             mov      byte ptr [ebp - 4], 0
0069edda  8d8d58ffffff         lea      ecx, [ebp - 0xa8]
0069ede0  e88bdfd8ff           call     0x42cd70
0069ede5  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ede8  8b5514               mov      edx, dword ptr [ebp + 0x14]
0069edeb  3b5140               cmp      edx, dword ptr [ecx + 0x40]
0069edee  7278                 jb       0x69ee68
0069edf0  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069edf3  83c168               add      ecx, 0x68
0069edf6  e8d5ecd6ff           call     0x40dad0
0069edfb  0fb6c0               movzx    eax, al
0069edfe  85c0                 test     eax, eax
0069ee00  7566                 jne      0x69ee68
0069ee02  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
0069ee05  e8c6a5d7ff           call     0x4193d0
0069ee0a  898524ffffff         mov      dword ptr [ebp - 0xdc], eax
0069ee10  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
0069ee13  83c168               add      ecx, 0x68
0069ee16  51                   push     ecx
0069ee17  8b5508               mov      edx, dword ptr [ebp + 8]
0069ee1a  8b4264               mov      eax, dword ptr [edx + 0x64]
0069ee1d  50                   push     eax
0069ee1e  8d8d48ffffff         lea      ecx, [ebp - 0xb8]
0069ee24  e897dfd8ff           call     0x42cdc0
0069ee29  898520ffffff         mov      dword ptr [ebp - 0xe0], eax
0069ee2f  8b8d20ffffff         mov      ecx, dword ptr [ebp - 0xe0]
0069ee35  898d1cffffff         mov      dword ptr [ebp - 0xe4], ecx
0069ee3b  c645fc03             mov      byte ptr [ebp - 4], 3
0069ee3f  8b951cffffff         mov      edx, dword ptr [ebp - 0xe4]
0069ee45  52                   push     edx
0069ee46  8b8524ffffff         mov      eax, dword ptr [ebp - 0xdc]
0069ee4c  8b10                 mov      edx, dword ptr [eax]
0069ee4e  8b8d24ffffff         mov      ecx, dword ptr [ebp - 0xdc]
0069ee54  8b4234               mov      eax, dword ptr [edx + 0x34]
0069ee57  ffd0                 call     eax
0069ee59  c645fc00             mov      byte ptr [ebp - 4], 0
0069ee5d  8d8d48ffffff         lea      ecx, [ebp - 0xb8]
0069ee63  e808dfd8ff           call     0x42cd70
0069ee68  e9eafcffff           jmp      0x69eb57
0069ee6d  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069ee74  8d4de4               lea      ecx, [ebp - 0x1c]
0069ee77  e8d462d9ff           call     0x435150
0069ee7c  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
0069ee7f  64890d00000000       mov      dword ptr fs:[0], ecx
0069ee86  59                   pop      ecx
0069ee87  5f                   pop      edi
0069ee88  5e                   pop      esi
0069ee89  8be5                 mov      esp, ebp
0069ee8b  5d                   pop      ebp
0069ee8c  c21000               ret      0x10
0069ee8f  cc                   int3     
0069ee90  55                   push     ebp
0069ee91  8bec                 mov      ebp, esp
0069ee93  6aff                 push     -1
0069ee95  687bb96c00           push     0x6cb97b
0069ee9a  64a100000000         mov      eax, dword ptr fs:[0]
0069eea0  50                   push     eax
0069eea1  51                   push     ecx
0069eea2  a108957c00           mov      eax, dword ptr [0x7c9508]
0069eea7  33c5                 xor      eax, ebp
0069eea9  50                   push     eax
0069eeaa  8d45f4               lea      eax, [ebp - 0xc]
0069eead  64a300000000         mov      dword ptr fs:[0], eax
0069eeb3  894df0               mov      dword ptr [ebp - 0x10], ecx
0069eeb6  8b45f0               mov      eax, dword ptr [ebp - 0x10]
0069eeb9  c7004c0e7500         mov      dword ptr [eax], 0x750e4c
0069eebf  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
0069eec2  c741047c0e7500       mov      dword ptr [ecx + 4], 0x750e7c
0069eec9  8b55f0               mov      edx, dword ptr [ebp - 0x10]
0069eecc  c7421c940e7500       mov      dword ptr [edx + 0x1c], 0x750e94
0069eed3  c745fc00000000       mov      dword ptr [ebp - 4], 0
0069eeda  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
0069eee1  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
0069eee4  e88716e3ff           call     0x4d0570
0069eee9  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
0069eeec  64890d00000000       mov      dword ptr fs:[0], ecx
0069eef3  59                   pop      ecx
0069eef4  8be5                 mov      esp, ebp
0069eef6  5d                   pop      ebp
0069eef7  c3                   ret      
0069eef8  cc                   int3     
0069eef9  cc                   int3     
0069eefa  cc                   int3     
0069eefb  cc                   int3     
0069eefc  cc                   int3     
0069eefd  cc                   int3     
0069eefe  cc                   int3     
0069eeff  cc                   int3     
0069ef00  55                   push     ebp
0069ef01  8bec                 mov      ebp, esp
0069ef03  6aff                 push     -1
0069ef05  6871c46c00           push     0x6cc471
0069ef0a  64a100000000         mov      eax, dword ptr fs:[0]
0069ef10  50                   push     eax
0069ef11  81ec94000000         sub      esp, 0x94
0069ef17  a108957c00           mov      eax, dword ptr [0x7c9508]
0069ef1c  33c5                 xor      eax, ebp
