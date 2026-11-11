STRING type 0x734854
STRING GameModeParams 0x750620
REF 0x417de8
FUNCTION 0x417de0
00417de0  55                   push     ebp
00417de1  8bec                 mov      ebp, esp
00417de3  51                   push     ecx
00417de4  894dfc               mov      dword ptr [ebp - 4], ecx
00417de7  b820067500           mov      eax, 0x750620
00417dec  8be5                 mov      esp, ebp
00417dee  5d                   pop      ebp
00417def  c3                   ret      
00417df0  55                   push     ebp
00417df1  8bec                 mov      ebp, esp
00417df3  51                   push     ecx
00417df4  894dfc               mov      dword ptr [ebp - 4], ecx
00417df7  8b4dfc               mov      ecx, dword ptr [ebp - 4]
00417dfa  e821b02a00           call     0x6c2e20
00417dff  8b4508               mov      eax, dword ptr [ebp + 8]
00417e02  83e001               and      eax, 1
00417e05  740c                 je       0x417e13
00417e07  8b4dfc               mov      ecx, dword ptr [ebp - 4]
00417e0a  51                   push     ecx
00417e0b  e8702a2900           call     0x6aa880
00417e10  83c404               add      esp, 4
00417e13  8b45fc               mov      eax, dword ptr [ebp - 4]
00417e16  8be5                 mov      esp, ebp
00417e18  5d                   pop      ebp
00417e19  c20400               ret      4
00417e1c  cc                   int3     
00417e1d  cc                   int3     
00417e1e  cc                   int3     
00417e1f  cc                   int3     
00417e20  55                   push     ebp
00417e21  8bec                 mov      ebp, esp
00417e23  51                   push     ecx
00417e24  894dfc               mov      dword ptr [ebp - 4], ecx
00417e27  8b45fc               mov      eax, dword ptr [ebp - 4]
00417e2a  c70014077500         mov      dword ptr [eax], 0x750714
00417e30  8b45fc               mov      eax, dword ptr [ebp - 4]
00417e33  8be5                 mov      esp, ebp
00417e35  5d                   pop      ebp
00417e36  c3                   ret      
00417e37  cc                   int3     
00417e38  cc                   int3     
00417e39  cc                   int3     
00417e3a  cc                   int3     
00417e3b  cc                   int3     
00417e3c  cc                   int3     
00417e3d  cc                   int3     
00417e3e  cc                   int3     
00417e3f  cc                   int3     
00417e40  55                   push     ebp
00417e41  8bec                 mov      ebp, esp
00417e43  51                   push     ecx
00417e44  894dfc               mov      dword ptr [ebp - 4], ecx
00417e47  8b4dfc               mov      ecx, dword ptr [ebp - 4]
00417e4a  e821000000           call     0x417e70
00417e4f  8b4508               mov      eax, dword ptr [ebp + 8]
00417e52  83e001               and      eax, 1
00417e55  740c                 je       0x417e63
00417e57  8b4dfc               mov      ecx, dword ptr [ebp - 4]
00417e5a  51                   push     ecx
00417e5b  e8202a2900           call     0x6aa880
00417e60  83c404               add      esp, 4
00417e63  8b45fc               mov      eax, dword ptr [ebp - 4]
00417e66  8be5                 mov      esp, ebp
00417e68  5d                   pop      ebp
00417e69  c20400               ret      4
00417e6c  cc                   int3     
00417e6d  cc                   int3     
00417e6e  cc                   int3     
00417e6f  cc                   int3     
00417e70  55                   push     ebp
00417e71  8bec                 mov      ebp, esp
00417e73  51                   push     ecx
00417e74  894dfc               mov      dword ptr [ebp - 4], ecx
00417e77  8b45fc               mov      eax, dword ptr [ebp - 4]
00417e7a  c70014077500         mov      dword ptr [eax], 0x750714
00417e80  8be5                 mov      esp, ebp
00417e82  5d                   pop      ebp
00417e83  c3                   ret      
00417e84  cc                   int3     
00417e85  cc                   int3     
00417e86  cc                   int3     
00417e87  cc                   int3     
00417e88  cc                   int3     
00417e89  cc                   int3     
00417e8a  cc                   int3     
00417e8b  cc                   int3     
00417e8c  cc                   int3     
00417e8d  cc                   int3     
00417e8e  cc                   int3     
00417e8f  cc                   int3     
00417e90  55                   push     ebp
00417e91  8bec                 mov      ebp, esp
00417e93  6aff                 push     -1
00417e95  685cc66e00           push     0x6ec65c
00417e9a  64a100000000         mov      eax, dword ptr fs:[0]
00417ea0  50                   push     eax
00417ea1  51                   push     ecx
00417ea2  56                   push     esi
00417ea3  a108957c00           mov      eax, dword ptr [0x7c9508]
00417ea8  33c5                 xor      eax, ebp
00417eaa  50                   push     eax
00417eab  8d45f4               lea      eax, [ebp - 0xc]
00417eae  64a300000000         mov      dword ptr fs:[0], eax
00417eb4  894df0               mov      dword ptr [ebp - 0x10], ecx
00417eb7  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00417eba  c7001c077500         mov      dword ptr [eax], 0x75071c
00417ec0  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417ec3  83c104               add      ecx, 4
00417ec6  e8d5e9feff           call     0x4068a0
00417ecb  c745fc00000000       mov      dword ptr [ebp - 4], 0
00417ed2  8b75f0               mov      esi, dword ptr [ebp - 0x10]
00417ed5  83c610               add      esi, 0x10
00417ed8  e893701900           call     0x5aef70
00417edd  c645fc01             mov      byte ptr [ebp - 4], 1
00417ee1  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417ee4  83c114               add      ecx, 0x14
00417ee7  e864030000           call     0x418250
00417eec  c645fc02             mov      byte ptr [ebp - 4], 2
00417ef0  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417ef3  83c124               add      ecx, 0x24
00417ef6  e8a5e9feff           call     0x4068a0
00417efb  c645fc03             mov      byte ptr [ebp - 4], 3
00417eff  6a64                 push     0x64
00417f01  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417f04  83c114               add      ecx, 0x14
00417f07  e814040000           call     0x418320
00417f0c  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
00417f13  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00417f16  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
00417f19  64890d00000000       mov      dword ptr fs:[0], ecx
00417f20  59                   pop      ecx
00417f21  5e                   pop      esi
00417f22  8be5                 mov      esp, ebp
00417f24  5d                   pop      ebp
00417f25  c3                   ret      
00417f26  cc                   int3     
00417f27  cc                   int3     
00417f28  cc                   int3     
00417f29  cc                   int3     
00417f2a  cc                   int3     
00417f2b  cc                   int3     
00417f2c  cc                   int3     
00417f2d  cc                   int3     
00417f2e  cc                   int3     
00417f2f  cc                   int3     
00417f30  55                   push     ebp
00417f31  8bec                 mov      ebp, esp
00417f33  6aff                 push     -1
00417f35  685cc66e00           push     0x6ec65c
00417f3a  64a100000000         mov      eax, dword ptr fs:[0]
00417f40  50                   push     eax
00417f41  51                   push     ecx
00417f42  56                   push     esi
00417f43  a108957c00           mov      eax, dword ptr [0x7c9508]
00417f48  33c5                 xor      eax, ebp
00417f4a  50                   push     eax
00417f4b  8d45f4               lea      eax, [ebp - 0xc]
00417f4e  64a300000000         mov      dword ptr fs:[0], eax
00417f54  894df0               mov      dword ptr [ebp - 0x10], ecx
00417f57  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00417f5a  c7001c077500         mov      dword ptr [eax], 0x75071c
00417f60  c745fc03000000       mov      dword ptr [ebp - 4], 3
00417f67  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00417f6a  83c010               add      eax, 0x10
00417f6d  e85e701900           call     0x5aefd0
00417f72  8b45f0               mov      eax, dword ptr [ebp - 0x10]
00417f75  83c010               add      eax, 0x10
00417f78  e863701900           call     0x5aefe0
00417f7d  c645fc02             mov      byte ptr [ebp - 4], 2
00417f81  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417f84  83c124               add      ecx, 0x24
00417f87  e8d4190000           call     0x419960
00417f8c  c645fc01             mov      byte ptr [ebp - 4], 1
00417f90  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417f93  83c114               add      ecx, 0x14
00417f96  e825030000           call     0x4182c0
00417f9b  c645fc00             mov      byte ptr [ebp - 4], 0
00417f9f  8b75f0               mov      esi, dword ptr [ebp - 0x10]
00417fa2  83c610               add      esi, 0x10
00417fa5  e8f66f1900           call     0x5aefa0
00417faa  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
00417fb1  8b4df0               mov      ecx, dword ptr [ebp - 0x10]
00417fb4  83c104               add      ecx, 4
00417fb7  e8a4190000           call     0x419960
00417fbc  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
00417fbf  64890d00000000       mov      dword ptr fs:[0], ecx
00417fc6  59                   pop      ecx
00417fc7  5e                   pop      esi
00417fc8  8be5                 mov      esp, ebp
00417fca  5d                   pop      ebp
00417fcb  c3                   ret      
00417fcc  cc                   int3     
00417fcd  cc                   int3     
00417fce  cc                   int3     
00417fcf  cc                   int3     
00417fd0  55                   push     ebp
00417fd1  8bec                 mov      ebp, esp
00417fd3  51                   push     ecx
00417fd4  894dfc               mov      dword ptr [ebp - 4], ecx
00417fd7  b001                 mov      al, 1
00417fd9  8be5                 mov      esp, ebp
00417fdb  5d                   pop      ebp
00417fdc  c20400               ret      4
00417fdf  cc                   int3     
00417fe0  55                   push     ebp
00417fe1  8bec                 mov      ebp, esp
00417fe3  6aff                 push     -1
00417fe5  6805c66e00           push     0x6ec605
00417fea  64a100000000         mov      eax, dword ptr fs:[0]
00417ff0  50                   push     eax
00417ff1  81ecb0000000         sub      esp, 0xb0
00417ff7  a108957c00           mov      eax, dword ptr [0x7c9508]
00417ffc  33c5                 xor      eax, ebp
00417ffe  8945f0               mov      dword ptr [ebp - 0x10], eax
00418001  50                   push     eax
00418002  8d45f4               lea      eax, [ebp - 0xc]
00418005  64a300000000         mov      dword ptr fs:[0], eax
0041800b  c78554ffffff00000000 mov      dword ptr [ebp - 0xac], 0
00418015  c745fc03000000       mov      dword ptr [ebp - 4], 3
0041801c  8d4d28               lea      ecx, [ebp + 0x28]
0041801f  e89cb3feff           call     0x4033c0
00418024  50                   push     eax
00418025  8d45d0               lea      eax, [ebp - 0x30]
00418028  50                   push     eax
00418029  e822470600           call     0x47c750
0041802e  83c408               add      esp, 8
00418031  c645fc04             mov      byte ptr [ebp - 4], 4
00418035  6842246400           push     0x642442
0041803a  8d4dc8               lea      ecx, [ebp - 0x38]
0041803d  51                   push     ecx
STRING survival 0x3fffff
REF 0x658816
FUNCTION 0x657f2b
00657f2b  55                   push     ebp
00657f2c  8bec                 mov      ebp, esp
00657f2e  81ecfc010000         sub      esp, 0x1fc
00657f34  a108957c00           mov      eax, dword ptr [0x7c9508]
00657f39  33c5                 xor      eax, ebp
00657f3b  8945fc               mov      dword ptr [ebp - 4], eax
00657f3e  8b4d14               mov      ecx, dword ptr [ebp + 0x14]
00657f41  8b4508               mov      eax, dword ptr [ebp + 8]
00657f44  56                   push     esi
00657f45  33f6                 xor      esi, esi
00657f47  57                   push     edi
00657f48  8b7d0c               mov      edi, dword ptr [ebp + 0xc]
00657f4b  898d1cfeffff         mov      dword ptr [ebp - 0x1e4], ecx
00657f51  8d8d7cfeffff         lea      ecx, [ebp - 0x184]
00657f57  898564feffff         mov      dword ptr [ebp - 0x19c], eax
00657f5d  898d54feffff         mov      dword ptr [ebp - 0x1ac], ecx
00657f63  c78524feffff5e010000 mov      dword ptr [ebp - 0x1dc], 0x15e
00657f6d  89b530feffff         mov      dword ptr [ebp - 0x1d0], esi
00657f73  89b518feffff         mov      dword ptr [ebp - 0x1e8], esi
00657f79  89b578feffff         mov      dword ptr [ebp - 0x188], esi
00657f7f  3bfe                 cmp      edi, esi
00657f81  7520                 jne      0x657fa3
00657f83  e8a1e9feff           call     0x646929
00657f88  56                   push     esi
00657f89  56                   push     esi
00657f8a  56                   push     esi
00657f8b  56                   push     esi
00657f8c  56                   push     esi
00657f8d  c70016000000         mov      dword ptr [eax], 0x16
00657f93  e863c5feff           call     0x6444fb
00657f98  83c414               add      esp, 0x14
00657f9b  83c8ff               or       eax, 0xffffffff
00657f9e  e9350f0000           jmp      0x658ed8
00657fa3  3bc6                 cmp      eax, esi
00657fa5  74dc                 je       0x657f83
00657fa7  f6400c40             test     byte ptr [eax + 0xc], 0x40
00657fab  53                   push     ebx
00657fac  757a                 jne      0x658028
00657fae  50                   push     eax
00657faf  e84083ffff           call     0x6502f4
00657fb4  59                   pop      ecx
00657fb5  bae0a37c00           mov      edx, 0x7ca3e0
00657fba  83f8ff               cmp      eax, -1
00657fbd  741b                 je       0x657fda
00657fbf  83f8fe               cmp      eax, -2
00657fc2  7416                 je       0x657fda
00657fc4  8bc8                 mov      ecx, eax
00657fc6  83e11f               and      ecx, 0x1f
00657fc9  8bd8                 mov      ebx, eax
00657fcb  c1fb05               sar      ebx, 5
00657fce  c1e106               shl      ecx, 6
00657fd1  030c9d20e37d00       add      ecx, dword ptr [ebx*4 + 0x7de320]
00657fd8  eb02                 jmp      0x657fdc
00657fda  8bca                 mov      ecx, edx
00657fdc  f641247f             test     byte ptr [ecx + 0x24], 0x7f
00657fe0  7526                 jne      0x658008
00657fe2  83f8ff               cmp      eax, -1
00657fe5  7419                 je       0x658000
00657fe7  83f8fe               cmp      eax, -2
00657fea  7414                 je       0x658000
00657fec  8bc8                 mov      ecx, eax
00657fee  83e01f               and      eax, 0x1f
00657ff1  c1f905               sar      ecx, 5
00657ff4  c1e006               shl      eax, 6
00657ff7  03048d20e37d00       add      eax, dword ptr [ecx*4 + 0x7de320]
00657ffe  eb02                 jmp      0x658002
00658000  8bc2                 mov      eax, edx
00658002  f6402480             test     byte ptr [eax + 0x24], 0x80
00658006  7420                 je       0x658028
00658008  e81ce9feff           call     0x646929
0065800d  56                   push     esi
0065800e  56                   push     esi
0065800f  56                   push     esi
00658010  56                   push     esi
00658011  56                   push     esi
00658012  c70016000000         mov      dword ptr [eax], 0x16
00658018  e8dec4feff           call     0x6444fb
0065801d  83c414               add      esp, 0x14
00658020  83c8ff               or       eax, 0xffffffff
00658023  e9af0e0000           jmp      0x658ed7
00658028  ff7510               push     dword ptr [ebp + 0x10]
0065802b  8d8d08feffff         lea      ecx, [ebp - 0x1f8]
00658031  e81f9bfeff           call     0x641b55
00658036  8a07                 mov      al, byte ptr [edi]
00658038  c68563feffff00       mov      byte ptr [ebp - 0x19d], 0
0065803f  89b574feffff         mov      dword ptr [ebp - 0x18c], esi
00658045  89b53cfeffff         mov      dword ptr [ebp - 0x1c4], esi
0065804b  84c0                 test     al, al
0065804d  0f846b0e0000         je       0x658ebe
00658053  8bb564feffff         mov      esi, dword ptr [ebp - 0x19c]
00658059  0fb6c0               movzx    eax, al
0065805c  50                   push     eax
0065805d  e8549efeff           call     0x641eb6
00658062  59                   pop      ecx
00658063  85c0                 test     eax, eax
00658065  7430                 je       0x658097
00658067  ff8d74feffff         dec      dword ptr [ebp - 0x18c]
0065806d  56                   push     esi
0065806e  56                   push     esi
0065806f  8db574feffff         lea      esi, [ebp - 0x18c]
00658075  e89f0e0000           call     0x658f19
0065807a  59                   pop      ecx
0065807b  50                   push     eax
0065807c  e8850e0000           call     0x658f06
00658081  59                   pop      ecx
00658082  59                   pop      ecx
00658083  47                   inc      edi
00658084  0fb607               movzx    eax, byte ptr [edi]
00658087  50                   push     eax
00658088  e8299efeff           call     0x641eb6
0065808d  59                   pop      ecx
0065808e  85c0                 test     eax, eax
00658090  75f1                 jne      0x658083
00658092  e9a90d0000           jmp      0x658e40
00658097  8a07                 mov      al, byte ptr [edi]
00658099  3c25                 cmp      al, 0x25
0065809b  0f85310d0000         jne      0x658dd2
006580a1  384701               cmp      byte ptr [edi + 1], al
006580a4  0f841a0d0000         je       0x658dc4
006580aa  33f6                 xor      esi, esi
006580ac  89b540feffff         mov      dword ptr [ebp - 0x1c0], esi
006580b2  c6852ffeffff00       mov      byte ptr [ebp - 0x1d1], 0
006580b9  89b558feffff         mov      dword ptr [ebp - 0x1a8], esi
006580bf  89b54cfeffff         mov      dword ptr [ebp - 0x1b4], esi
006580c5  89b56cfeffff         mov      dword ptr [ebp - 0x194], esi
006580cb  c68561feffff00       mov      byte ptr [ebp - 0x19f], 0
006580d2  c68560feffff00       mov      byte ptr [ebp - 0x1a0], 0
006580d9  c6856afeffff00       mov      byte ptr [ebp - 0x196], 0
006580e0  c68553feffff00       mov      byte ptr [ebp - 0x1ad], 0
006580e7  c68562feffff00       mov      byte ptr [ebp - 0x19e], 0
006580ee  c68573feffff00       mov      byte ptr [ebp - 0x18d], 0
006580f5  c6856bfeffff01       mov      byte ptr [ebp - 0x195], 1
006580fc  89b528feffff         mov      dword ptr [ebp - 0x1d8], esi
00658102  47                   inc      edi
00658103  0fb61f               movzx    ebx, byte ptr [edi]
00658106  0fb6c3               movzx    eax, bl
00658109  50                   push     eax
0065810a  e8a29cfeff           call     0x641db1
0065810f  59                   pop      ecx
00658110  85c0                 test     eax, eax
00658112  741e                 je       0x658132
00658114  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
0065811a  ff854cfeffff         inc      dword ptr [ebp - 0x1b4]
00658120  6bc00a               imul     eax, eax, 0xa
00658123  8d4418d0             lea      eax, [eax + ebx - 0x30]
00658127  89856cfeffff         mov      dword ptr [ebp - 0x194], eax
0065812d  e9c5000000           jmp      0x6581f7
00658132  83fb4e               cmp      ebx, 0x4e
00658135  0f8f83000000         jg       0x6581be
0065813b  0f84b6000000         je       0x6581f7
00658141  83fb2a               cmp      ebx, 0x2a
00658144  7470                 je       0x6581b6
00658146  83fb46               cmp      ebx, 0x46
00658149  0f84a8000000         je       0x6581f7
0065814f  83fb49               cmp      ebx, 0x49
00658152  7410                 je       0x658164
00658154  83fb4c               cmp      ebx, 0x4c
00658157  7574                 jne      0x6581cd
00658159  fe856bfeffff         inc      byte ptr [ebp - 0x195]
0065815f  e993000000           jmp      0x6581f7
00658164  8a4f01               mov      cl, byte ptr [edi + 1]
00658167  80f936               cmp      cl, 0x36
0065816a  751e                 jne      0x65818a
0065816c  8d4702               lea      eax, [edi + 2]
0065816f  803834               cmp      byte ptr [eax], 0x34
00658172  7516                 jne      0x65818a
00658174  ff8528feffff         inc      dword ptr [ebp - 0x1d8]
0065817a  8bf8                 mov      edi, eax
0065817c  89b534feffff         mov      dword ptr [ebp - 0x1cc], esi
00658182  89b538feffff         mov      dword ptr [ebp - 0x1c8], esi
00658188  eb6d                 jmp      0x6581f7
0065818a  80f933               cmp      cl, 0x33
0065818d  750c                 jne      0x65819b
0065818f  8d4702               lea      eax, [edi + 2]
00658192  803832               cmp      byte ptr [eax], 0x32
00658195  7504                 jne      0x65819b
00658197  8bf8                 mov      edi, eax
00658199  eb5c                 jmp      0x6581f7
0065819b  80f964               cmp      cl, 0x64
0065819e  7457                 je       0x6581f7
006581a0  80f969               cmp      cl, 0x69
006581a3  7452                 je       0x6581f7
006581a5  80f96f               cmp      cl, 0x6f
006581a8  744d                 je       0x6581f7
006581aa  80f978               cmp      cl, 0x78
006581ad  7448                 je       0x6581f7
006581af  80f958               cmp      cl, 0x58
006581b2  7519                 jne      0x6581cd
006581b4  eb41                 jmp      0x6581f7
006581b6  fe856afeffff         inc      byte ptr [ebp - 0x196]
006581bc  eb39                 jmp      0x6581f7
006581be  83fb68               cmp      ebx, 0x68
006581c1  7428                 je       0x6581eb
006581c3  83fb6c               cmp      ebx, 0x6c
006581c6  740d                 je       0x6581d5
006581c8  83fb77               cmp      ebx, 0x77
006581cb  7416                 je       0x6581e3
006581cd  fe8553feffff         inc      byte ptr [ebp - 0x1ad]
006581d3  eb22                 jmp      0x6581f7
006581d5  8d4701               lea      eax, [edi + 1]
006581d8  80386c               cmp      byte ptr [eax], 0x6c
006581db  7497                 je       0x658174
006581dd  fe856bfeffff         inc      byte ptr [ebp - 0x195]
006581e3  fe8573feffff         inc      byte ptr [ebp - 0x18d]
006581e9  eb0c                 jmp      0x6581f7
006581eb  fe8d6bfeffff         dec      byte ptr [ebp - 0x195]
006581f1  fe8d73feffff         dec      byte ptr [ebp - 0x18d]
006581f7  80bd53feffff00       cmp      byte ptr [ebp - 0x1ad], 0
006581fe  0f84fefeffff         je       0x658102
00658204  80bd6afeffff00       cmp      byte ptr [ebp - 0x196], 0
0065820b  89bd48feffff         mov      dword ptr [ebp - 0x1b8], edi
00658211  7519                 jne      0x65822c
00658213  8b851cfeffff         mov      eax, dword ptr [ebp - 0x1e4]
00658219  8b30                 mov      esi, dword ptr [eax]
0065821b  898504feffff         mov      dword ptr [ebp - 0x1fc], eax
00658221  83c004               add      eax, 4
00658224  89851cfeffff         mov      dword ptr [ebp - 0x1e4], eax
0065822a  eb02                 jmp      0x65822e
0065822c  33f6                 xor      esi, esi
0065822e  32db                 xor      bl, bl
00658230  89b544feffff         mov      dword ptr [ebp - 0x1bc], esi
00658236  389d73feffff         cmp      byte ptr [ebp - 0x18d], bl
0065823c  7518                 jne      0x658256
0065823e  8a07                 mov      al, byte ptr [edi]
00658240  3c53                 cmp      al, 0x53
00658242  740b                 je       0x65824f
00658244  c68573feffffff       mov      byte ptr [ebp - 0x18d], 0xff
0065824b  3c43                 cmp      al, 0x43
0065824d  7507                 jne      0x658256
0065824f  c68573feffff01       mov      byte ptr [ebp - 0x18d], 1
00658256  0fb607               movzx    eax, byte ptr [edi]
00658259  83c820               or       eax, 0x20
0065825c  89855cfeffff         mov      dword ptr [ebp - 0x1a4], eax
00658262  83f86e               cmp      eax, 0x6e
00658265  744a                 je       0x6582b1
00658267  83f863               cmp      eax, 0x63
0065826a  7419                 je       0x658285
0065826c  83f87b               cmp      eax, 0x7b
0065826f  7414                 je       0x658285
00658271  ffb564feffff         push     dword ptr [ebp - 0x19c]
00658277  8db574feffff         lea      esi, [ebp - 0x18c]
0065827d  e8970c0000           call     0x658f19
00658282  59                   pop      ecx
00658283  eb11                 jmp      0x658296
00658285  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
0065828b  ff8574feffff         inc      dword ptr [ebp - 0x18c]
00658291  e87dfcffff           call     0x657f13
00658296  898578feffff         mov      dword ptr [ebp - 0x188], eax
0065829c  83f8ff               cmp      eax, -1
0065829f  0f84d10b0000         je       0x658e76
006582a5  8bb544feffff         mov      esi, dword ptr [ebp - 0x1bc]
006582ab  8bbd48feffff         mov      edi, dword ptr [ebp - 0x1b8]
006582b1  8b8d4cfeffff         mov      ecx, dword ptr [ebp - 0x1b4]
006582b7  85c9                 test     ecx, ecx
006582b9  740d                 je       0x6582c8
006582bb  83bd6cfeffff00       cmp      dword ptr [ebp - 0x194], 0
006582c2  0f84840b0000         je       0x658e4c
006582c8  8b855cfeffff         mov      eax, dword ptr [ebp - 0x1a4]
006582ce  83f86f               cmp      eax, 0x6f
006582d1  0f8f72050000         jg       0x658849
006582d7  0f8401080000         je       0x658ade
006582dd  83f863               cmp      eax, 0x63
006582e0  0f840a040000         je       0x6586f0
006582e6  6a64                 push     0x64
006582e8  5a                   pop      edx
006582e9  3bc2                 cmp      eax, edx
006582eb  0f84ed070000         je       0x658ade
006582f1  0f8e7a050000         jle      0x658871
006582f7  83f867               cmp      eax, 0x67
006582fa  7e45                 jle      0x658341
006582fc  83f869               cmp      eax, 0x69
006582ff  7421                 je       0x658322
00658301  83f86e               cmp      eax, 0x6e
00658304  0f8567050000         jne      0x658871
0065830a  80bd6afeffff00       cmp      byte ptr [ebp - 0x196], 0
00658311  8bbd74feffff         mov      edi, dword ptr [ebp - 0x18c]
00658317  0f84660a0000         je       0x658d83
0065831d  e98d0a0000           jmp      0x658daf
00658322  89955cfeffff         mov      dword ptr [ebp - 0x1a4], edx
00658328  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
0065832f  0f8534060000         jne      0x658969
00658335  c68560feffff01       mov      byte ptr [ebp - 0x1a0], 1
0065833c  e931060000           jmp      0x658972
00658341  33db                 xor      ebx, ebx
00658343  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
0065834a  750c                 jne      0x658358
0065834c  8b8554feffff         mov      eax, dword ptr [ebp - 0x1ac]
00658352  c6002d               mov      byte ptr [eax], 0x2d
00658355  43                   inc      ebx
00658356  eb09                 jmp      0x658361
00658358  83bd78feffff2b       cmp      dword ptr [ebp - 0x188], 0x2b
0065835f  751d                 jne      0x65837e
00658361  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
00658367  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
0065836d  ff8574feffff         inc      dword ptr [ebp - 0x18c]
00658373  e89bfbffff           call     0x657f13
00658378  898578feffff         mov      dword ptr [ebp - 0x188], eax
0065837e  83bd4cfeffff00       cmp      dword ptr [ebp - 0x1b4], 0
00658385  7507                 jne      0x65838e
00658387  838d6cfeffffff       or       dword ptr [ebp - 0x194], 0xffffffff
0065838e  0fb68578feffff       movzx    eax, byte ptr [ebp - 0x188]
00658395  eb6b                 jmp      0x658402
00658397  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
0065839d  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006583a3  85c0                 test     eax, eax
006583a5  7466                 je       0x65840d
006583a7  8a8578feffff         mov      al, byte ptr [ebp - 0x188]
006583ad  8b8d54feffff         mov      ecx, dword ptr [ebp - 0x1ac]
006583b3  ff8558feffff         inc      dword ptr [ebp - 0x1a8]
006583b9  88040b               mov      byte ptr [ebx + ecx], al
006583bc  8d8530feffff         lea      eax, [ebp - 0x1d0]
006583c2  50                   push     eax
006583c3  8d857cfeffff         lea      eax, [ebp - 0x184]
006583c9  50                   push     eax
006583ca  43                   inc      ebx
006583cb  53                   push     ebx
006583cc  8dbd54feffff         lea      edi, [ebp - 0x1ac]
006583d2  8db524feffff         lea      esi, [ebp - 0x1dc]
006583d8  e8dffaffff           call     0x657ebc
006583dd  83c40c               add      esp, 0xc
006583e0  85c0                 test     eax, eax
006583e2  0f848e0a0000         je       0x658e76
006583e8  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006583ee  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006583f4  e81afbffff           call     0x657f13
006583f9  898578feffff         mov      dword ptr [ebp - 0x188], eax
006583ff  0fb6c0               movzx    eax, al
00658402  50                   push     eax
00658403  e8a999feff           call     0x641db1
00658408  59                   pop      ecx
00658409  85c0                 test     eax, eax
0065840b  758a                 jne      0x658397
0065840d  8b8508feffff         mov      eax, dword ptr [ebp - 0x1f8]
00658413  8b80bc000000         mov      eax, dword ptr [eax + 0xbc]
00658419  8b00                 mov      eax, dword ptr [eax]
0065841b  8a00                 mov      al, byte ptr [eax]
0065841d  888561feffff         mov      byte ptr [ebp - 0x19f], al
00658423  3a8578feffff         cmp      al, byte ptr [ebp - 0x188]
00658429  0f85e5000000         jne      0x658514
0065842f  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
00658435  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
0065843b  85c0                 test     eax, eax
0065843d  0f84d1000000         je       0x658514
00658443  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
00658449  ff8574feffff         inc      dword ptr [ebp - 0x18c]
0065844f  e8bffaffff           call     0x657f13
00658454  8b8d54feffff         mov      ecx, dword ptr [ebp - 0x1ac]
0065845a  898578feffff         mov      dword ptr [ebp - 0x188], eax
00658460  8a8561feffff         mov      al, byte ptr [ebp - 0x19f]
00658466  88040b               mov      byte ptr [ebx + ecx], al
00658469  8d8530feffff         lea      eax, [ebp - 0x1d0]
0065846f  50                   push     eax
00658470  8d857cfeffff         lea      eax, [ebp - 0x184]
00658476  50                   push     eax
00658477  43                   inc      ebx
00658478  53                   push     ebx
00658479  8dbd54feffff         lea      edi, [ebp - 0x1ac]
0065847f  8db524feffff         lea      esi, [ebp - 0x1dc]
00658485  e832faffff           call     0x657ebc
0065848a  83c40c               add      esp, 0xc
0065848d  85c0                 test     eax, eax
0065848f  0f84e1090000         je       0x658e76
00658495  0fb68578feffff       movzx    eax, byte ptr [ebp - 0x188]
0065849c  eb6b                 jmp      0x658509
0065849e  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
006584a4  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006584aa  85c0                 test     eax, eax
006584ac  7466                 je       0x658514
006584ae  8b8554feffff         mov      eax, dword ptr [ebp - 0x1ac]
006584b4  8a8d78feffff         mov      cl, byte ptr [ebp - 0x188]
006584ba  ff8558feffff         inc      dword ptr [ebp - 0x1a8]
006584c0  880c03               mov      byte ptr [ebx + eax], cl
006584c3  8d8530feffff         lea      eax, [ebp - 0x1d0]
006584c9  50                   push     eax
006584ca  8d857cfeffff         lea      eax, [ebp - 0x184]
006584d0  50                   push     eax
006584d1  43                   inc      ebx
006584d2  53                   push     ebx
006584d3  8dbd54feffff         lea      edi, [ebp - 0x1ac]
006584d9  8db524feffff         lea      esi, [ebp - 0x1dc]
006584df  e8d8f9ffff           call     0x657ebc
006584e4  83c40c               add      esp, 0xc
006584e7  85c0                 test     eax, eax
006584e9  0f8487090000         je       0x658e76
006584ef  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006584f5  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006584fb  e813faffff           call     0x657f13
00658500  898578feffff         mov      dword ptr [ebp - 0x188], eax
REF 0x6598af
FUNCTION 0x658f45
00658f45  55                   push     ebp
00658f46  8bec                 mov      ebp, esp
00658f48  81ec00020000         sub      esp, 0x200
00658f4e  a108957c00           mov      eax, dword ptr [0x7c9508]
00658f53  33c5                 xor      eax, ebp
00658f55  8945fc               mov      dword ptr [ebp - 4], eax
00658f58  8b4d14               mov      ecx, dword ptr [ebp + 0x14]
00658f5b  8b4508               mov      eax, dword ptr [ebp + 8]
00658f5e  56                   push     esi
00658f5f  33f6                 xor      esi, esi
00658f61  57                   push     edi
00658f62  8b7d0c               mov      edi, dword ptr [ebp + 0xc]
00658f65  898d20feffff         mov      dword ptr [ebp - 0x1e0], ecx
00658f6b  8d8d7cfeffff         lea      ecx, [ebp - 0x184]
00658f71  898564feffff         mov      dword ptr [ebp - 0x19c], eax
00658f77  89bd54feffff         mov      dword ptr [ebp - 0x1ac], edi
00658f7d  898d5cfeffff         mov      dword ptr [ebp - 0x1a4], ecx
00658f83  c78528feffff5e010000 mov      dword ptr [ebp - 0x1d8], 0x15e
00658f8d  89b530feffff         mov      dword ptr [ebp - 0x1d0], esi
00658f93  89b514feffff         mov      dword ptr [ebp - 0x1ec], esi
00658f99  89b578feffff         mov      dword ptr [ebp - 0x188], esi
00658f9f  89b510feffff         mov      dword ptr [ebp - 0x1f0], esi
00658fa5  3bfe                 cmp      edi, esi
00658fa7  7520                 jne      0x658fc9
00658fa9  e87bd9feff           call     0x646929
00658fae  56                   push     esi
00658faf  56                   push     esi
00658fb0  56                   push     esi
00658fb1  56                   push     esi
00658fb2  56                   push     esi
00658fb3  c70016000000         mov      dword ptr [eax], 0x16
00658fb9  e83db5feff           call     0x6444fb
00658fbe  83c414               add      esp, 0x14
00658fc1  83c8ff               or       eax, 0xffffffff
00658fc4  e990100000           jmp      0x65a059
00658fc9  3bc6                 cmp      eax, esi
00658fcb  74dc                 je       0x658fa9
00658fcd  f6400c40             test     byte ptr [eax + 0xc], 0x40
00658fd1  53                   push     ebx
00658fd2  757a                 jne      0x65904e
00658fd4  50                   push     eax
00658fd5  e81a73ffff           call     0x6502f4
00658fda  59                   pop      ecx
00658fdb  bae0a37c00           mov      edx, 0x7ca3e0
00658fe0  83f8ff               cmp      eax, -1
00658fe3  741b                 je       0x659000
00658fe5  83f8fe               cmp      eax, -2
00658fe8  7416                 je       0x659000
00658fea  8bc8                 mov      ecx, eax
00658fec  83e11f               and      ecx, 0x1f
00658fef  8bd8                 mov      ebx, eax
00658ff1  c1fb05               sar      ebx, 5
00658ff4  c1e106               shl      ecx, 6
00658ff7  030c9d20e37d00       add      ecx, dword ptr [ebx*4 + 0x7de320]
00658ffe  eb02                 jmp      0x659002
00659000  8bca                 mov      ecx, edx
00659002  f641247f             test     byte ptr [ecx + 0x24], 0x7f
00659006  7526                 jne      0x65902e
00659008  83f8ff               cmp      eax, -1
0065900b  7419                 je       0x659026
0065900d  83f8fe               cmp      eax, -2
00659010  7414                 je       0x659026
00659012  8bc8                 mov      ecx, eax
00659014  83e01f               and      eax, 0x1f
00659017  c1f905               sar      ecx, 5
0065901a  c1e006               shl      eax, 6
0065901d  03048d20e37d00       add      eax, dword ptr [ecx*4 + 0x7de320]
00659024  eb02                 jmp      0x659028
00659026  8bc2                 mov      eax, edx
00659028  f6402480             test     byte ptr [eax + 0x24], 0x80
0065902c  7420                 je       0x65904e
0065902e  e8f6d8feff           call     0x646929
00659033  56                   push     esi
00659034  56                   push     esi
00659035  56                   push     esi
00659036  56                   push     esi
00659037  56                   push     esi
00659038  c70016000000         mov      dword ptr [eax], 0x16
0065903e  e8b8b4feff           call     0x6444fb
00659043  83c414               add      esp, 0x14
00659046  83c8ff               or       eax, 0xffffffff
00659049  e90a100000           jmp      0x65a058
0065904e  ff7510               push     dword ptr [ebp + 0x10]
00659051  8d8d00feffff         lea      ecx, [ebp - 0x200]
00659057  e8f98afeff           call     0x641b55
0065905c  8a07                 mov      al, byte ptr [edi]
0065905e  c68563feffff00       mov      byte ptr [ebp - 0x19d], 0
00659065  89b574feffff         mov      dword ptr [ebp - 0x18c], esi
0065906b  89b53cfeffff         mov      dword ptr [ebp - 0x1c4], esi
00659071  84c0                 test     al, al
00659073  0f84c60f0000         je       0x65a03f
00659079  0fb6c0               movzx    eax, al
0065907c  50                   push     eax
0065907d  e8348efeff           call     0x641eb6
00659082  59                   pop      ecx
00659083  85c0                 test     eax, eax
00659085  7446                 je       0x6590cd
00659087  ffb564feffff         push     dword ptr [ebp - 0x19c]
0065908d  ff8d74feffff         dec      dword ptr [ebp - 0x18c]
00659093  ffb564feffff         push     dword ptr [ebp - 0x19c]
00659099  8db574feffff         lea      esi, [ebp - 0x18c]
0065909f  e875feffff           call     0x658f19
006590a4  59                   pop      ecx
006590a5  50                   push     eax
006590a6  e85bfeffff           call     0x658f06
006590ab  8bb554feffff         mov      esi, dword ptr [ebp - 0x1ac]
006590b1  59                   pop      ecx
006590b2  59                   pop      ecx
006590b3  46                   inc      esi
006590b4  0fb606               movzx    eax, byte ptr [esi]
006590b7  50                   push     eax
006590b8  e8f98dfeff           call     0x641eb6
006590bd  59                   pop      ecx
006590be  85c0                 test     eax, eax
006590c0  75f1                 jne      0x6590b3
006590c2  89b554feffff         mov      dword ptr [ebp - 0x1ac], esi
006590c8  e9600e0000           jmp      0x659f2d
006590cd  8bb554feffff         mov      esi, dword ptr [ebp - 0x1ac]
006590d3  8a06                 mov      al, byte ptr [esi]
006590d5  3c25                 cmp      al, 0x25
006590d7  0f85cc0d0000         jne      0x659ea9
006590dd  384601               cmp      byte ptr [esi + 1], al
006590e0  0f84b50d0000         je       0x659e9b
006590e6  33ff                 xor      edi, edi
006590e8  89bd38feffff         mov      dword ptr [ebp - 0x1c8], edi
006590ee  c6852ffeffff00       mov      byte ptr [ebp - 0x1d1], 0
006590f5  89bd58feffff         mov      dword ptr [ebp - 0x1a8], edi
006590fb  89bd40feffff         mov      dword ptr [ebp - 0x1c0], edi
00659101  89bd6cfeffff         mov      dword ptr [ebp - 0x194], edi
00659107  89bd34feffff         mov      dword ptr [ebp - 0x1cc], edi
0065910d  c68562feffff00       mov      byte ptr [ebp - 0x19e], 0
00659114  c68561feffff00       mov      byte ptr [ebp - 0x19f], 0
0065911b  c68571feffff00       mov      byte ptr [ebp - 0x18f], 0
00659122  c68573feffff00       mov      byte ptr [ebp - 0x18d], 0
00659129  c6856afeffff00       mov      byte ptr [ebp - 0x196], 0
00659130  c68572feffff00       mov      byte ptr [ebp - 0x18e], 0
00659137  c6856bfeffff01       mov      byte ptr [ebp - 0x195], 1
0065913e  89bd50feffff         mov      dword ptr [ebp - 0x1b0], edi
00659144  46                   inc      esi
00659145  0fb61e               movzx    ebx, byte ptr [esi]
00659148  0fb6c3               movzx    eax, bl
0065914b  50                   push     eax
0065914c  e8608cfeff           call     0x641db1
00659151  59                   pop      ecx
00659152  85c0                 test     eax, eax
00659154  741e                 je       0x659174
00659156  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
0065915c  ff8540feffff         inc      dword ptr [ebp - 0x1c0]
00659162  6bc00a               imul     eax, eax, 0xa
00659165  8d4418d0             lea      eax, [eax + ebx - 0x30]
00659169  89856cfeffff         mov      dword ptr [ebp - 0x194], eax
0065916f  e9c5000000           jmp      0x659239
00659174  83fb4e               cmp      ebx, 0x4e
00659177  0f8f83000000         jg       0x659200
0065917d  0f84b6000000         je       0x659239
00659183  83fb2a               cmp      ebx, 0x2a
00659186  7470                 je       0x6591f8
00659188  83fb46               cmp      ebx, 0x46
0065918b  0f84a8000000         je       0x659239
00659191  83fb49               cmp      ebx, 0x49
00659194  7410                 je       0x6591a6
00659196  83fb4c               cmp      ebx, 0x4c
00659199  7574                 jne      0x65920f
0065919b  fe856bfeffff         inc      byte ptr [ebp - 0x195]
006591a1  e993000000           jmp      0x659239
006591a6  8a4e01               mov      cl, byte ptr [esi + 1]
006591a9  80f936               cmp      cl, 0x36
006591ac  751e                 jne      0x6591cc
006591ae  8d4602               lea      eax, [esi + 2]
006591b1  803834               cmp      byte ptr [eax], 0x34
006591b4  7516                 jne      0x6591cc
006591b6  ff8550feffff         inc      dword ptr [ebp - 0x1b0]
006591bc  8bf0                 mov      esi, eax
006591be  89bd48feffff         mov      dword ptr [ebp - 0x1b8], edi
006591c4  89bd4cfeffff         mov      dword ptr [ebp - 0x1b4], edi
006591ca  eb6d                 jmp      0x659239
006591cc  80f933               cmp      cl, 0x33
006591cf  750c                 jne      0x6591dd
006591d1  8d4602               lea      eax, [esi + 2]
006591d4  803832               cmp      byte ptr [eax], 0x32
006591d7  7504                 jne      0x6591dd
006591d9  8bf0                 mov      esi, eax
006591db  eb5c                 jmp      0x659239
006591dd  80f964               cmp      cl, 0x64
006591e0  7457                 je       0x659239
006591e2  80f969               cmp      cl, 0x69
006591e5  7452                 je       0x659239
006591e7  80f96f               cmp      cl, 0x6f
006591ea  744d                 je       0x659239
006591ec  80f978               cmp      cl, 0x78
006591ef  7448                 je       0x659239
006591f1  80f958               cmp      cl, 0x58
006591f4  7519                 jne      0x65920f
006591f6  eb41                 jmp      0x659239
006591f8  fe8571feffff         inc      byte ptr [ebp - 0x18f]
006591fe  eb39                 jmp      0x659239
00659200  83fb68               cmp      ebx, 0x68
00659203  7428                 je       0x65922d
00659205  83fb6c               cmp      ebx, 0x6c
00659208  740d                 je       0x659217
0065920a  83fb77               cmp      ebx, 0x77
0065920d  7416                 je       0x659225
0065920f  fe8573feffff         inc      byte ptr [ebp - 0x18d]
00659215  eb22                 jmp      0x659239
00659217  8d4601               lea      eax, [esi + 1]
0065921a  80386c               cmp      byte ptr [eax], 0x6c
0065921d  7497                 je       0x6591b6
0065921f  fe856bfeffff         inc      byte ptr [ebp - 0x195]
00659225  fe8572feffff         inc      byte ptr [ebp - 0x18e]
0065922b  eb0c                 jmp      0x659239
0065922d  fe8d6bfeffff         dec      byte ptr [ebp - 0x195]
00659233  fe8d72feffff         dec      byte ptr [ebp - 0x18e]
00659239  80bd73feffff00       cmp      byte ptr [ebp - 0x18d], 0
00659240  0f84fefeffff         je       0x659144
00659246  80bd71feffff00       cmp      byte ptr [ebp - 0x18f], 0
0065924d  89b554feffff         mov      dword ptr [ebp - 0x1ac], esi
00659253  7519                 jne      0x65926e
00659255  8b8520feffff         mov      eax, dword ptr [ebp - 0x1e0]
0065925b  8b18                 mov      ebx, dword ptr [eax]
0065925d  898518feffff         mov      dword ptr [ebp - 0x1e8], eax
00659263  83c004               add      eax, 4
00659266  898520feffff         mov      dword ptr [ebp - 0x1e0], eax
0065926c  eb02                 jmp      0x659270
0065926e  33db                 xor      ebx, ebx
00659270  80bd72feffff00       cmp      byte ptr [ebp - 0x18e], 0
00659277  899d44feffff         mov      dword ptr [ebp - 0x1bc], ebx
0065927d  c68573feffff00       mov      byte ptr [ebp - 0x18d], 0
00659284  7518                 jne      0x65929e
00659286  8a06                 mov      al, byte ptr [esi]
00659288  3c53                 cmp      al, 0x53
0065928a  740b                 je       0x659297
0065928c  c68572feffffff       mov      byte ptr [ebp - 0x18e], 0xff
00659293  3c43                 cmp      al, 0x43
00659295  7507                 jne      0x65929e
00659297  c68572feffff01       mov      byte ptr [ebp - 0x18e], 1
0065929e  0fb63e               movzx    edi, byte ptr [esi]
006592a1  83cf20               or       edi, 0x20
006592a4  89bd1cfeffff         mov      dword ptr [ebp - 0x1e4], edi
006592aa  83ff6e               cmp      edi, 0x6e
006592ad  744a                 je       0x6592f9
006592af  83ff63               cmp      edi, 0x63
006592b2  7419                 je       0x6592cd
006592b4  83ff7b               cmp      edi, 0x7b
006592b7  7414                 je       0x6592cd
006592b9  ffb564feffff         push     dword ptr [ebp - 0x19c]
006592bf  8db574feffff         lea      esi, [ebp - 0x18c]
006592c5  e84ffcffff           call     0x658f19
006592ca  59                   pop      ecx
006592cb  eb11                 jmp      0x6592de
006592cd  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006592d3  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006592d9  e835ecffff           call     0x657f13
006592de  898578feffff         mov      dword ptr [ebp - 0x188], eax
006592e4  83f8ff               cmp      eax, -1
006592e7  0f84e70c0000         je       0x659fd4
006592ed  8b9d44feffff         mov      ebx, dword ptr [ebp - 0x1bc]
006592f3  8bb554feffff         mov      esi, dword ptr [ebp - 0x1ac]
006592f9  8b8d40feffff         mov      ecx, dword ptr [ebp - 0x1c0]
006592ff  85c9                 test     ecx, ecx
00659301  740d                 je       0x659310
00659303  83bd6cfeffff00       cmp      dword ptr [ebp - 0x194], 0
0065930a  0f842c0c0000         je       0x659f3c
00659310  80bd71feffff00       cmp      byte ptr [ebp - 0x18f], 0
00659317  7541                 jne      0x65935a
00659319  83ff63               cmp      edi, 0x63
0065931c  740a                 je       0x659328
0065931e  83ff73               cmp      edi, 0x73
00659321  7405                 je       0x659328
00659323  83ff7b               cmp      edi, 0x7b
00659326  7532                 jne      0x65935a
00659328  8b8518feffff         mov      eax, dword ptr [ebp - 0x1e8]
0065932e  8b18                 mov      ebx, dword ptr [eax]
00659330  83c004               add      eax, 4
00659333  898518feffff         mov      dword ptr [ebp - 0x1e8], eax
00659339  83c004               add      eax, 4
0065933c  898520feffff         mov      dword ptr [ebp - 0x1e0], eax
00659342  8b40fc               mov      eax, dword ptr [eax - 4]
00659345  899d44feffff         mov      dword ptr [ebp - 0x1bc], ebx
0065934b  898534feffff         mov      dword ptr [ebp - 0x1cc], eax
00659351  83f801               cmp      eax, 1
00659354  0f82fa0b0000         jb       0x659f54
0065935a  83ff6f               cmp      edi, 0x6f
0065935d  0f8f7f050000         jg       0x6598e2
00659363  0f8412080000         je       0x659b7b
00659369  83ff63               cmp      edi, 0x63
0065936c  0f8405040000         je       0x659777
00659372  83ff64               cmp      edi, 0x64
00659375  0f8400080000         je       0x659b7b
0065937b  0f8e8b050000         jle      0x65990c
00659381  83ff67               cmp      edi, 0x67
00659384  7e42                 jle      0x6593c8
00659386  83ff69               cmp      edi, 0x69
00659389  7421                 je       0x6593ac
0065938b  83ff6e               cmp      edi, 0x6e
0065938e  0f8578050000         jne      0x65990c
00659394  80bd71feffff00       cmp      byte ptr [ebp - 0x18f], 0
0065939b  8b8574feffff         mov      eax, dword ptr [ebp - 0x18c]
006593a1  0f84b0090000         je       0x659d57
006593a7  e9da0a0000           jmp      0x659e86
006593ac  6a64                 push     0x64
006593ae  5f                   pop      edi
006593af  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
006593b6  0f8550060000         jne      0x659a0c
006593bc  c68561feffff01       mov      byte ptr [ebp - 0x19f], 1
006593c3  e94d060000           jmp      0x659a15
006593c8  33db                 xor      ebx, ebx
006593ca  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
006593d1  750c                 jne      0x6593df
006593d3  8b855cfeffff         mov      eax, dword ptr [ebp - 0x1a4]
006593d9  c6002d               mov      byte ptr [eax], 0x2d
006593dc  43                   inc      ebx
006593dd  eb09                 jmp      0x6593e8
006593df  83bd78feffff2b       cmp      dword ptr [ebp - 0x188], 0x2b
006593e6  751d                 jne      0x659405
006593e8  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006593ee  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006593f4  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006593fa  e814ebffff           call     0x657f13
006593ff  898578feffff         mov      dword ptr [ebp - 0x188], eax
00659405  83bd40feffff00       cmp      dword ptr [ebp - 0x1c0], 0
0065940c  7507                 jne      0x659415
0065940e  838d6cfeffffff       or       dword ptr [ebp - 0x194], 0xffffffff
00659415  0fb68578feffff       movzx    eax, byte ptr [ebp - 0x188]
0065941c  eb6b                 jmp      0x659489
0065941e  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
00659424  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
0065942a  85c0                 test     eax, eax
0065942c  7466                 je       0x659494
0065942e  8a8578feffff         mov      al, byte ptr [ebp - 0x188]
00659434  8b8d5cfeffff         mov      ecx, dword ptr [ebp - 0x1a4]
0065943a  ff8558feffff         inc      dword ptr [ebp - 0x1a8]
00659440  88040b               mov      byte ptr [ebx + ecx], al
00659443  8d8530feffff         lea      eax, [ebp - 0x1d0]
00659449  50                   push     eax
0065944a  8d857cfeffff         lea      eax, [ebp - 0x184]
00659450  50                   push     eax
00659451  43                   inc      ebx
00659452  53                   push     ebx
00659453  8dbd5cfeffff         lea      edi, [ebp - 0x1a4]
00659459  8db528feffff         lea      esi, [ebp - 0x1d8]
0065945f  e858eaffff           call     0x657ebc
00659464  83c40c               add      esp, 0xc
00659467  85c0                 test     eax, eax
00659469  0f84650b0000         je       0x659fd4
0065946f  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
00659475  ff8574feffff         inc      dword ptr [ebp - 0x18c]
0065947b  e893eaffff           call     0x657f13
00659480  898578feffff         mov      dword ptr [ebp - 0x188], eax
00659486  0fb6c0               movzx    eax, al
00659489  50                   push     eax
0065948a  e82289feff           call     0x641db1
0065948f  59                   pop      ecx
00659490  85c0                 test     eax, eax
00659492  758a                 jne      0x65941e
00659494  8b8500feffff         mov      eax, dword ptr [ebp - 0x200]
0065949a  8b80bc000000         mov      eax, dword ptr [eax + 0xbc]
006594a0  8b00                 mov      eax, dword ptr [eax]
006594a2  8a00                 mov      al, byte ptr [eax]
006594a4  888562feffff         mov      byte ptr [ebp - 0x19e], al
006594aa  3a8578feffff         cmp      al, byte ptr [ebp - 0x188]
006594b0  0f85e5000000         jne      0x65959b
006594b6  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
006594bc  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006594c2  85c0                 test     eax, eax
006594c4  0f84d1000000         je       0x65959b
006594ca  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006594d0  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006594d6  e838eaffff           call     0x657f13
006594db  8b8d5cfeffff         mov      ecx, dword ptr [ebp - 0x1a4]
006594e1  898578feffff         mov      dword ptr [ebp - 0x188], eax
006594e7  8a8562feffff         mov      al, byte ptr [ebp - 0x19e]
006594ed  88040b               mov      byte ptr [ebx + ecx], al
006594f0  8d8530feffff         lea      eax, [ebp - 0x1d0]
006594f6  50                   push     eax
006594f7  8d857cfeffff         lea      eax, [ebp - 0x184]
006594fd  50                   push     eax
006594fe  43                   inc      ebx
006594ff  53                   push     ebx
00659500  8dbd5cfeffff         lea      edi, [ebp - 0x1a4]
00659506  8db528feffff         lea      esi, [ebp - 0x1d8]
0065950c  e8abe9ffff           call     0x657ebc
00659511  83c40c               add      esp, 0xc
00659514  85c0                 test     eax, eax
00659516  0f84b80a0000         je       0x659fd4
STRING campaign 0x3fffff
REF 0x658816
FUNCTION 0x657f2b
00657f2b  55                   push     ebp
00657f2c  8bec                 mov      ebp, esp
00657f2e  81ecfc010000         sub      esp, 0x1fc
00657f34  a108957c00           mov      eax, dword ptr [0x7c9508]
00657f39  33c5                 xor      eax, ebp
00657f3b  8945fc               mov      dword ptr [ebp - 4], eax
00657f3e  8b4d14               mov      ecx, dword ptr [ebp + 0x14]
00657f41  8b4508               mov      eax, dword ptr [ebp + 8]
00657f44  56                   push     esi
00657f45  33f6                 xor      esi, esi
00657f47  57                   push     edi
00657f48  8b7d0c               mov      edi, dword ptr [ebp + 0xc]
00657f4b  898d1cfeffff         mov      dword ptr [ebp - 0x1e4], ecx
00657f51  8d8d7cfeffff         lea      ecx, [ebp - 0x184]
00657f57  898564feffff         mov      dword ptr [ebp - 0x19c], eax
00657f5d  898d54feffff         mov      dword ptr [ebp - 0x1ac], ecx
00657f63  c78524feffff5e010000 mov      dword ptr [ebp - 0x1dc], 0x15e
00657f6d  89b530feffff         mov      dword ptr [ebp - 0x1d0], esi
00657f73  89b518feffff         mov      dword ptr [ebp - 0x1e8], esi
00657f79  89b578feffff         mov      dword ptr [ebp - 0x188], esi
00657f7f  3bfe                 cmp      edi, esi
00657f81  7520                 jne      0x657fa3
00657f83  e8a1e9feff           call     0x646929
00657f88  56                   push     esi
00657f89  56                   push     esi
00657f8a  56                   push     esi
00657f8b  56                   push     esi
00657f8c  56                   push     esi
00657f8d  c70016000000         mov      dword ptr [eax], 0x16
00657f93  e863c5feff           call     0x6444fb
00657f98  83c414               add      esp, 0x14
00657f9b  83c8ff               or       eax, 0xffffffff
00657f9e  e9350f0000           jmp      0x658ed8
00657fa3  3bc6                 cmp      eax, esi
00657fa5  74dc                 je       0x657f83
00657fa7  f6400c40             test     byte ptr [eax + 0xc], 0x40
00657fab  53                   push     ebx
00657fac  757a                 jne      0x658028
00657fae  50                   push     eax
00657faf  e84083ffff           call     0x6502f4
00657fb4  59                   pop      ecx
00657fb5  bae0a37c00           mov      edx, 0x7ca3e0
00657fba  83f8ff               cmp      eax, -1
00657fbd  741b                 je       0x657fda
00657fbf  83f8fe               cmp      eax, -2
00657fc2  7416                 je       0x657fda
00657fc4  8bc8                 mov      ecx, eax
00657fc6  83e11f               and      ecx, 0x1f
00657fc9  8bd8                 mov      ebx, eax
00657fcb  c1fb05               sar      ebx, 5
00657fce  c1e106               shl      ecx, 6
00657fd1  030c9d20e37d00       add      ecx, dword ptr [ebx*4 + 0x7de320]
00657fd8  eb02                 jmp      0x657fdc
00657fda  8bca                 mov      ecx, edx
00657fdc  f641247f             test     byte ptr [ecx + 0x24], 0x7f
00657fe0  7526                 jne      0x658008
00657fe2  83f8ff               cmp      eax, -1
00657fe5  7419                 je       0x658000
00657fe7  83f8fe               cmp      eax, -2
00657fea  7414                 je       0x658000
00657fec  8bc8                 mov      ecx, eax
00657fee  83e01f               and      eax, 0x1f
00657ff1  c1f905               sar      ecx, 5
00657ff4  c1e006               shl      eax, 6
00657ff7  03048d20e37d00       add      eax, dword ptr [ecx*4 + 0x7de320]
00657ffe  eb02                 jmp      0x658002
00658000  8bc2                 mov      eax, edx
00658002  f6402480             test     byte ptr [eax + 0x24], 0x80
00658006  7420                 je       0x658028
00658008  e81ce9feff           call     0x646929
0065800d  56                   push     esi
0065800e  56                   push     esi
0065800f  56                   push     esi
00658010  56                   push     esi
00658011  56                   push     esi
00658012  c70016000000         mov      dword ptr [eax], 0x16
00658018  e8dec4feff           call     0x6444fb
0065801d  83c414               add      esp, 0x14
00658020  83c8ff               or       eax, 0xffffffff
00658023  e9af0e0000           jmp      0x658ed7
00658028  ff7510               push     dword ptr [ebp + 0x10]
0065802b  8d8d08feffff         lea      ecx, [ebp - 0x1f8]
00658031  e81f9bfeff           call     0x641b55
00658036  8a07                 mov      al, byte ptr [edi]
00658038  c68563feffff00       mov      byte ptr [ebp - 0x19d], 0
0065803f  89b574feffff         mov      dword ptr [ebp - 0x18c], esi
00658045  89b53cfeffff         mov      dword ptr [ebp - 0x1c4], esi
0065804b  84c0                 test     al, al
0065804d  0f846b0e0000         je       0x658ebe
00658053  8bb564feffff         mov      esi, dword ptr [ebp - 0x19c]
00658059  0fb6c0               movzx    eax, al
0065805c  50                   push     eax
0065805d  e8549efeff           call     0x641eb6
00658062  59                   pop      ecx
00658063  85c0                 test     eax, eax
00658065  7430                 je       0x658097
00658067  ff8d74feffff         dec      dword ptr [ebp - 0x18c]
0065806d  56                   push     esi
0065806e  56                   push     esi
0065806f  8db574feffff         lea      esi, [ebp - 0x18c]
00658075  e89f0e0000           call     0x658f19
0065807a  59                   pop      ecx
0065807b  50                   push     eax
0065807c  e8850e0000           call     0x658f06
00658081  59                   pop      ecx
00658082  59                   pop      ecx
00658083  47                   inc      edi
00658084  0fb607               movzx    eax, byte ptr [edi]
00658087  50                   push     eax
00658088  e8299efeff           call     0x641eb6
0065808d  59                   pop      ecx
0065808e  85c0                 test     eax, eax
00658090  75f1                 jne      0x658083
00658092  e9a90d0000           jmp      0x658e40
00658097  8a07                 mov      al, byte ptr [edi]
00658099  3c25                 cmp      al, 0x25
0065809b  0f85310d0000         jne      0x658dd2
006580a1  384701               cmp      byte ptr [edi + 1], al
006580a4  0f841a0d0000         je       0x658dc4
006580aa  33f6                 xor      esi, esi
006580ac  89b540feffff         mov      dword ptr [ebp - 0x1c0], esi
006580b2  c6852ffeffff00       mov      byte ptr [ebp - 0x1d1], 0
006580b9  89b558feffff         mov      dword ptr [ebp - 0x1a8], esi
006580bf  89b54cfeffff         mov      dword ptr [ebp - 0x1b4], esi
006580c5  89b56cfeffff         mov      dword ptr [ebp - 0x194], esi
006580cb  c68561feffff00       mov      byte ptr [ebp - 0x19f], 0
006580d2  c68560feffff00       mov      byte ptr [ebp - 0x1a0], 0
006580d9  c6856afeffff00       mov      byte ptr [ebp - 0x196], 0
006580e0  c68553feffff00       mov      byte ptr [ebp - 0x1ad], 0
006580e7  c68562feffff00       mov      byte ptr [ebp - 0x19e], 0
006580ee  c68573feffff00       mov      byte ptr [ebp - 0x18d], 0
006580f5  c6856bfeffff01       mov      byte ptr [ebp - 0x195], 1
006580fc  89b528feffff         mov      dword ptr [ebp - 0x1d8], esi
00658102  47                   inc      edi
00658103  0fb61f               movzx    ebx, byte ptr [edi]
00658106  0fb6c3               movzx    eax, bl
00658109  50                   push     eax
0065810a  e8a29cfeff           call     0x641db1
0065810f  59                   pop      ecx
00658110  85c0                 test     eax, eax
00658112  741e                 je       0x658132
00658114  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
0065811a  ff854cfeffff         inc      dword ptr [ebp - 0x1b4]
00658120  6bc00a               imul     eax, eax, 0xa
00658123  8d4418d0             lea      eax, [eax + ebx - 0x30]
00658127  89856cfeffff         mov      dword ptr [ebp - 0x194], eax
0065812d  e9c5000000           jmp      0x6581f7
00658132  83fb4e               cmp      ebx, 0x4e
00658135  0f8f83000000         jg       0x6581be
0065813b  0f84b6000000         je       0x6581f7
00658141  83fb2a               cmp      ebx, 0x2a
00658144  7470                 je       0x6581b6
00658146  83fb46               cmp      ebx, 0x46
00658149  0f84a8000000         je       0x6581f7
0065814f  83fb49               cmp      ebx, 0x49
00658152  7410                 je       0x658164
00658154  83fb4c               cmp      ebx, 0x4c
00658157  7574                 jne      0x6581cd
00658159  fe856bfeffff         inc      byte ptr [ebp - 0x195]
0065815f  e993000000           jmp      0x6581f7
00658164  8a4f01               mov      cl, byte ptr [edi + 1]
00658167  80f936               cmp      cl, 0x36
0065816a  751e                 jne      0x65818a
0065816c  8d4702               lea      eax, [edi + 2]
0065816f  803834               cmp      byte ptr [eax], 0x34
00658172  7516                 jne      0x65818a
00658174  ff8528feffff         inc      dword ptr [ebp - 0x1d8]
0065817a  8bf8                 mov      edi, eax
0065817c  89b534feffff         mov      dword ptr [ebp - 0x1cc], esi
00658182  89b538feffff         mov      dword ptr [ebp - 0x1c8], esi
00658188  eb6d                 jmp      0x6581f7
0065818a  80f933               cmp      cl, 0x33
0065818d  750c                 jne      0x65819b
0065818f  8d4702               lea      eax, [edi + 2]
00658192  803832               cmp      byte ptr [eax], 0x32
00658195  7504                 jne      0x65819b
00658197  8bf8                 mov      edi, eax
00658199  eb5c                 jmp      0x6581f7
0065819b  80f964               cmp      cl, 0x64
0065819e  7457                 je       0x6581f7
006581a0  80f969               cmp      cl, 0x69
006581a3  7452                 je       0x6581f7
006581a5  80f96f               cmp      cl, 0x6f
006581a8  744d                 je       0x6581f7
006581aa  80f978               cmp      cl, 0x78
006581ad  7448                 je       0x6581f7
006581af  80f958               cmp      cl, 0x58
006581b2  7519                 jne      0x6581cd
006581b4  eb41                 jmp      0x6581f7
006581b6  fe856afeffff         inc      byte ptr [ebp - 0x196]
006581bc  eb39                 jmp      0x6581f7
006581be  83fb68               cmp      ebx, 0x68
006581c1  7428                 je       0x6581eb
006581c3  83fb6c               cmp      ebx, 0x6c
006581c6  740d                 je       0x6581d5
006581c8  83fb77               cmp      ebx, 0x77
006581cb  7416                 je       0x6581e3
006581cd  fe8553feffff         inc      byte ptr [ebp - 0x1ad]
006581d3  eb22                 jmp      0x6581f7
006581d5  8d4701               lea      eax, [edi + 1]
006581d8  80386c               cmp      byte ptr [eax], 0x6c
006581db  7497                 je       0x658174
006581dd  fe856bfeffff         inc      byte ptr [ebp - 0x195]
006581e3  fe8573feffff         inc      byte ptr [ebp - 0x18d]
006581e9  eb0c                 jmp      0x6581f7
006581eb  fe8d6bfeffff         dec      byte ptr [ebp - 0x195]
006581f1  fe8d73feffff         dec      byte ptr [ebp - 0x18d]
006581f7  80bd53feffff00       cmp      byte ptr [ebp - 0x1ad], 0
006581fe  0f84fefeffff         je       0x658102
00658204  80bd6afeffff00       cmp      byte ptr [ebp - 0x196], 0
0065820b  89bd48feffff         mov      dword ptr [ebp - 0x1b8], edi
00658211  7519                 jne      0x65822c
00658213  8b851cfeffff         mov      eax, dword ptr [ebp - 0x1e4]
00658219  8b30                 mov      esi, dword ptr [eax]
0065821b  898504feffff         mov      dword ptr [ebp - 0x1fc], eax
00658221  83c004               add      eax, 4
00658224  89851cfeffff         mov      dword ptr [ebp - 0x1e4], eax
0065822a  eb02                 jmp      0x65822e
0065822c  33f6                 xor      esi, esi
0065822e  32db                 xor      bl, bl
00658230  89b544feffff         mov      dword ptr [ebp - 0x1bc], esi
00658236  389d73feffff         cmp      byte ptr [ebp - 0x18d], bl
0065823c  7518                 jne      0x658256
0065823e  8a07                 mov      al, byte ptr [edi]
00658240  3c53                 cmp      al, 0x53
00658242  740b                 je       0x65824f
00658244  c68573feffffff       mov      byte ptr [ebp - 0x18d], 0xff
0065824b  3c43                 cmp      al, 0x43
0065824d  7507                 jne      0x658256
0065824f  c68573feffff01       mov      byte ptr [ebp - 0x18d], 1
00658256  0fb607               movzx    eax, byte ptr [edi]
00658259  83c820               or       eax, 0x20
0065825c  89855cfeffff         mov      dword ptr [ebp - 0x1a4], eax
00658262  83f86e               cmp      eax, 0x6e
00658265  744a                 je       0x6582b1
00658267  83f863               cmp      eax, 0x63
0065826a  7419                 je       0x658285
0065826c  83f87b               cmp      eax, 0x7b
0065826f  7414                 je       0x658285
00658271  ffb564feffff         push     dword ptr [ebp - 0x19c]
00658277  8db574feffff         lea      esi, [ebp - 0x18c]
0065827d  e8970c0000           call     0x658f19
00658282  59                   pop      ecx
00658283  eb11                 jmp      0x658296
00658285  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
0065828b  ff8574feffff         inc      dword ptr [ebp - 0x18c]
00658291  e87dfcffff           call     0x657f13
00658296  898578feffff         mov      dword ptr [ebp - 0x188], eax
0065829c  83f8ff               cmp      eax, -1
0065829f  0f84d10b0000         je       0x658e76
006582a5  8bb544feffff         mov      esi, dword ptr [ebp - 0x1bc]
006582ab  8bbd48feffff         mov      edi, dword ptr [ebp - 0x1b8]
006582b1  8b8d4cfeffff         mov      ecx, dword ptr [ebp - 0x1b4]
006582b7  85c9                 test     ecx, ecx
006582b9  740d                 je       0x6582c8
006582bb  83bd6cfeffff00       cmp      dword ptr [ebp - 0x194], 0
006582c2  0f84840b0000         je       0x658e4c
006582c8  8b855cfeffff         mov      eax, dword ptr [ebp - 0x1a4]
006582ce  83f86f               cmp      eax, 0x6f
006582d1  0f8f72050000         jg       0x658849
006582d7  0f8401080000         je       0x658ade
006582dd  83f863               cmp      eax, 0x63
006582e0  0f840a040000         je       0x6586f0
006582e6  6a64                 push     0x64
006582e8  5a                   pop      edx
006582e9  3bc2                 cmp      eax, edx
006582eb  0f84ed070000         je       0x658ade
006582f1  0f8e7a050000         jle      0x658871
006582f7  83f867               cmp      eax, 0x67
006582fa  7e45                 jle      0x658341
006582fc  83f869               cmp      eax, 0x69
006582ff  7421                 je       0x658322
00658301  83f86e               cmp      eax, 0x6e
00658304  0f8567050000         jne      0x658871
0065830a  80bd6afeffff00       cmp      byte ptr [ebp - 0x196], 0
00658311  8bbd74feffff         mov      edi, dword ptr [ebp - 0x18c]
00658317  0f84660a0000         je       0x658d83
0065831d  e98d0a0000           jmp      0x658daf
00658322  89955cfeffff         mov      dword ptr [ebp - 0x1a4], edx
00658328  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
0065832f  0f8534060000         jne      0x658969
00658335  c68560feffff01       mov      byte ptr [ebp - 0x1a0], 1
0065833c  e931060000           jmp      0x658972
00658341  33db                 xor      ebx, ebx
00658343  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
0065834a  750c                 jne      0x658358
0065834c  8b8554feffff         mov      eax, dword ptr [ebp - 0x1ac]
00658352  c6002d               mov      byte ptr [eax], 0x2d
00658355  43                   inc      ebx
00658356  eb09                 jmp      0x658361
00658358  83bd78feffff2b       cmp      dword ptr [ebp - 0x188], 0x2b
0065835f  751d                 jne      0x65837e
00658361  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
00658367  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
0065836d  ff8574feffff         inc      dword ptr [ebp - 0x18c]
00658373  e89bfbffff           call     0x657f13
00658378  898578feffff         mov      dword ptr [ebp - 0x188], eax
0065837e  83bd4cfeffff00       cmp      dword ptr [ebp - 0x1b4], 0
00658385  7507                 jne      0x65838e
00658387  838d6cfeffffff       or       dword ptr [ebp - 0x194], 0xffffffff
0065838e  0fb68578feffff       movzx    eax, byte ptr [ebp - 0x188]
00658395  eb6b                 jmp      0x658402
00658397  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
0065839d  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006583a3  85c0                 test     eax, eax
006583a5  7466                 je       0x65840d
006583a7  8a8578feffff         mov      al, byte ptr [ebp - 0x188]
006583ad  8b8d54feffff         mov      ecx, dword ptr [ebp - 0x1ac]
006583b3  ff8558feffff         inc      dword ptr [ebp - 0x1a8]
006583b9  88040b               mov      byte ptr [ebx + ecx], al
006583bc  8d8530feffff         lea      eax, [ebp - 0x1d0]
006583c2  50                   push     eax
006583c3  8d857cfeffff         lea      eax, [ebp - 0x184]
006583c9  50                   push     eax
006583ca  43                   inc      ebx
006583cb  53                   push     ebx
006583cc  8dbd54feffff         lea      edi, [ebp - 0x1ac]
006583d2  8db524feffff         lea      esi, [ebp - 0x1dc]
006583d8  e8dffaffff           call     0x657ebc
006583dd  83c40c               add      esp, 0xc
006583e0  85c0                 test     eax, eax
006583e2  0f848e0a0000         je       0x658e76
006583e8  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006583ee  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006583f4  e81afbffff           call     0x657f13
006583f9  898578feffff         mov      dword ptr [ebp - 0x188], eax
006583ff  0fb6c0               movzx    eax, al
00658402  50                   push     eax
00658403  e8a999feff           call     0x641db1
00658408  59                   pop      ecx
00658409  85c0                 test     eax, eax
0065840b  758a                 jne      0x658397
0065840d  8b8508feffff         mov      eax, dword ptr [ebp - 0x1f8]
00658413  8b80bc000000         mov      eax, dword ptr [eax + 0xbc]
00658419  8b00                 mov      eax, dword ptr [eax]
0065841b  8a00                 mov      al, byte ptr [eax]
0065841d  888561feffff         mov      byte ptr [ebp - 0x19f], al
00658423  3a8578feffff         cmp      al, byte ptr [ebp - 0x188]
00658429  0f85e5000000         jne      0x658514
0065842f  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
00658435  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
0065843b  85c0                 test     eax, eax
0065843d  0f84d1000000         je       0x658514
00658443  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
00658449  ff8574feffff         inc      dword ptr [ebp - 0x18c]
0065844f  e8bffaffff           call     0x657f13
00658454  8b8d54feffff         mov      ecx, dword ptr [ebp - 0x1ac]
0065845a  898578feffff         mov      dword ptr [ebp - 0x188], eax
00658460  8a8561feffff         mov      al, byte ptr [ebp - 0x19f]
00658466  88040b               mov      byte ptr [ebx + ecx], al
00658469  8d8530feffff         lea      eax, [ebp - 0x1d0]
0065846f  50                   push     eax
00658470  8d857cfeffff         lea      eax, [ebp - 0x184]
00658476  50                   push     eax
00658477  43                   inc      ebx
00658478  53                   push     ebx
00658479  8dbd54feffff         lea      edi, [ebp - 0x1ac]
0065847f  8db524feffff         lea      esi, [ebp - 0x1dc]
00658485  e832faffff           call     0x657ebc
0065848a  83c40c               add      esp, 0xc
0065848d  85c0                 test     eax, eax
0065848f  0f84e1090000         je       0x658e76
00658495  0fb68578feffff       movzx    eax, byte ptr [ebp - 0x188]
0065849c  eb6b                 jmp      0x658509
0065849e  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
006584a4  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006584aa  85c0                 test     eax, eax
006584ac  7466                 je       0x658514
006584ae  8b8554feffff         mov      eax, dword ptr [ebp - 0x1ac]
006584b4  8a8d78feffff         mov      cl, byte ptr [ebp - 0x188]
006584ba  ff8558feffff         inc      dword ptr [ebp - 0x1a8]
006584c0  880c03               mov      byte ptr [ebx + eax], cl
006584c3  8d8530feffff         lea      eax, [ebp - 0x1d0]
006584c9  50                   push     eax
006584ca  8d857cfeffff         lea      eax, [ebp - 0x184]
006584d0  50                   push     eax
006584d1  43                   inc      ebx
006584d2  53                   push     ebx
006584d3  8dbd54feffff         lea      edi, [ebp - 0x1ac]
006584d9  8db524feffff         lea      esi, [ebp - 0x1dc]
006584df  e8d8f9ffff           call     0x657ebc
006584e4  83c40c               add      esp, 0xc
006584e7  85c0                 test     eax, eax
006584e9  0f8487090000         je       0x658e76
006584ef  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006584f5  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006584fb  e813faffff           call     0x657f13
00658500  898578feffff         mov      dword ptr [ebp - 0x188], eax
REF 0x6598af
FUNCTION 0x658f45
00658f45  55                   push     ebp
00658f46  8bec                 mov      ebp, esp
00658f48  81ec00020000         sub      esp, 0x200
00658f4e  a108957c00           mov      eax, dword ptr [0x7c9508]
00658f53  33c5                 xor      eax, ebp
00658f55  8945fc               mov      dword ptr [ebp - 4], eax
00658f58  8b4d14               mov      ecx, dword ptr [ebp + 0x14]
00658f5b  8b4508               mov      eax, dword ptr [ebp + 8]
00658f5e  56                   push     esi
00658f5f  33f6                 xor      esi, esi
00658f61  57                   push     edi
00658f62  8b7d0c               mov      edi, dword ptr [ebp + 0xc]
00658f65  898d20feffff         mov      dword ptr [ebp - 0x1e0], ecx
00658f6b  8d8d7cfeffff         lea      ecx, [ebp - 0x184]
00658f71  898564feffff         mov      dword ptr [ebp - 0x19c], eax
00658f77  89bd54feffff         mov      dword ptr [ebp - 0x1ac], edi
00658f7d  898d5cfeffff         mov      dword ptr [ebp - 0x1a4], ecx
00658f83  c78528feffff5e010000 mov      dword ptr [ebp - 0x1d8], 0x15e
00658f8d  89b530feffff         mov      dword ptr [ebp - 0x1d0], esi
00658f93  89b514feffff         mov      dword ptr [ebp - 0x1ec], esi
00658f99  89b578feffff         mov      dword ptr [ebp - 0x188], esi
00658f9f  89b510feffff         mov      dword ptr [ebp - 0x1f0], esi
00658fa5  3bfe                 cmp      edi, esi
00658fa7  7520                 jne      0x658fc9
00658fa9  e87bd9feff           call     0x646929
00658fae  56                   push     esi
00658faf  56                   push     esi
00658fb0  56                   push     esi
00658fb1  56                   push     esi
00658fb2  56                   push     esi
00658fb3  c70016000000         mov      dword ptr [eax], 0x16
00658fb9  e83db5feff           call     0x6444fb
00658fbe  83c414               add      esp, 0x14
00658fc1  83c8ff               or       eax, 0xffffffff
00658fc4  e990100000           jmp      0x65a059
00658fc9  3bc6                 cmp      eax, esi
00658fcb  74dc                 je       0x658fa9
00658fcd  f6400c40             test     byte ptr [eax + 0xc], 0x40
00658fd1  53                   push     ebx
00658fd2  757a                 jne      0x65904e
00658fd4  50                   push     eax
00658fd5  e81a73ffff           call     0x6502f4
00658fda  59                   pop      ecx
00658fdb  bae0a37c00           mov      edx, 0x7ca3e0
00658fe0  83f8ff               cmp      eax, -1
00658fe3  741b                 je       0x659000
00658fe5  83f8fe               cmp      eax, -2
00658fe8  7416                 je       0x659000
00658fea  8bc8                 mov      ecx, eax
00658fec  83e11f               and      ecx, 0x1f
00658fef  8bd8                 mov      ebx, eax
00658ff1  c1fb05               sar      ebx, 5
00658ff4  c1e106               shl      ecx, 6
00658ff7  030c9d20e37d00       add      ecx, dword ptr [ebx*4 + 0x7de320]
00658ffe  eb02                 jmp      0x659002
00659000  8bca                 mov      ecx, edx
00659002  f641247f             test     byte ptr [ecx + 0x24], 0x7f
00659006  7526                 jne      0x65902e
00659008  83f8ff               cmp      eax, -1
0065900b  7419                 je       0x659026
0065900d  83f8fe               cmp      eax, -2
00659010  7414                 je       0x659026
00659012  8bc8                 mov      ecx, eax
00659014  83e01f               and      eax, 0x1f
00659017  c1f905               sar      ecx, 5
0065901a  c1e006               shl      eax, 6
0065901d  03048d20e37d00       add      eax, dword ptr [ecx*4 + 0x7de320]
00659024  eb02                 jmp      0x659028
00659026  8bc2                 mov      eax, edx
00659028  f6402480             test     byte ptr [eax + 0x24], 0x80
0065902c  7420                 je       0x65904e
0065902e  e8f6d8feff           call     0x646929
00659033  56                   push     esi
00659034  56                   push     esi
00659035  56                   push     esi
00659036  56                   push     esi
00659037  56                   push     esi
00659038  c70016000000         mov      dword ptr [eax], 0x16
0065903e  e8b8b4feff           call     0x6444fb
00659043  83c414               add      esp, 0x14
00659046  83c8ff               or       eax, 0xffffffff
00659049  e90a100000           jmp      0x65a058
0065904e  ff7510               push     dword ptr [ebp + 0x10]
00659051  8d8d00feffff         lea      ecx, [ebp - 0x200]
00659057  e8f98afeff           call     0x641b55
0065905c  8a07                 mov      al, byte ptr [edi]
0065905e  c68563feffff00       mov      byte ptr [ebp - 0x19d], 0
00659065  89b574feffff         mov      dword ptr [ebp - 0x18c], esi
0065906b  89b53cfeffff         mov      dword ptr [ebp - 0x1c4], esi
00659071  84c0                 test     al, al
00659073  0f84c60f0000         je       0x65a03f
00659079  0fb6c0               movzx    eax, al
0065907c  50                   push     eax
0065907d  e8348efeff           call     0x641eb6
00659082  59                   pop      ecx
00659083  85c0                 test     eax, eax
00659085  7446                 je       0x6590cd
00659087  ffb564feffff         push     dword ptr [ebp - 0x19c]
0065908d  ff8d74feffff         dec      dword ptr [ebp - 0x18c]
00659093  ffb564feffff         push     dword ptr [ebp - 0x19c]
00659099  8db574feffff         lea      esi, [ebp - 0x18c]
0065909f  e875feffff           call     0x658f19
006590a4  59                   pop      ecx
006590a5  50                   push     eax
006590a6  e85bfeffff           call     0x658f06
006590ab  8bb554feffff         mov      esi, dword ptr [ebp - 0x1ac]
006590b1  59                   pop      ecx
006590b2  59                   pop      ecx
006590b3  46                   inc      esi
006590b4  0fb606               movzx    eax, byte ptr [esi]
006590b7  50                   push     eax
006590b8  e8f98dfeff           call     0x641eb6
006590bd  59                   pop      ecx
006590be  85c0                 test     eax, eax
006590c0  75f1                 jne      0x6590b3
006590c2  89b554feffff         mov      dword ptr [ebp - 0x1ac], esi
006590c8  e9600e0000           jmp      0x659f2d
006590cd  8bb554feffff         mov      esi, dword ptr [ebp - 0x1ac]
006590d3  8a06                 mov      al, byte ptr [esi]
006590d5  3c25                 cmp      al, 0x25
006590d7  0f85cc0d0000         jne      0x659ea9
006590dd  384601               cmp      byte ptr [esi + 1], al
006590e0  0f84b50d0000         je       0x659e9b
006590e6  33ff                 xor      edi, edi
006590e8  89bd38feffff         mov      dword ptr [ebp - 0x1c8], edi
006590ee  c6852ffeffff00       mov      byte ptr [ebp - 0x1d1], 0
006590f5  89bd58feffff         mov      dword ptr [ebp - 0x1a8], edi
006590fb  89bd40feffff         mov      dword ptr [ebp - 0x1c0], edi
00659101  89bd6cfeffff         mov      dword ptr [ebp - 0x194], edi
00659107  89bd34feffff         mov      dword ptr [ebp - 0x1cc], edi
0065910d  c68562feffff00       mov      byte ptr [ebp - 0x19e], 0
00659114  c68561feffff00       mov      byte ptr [ebp - 0x19f], 0
0065911b  c68571feffff00       mov      byte ptr [ebp - 0x18f], 0
00659122  c68573feffff00       mov      byte ptr [ebp - 0x18d], 0
00659129  c6856afeffff00       mov      byte ptr [ebp - 0x196], 0
00659130  c68572feffff00       mov      byte ptr [ebp - 0x18e], 0
00659137  c6856bfeffff01       mov      byte ptr [ebp - 0x195], 1
0065913e  89bd50feffff         mov      dword ptr [ebp - 0x1b0], edi
00659144  46                   inc      esi
00659145  0fb61e               movzx    ebx, byte ptr [esi]
00659148  0fb6c3               movzx    eax, bl
0065914b  50                   push     eax
0065914c  e8608cfeff           call     0x641db1
00659151  59                   pop      ecx
00659152  85c0                 test     eax, eax
00659154  741e                 je       0x659174
00659156  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
0065915c  ff8540feffff         inc      dword ptr [ebp - 0x1c0]
00659162  6bc00a               imul     eax, eax, 0xa
00659165  8d4418d0             lea      eax, [eax + ebx - 0x30]
00659169  89856cfeffff         mov      dword ptr [ebp - 0x194], eax
0065916f  e9c5000000           jmp      0x659239
00659174  83fb4e               cmp      ebx, 0x4e
00659177  0f8f83000000         jg       0x659200
0065917d  0f84b6000000         je       0x659239
00659183  83fb2a               cmp      ebx, 0x2a
00659186  7470                 je       0x6591f8
00659188  83fb46               cmp      ebx, 0x46
0065918b  0f84a8000000         je       0x659239
00659191  83fb49               cmp      ebx, 0x49
00659194  7410                 je       0x6591a6
00659196  83fb4c               cmp      ebx, 0x4c
00659199  7574                 jne      0x65920f
0065919b  fe856bfeffff         inc      byte ptr [ebp - 0x195]
006591a1  e993000000           jmp      0x659239
006591a6  8a4e01               mov      cl, byte ptr [esi + 1]
006591a9  80f936               cmp      cl, 0x36
006591ac  751e                 jne      0x6591cc
006591ae  8d4602               lea      eax, [esi + 2]
006591b1  803834               cmp      byte ptr [eax], 0x34
006591b4  7516                 jne      0x6591cc
006591b6  ff8550feffff         inc      dword ptr [ebp - 0x1b0]
006591bc  8bf0                 mov      esi, eax
006591be  89bd48feffff         mov      dword ptr [ebp - 0x1b8], edi
006591c4  89bd4cfeffff         mov      dword ptr [ebp - 0x1b4], edi
006591ca  eb6d                 jmp      0x659239
006591cc  80f933               cmp      cl, 0x33
006591cf  750c                 jne      0x6591dd
006591d1  8d4602               lea      eax, [esi + 2]
006591d4  803832               cmp      byte ptr [eax], 0x32
006591d7  7504                 jne      0x6591dd
006591d9  8bf0                 mov      esi, eax
006591db  eb5c                 jmp      0x659239
006591dd  80f964               cmp      cl, 0x64
006591e0  7457                 je       0x659239
006591e2  80f969               cmp      cl, 0x69
006591e5  7452                 je       0x659239
006591e7  80f96f               cmp      cl, 0x6f
006591ea  744d                 je       0x659239
006591ec  80f978               cmp      cl, 0x78
006591ef  7448                 je       0x659239
006591f1  80f958               cmp      cl, 0x58
006591f4  7519                 jne      0x65920f
006591f6  eb41                 jmp      0x659239
006591f8  fe8571feffff         inc      byte ptr [ebp - 0x18f]
006591fe  eb39                 jmp      0x659239
00659200  83fb68               cmp      ebx, 0x68
00659203  7428                 je       0x65922d
00659205  83fb6c               cmp      ebx, 0x6c
00659208  740d                 je       0x659217
0065920a  83fb77               cmp      ebx, 0x77
0065920d  7416                 je       0x659225
0065920f  fe8573feffff         inc      byte ptr [ebp - 0x18d]
00659215  eb22                 jmp      0x659239
00659217  8d4601               lea      eax, [esi + 1]
0065921a  80386c               cmp      byte ptr [eax], 0x6c
0065921d  7497                 je       0x6591b6
0065921f  fe856bfeffff         inc      byte ptr [ebp - 0x195]
00659225  fe8572feffff         inc      byte ptr [ebp - 0x18e]
0065922b  eb0c                 jmp      0x659239
0065922d  fe8d6bfeffff         dec      byte ptr [ebp - 0x195]
00659233  fe8d72feffff         dec      byte ptr [ebp - 0x18e]
00659239  80bd73feffff00       cmp      byte ptr [ebp - 0x18d], 0
00659240  0f84fefeffff         je       0x659144
00659246  80bd71feffff00       cmp      byte ptr [ebp - 0x18f], 0
0065924d  89b554feffff         mov      dword ptr [ebp - 0x1ac], esi
00659253  7519                 jne      0x65926e
00659255  8b8520feffff         mov      eax, dword ptr [ebp - 0x1e0]
0065925b  8b18                 mov      ebx, dword ptr [eax]
0065925d  898518feffff         mov      dword ptr [ebp - 0x1e8], eax
00659263  83c004               add      eax, 4
00659266  898520feffff         mov      dword ptr [ebp - 0x1e0], eax
0065926c  eb02                 jmp      0x659270
0065926e  33db                 xor      ebx, ebx
00659270  80bd72feffff00       cmp      byte ptr [ebp - 0x18e], 0
00659277  899d44feffff         mov      dword ptr [ebp - 0x1bc], ebx
0065927d  c68573feffff00       mov      byte ptr [ebp - 0x18d], 0
00659284  7518                 jne      0x65929e
00659286  8a06                 mov      al, byte ptr [esi]
00659288  3c53                 cmp      al, 0x53
0065928a  740b                 je       0x659297
0065928c  c68572feffffff       mov      byte ptr [ebp - 0x18e], 0xff
00659293  3c43                 cmp      al, 0x43
00659295  7507                 jne      0x65929e
00659297  c68572feffff01       mov      byte ptr [ebp - 0x18e], 1
0065929e  0fb63e               movzx    edi, byte ptr [esi]
006592a1  83cf20               or       edi, 0x20
006592a4  89bd1cfeffff         mov      dword ptr [ebp - 0x1e4], edi
006592aa  83ff6e               cmp      edi, 0x6e
006592ad  744a                 je       0x6592f9
006592af  83ff63               cmp      edi, 0x63
006592b2  7419                 je       0x6592cd
006592b4  83ff7b               cmp      edi, 0x7b
006592b7  7414                 je       0x6592cd
006592b9  ffb564feffff         push     dword ptr [ebp - 0x19c]
006592bf  8db574feffff         lea      esi, [ebp - 0x18c]
006592c5  e84ffcffff           call     0x658f19
006592ca  59                   pop      ecx
006592cb  eb11                 jmp      0x6592de
006592cd  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006592d3  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006592d9  e835ecffff           call     0x657f13
006592de  898578feffff         mov      dword ptr [ebp - 0x188], eax
006592e4  83f8ff               cmp      eax, -1
006592e7  0f84e70c0000         je       0x659fd4
006592ed  8b9d44feffff         mov      ebx, dword ptr [ebp - 0x1bc]
006592f3  8bb554feffff         mov      esi, dword ptr [ebp - 0x1ac]
006592f9  8b8d40feffff         mov      ecx, dword ptr [ebp - 0x1c0]
006592ff  85c9                 test     ecx, ecx
00659301  740d                 je       0x659310
00659303  83bd6cfeffff00       cmp      dword ptr [ebp - 0x194], 0
0065930a  0f842c0c0000         je       0x659f3c
00659310  80bd71feffff00       cmp      byte ptr [ebp - 0x18f], 0
00659317  7541                 jne      0x65935a
00659319  83ff63               cmp      edi, 0x63
0065931c  740a                 je       0x659328
0065931e  83ff73               cmp      edi, 0x73
00659321  7405                 je       0x659328
00659323  83ff7b               cmp      edi, 0x7b
00659326  7532                 jne      0x65935a
00659328  8b8518feffff         mov      eax, dword ptr [ebp - 0x1e8]
0065932e  8b18                 mov      ebx, dword ptr [eax]
00659330  83c004               add      eax, 4
00659333  898518feffff         mov      dword ptr [ebp - 0x1e8], eax
00659339  83c004               add      eax, 4
0065933c  898520feffff         mov      dword ptr [ebp - 0x1e0], eax
00659342  8b40fc               mov      eax, dword ptr [eax - 4]
00659345  899d44feffff         mov      dword ptr [ebp - 0x1bc], ebx
0065934b  898534feffff         mov      dword ptr [ebp - 0x1cc], eax
00659351  83f801               cmp      eax, 1
00659354  0f82fa0b0000         jb       0x659f54
0065935a  83ff6f               cmp      edi, 0x6f
0065935d  0f8f7f050000         jg       0x6598e2
00659363  0f8412080000         je       0x659b7b
00659369  83ff63               cmp      edi, 0x63
0065936c  0f8405040000         je       0x659777
00659372  83ff64               cmp      edi, 0x64
00659375  0f8400080000         je       0x659b7b
0065937b  0f8e8b050000         jle      0x65990c
00659381  83ff67               cmp      edi, 0x67
00659384  7e42                 jle      0x6593c8
00659386  83ff69               cmp      edi, 0x69
00659389  7421                 je       0x6593ac
0065938b  83ff6e               cmp      edi, 0x6e
0065938e  0f8578050000         jne      0x65990c
00659394  80bd71feffff00       cmp      byte ptr [ebp - 0x18f], 0
0065939b  8b8574feffff         mov      eax, dword ptr [ebp - 0x18c]
006593a1  0f84b0090000         je       0x659d57
006593a7  e9da0a0000           jmp      0x659e86
006593ac  6a64                 push     0x64
006593ae  5f                   pop      edi
006593af  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
006593b6  0f8550060000         jne      0x659a0c
006593bc  c68561feffff01       mov      byte ptr [ebp - 0x19f], 1
006593c3  e94d060000           jmp      0x659a15
006593c8  33db                 xor      ebx, ebx
006593ca  83bd78feffff2d       cmp      dword ptr [ebp - 0x188], 0x2d
006593d1  750c                 jne      0x6593df
006593d3  8b855cfeffff         mov      eax, dword ptr [ebp - 0x1a4]
006593d9  c6002d               mov      byte ptr [eax], 0x2d
006593dc  43                   inc      ebx
006593dd  eb09                 jmp      0x6593e8
006593df  83bd78feffff2b       cmp      dword ptr [ebp - 0x188], 0x2b
006593e6  751d                 jne      0x659405
006593e8  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006593ee  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006593f4  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006593fa  e814ebffff           call     0x657f13
006593ff  898578feffff         mov      dword ptr [ebp - 0x188], eax
00659405  83bd40feffff00       cmp      dword ptr [ebp - 0x1c0], 0
0065940c  7507                 jne      0x659415
0065940e  838d6cfeffffff       or       dword ptr [ebp - 0x194], 0xffffffff
00659415  0fb68578feffff       movzx    eax, byte ptr [ebp - 0x188]
0065941c  eb6b                 jmp      0x659489
0065941e  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
00659424  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
0065942a  85c0                 test     eax, eax
0065942c  7466                 je       0x659494
0065942e  8a8578feffff         mov      al, byte ptr [ebp - 0x188]
00659434  8b8d5cfeffff         mov      ecx, dword ptr [ebp - 0x1a4]
0065943a  ff8558feffff         inc      dword ptr [ebp - 0x1a8]
00659440  88040b               mov      byte ptr [ebx + ecx], al
00659443  8d8530feffff         lea      eax, [ebp - 0x1d0]
00659449  50                   push     eax
0065944a  8d857cfeffff         lea      eax, [ebp - 0x184]
00659450  50                   push     eax
00659451  43                   inc      ebx
00659452  53                   push     ebx
00659453  8dbd5cfeffff         lea      edi, [ebp - 0x1a4]
00659459  8db528feffff         lea      esi, [ebp - 0x1d8]
0065945f  e858eaffff           call     0x657ebc
00659464  83c40c               add      esp, 0xc
00659467  85c0                 test     eax, eax
00659469  0f84650b0000         je       0x659fd4
0065946f  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
00659475  ff8574feffff         inc      dword ptr [ebp - 0x18c]
0065947b  e893eaffff           call     0x657f13
00659480  898578feffff         mov      dword ptr [ebp - 0x188], eax
00659486  0fb6c0               movzx    eax, al
00659489  50                   push     eax
0065948a  e82289feff           call     0x641db1
0065948f  59                   pop      ecx
00659490  85c0                 test     eax, eax
00659492  758a                 jne      0x65941e
00659494  8b8500feffff         mov      eax, dword ptr [ebp - 0x200]
0065949a  8b80bc000000         mov      eax, dword ptr [eax + 0xbc]
006594a0  8b00                 mov      eax, dword ptr [eax]
006594a2  8a00                 mov      al, byte ptr [eax]
006594a4  888562feffff         mov      byte ptr [ebp - 0x19e], al
006594aa  3a8578feffff         cmp      al, byte ptr [ebp - 0x188]
006594b0  0f85e5000000         jne      0x65959b
006594b6  8b856cfeffff         mov      eax, dword ptr [ebp - 0x194]
006594bc  ff8d6cfeffff         dec      dword ptr [ebp - 0x194]
006594c2  85c0                 test     eax, eax
006594c4  0f84d1000000         je       0x65959b
006594ca  8b9564feffff         mov      edx, dword ptr [ebp - 0x19c]
006594d0  ff8574feffff         inc      dword ptr [ebp - 0x18c]
006594d6  e838eaffff           call     0x657f13
006594db  8b8d5cfeffff         mov      ecx, dword ptr [ebp - 0x1a4]
006594e1  898578feffff         mov      dword ptr [ebp - 0x188], eax
006594e7  8a8562feffff         mov      al, byte ptr [ebp - 0x19e]
006594ed  88040b               mov      byte ptr [ebx + ecx], al
006594f0  8d8530feffff         lea      eax, [ebp - 0x1d0]
006594f6  50                   push     eax
006594f7  8d857cfeffff         lea      eax, [ebp - 0x184]
006594fd  50                   push     eax
006594fe  43                   inc      ebx
006594ff  53                   push     ebx
00659500  8dbd5cfeffff         lea      edi, [ebp - 0x1a4]
00659506  8db528feffff         lea      esi, [ebp - 0x1d8]
0065950c  e8abe9ffff           call     0x657ebc
00659511  83c40c               add      esp, 0xc
00659514  85c0                 test     eax, eax
00659516  0f84b80a0000         je       0x659fd4
