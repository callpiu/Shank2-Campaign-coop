STRING Xbox360 Controller [%d] 0x75e798
REF 0x5bdce7
FUNCTION 0x5bce50
005bce50  55                   push     ebp
005bce51  8bec                 mov      ebp, esp
005bce53  83e4f8               and      esp, 0xfffffff8
005bce56  83ec58               sub      esp, 0x58
005bce59  a108957c00           mov      eax, dword ptr [0x7c9508]
005bce5e  33c4                 xor      eax, esp
005bce60  89442454             mov      dword ptr [esp + 0x54], eax
005bce64  56                   push     esi
005bce65  8bf1                 mov      esi, ecx
005bce67  837e0800             cmp      dword ptr [esi + 8], 0
005bce6b  57                   push     edi
005bce6c  8b7d0c               mov      edi, dword ptr [ebp + 0xc]
005bce6f  756a                 jne      0x5bcedb
005bce71  8b86f8010000         mov      eax, dword ptr [esi + 0x1f8]
005bce77  8b08                 mov      ecx, dword ptr [eax]
005bce79  8b5164               mov      edx, dword ptr [ecx + 0x64]
005bce7c  50                   push     eax
005bce7d  ffd2                 call     edx
005bce7f  6a50                 push     0x50
005bce81  8d44240c             lea      eax, [esp + 0xc]
005bce85  6a00                 push     0
005bce87  50                   push     eax
005bce88  e833720800           call     0x6440c0
005bce8d  8b86f8010000         mov      eax, dword ptr [esi + 0x1f8]
005bce93  8b08                 mov      ecx, dword ptr [eax]
005bce95  83c40c               add      esp, 0xc
005bce98  8d542408             lea      edx, [esp + 8]
005bce9c  52                   push     edx
005bce9d  6a50                 push     0x50
005bce9f  50                   push     eax
005bcea0  8b4124               mov      eax, dword ptr [ecx + 0x24]
005bcea3  ffd0                 call     eax
005bcea5  85c0                 test     eax, eax
005bcea7  7c2b                 jl       0x5bced4
005bcea9  8d4c2408             lea      ecx, [esp + 8]
005bcead  51                   push     ecx
005bceae  8bce                 mov      ecx, esi
005bceb0  e89b000000           call     0x5bcf50
005bceb5  8d542408             lea      edx, [esp + 8]
005bceb9  52                   push     edx
005bceba  57                   push     edi
005bcebb  56                   push     esi
005bcebc  e83f070000           call     0x5bd600
005bcec1  5f                   pop      edi
005bcec2  5e                   pop      esi
005bcec3  8b4c2454             mov      ecx, dword ptr [esp + 0x54]
005bcec7  33cc                 xor      ecx, esp
005bcec9  e8d7410800           call     0x6410a5
005bcece  8be5                 mov      esp, ebp
005bced0  5d                   pop      ebp
005bced1  c20800               ret      8
005bced4  c7460801000000       mov      dword ptr [esi + 8], 1
005bcedb  8b4c245c             mov      ecx, dword ptr [esp + 0x5c]
005bcedf  5f                   pop      edi
005bcee0  5e                   pop      esi
005bcee1  33cc                 xor      ecx, esp
005bcee3  e8bd410800           call     0x6410a5
005bcee8  8be5                 mov      esp, ebp
005bceea  5d                   pop      ebp
005bceeb  c20800               ret      8
005bceee  cc                   int3     
005bceef  cc                   int3     
005bcef0  8d8836f7ffff         lea      ecx, [eax - 0x8ca]
005bcef6  81f90b7b0000         cmp      ecx, 0x7b0b
005bcefc  774c                 ja       0x5bcf4a
005bcefe  3d5e1a0000           cmp      eax, 0x1a5e
005bcf03  7306                 jae      0x5bcf0b
005bcf05  b809000000           mov      eax, 9
005bcf0a  c3                   ret      
005bcf0b  3df22b0000           cmp      eax, 0x2bf2
005bcf10  7306                 jae      0x5bcf18
005bcf12  b808000000           mov      eax, 8
005bcf17  c3                   ret      
005bcf18  3d863d0000           cmp      eax, 0x3d86
005bcf1d  7306                 jae      0x5bcf25
005bcf1f  b80a000000           mov      eax, 0xa
005bcf24  c3                   ret      
005bcf25  3d1a4f0000           cmp      eax, 0x4f1a
005bcf2a  7306                 jae      0x5bcf32
005bcf2c  b802000000           mov      eax, 2
005bcf31  c3                   ret      
005bcf32  3dae600000           cmp      eax, 0x60ae
005bcf37  7306                 jae      0x5bcf3f
005bcf39  b806000000           mov      eax, 6
005bcf3e  c3                   ret      
005bcf3f  3d42720000           cmp      eax, 0x7242
005bcf44  1bc0                 sbb      eax, eax
005bcf46  83c005               add      eax, 5
005bcf49  c3                   ret      
005bcf4a  b801000000           mov      eax, 1
005bcf4f  c3                   ret      
005bcf50  6aff                 push     -1
005bcf52  68c6576e00           push     0x6e57c6
005bcf57  64a100000000         mov      eax, dword ptr fs:[0]
005bcf5d  50                   push     eax
005bcf5e  83ec40               sub      esp, 0x40
005bcf61  53                   push     ebx
005bcf62  55                   push     ebp
005bcf63  56                   push     esi
005bcf64  57                   push     edi
005bcf65  a108957c00           mov      eax, dword ptr [0x7c9508]
005bcf6a  33c4                 xor      eax, esp
005bcf6c  50                   push     eax
005bcf6d  8d442454             lea      eax, [esp + 0x54]
005bcf71  64a300000000         mov      dword ptr fs:[0], eax
005bcf77  8bf1                 mov      esi, ecx
005bcf79  8b442464             mov      eax, dword ptr [esp + 0x64]
005bcf7d  33ed                 xor      ebp, ebp
005bcf7f  83c020               add      eax, 0x20
005bcf82  8d8e1c020000         lea      ecx, [esi + 0x21c]
005bcf88  896c2418             mov      dword ptr [esp + 0x18], ebp
005bcf8c  896c2430             mov      dword ptr [esp + 0x30], ebp
005bcf90  896c241c             mov      dword ptr [esp + 0x1c], ebp
005bcf94  896c2424             mov      dword ptr [esp + 0x24], ebp
005bcf98  8944242c             mov      dword ptr [esp + 0x2c], eax
005bcf9c  894c2428             mov      dword ptr [esp + 0x28], ecx
005bcfa0  c744243404000000     mov      dword ptr [esp + 0x34], 4
005bcfa8  8b542428             mov      edx, dword ptr [esp + 0x28]
005bcfac  8b02                 mov      eax, dword ptr [edx]
005bcfae  8b4c242c             mov      ecx, dword ptr [esp + 0x2c]
005bcfb2  8b11                 mov      edx, dword ptr [ecx]
005bcfb4  3bc2                 cmp      eax, edx
005bcfb6  0f8409020000         je       0x5bd1c5
005bcfbc  8b4c2424             mov      ecx, dword ptr [esp + 0x24]
005bcfc0  894c241c             mov      dword ptr [esp + 0x1c], ecx
005bcfc4  b9ffff0000           mov      ecx, 0xffff
005bcfc9  bf02000000           mov      edi, 2
005bcfce  897c2430             mov      dword ptr [esp + 0x30], edi
005bcfd2  663bc1               cmp      ax, cx
005bcfd5  7409                 je       0x5bcfe0
005bcfd7  e814ffffff           call     0x5bcef0
005bcfdc  8bd8                 mov      ebx, eax
005bcfde  eb02                 jmp      0x5bcfe2
005bcfe0  33db                 xor      ebx, ebx
005bcfe2  b8ffff0000           mov      eax, 0xffff
005bcfe7  663bd0               cmp      dx, ax
005bcfea  7409                 je       0x5bcff5
005bcfec  8bc2                 mov      eax, edx
005bcfee  e8fdfeffff           call     0x5bcef0
005bcff3  eb02                 jmp      0x5bcff7
005bcff5  33c0                 xor      eax, eax
005bcff7  32c3                 xor      al, bl
005bcff9  88442417             mov      byte ptr [esp + 0x17], al
005bcffd  a801                 test     al, 1
005bcfff  7470                 je       0x5bd071
005bd001  8b4e04               mov      ecx, dword ptr [esi + 4]
005bd004  d9ee                 fldz     
005bd006  f6c301               test     bl, 1
005bd009  d95c2444             fstp     dword ptr [esp + 0x44]
005bd00d  8bd5                 mov      edx, ebp
005bd00f  0f95c2               setne    dl
005bd012  894c243c             mov      dword ptr [esp + 0x3c], ecx
005bd016  8d8e70010000         lea      ecx, [esi + 0x170]
005bd01c  896c2448             mov      dword ptr [esp + 0x48], ebp
005bd020  896c244c             mov      dword ptr [esp + 0x4c], ebp
005bd024  896c2450             mov      dword ptr [esp + 0x50], ebp
005bd028  c74424400d000000     mov      dword ptr [esp + 0x40], 0xd
005bd030  42                   inc      edx
005bd031  89542438             mov      dword ptr [esp + 0x38], edx
005bd035  e8e654e8ff           call     0x442520
005bd03a  84c0                 test     al, al
005bd03c  741f                 je       0x5bd05d
005bd03e  8b460c               mov      eax, dword ptr [esi + 0xc]
005bd041  80783c00             cmp      byte ptr [eax + 0x3c], 0
005bd045  7516                 jne      0x5bd05d
005bd047  396838               cmp      dword ptr [eax + 0x38], ebp
005bd04a  7411                 je       0x5bd05d
005bd04c  8b4038               mov      eax, dword ptr [eax + 0x38]
005bd04f  8b10                 mov      edx, dword ptr [eax]
005bd051  8b5204               mov      edx, dword ptr [edx + 4]
005bd054  8d4c2438             lea      ecx, [esp + 0x38]
005bd058  51                   push     ecx
005bd059  8bc8                 mov      ecx, eax
005bd05b  ffd2                 call     edx
005bd05d  8b442438             mov      eax, dword ptr [esp + 0x38]
005bd061  89442418             mov      dword ptr [esp + 0x18], eax
005bd065  8a442417             mov      al, byte ptr [esp + 0x17]
005bd069  c744242001000000     mov      dword ptr [esp + 0x20], 1
005bd071  a802                 test     al, 2
005bd073  746c                 je       0x5bd0e1
005bd075  8b4e04               mov      ecx, dword ptr [esi + 4]
005bd078  d9ee                 fldz     
005bd07a  f6c302               test     bl, 2
005bd07d  d95c2444             fstp     dword ptr [esp + 0x44]
005bd081  8bd5                 mov      edx, ebp
005bd083  0f95c2               setne    dl
005bd086  894c243c             mov      dword ptr [esp + 0x3c], ecx
005bd08a  8d8e70010000         lea      ecx, [esi + 0x170]
005bd090  896c2448             mov      dword ptr [esp + 0x48], ebp
005bd094  896c244c             mov      dword ptr [esp + 0x4c], ebp
005bd098  896c2450             mov      dword ptr [esp + 0x50], ebp
005bd09c  c74424400f000000     mov      dword ptr [esp + 0x40], 0xf
005bd0a4  42                   inc      edx
005bd0a5  89542438             mov      dword ptr [esp + 0x38], edx
005bd0a9  e87254e8ff           call     0x442520
005bd0ae  84c0                 test     al, al
005bd0b0  741f                 je       0x5bd0d1
005bd0b2  8b460c               mov      eax, dword ptr [esi + 0xc]
005bd0b5  80783c00             cmp      byte ptr [eax + 0x3c], 0
005bd0b9  7516                 jne      0x5bd0d1
005bd0bb  396838               cmp      dword ptr [eax + 0x38], ebp
005bd0be  7411                 je       0x5bd0d1
005bd0c0  8b4038               mov      eax, dword ptr [eax + 0x38]
005bd0c3  8b10                 mov      edx, dword ptr [eax]
005bd0c5  8b5204               mov      edx, dword ptr [edx + 4]
005bd0c8  8d4c2438             lea      ecx, [esp + 0x38]
005bd0cc  51                   push     ecx
005bd0cd  8bc8                 mov      ecx, eax
005bd0cf  ffd2                 call     edx
005bd0d1  8b442438             mov      eax, dword ptr [esp + 0x38]
005bd0d5  89442418             mov      dword ptr [esp + 0x18], eax
005bd0d9  8a442417             mov      al, byte ptr [esp + 0x17]
005bd0dd  897c2420             mov      dword ptr [esp + 0x20], edi
005bd0e1  a804                 test     al, 4
005bd0e3  7470                 je       0x5bd155
005bd0e5  8b4e04               mov      ecx, dword ptr [esi + 4]
005bd0e8  d9ee                 fldz     
005bd0ea  f6c304               test     bl, 4
005bd0ed  d95c2444             fstp     dword ptr [esp + 0x44]
005bd0f1  8bd5                 mov      edx, ebp
005bd0f3  0f95c2               setne    dl
005bd0f6  894c243c             mov      dword ptr [esp + 0x3c], ecx
005bd0fa  8d8e70010000         lea      ecx, [esi + 0x170]
005bd100  896c2448             mov      dword ptr [esp + 0x48], ebp
005bd104  896c244c             mov      dword ptr [esp + 0x4c], ebp
005bd108  896c2450             mov      dword ptr [esp + 0x50], ebp
005bd10c  c744244010000000     mov      dword ptr [esp + 0x40], 0x10
005bd114  42                   inc      edx
005bd115  89542438             mov      dword ptr [esp + 0x38], edx
005bd119  e80254e8ff           call     0x442520
005bd11e  84c0                 test     al, al
005bd120  741f                 je       0x5bd141
005bd122  8b460c               mov      eax, dword ptr [esi + 0xc]
005bd125  80783c00             cmp      byte ptr [eax + 0x3c], 0
005bd129  7516                 jne      0x5bd141
005bd12b  396838               cmp      dword ptr [eax + 0x38], ebp
005bd12e  7411                 je       0x5bd141
005bd130  8b4038               mov      eax, dword ptr [eax + 0x38]
005bd133  8b10                 mov      edx, dword ptr [eax]
005bd135  8b5204               mov      edx, dword ptr [edx + 4]
005bd138  8d4c2438             lea      ecx, [esp + 0x38]
005bd13c  51                   push     ecx
005bd13d  8bc8                 mov      ecx, eax
005bd13f  ffd2                 call     edx
005bd141  8b442438             mov      eax, dword ptr [esp + 0x38]
005bd145  89442418             mov      dword ptr [esp + 0x18], eax
005bd149  8a442417             mov      al, byte ptr [esp + 0x17]
005bd14d  c744242004000000     mov      dword ptr [esp + 0x20], 4
005bd155  a808                 test     al, 8
005bd157  746c                 je       0x5bd1c5
005bd159  8b4e04               mov      ecx, dword ptr [esi + 4]
005bd15c  d9ee                 fldz     
005bd15e  f6c308               test     bl, 8
005bd161  d95c2444             fstp     dword ptr [esp + 0x44]
005bd165  8bd5                 mov      edx, ebp
005bd167  0f95c2               setne    dl
005bd16a  894c243c             mov      dword ptr [esp + 0x3c], ecx
005bd16e  8d8e70010000         lea      ecx, [esi + 0x170]
005bd174  896c2448             mov      dword ptr [esp + 0x48], ebp
005bd178  896c244c             mov      dword ptr [esp + 0x4c], ebp
005bd17c  896c2450             mov      dword ptr [esp + 0x50], ebp
005bd180  c74424400e000000     mov      dword ptr [esp + 0x40], 0xe
005bd188  42                   inc      edx
005bd189  89542438             mov      dword ptr [esp + 0x38], edx
005bd18d  e88e53e8ff           call     0x442520
005bd192  84c0                 test     al, al
005bd194  741f                 je       0x5bd1b5
005bd196  8b460c               mov      eax, dword ptr [esi + 0xc]
005bd199  80783c00             cmp      byte ptr [eax + 0x3c], 0
005bd19d  7516                 jne      0x5bd1b5
005bd19f  396838               cmp      dword ptr [eax + 0x38], ebp
005bd1a2  7411                 je       0x5bd1b5
005bd1a4  8b4038               mov      eax, dword ptr [eax + 0x38]
005bd1a7  8b10                 mov      edx, dword ptr [eax]
005bd1a9  8b5204               mov      edx, dword ptr [edx + 4]
005bd1ac  8d4c2438             lea      ecx, [esp + 0x38]
005bd1b0  51                   push     ecx
005bd1b1  8bc8                 mov      ecx, eax
005bd1b3  ffd2                 call     edx
005bd1b5  8b442438             mov      eax, dword ptr [esp + 0x38]
005bd1b9  c744242008000000     mov      dword ptr [esp + 0x20], 8
005bd1c1  89442418             mov      dword ptr [esp + 0x18], eax
005bd1c5  b801000000           mov      eax, 1
005bd1ca  01442424             add      dword ptr [esp + 0x24], eax
005bd1ce  b904000000           mov      ecx, 4
005bd1d3  014c2428             add      dword ptr [esp + 0x28], ecx
005bd1d7  014c242c             add      dword ptr [esp + 0x2c], ecx
005bd1db  29442434             sub      dword ptr [esp + 0x34], eax
005bd1df  0f85c3fdffff         jne      0x5bcfa8
005bd1e5  32db                 xor      bl, bl
005bd1e7  80fb0c               cmp      bl, 0xc
005bd1ea  0f838d000000         jae      0x5bd27d
005bd1f0  8b4c2464             mov      ecx, dword ptr [esp + 0x64]
005bd1f4  0fb6fb               movzx    edi, bl
005bd1f7  8a84372c020000       mov      al, byte ptr [edi + esi + 0x22c]
005bd1fe  3a440f30             cmp      al, byte ptr [edi + ecx + 0x30]
005bd202  746e                 je       0x5bd272
005bd204  8b5604               mov      edx, dword ptr [esi + 4]
005bd207  d9ee                 fldz     
005bd209  8954243c             mov      dword ptr [esp + 0x3c], edx
005bd20d  d95c2444             fstp     dword ptr [esp + 0x44]
005bd211  a880                 test     al, 0x80
005bd213  8bd5                 mov      edx, ebp
005bd215  0f95c2               setne    dl
005bd218  8d4f01               lea      ecx, [edi + 1]
005bd21b  894c2440             mov      dword ptr [esp + 0x40], ecx
005bd21f  8d8e70010000         lea      ecx, [esi + 0x170]
005bd225  896c2448             mov      dword ptr [esp + 0x48], ebp
005bd229  896c244c             mov      dword ptr [esp + 0x4c], ebp
005bd22d  896c2450             mov      dword ptr [esp + 0x50], ebp
005bd231  42                   inc      edx
005bd232  89542438             mov      dword ptr [esp + 0x38], edx
005bd236  e8e552e8ff           call     0x442520
005bd23b  84c0                 test     al, al
005bd23d  741f                 je       0x5bd25e
005bd23f  8b460c               mov      eax, dword ptr [esi + 0xc]
005bd242  80783c00             cmp      byte ptr [eax + 0x3c], 0
005bd246  7516                 jne      0x5bd25e
005bd248  396838               cmp      dword ptr [eax + 0x38], ebp
005bd24b  7411                 je       0x5bd25e
005bd24d  8b4038               mov      eax, dword ptr [eax + 0x38]
005bd250  8b10                 mov      edx, dword ptr [eax]
005bd252  8b5204               mov      edx, dword ptr [edx + 4]
005bd255  8d4c2438             lea      ecx, [esp + 0x38]
005bd259  51                   push     ecx
005bd25a  8bc8                 mov      ecx, eax
005bd25c  ffd2                 call     edx
005bd25e  8b442438             mov      eax, dword ptr [esp + 0x38]
005bd262  c744243001000000     mov      dword ptr [esp + 0x30], 1
005bd26a  897c241c             mov      dword ptr [esp + 0x1c], edi
005bd26e  89442418             mov      dword ptr [esp + 0x18], eax
005bd272  fec3                 inc      bl
005bd274  80fb20               cmp      bl, 0x20
005bd277  0f826affffff         jb       0x5bd1e7
005bd27d  8d9e70010000         lea      ebx, [esi + 0x170]
005bd283  8bcb                 mov      ecx, ebx
005bd285  e89652e8ff           call     0x442520
005bd28a  84c0                 test     al, al
005bd28c  0f850e010000         jne      0x5bd3a0
005bd292  8b7c2464             mov      edi, dword ptr [esp + 0x64]
005bd296  8d96fc010000         lea      edx, [esi + 0x1fc]
005bd29c  b950000000           mov      ecx, 0x50
005bd2a1  8bc2                 mov      eax, edx
005bd2a3  2bfa                 sub      edi, edx
005bd2a5  8b2c38               mov      ebp, dword ptr [eax + edi]
005bd2a8  3b28                 cmp      ebp, dword ptr [eax]
005bd2aa  7510                 jne      0x5bd2bc
005bd2ac  83e904               sub      ecx, 4
005bd2af  83c004               add      eax, 4
005bd2b2  83f904               cmp      ecx, 4
005bd2b5  73ee                 jae      0x5bd2a5
005bd2b7  e9e4000000           jmp      0x5bd3a0
005bd2bc  8b442430             mov      eax, dword ptr [esp + 0x30]
005bd2c0  83f801               cmp      eax, 1
005bd2c3  7557                 jne      0x5bd31c
005bd2c5  837c241802           cmp      dword ptr [esp + 0x18], 2
005bd2ca  0f85d0000000         jne      0x5bd3a0
005bd2d0  6a10                 push     0x10
005bd2d2  e889de0e00           call     0x6ab160
005bd2d7  83c404               add      esp, 4
005bd2da  89442434             mov      dword ptr [esp + 0x34], eax
005bd2de  33c9                 xor      ecx, ecx
005bd2e0  894c245c             mov      dword ptr [esp + 0x5c], ecx
005bd2e4  3bc1                 cmp      eax, ecx
005bd2e6  0f8486000000         je       0x5bd372
005bd2ec  8b54241c             mov      edx, dword ptr [esp + 0x1c]
005bd2f0  c700f8dc7500         mov      dword ptr [eax], 0x75dcf8
005bd2f6  c7400401000000       mov      dword ptr [eax + 4], 1
005bd2fd  895008               mov      dword ptr [eax + 8], edx
005bd300  c644245c01           mov      byte ptr [esp + 0x5c], 1
005bd305  c70010dd7500         mov      dword ptr [eax], 0x75dd10
005bd30b  89480c               mov      dword ptr [eax + 0xc], ecx
005bd30e  884c245c             mov      byte ptr [esp + 0x5c], cl
005bd312  c744245cffffffff     mov      dword ptr [esp + 0x5c], 0xffffffff
005bd31a  eb6b                 jmp      0x5bd387
005bd31c  bf02000000           mov      edi, 2
005bd321  3bc7                 cmp      eax, edi
005bd323  7559                 jne      0x5bd37e
005bd325  397c2418             cmp      dword ptr [esp + 0x18], edi
005bd329  7575                 jne      0x5bd3a0
005bd32b  6a10                 push     0x10
005bd32d  e82ede0e00           call     0x6ab160
005bd332  83c404               add      esp, 4
005bd335  89442434             mov      dword ptr [esp + 0x34], eax
005bd339  897c245c             mov      dword ptr [esp + 0x5c], edi
005bd33d  85c0                 test     eax, eax
005bd33f  7431                 je       0x5bd372
005bd341  8b4c241c             mov      ecx, dword ptr [esp + 0x1c]
005bd345  c700f8dc7500         mov      dword ptr [eax], 0x75dcf8
005bd34b  897804               mov      dword ptr [eax + 4], edi
005bd34e  894808               mov      dword ptr [eax + 8], ecx
005bd351  c644245c03           mov      byte ptr [esp + 0x5c], 3
005bd356  8b542420             mov      edx, dword ptr [esp + 0x20]
005bd35a  c70028dd7500         mov      dword ptr [eax], 0x75dd28
005bd360  89500c               mov      dword ptr [eax + 0xc], edx
005bd363  c644245c02           mov      byte ptr [esp + 0x5c], 2
005bd368  c744245cffffffff     mov      dword ptr [esp + 0x5c], 0xffffffff
005bd370  eb15                 jmp      0x5bd387
005bd372  33c0                 xor      eax, eax
005bd374  c744245cffffffff     mov      dword ptr [esp + 0x5c], 0xffffffff
005bd37c  eb09                 jmp      0x5bd387
005bd37e  8b4c2464             mov      ecx, dword ptr [esp + 0x64]
005bd382  e849000000           call     0x5bd3d0
005bd387  85c0                 test     eax, eax
005bd389  7415                 je       0x5bd3a0
005bd38b  8b0b                 mov      ecx, dword ptr [ebx]
005bd38d  50                   push     eax
005bd38e  8b4304               mov      eax, dword ptr [ebx + 4]
005bd391  ffd0                 call     eax
005bd393  c7430400000000       mov      dword ptr [ebx + 4], 0
005bd39a  c70300000000         mov      dword ptr [ebx], 0
005bd3a0  8dbefc010000         lea      edi, [esi + 0x1fc]
005bd3a6  8b742464             mov      esi, dword ptr [esp + 0x64]
005bd3aa  b914000000           mov      ecx, 0x14
005bd3af  f3a5                 rep movsd dword ptr es:[edi], dword ptr [esi]
005bd3b1  8b4c2454             mov      ecx, dword ptr [esp + 0x54]
005bd3b5  64890d00000000       mov      dword ptr fs:[0], ecx
005bd3bc  59                   pop      ecx
005bd3bd  5f                   pop      edi
005bd3be  5e                   pop      esi
005bd3bf  5d                   pop      ebp
005bd3c0  5b                   pop      ebx
005bd3c1  83c44c               add      esp, 0x4c
005bd3c4  c20400               ret      4
005bd3c7  cc                   int3     
005bd3c8  cc                   int3     
005bd3c9  cc                   int3     
005bd3ca  cc                   int3     
005bd3cb  cc                   int3     
005bd3cc  cc                   int3     
005bd3cd  cc                   int3     
005bd3ce  cc                   int3     
005bd3cf  cc                   int3     
005bd3d0  57                   push     edi
005bd3d1  8b3a                 mov      edi, dword ptr [edx]
005bd3d3  33c0                 xor      eax, eax
005bd3d5  3b39                 cmp      edi, dword ptr [ecx]
005bd3d7  740a                 je       0x5bd3e3
005bd3d9  33ff                 xor      edi, edi
005bd3db  56                   push     esi
005bd3dc  e8eff4ffff           call     0x5bc8d0
005bd3e1  5f                   pop      edi
005bd3e2  c3                   ret      
005bd3e3  8b7a04               mov      edi, dword ptr [edx + 4]
005bd3e6  3b7904               cmp      edi, dword ptr [ecx + 4]
005bd3e9  740d                 je       0x5bd3f8
005bd3eb  bf01000000           mov      edi, 1
005bd3f0  56                   push     esi
005bd3f1  e8daf4ffff           call     0x5bc8d0
005bd3f6  5f                   pop      edi
005bd3f7  c3                   ret      
005bd3f8  8b7a08               mov      edi, dword ptr [edx + 8]
005bd3fb  3b7908               cmp      edi, dword ptr [ecx + 8]
005bd3fe  740d                 je       0x5bd40d
005bd400  bf02000000           mov      edi, 2
005bd405  56                   push     esi
005bd406  e8c5f4ffff           call     0x5bc8d0
005bd40b  5f                   pop      edi
005bd40c  c3                   ret      
005bd40d  8b7a0c               mov      edi, dword ptr [edx + 0xc]
005bd410  3b790c               cmp      edi, dword ptr [ecx + 0xc]
005bd413  740d                 je       0x5bd422
005bd415  bf03000000           mov      edi, 3
005bd41a  56                   push     esi
005bd41b  e8b0f4ffff           call     0x5bc8d0
005bd420  5f                   pop      edi
005bd421  c3                   ret      
005bd422  8b7a10               mov      edi, dword ptr [edx + 0x10]
005bd425  3b7910               cmp      edi, dword ptr [ecx + 0x10]
005bd428  740d                 je       0x5bd437
STRING Failed to register for WM_INPUT 0x75e028
REF 0x5b7495
FUNCTION 0x5b7400
005b7400  55                   push     ebp
005b7401  8bec                 mov      ebp, esp
005b7403  83e4f8               and      esp, 0xfffffff8
005b7406  83ec0c               sub      esp, 0xc
005b7409  56                   push     esi
005b740a  8b353ce27200         mov      esi, dword ptr [0x72e23c]
005b7410  6a00                 push     0
005b7412  6804b07c00           push     0x7cb004
005b7417  6a08                 push     8
005b7419  6a3a                 push     0x3a
005b741b  ffd6                 call     esi
005b741d  6a00                 push     0
005b741f  680cb07c00           push     0x7cb00c
005b7424  6a08                 push     8
005b7426  6a34                 push     0x34
005b7428  ffd6                 call     esi
005b742a  6a00                 push     0
005b742c  6814b07c00           push     0x7cb014
005b7431  6a18                 push     0x18
005b7433  6a32                 push     0x32
005b7435  ffd6                 call     esi
005b7437  6a00                 push     0
005b7439  6804b07c00           push     0x7cb004
005b743e  6a08                 push     8
005b7440  6a3b                 push     0x3b
005b7442  ffd6                 call     esi
005b7444  6a00                 push     0
005b7446  680cb07c00           push     0x7cb00c
005b744b  6a08                 push     8
005b744d  6a35                 push     0x35
005b744f  ffd6                 call     esi
005b7451  6a00                 push     0
005b7453  6814b07c00           push     0x7cb014
005b7458  6a18                 push     0x18
005b745a  6a33                 push     0x33
005b745c  ffd6                 call     esi
005b745e  b801000000           mov      eax, 1
005b7463  6a0c                 push     0xc
005b7465  50                   push     eax
005b7466  8d54240c             lea      edx, [esp + 0xc]
005b746a  b906000000           mov      ecx, 6
005b746f  52                   push     edx
005b7470  6689442410           mov      word ptr [esp + 0x10], ax
005b7475  66894c2412           mov      word ptr [esp + 0x12], cx
005b747a  c744241400020000     mov      dword ptr [esp + 0x14], 0x200
005b7482  c744241800000000     mov      dword ptr [esp + 0x18], 0
005b748a  ff1538e27200         call     dword ptr [0x72e238]
005b7490  85c0                 test     eax, eax
005b7492  751a                 jne      0x5b74ae
005b7494  6828e07500           push     0x75e028
005b7499  6a02                 push     2
005b749b  6847414d45           push     0x454d4147
005b74a0  e80b4ae5ff           call     0x40beb0
005b74a5  50                   push     eax
005b74a6  e84563ecff           call     0x47d7f0
005b74ab  83c410               add      esp, 0x10
005b74ae  5e                   pop      esi
005b74af  8be5                 mov      esp, ebp
005b74b1  5d                   pop      ebp
005b74b2  c3                   ret      
005b74b3  cc                   int3     
005b74b4  cc                   int3     
005b74b5  cc                   int3     
005b74b6  cc                   int3     
005b74b7  cc                   int3     
005b74b8  cc                   int3     
005b74b9  cc                   int3     
005b74ba  cc                   int3     
005b74bb  cc                   int3     
005b74bc  cc                   int3     
005b74bd  cc                   int3     
005b74be  cc                   int3     
005b74bf  cc                   int3     
005b74c0  6a00                 push     0
005b74c2  e8b9f4ffff           call     0x5b6980
005b74c7  59                   pop      ecx
005b74c8  c3                   ret      
005b74c9  cc                   int3     
005b74ca  cc                   int3     
005b74cb  cc                   int3     
005b74cc  cc                   int3     
005b74cd  cc                   int3     
005b74ce  cc                   int3     
005b74cf  cc                   int3     
005b74d0  55                   push     ebp
005b74d1  8bec                 mov      ebp, esp
005b74d3  83e4f8               and      esp, 0xfffffff8
005b74d6  6aff                 push     -1
005b74d8  6880337000           push     0x703380
005b74dd  64a100000000         mov      eax, dword ptr fs:[0]
005b74e3  50                   push     eax
005b74e4  83ec5c               sub      esp, 0x5c
005b74e7  53                   push     ebx
005b74e8  55                   push     ebp
005b74e9  56                   push     esi
005b74ea  57                   push     edi
005b74eb  a108957c00           mov      eax, dword ptr [0x7c9508]
005b74f0  33c4                 xor      eax, esp
005b74f2  50                   push     eax
005b74f3  8d442470             lea      eax, [esp + 0x70]
005b74f7  64a300000000         mov      dword ptr fs:[0], eax
005b74fd  8bd9                 mov      ebx, ecx
005b74ff  8bf3                 mov      esi, ebx
005b7501  e83a0b0000           call     0x5b8040
005b7506  53                   push     ebx
005b7507  e824030000           call     0x5b7830
005b750c  8b35a0e17200         mov      esi, dword ptr [0x72e1a0]
005b7512  8d44242c             lea      eax, [esp + 0x2c]
005b7516  50                   push     eax
005b7517  ffd6                 call     esi
005b7519  803d79817d0000       cmp      byte ptr [0x7d8179], 0
005b7520  c644243400           mov      byte ptr [esp + 0x34], 0
005b7525  7512                 jne      0x5b7539
005b7527  68e07f7d00           push     0x7d7fe0
005b752c  ff159ce17200         call     dword ptr [0x72e19c]
005b7532  c60579817d0001       mov      byte ptr [0x7d8179], 1
005b7539  c744247800000000     mov      dword ptr [esp + 0x78], 0
005b7541  d94358               fld      dword ptr [ebx + 0x58]
005b7544  d9e8                 fld1     
005b7546  8d4c242c             lea      ecx, [esp + 0x2c]
005b754a  def1                 fdivrp   st(1)
005b754c  51                   push     ecx
005b754d  dd5c2428             fstp     qword ptr [esp + 0x28]
005b7551  ffd6                 call     esi
005b7553  df2de07f7d00         fild     qword ptr [0x7d7fe0]
005b7559  dd442424             fld      qword ptr [esp + 0x24]
005b755d  8b7c242c             mov      edi, dword ptr [esp + 0x2c]
005b7561  8b6c2430             mov      ebp, dword ptr [esp + 0x30]
005b7565  c644243400           mov      byte ptr [esp + 0x34], 0
005b756a  dcc9                 fmul     st(1), st(0)
005b756c  897c243c             mov      dword ptr [esp + 0x3c], edi
005b7570  d9c9                 fxch     st(1)
005b7572  896c2440             mov      dword ptr [esp + 0x40], ebp
005b7576  e89b060900           call     0x647c16
005b757b  dd5c2444             fstp     qword ptr [esp + 0x44]
005b757f  03c7                 add      eax, edi
005b7581  13d5                 adc      edx, ebp
005b7583  89542440             mov      dword ptr [esp + 0x40], edx
005b7587  8d54244c             lea      edx, [esp + 0x4c]
005b758b  52                   push     edx
005b758c  89442440             mov      dword ptr [esp + 0x40], eax
005b7590  c644243801           mov      byte ptr [esp + 0x38], 1
005b7595  ffd6                 call     esi
005b7597  803d79817d0000       cmp      byte ptr [0x7d8179], 0
005b759e  c644245400           mov      byte ptr [esp + 0x54], 0
005b75a3  7512                 jne      0x5b75b7
005b75a5  68e07f7d00           push     0x7d7fe0
005b75aa  ff159ce17200         call     dword ptr [0x72e19c]
005b75b0  c60579817d0001       mov      byte ptr [0x7d8179], 1
005b75b7  c644247801           mov      byte ptr [esp + 0x78], 1
005b75bc  807b0400             cmp      byte ptr [ebx + 4], 0
005b75c0  0f84a3000000         je       0x5b7669
005b75c6  8b2d34e27200         mov      ebp, dword ptr [0x72e234]
005b75cc  8d642400             lea      esp, [esp]
005b75d0  ffd5                 call     ebp
005b75d2  3905d47e7d00         cmp      dword ptr [0x7d7ed4], eax
005b75d8  7507                 jne      0x5b75e1
005b75da  8bfb                 mov      edi, ebx
005b75dc  e84f010000           call     0x5b7730
005b75e1  6888d77500           push     0x75d788
005b75e6  e85589ecff           call     0x47ff40
005b75eb  83c404               add      esp, 4
005b75ee  84c0                 test     al, al
005b75f0  7519                 jne      0x5b760b
005b75f2  d94358               fld      dword ptr [ebx + 0x58]
005b75f5  51                   push     ecx
005b75f6  d9e8                 fld1     
005b75f8  def1                 fdivrp   st(1)
005b75fa  d95c241c             fstp     dword ptr [esp + 0x1c]
005b75fe  d944241c             fld      dword ptr [esp + 0x1c]
005b7602  d91c24               fstp     dword ptr [esp]
005b7605  53                   push     ebx
005b7606  e8c5010000           call     0x5b77d0
005b760b  8d44241c             lea      eax, [esp + 0x1c]
005b760f  50                   push     eax
005b7610  ffd6                 call     esi
005b7612  8b4c241c             mov      ecx, dword ptr [esp + 0x1c]
005b7616  2b4c244c             sub      ecx, dword ptr [esp + 0x4c]
005b761a  8b542420             mov      edx, dword ptr [esp + 0x20]
005b761e  1b542450             sbb      edx, dword ptr [esp + 0x50]
005b7622  894c2424             mov      dword ptr [esp + 0x24], ecx
005b7626  89542428             mov      dword ptr [esp + 0x28], edx
005b762a  df6c2424             fild     qword ptr [esp + 0x24]
005b762e  df2de07f7d00         fild     qword ptr [0x7d7fe0]
005b7634  def9                 fdivp    st(1)
005b7636  dc1dd0297600         fcomp    qword ptr [0x7629d0]
005b763c  dfe0                 fnstsw   ax
005b763e  f6c441               test     ah, 0x41
005b7641  7512                 jne      0x5b7655
005b7643  53                   push     ebx
005b7644  e8e7010000           call     0x5b7830
005b7649  8d44244c             lea      eax, [esp + 0x4c]
005b764d  50                   push     eax
005b764e  ffd6                 call     esi
005b7650  c644245400           mov      byte ptr [esp + 0x54], 0
005b7655  8d4c242c             lea      ecx, [esp + 0x2c]
005b7659  51                   push     ecx
005b765a  e89153ffff           call     0x5ac9f0
005b765f  807b0400             cmp      byte ptr [ebx + 4], 0
005b7663  0f8567ffffff         jne      0x5b75d0
005b7669  8dab88070000         lea      ebp, [ebx + 0x788]
005b766f  c744241804000000     mov      dword ptr [esp + 0x18], 4
005b7677  8b4500               mov      eax, dword ptr [ebp]
005b767a  8b4dfc               mov      ecx, dword ptr [ebp - 4]
005b767d  3bc8                 cmp      ecx, eax
005b767f  7432                 je       0x5b76b3
005b7681  c644241c00           mov      byte ptr [esp + 0x1c], 0
005b7686  8b54241c             mov      edx, dword ptr [esp + 0x1c]
005b768a  52                   push     edx
005b768b  8b542420             mov      edx, dword ptr [esp + 0x20]
005b768f  52                   push     edx
005b7690  8b542424             mov      edx, dword ptr [esp + 0x24]
005b7694  52                   push     edx
005b7695  51                   push     ecx
005b7696  50                   push     eax
005b7697  50                   push     eax
005b7698  e8f3deffff           call     0x5b5590
005b769d  8b7d00               mov      edi, dword ptr [ebp]
005b76a0  8bf0                 mov      esi, eax
005b76a2  8b442434             mov      eax, dword ptr [esp + 0x34]
005b76a6  50                   push     eax
005b76a7  56                   push     esi
005b76a8  e843dfffff           call     0x5b55f0
005b76ad  83c420               add      esp, 0x20
005b76b0  897500               mov      dword ptr [ebp], esi
005b76b3  8d7df8               lea      edi, [ebp - 8]
005b76b6  e805d7ffff           call     0x5b4dc0
005b76bb  83c520               add      ebp, 0x20
005b76be  836c241801           sub      dword ptr [esp + 0x18], 1
005b76c3  75b2                 jne      0x5b7677
005b76c5  81c308080000         add      ebx, 0x808
005b76cb  be20000000           mov      esi, 0x20
005b76d0  8b0b                 mov      ecx, dword ptr [ebx]
005b76d2  85c9                 test     ecx, ecx
005b76d4  7408                 je       0x5b76de
005b76d6  8b11                 mov      edx, dword ptr [ecx]
005b76d8  8b02                 mov      eax, dword ptr [edx]
005b76da  6a01                 push     1
005b76dc  ffd0                 call     eax
005b76de  c70300000000         mov      dword ptr [ebx], 0
005b76e4  83c304               add      ebx, 4
005b76e7  83ee01               sub      esi, 1
005b76ea  75e4                 jne      0x5b76d0
005b76ec  56                   push     esi
