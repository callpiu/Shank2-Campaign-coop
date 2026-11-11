VTABLE WRITES 0x75023c
FUNCTION 0x6a8680
006a8680  55                   push     ebp
006a8681  8bec                 mov      ebp, esp
006a8683  6aff                 push     -1
006a8685  6854776c00           push     0x6c7754
006a868a  64a100000000         mov      eax, dword ptr fs:[0]
006a8690  50                   push     eax
006a8691  51                   push     ecx
006a8692  a108957c00           mov      eax, dword ptr [0x7c9508]
006a8697  33c5                 xor      eax, ebp
006a8699  50                   push     eax
006a869a  8d45f4               lea      eax, [ebp - 0xc]
006a869d  64a300000000         mov      dword ptr fs:[0], eax
006a86a3  894df0               mov      dword ptr [ebp - 0x10], ecx
006a86a6  8b45f0               mov      eax, dword ptr [ebp - 0x10]
006a86a9  c7003c027500         mov      dword ptr [eax], 0x75023c
006a86af  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a86b2  c74104a4027500       mov      dword ptr [ecx + 4], 0x7502a4
006a86b9  c745fc01000000       mov      dword ptr [ebp - 4], 1
006a86c0  c645fc00             mov      byte ptr [ebp - 4], 0
006a86c4  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a86c7  83c13c               add      ecx, 0x3c
006a86ca  e8a132d6ff           call     0x40b970
006a86cf  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a86d6  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a86d9  e862ebffff           call     0x6a7240
006a86de  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
FUNCTION 0x6a8b40
006a8b40  55                   push     ebp
006a8b41  8bec                 mov      ebp, esp
006a8b43  6aff                 push     -1
006a8b45  6868ba6c00           push     0x6cba68
006a8b4a  64a100000000         mov      eax, dword ptr fs:[0]
006a8b50  50                   push     eax
006a8b51  51                   push     ecx
006a8b52  a108957c00           mov      eax, dword ptr [0x7c9508]
006a8b57  33c5                 xor      eax, ebp
006a8b59  50                   push     eax
006a8b5a  8d45f4               lea      eax, [ebp - 0xc]
006a8b5d  64a300000000         mov      dword ptr fs:[0], eax
006a8b63  894df0               mov      dword ptr [ebp - 0x10], ecx
006a8b66  8b4508               mov      eax, dword ptr [ebp + 8]
006a8b69  50                   push     eax
006a8b6a  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a8b6d  e89ef2ffff           call     0x6a7e10
006a8b72  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a8b79  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a8b7c  c7013c027500         mov      dword ptr [ecx], 0x75023c
006a8b82  8b55f0               mov      edx, dword ptr [ebp - 0x10]
006a8b85  c74204a4027500       mov      dword ptr [edx + 4], 0x7502a4
006a8b8c  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a8b8f  83c13c               add      ecx, 0x3c
006a8b92  e8d925d6ff           call     0x40b170
006a8b97  c645fc01             mov      byte ptr [ebp - 4], 1
006a8b9b  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006a8ba2  8b45f0               mov      eax, dword ptr [ebp - 0x10]
006a8ba5  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006a8ba8  64890d00000000       mov      dword ptr fs:[0], ecx
006a8baf  59                   pop      ecx
006a8bb0  8be5                 mov      esp, ebp
006a8bb2  5d                   pop      ebp
006a8bb3  c20400               ret      4
006a8bb6  cc                   int3     
006a8bb7  cc                   int3     
006a8bb8  cc                   int3     
006a8bb9  cc                   int3     
VTABLE WRITES 0x750ab4
FUNCTION 0x6a59d0
006a59d0  55                   push     ebp
006a59d1  8bec                 mov      ebp, esp
006a59d3  6aff                 push     -1
006a59d5  686ec76c00           push     0x6cc76e
006a59da  64a100000000         mov      eax, dword ptr fs:[0]
006a59e0  50                   push     eax
006a59e1  83ec10               sub      esp, 0x10
006a59e4  a108957c00           mov      eax, dword ptr [0x7c9508]
006a59e9  33c5                 xor      eax, ebp
006a59eb  50                   push     eax
006a59ec  8d45f4               lea      eax, [ebp - 0xc]
006a59ef  64a300000000         mov      dword ptr fs:[0], eax
006a59f5  894de8               mov      dword ptr [ebp - 0x18], ecx
006a59f8  8b45e8               mov      eax, dword ptr [ebp - 0x18]
006a59fb  c700b40a7500         mov      dword ptr [eax], 0x750ab4
006a5a01  8b4de8               mov      ecx, dword ptr [ebp - 0x18]
006a5a04  c74104200b7500       mov      dword ptr [ecx + 4], 0x750b20
006a5a0b  c745fc06000000       mov      dword ptr [ebp - 4], 6
006a5a12  8b55e8               mov      edx, dword ptr [ebp - 0x18]
006a5a15  8b4274               mov      eax, dword ptr [edx + 0x74]
006a5a18  8945ec               mov      dword ptr [ebp - 0x14], eax
006a5a1b  8b4dec               mov      ecx, dword ptr [ebp - 0x14]
006a5a1e  894df0               mov      dword ptr [ebp - 0x10], ecx
006a5a21  837df000             cmp      dword ptr [ebp - 0x10], 0
006a5a25  740f                 je       0x6a5a36
006a5a27  6a01                 push     1
006a5a29  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
006a5a2c  e87f3fd7ff           call     0x4199b0
006a5a31  8945e4               mov      dword ptr [ebp - 0x1c], eax
006a5a34  eb07                 jmp      0x6a5a3d
FUNCTION 0x6a5ac0
006a5ac0  55                   push     ebp
006a5ac1  8bec                 mov      ebp, esp
006a5ac3  6aff                 push     -1
006a5ac5  68efc76c00           push     0x6cc7ef
006a5aca  64a100000000         mov      eax, dword ptr fs:[0]
006a5ad0  50                   push     eax
006a5ad1  83ec34               sub      esp, 0x34
006a5ad4  a108957c00           mov      eax, dword ptr [0x7c9508]
006a5ad9  33c5                 xor      eax, ebp
006a5adb  8945f0               mov      dword ptr [ebp - 0x10], eax
006a5ade  50                   push     eax
006a5adf  8d45f4               lea      eax, [ebp - 0xc]
006a5ae2  64a300000000         mov      dword ptr fs:[0], eax
006a5ae8  894dc4               mov      dword ptr [ebp - 0x3c], ecx
006a5aeb  8b4508               mov      eax, dword ptr [ebp + 8]
006a5aee  50                   push     eax
006a5aef  8b4dc4               mov      ecx, dword ptr [ebp - 0x3c]
006a5af2  e819230000           call     0x6a7e10
006a5af7  c745fc00000000       mov      dword ptr [ebp - 4], 0
006a5afe  8b4dc4               mov      ecx, dword ptr [ebp - 0x3c]
006a5b01  c701b40a7500         mov      dword ptr [ecx], 0x750ab4
006a5b07  8b55c4               mov      edx, dword ptr [ebp - 0x3c]
006a5b0a  c74204200b7500       mov      dword ptr [edx + 4], 0x750b20
006a5b11  8b4dc4               mov      ecx, dword ptr [ebp - 0x3c]
006a5b14  83c13c               add      ecx, 0x3c
006a5b17  e8a4acd6ff           call     0x4107c0
006a5b1c  c645fc01             mov      byte ptr [ebp - 4], 1
006a5b20  8b4dc4               mov      ecx, dword ptr [ebp - 0x3c]
006a5b23  83c14c               add      ecx, 0x4c
006a5b26  e8a540d7ff           call     0x419bd0
006a5b2b  c645fc02             mov      byte ptr [ebp - 4], 2
006a5b2f  8b45c4               mov      eax, dword ptr [ebp - 0x3c]
006a5b32  83c078               add      eax, 0x78
006a5b35  50                   push     eax
006a5b36  e8c518e5ff           call     0x4f7400
006a5b3b  c645fc03             mov      byte ptr [ebp - 4], 3
