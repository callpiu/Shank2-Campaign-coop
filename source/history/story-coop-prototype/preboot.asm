STRING PreBootInitialize failed 0x751770
REF 0x699b2a
FUNCTION 0x699ae0
00699ae0  55                   push     ebp
00699ae1  8bec                 mov      ebp, esp
00699ae3  6aff                 push     -1
00699ae5  68f0ea6c00           push     0x6ceaf0
00699aea  64a100000000         mov      eax, dword ptr fs:[0]
00699af0  50                   push     eax
00699af1  83ec38               sub      esp, 0x38
00699af4  56                   push     esi
00699af5  a108957c00           mov      eax, dword ptr [0x7c9508]
00699afa  33c5                 xor      eax, ebp
00699afc  50                   push     eax
00699afd  8d45f4               lea      eax, [ebp - 0xc]
00699b00  64a300000000         mov      dword ptr fs:[0], eax
00699b06  894dbc               mov      dword ptr [ebp - 0x44], ecx
00699b09  8b4dbc               mov      ecx, dword ptr [ebp - 0x44]
00699b0c  e87ffcffff           call     0x699790
00699b11  c645c301             mov      byte ptr [ebp - 0x3d], 1
00699b15  8b45bc               mov      eax, dword ptr [ebp - 0x44]
00699b18  8b10                 mov      edx, dword ptr [eax]
00699b1a  8b4dbc               mov      ecx, dword ptr [ebp - 0x44]
00699b1d  8b4208               mov      eax, dword ptr [edx + 8]
00699b20  ffd0                 call     eax
00699b22  0fb6c8               movzx    ecx, al
00699b25  85c9                 test     ecx, ecx
00699b27  7520                 jne      0x699b49
00699b29  6870177500           push     0x751770
00699b2e  6a00                 push     0
00699b30  8b152cf47400         mov      edx, dword ptr [0x74f42c]
00699b36  52                   push     edx
00699b37  e87423d7ff           call     0x40beb0
00699b3c  50                   push     eax
00699b3d  e8ae3cdeff           call     0x47d7f0
00699b42  83c410               add      esp, 0x10
00699b45  c645c300             mov      byte ptr [ebp - 0x3d], 0
00699b49  e8b233f1ff           call     0x5acf00
00699b4e  0fb6404a             movzx    eax, byte ptr [eax + 0x4a]
00699b52  85c0                 test     eax, eax
00699b54  7412                 je       0x699b68
00699b56  6a04                 push     4
00699b58  6a00                 push     0
00699b5a  6a00                 push     0
00699b5c  e85fa5faff           call     0x6440c0
00699b61  83c40c               add      esp, 0xc
00699b64  c645c300             mov      byte ptr [ebp - 0x3d], 0
00699b68  e8f318daff           call     0x43b460
00699b6d  e89e79deff           call     0x481510
00699b72  8d4dc4               lea      ecx, [ebp - 0x3c]
00699b75  e8362ef1ff           call     0x5ac9b0
00699b7a  c745fc00000000       mov      dword ptr [ebp - 4], 0
00699b81  8d45e8               lea      eax, [ebp - 0x18]
00699b84  e8c75be0ff           call     0x49f750
00699b89  8b4d08               mov      ecx, dword ptr [ebp + 8]
00699b8c  894de8               mov      dword ptr [ebp - 0x18], ecx
00699b8f  8d4de8               lea      ecx, [ebp - 0x18]
00699b92  e8d9f3deff           call     0x488f70
00699b97  0fb6d0               movzx    edx, al
00699b9a  85d2                 test     edx, edx
00699b9c  751f                 jne      0x699bbd
00699b9e  688c177500           push     0x75178c
00699ba3  6a00                 push     0
00699ba5  a12cf47400           mov      eax, dword ptr [0x74f42c]
00699baa  50                   push     eax
00699bab  e80023d7ff           call     0x40beb0
00699bb0  50                   push     eax
00699bb1  e83a3cdeff           call     0x47d7f0
00699bb6  83c410               add      esp, 0x10
00699bb9  c645c300             mov      byte ptr [ebp - 0x3d], 0
00699bbd  68ac177500           push     0x7517ac
00699bc2  8d75c4               lea      esi, [ebp - 0x3c]
00699bc5  e86671f1ff           call     0x5b0d30
00699bca  83c404               add      esp, 4
00699bcd  e86e19daff           call     0x43b540
00699bd2  0fb6c8               movzx    ecx, al
00699bd5  85c9                 test     ecx, ecx
00699bd7  7413                 je       0x699bec
00699bd9  e86206d8ff           call     0x41a240
00699bde  8bc8                 mov      ecx, eax
00699be0  e87b17daff           call     0x43b360
00699be5  0fb6d0               movzx    edx, al
00699be8  85d2                 test     edx, edx
00699bea  751b                 jne      0x699c07
00699bec  68c4177500           push     0x7517c4
00699bf1  6a00                 push     0
00699bf3  a12cf47400           mov      eax, dword ptr [0x74f42c]
00699bf8  50                   push     eax
00699bf9  e8b222d7ff           call     0x40beb0
00699bfe  50                   push     eax
00699bff  e8ec3bdeff           call     0x47d7f0
00699c04  83c410               add      esp, 0x10
00699c07  68e4177500           push     0x7517e4
00699c0c  8d75c4               lea      esi, [ebp - 0x3c]
00699c0f  e81c71f1ff           call     0x5b0d30
00699c14  83c404               add      esp, 4
00699c17  0fb64dc3             movzx    ecx, byte ptr [ebp - 0x3d]
00699c1b  85c9                 test     ecx, ecx
00699c1d  750e                 jne      0x699c2d
00699c1f  6a04                 push     4
00699c21  6a00                 push     0
00699c23  6a00                 push     0
00699c25  e896a4faff           call     0x6440c0
00699c2a  83c40c               add      esp, 0xc
00699c2d  8a55c3               mov      dl, byte ptr [ebp - 0x3d]
00699c30  8855c2               mov      byte ptr [ebp - 0x3e], dl
00699c33  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
00699c3a  8d4dc4               lea      ecx, [ebp - 0x3c]
00699c3d  e8ce24d9ff           call     0x42c110
00699c42  8a45c2               mov      al, byte ptr [ebp - 0x3e]
00699c45  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
00699c48  64890d00000000       mov      dword ptr fs:[0], ecx
00699c4f  59                   pop      ecx
00699c50  5e                   pop      esi
00699c51  8be5                 mov      esp, ebp
00699c53  5d                   pop      ebp
00699c54  c20400               ret      4
00699c57  cc                   int3     
00699c58  cc                   int3     
00699c59  cc                   int3     
00699c5a  cc                   int3     
00699c5b  cc                   int3     
00699c5c  cc                   int3     
00699c5d  cc                   int3     
00699c5e  cc                   int3     
00699c5f  cc                   int3     
00699c60  55                   push     ebp
00699c61  8bec                 mov      ebp, esp
00699c63  b8b08d7d00           mov      eax, 0x7d8db0
00699c68  5d                   pop      ebp
00699c69  c3                   ret      
00699c6a  cc                   int3     
00699c6b  cc                   int3     
00699c6c  cc                   int3     
00699c6d  cc                   int3     
00699c6e  cc                   int3     
00699c6f  cc                   int3     
00699c70  55                   push     ebp
00699c71  8bec                 mov      ebp, esp
00699c73  51                   push     ecx
00699c74  894dfc               mov      dword ptr [ebp - 4], ecx
00699c77  8be5                 mov      esp, ebp
00699c79  5d                   pop      ebp
00699c7a  c3                   ret      
00699c7b  cc                   int3     
00699c7c  cc                   int3     
00699c7d  cc                   int3     
00699c7e  cc                   int3     
00699c7f  cc                   int3     
00699c80  55                   push     ebp
00699c81  8bec                 mov      ebp, esp
00699c83  6aff                 push     -1
00699c85  68c8936c00           push     0x6c93c8
00699c8a  64a100000000         mov      eax, dword ptr fs:[0]
00699c90  50                   push     eax
00699c91  51                   push     ecx
00699c92  a108957c00           mov      eax, dword ptr [0x7c9508]
00699c97  33c5                 xor      eax, ebp
00699c99  50                   push     eax
00699c9a  8d45f4               lea      eax, [ebp - 0xc]
00699c9d  64a300000000         mov      dword ptr fs:[0], eax
00699ca3  894df0               mov      dword ptr [ebp - 0x10], ecx
00699ca6  68e0b24300           push     0x43b2e0
00699cab  68b0b14300           push     0x43b1b0
00699cb0  6a02                 push     2
00699cb2  6a74                 push     0x74
00699cb4  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00699cb7  50                   push     eax
00699cb8  e83575faff           call     0x6411f2
00699cbd  c745fc00000000       mov      dword ptr [ebp - 4], 0
00699cc4  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
00699ccb  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00699cce  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
00699cd1  64890d00000000       mov      dword ptr fs:[0], ecx
00699cd8  59                   pop      ecx
00699cd9  8be5                 mov      esp, ebp
00699cdb  5d                   pop      ebp
00699cdc  c3                   ret      
00699cdd  cc                   int3     
00699cde  cc                   int3     
00699cdf  cc                   int3     
00699ce0  55                   push     ebp
00699ce1  8bec                 mov      ebp, esp
00699ce3  51                   push     ecx
00699ce4  894dfc               mov      dword ptr [ebp - 4], ecx
00699ce7  8b45fc               mov      eax, dword ptr [ebp - 4]
00699cea  05c4000000           add      eax, 0xc4
00699cef  8be5                 mov      esp, ebp
00699cf1  5d                   pop      ebp
00699cf2  c3                   ret      
00699cf3  cc                   int3     
00699cf4  cc                   int3     
00699cf5  cc                   int3     
00699cf6  cc                   int3     
00699cf7  cc                   int3     
00699cf8  cc                   int3     
00699cf9  cc                   int3     
00699cfa  cc                   int3     
00699cfb  cc                   int3     
00699cfc  cc                   int3     
00699cfd  cc                   int3     
00699cfe  cc                   int3     
00699cff  cc                   int3     
00699d00  55                   push     ebp
00699d01  8bec                 mov      ebp, esp
00699d03  51                   push     ecx
00699d04  894dfc               mov      dword ptr [ebp - 4], ecx
00699d07  8b45fc               mov      eax, dword ptr [ebp - 4]
00699d0a  33c9                 xor      ecx, ecx
00699d0c  83b8bc00000004       cmp      dword ptr [eax + 0xbc], 4
00699d13  0f94c1               sete     cl
00699d16  8ac1                 mov      al, cl
00699d18  8be5                 mov      esp, ebp
00699d1a  5d                   pop      ebp
00699d1b  c3                   ret      
00699d1c  cc                   int3     
00699d1d  cc                   int3     
00699d1e  cc                   int3     
00699d1f  cc                   int3     
00699d20  55                   push     ebp
00699d21  8bec                 mov      ebp, esp
00699d23  83ec10               sub      esp, 0x10
00699d26  894df4               mov      dword ptr [ebp - 0xc], ecx
00699d29  8b45f4               mov      eax, dword ptr [ebp - 0xc]
00699d2c  8b886c040000         mov      ecx, dword ptr [eax + 0x46c]
00699d32  894df8               mov      dword ptr [ebp - 8], ecx
00699d35  8b55f8               mov      edx, dword ptr [ebp - 8]
00699d38  8955fc               mov      dword ptr [ebp - 4], edx
00699d3b  837dfc00             cmp      dword ptr [ebp - 4], 0
00699d3f  7413                 je       0x699d54
00699d41  6a01                 push     1
00699d43  8b45fc               mov      eax, dword ptr [ebp - 4]
00699d46  8b10                 mov      edx, dword ptr [eax]
00699d48  8b4dfc               mov      ecx, dword ptr [ebp - 4]
00699d4b  8b02                 mov      eax, dword ptr [edx]
00699d4d  ffd0                 call     eax
00699d4f  8945f0               mov      dword ptr [ebp - 0x10], eax
00699d52  eb07                 jmp      0x699d5b
00699d54  c745f000000000       mov      dword ptr [ebp - 0x10], 0
00699d5b  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
00699d5e  c7816c04000000000000 mov      dword ptr [ecx + 0x46c], 0
00699d68  8be5                 mov      esp, ebp
00699d6a  5d                   pop      ebp
00699d6b  c3                   ret      
00699d6c  cc                   int3     
00699d6d  cc                   int3     
00699d6e  cc                   int3     
00699d6f  cc                   int3     
00699d70  55                   push     ebp
00699d71  8bec                 mov      ebp, esp
00699d73  83ec10               sub      esp, 0x10
00699d76  894df4               mov      dword ptr [ebp - 0xc], ecx
00699d79  8b45f4               mov      eax, dword ptr [ebp - 0xc]
00699d7c  8b8868040000         mov      ecx, dword ptr [eax + 0x468]
