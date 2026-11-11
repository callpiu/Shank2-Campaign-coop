STRING gamemode params file %s has no type set 0x7506ac
REF 0x6c30e5
FUNCTION 0x6c2f00
006c2f00  55                   push     ebp
006c2f01  8bec                 mov      ebp, esp
006c2f03  6aff                 push     -1
006c2f05  68ffb96c00           push     0x6cb9ff
006c2f0a  64a100000000         mov      eax, dword ptr fs:[0]
006c2f10  50                   push     eax
006c2f11  81eca8000000         sub      esp, 0xa8
006c2f17  a108957c00           mov      eax, dword ptr [0x7c9508]
006c2f1c  33c5                 xor      eax, ebp
006c2f1e  8945dc               mov      dword ptr [ebp - 0x24], eax
006c2f21  56                   push     esi
006c2f22  50                   push     eax
006c2f23  8d45f4               lea      eax, [ebp - 0xc]
006c2f26  64a300000000         mov      dword ptr fs:[0], eax
006c2f2c  898d70ffffff         mov      dword ptr [ebp - 0x90], ecx
006c2f32  83ec1c               sub      esp, 0x1c
006c2f35  8bcc                 mov      ecx, esp
006c2f37  8965a0               mov      dword ptr [ebp - 0x60], esp
006c2f3a  6830067500           push     0x750630
006c2f3f  e8fc02d4ff           call     0x403240
006c2f44  89856cffffff         mov      dword ptr [ebp - 0x94], eax
006c2f4a  8b856cffffff         mov      eax, dword ptr [ebp - 0x94]
006c2f50  898568ffffff         mov      dword ptr [ebp - 0x98], eax
006c2f56  c745fc00000000       mov      dword ptr [ebp - 4], 0
006c2f5d  83ec1c               sub      esp, 0x1c
006c2f60  8bcc                 mov      ecx, esp
006c2f62  89659c               mov      dword ptr [ebp - 0x64], esp
006c2f65  8b5508               mov      edx, dword ptr [ebp + 8]
006c2f68  52                   push     edx
006c2f69  e8d202d4ff           call     0x403240
006c2f6e  898564ffffff         mov      dword ptr [ebp - 0x9c], eax
006c2f74  8b8564ffffff         mov      eax, dword ptr [ebp - 0x9c]
006c2f7a  898560ffffff         mov      dword ptr [ebp - 0xa0], eax
006c2f80  c645fc01             mov      byte ptr [ebp - 4], 1
006c2f84  83ec1c               sub      esp, 0x1c
006c2f87  8bcc                 mov      ecx, esp
006c2f89  896598               mov      dword ptr [ebp - 0x68], esp
006c2f8c  6834067500           push     0x750634
006c2f91  e8aa02d4ff           call     0x403240
006c2f96  89855cffffff         mov      dword ptr [ebp - 0xa4], eax
006c2f9c  8b8d5cffffff         mov      ecx, dword ptr [ebp - 0xa4]
006c2fa2  898d58ffffff         mov      dword ptr [ebp - 0xa8], ecx
006c2fa8  c645fc02             mov      byte ptr [ebp - 4], 2
006c2fac  8d55a4               lea      edx, [ebp - 0x5c]
006c2faf  52                   push     edx
006c2fb0  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006c2fb7  e82450d5ff           call     0x417fe0
006c2fbc  83c458               add      esp, 0x58
006c2fbf  898554ffffff         mov      dword ptr [ebp - 0xac], eax
006c2fc5  c745fc03000000       mov      dword ptr [ebp - 4], 3
006c2fcc  8d4de4               lea      ecx, [ebp - 0x1c]
006c2fcf  e83c06f6ff           call     0x623610
006c2fd4  c645fc04             mov      byte ptr [ebp - 4], 4
006c2fd8  8b750c               mov      esi, dword ptr [ebp + 0xc]
006c2fdb  e890bfdbff           call     0x47ef70
006c2fe0  0fb6c0               movzx    eax, al
006c2fe3  85c0                 test     eax, eax
006c2fe5  756d                 jne      0x6c3054
006c2fe7  8b0dc46e7d00         mov      ecx, dword ptr [0x7d6ec4]
006c2fed  51                   push     ecx
006c2fee  8d4da4               lea      ecx, [ebp - 0x5c]
006c2ff1  e8ca03d4ff           call     0x4033c0
006c2ff6  50                   push     eax
006c2ff7  8d4de4               lea      ecx, [ebp - 0x1c]
006c2ffa  e8a112f6ff           call     0x6242a0
006c2fff  0fb6d0               movzx    edx, al
006c3002  85d2                 test     edx, edx
006c3004  754e                 jne      0x6c3054
006c3006  8d4da4               lea      ecx, [ebp - 0x5c]
006c3009  e8b203d4ff           call     0x4033c0
006c300e  50                   push     eax
006c300f  6844067500           push     0x750644
006c3014  6a02                 push     2
006c3016  a120f47400           mov      eax, dword ptr [0x74f420]
006c301b  50                   push     eax
006c301c  e88f8ed4ff           call     0x40beb0
006c3021  50                   push     eax
006c3022  e8c9a7dbff           call     0x47d7f0
006c3027  83c414               add      esp, 0x14
006c302a  c7459400000000       mov      dword ptr [ebp - 0x6c], 0
006c3031  c645fc03             mov      byte ptr [ebp - 4], 3
006c3035  8d4de4               lea      ecx, [ebp - 0x1c]
006c3038  e81306f6ff           call     0x623650
006c303d  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006c3044  8d4da4               lea      ecx, [ebp - 0x5c]
006c3047  e81404d4ff           call     0x403460
006c304c  8b4594               mov      eax, dword ptr [ebp - 0x6c]
006c304f  e92d020000           jmp      0x6c3281
006c3054  6870067500           push     0x750670
006c3059  8d4de4               lea      ecx, [ebp - 0x1c]
006c305c  e82f0df6ff           call     0x623d90
006c3061  0fb6c8               movzx    ecx, al
006c3064  85c9                 test     ecx, ecx
006c3066  754f                 jne      0x6c30b7
006c3068  8d4da4               lea      ecx, [ebp - 0x5c]
006c306b  e85003d4ff           call     0x4033c0
006c3070  50                   push     eax
006c3071  6878067500           push     0x750678
006c3076  6a02                 push     2
006c3078  8b1520f47400         mov      edx, dword ptr [0x74f420]
006c307e  52                   push     edx
006c307f  e82c8ed4ff           call     0x40beb0
006c3084  50                   push     eax
006c3085  e866a7dbff           call     0x47d7f0
006c308a  83c414               add      esp, 0x14
006c308d  c7459000000000       mov      dword ptr [ebp - 0x70], 0
006c3094  c645fc03             mov      byte ptr [ebp - 4], 3
006c3098  8d4de4               lea      ecx, [ebp - 0x1c]
006c309b  e8b005f6ff           call     0x623650
006c30a0  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006c30a7  8d4da4               lea      ecx, [ebp - 0x5c]
006c30aa  e8b103d4ff           call     0x403460
006c30af  8b4590               mov      eax, dword ptr [ebp - 0x70]
006c30b2  e9ca010000           jmp      0x6c3281
006c30b7  8d4dc0               lea      ecx, [ebp - 0x40]
006c30ba  e8c17fd4ff           call     0x40b080
006c30bf  c645fc05             mov      byte ptr [ebp - 4], 5
006c30c3  8d45c0               lea      eax, [ebp - 0x40]
006c30c6  50                   push     eax
006c30c7  68a4067500           push     0x7506a4
006c30cc  8d4de4               lea      ecx, [ebp - 0x1c]
006c30cf  e80c12f6ff           call     0x6242e0
006c30d4  0fb6c8               movzx    ecx, al
006c30d7  85c9                 test     ecx, ecx
006c30d9  755b                 jne      0x6c3136
006c30db  8d4da4               lea      ecx, [ebp - 0x5c]
006c30de  e8dd02d4ff           call     0x4033c0
006c30e3  50                   push     eax
006c30e4  68ac067500           push     0x7506ac
006c30e9  6a02                 push     2
006c30eb  8b1520f47400         mov      edx, dword ptr [0x74f420]
006c30f1  52                   push     edx
006c30f2  e8b98dd4ff           call     0x40beb0
006c30f7  50                   push     eax
006c30f8  e8f3a6dbff           call     0x47d7f0
006c30fd  83c414               add      esp, 0x14
006c3100  c7458c00000000       mov      dword ptr [ebp - 0x74], 0
006c3107  c645fc04             mov      byte ptr [ebp - 4], 4
006c310b  8d4dc0               lea      ecx, [ebp - 0x40]
006c310e  e84d03d4ff           call     0x403460
006c3113  c645fc03             mov      byte ptr [ebp - 4], 3
006c3117  8d4de4               lea      ecx, [ebp - 0x1c]
006c311a  e83105f6ff           call     0x623650
006c311f  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006c3126  8d4da4               lea      ecx, [ebp - 0x5c]
006c3129  e83203d4ff           call     0x403460
006c312e  8b458c               mov      eax, dword ptr [ebp - 0x74]
006c3131  e94b010000           jmp      0x6c3281
006c3136  68b0000000           push     0xb0
006c313b  e82080feff           call     0x6ab160
006c3140  83c404               add      esp, 4
006c3143  894584               mov      dword ptr [ebp - 0x7c], eax
006c3146  c645fc06             mov      byte ptr [ebp - 4], 6
006c314a  837d8400             cmp      dword ptr [ebp - 0x7c], 0
006c314e  7410                 je       0x6c3160
006c3150  8b4d84               mov      ecx, dword ptr [ebp - 0x7c]
006c3153  e8f8040000           call     0x6c3650
006c3158  898550ffffff         mov      dword ptr [ebp - 0xb0], eax
006c315e  eb0a                 jmp      0x6c316a
006c3160  c78550ffffff00000000 mov      dword ptr [ebp - 0xb0], 0
006c316a  8b8550ffffff         mov      eax, dword ptr [ebp - 0xb0]
006c3170  894588               mov      dword ptr [ebp - 0x78], eax
006c3173  c645fc05             mov      byte ptr [ebp - 4], 5
006c3177  8b4d88               mov      ecx, dword ptr [ebp - 0x78]
006c317a  894de0               mov      dword ptr [ebp - 0x20], ecx
006c317d  8d55a4               lea      edx, [ebp - 0x5c]
006c3180  52                   push     edx
006c3181  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006c3184  83c120               add      ecx, 0x20
006c3187  e8a47ed4ff           call     0x40b030
006c318c  8b750c               mov      esi, dword ptr [ebp + 0xc]
006c318f  e8dcbddbff           call     0x47ef70
006c3194  0fb6c0               movzx    eax, al
006c3197  85c0                 test     eax, eax
006c3199  0f85ac000000         jne      0x6c324b
006c319f  8d4de4               lea      ecx, [ebp - 0x1c]
006c31a2  51                   push     ecx
006c31a3  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006c31a6  e855020000           call     0x6c3400
006c31ab  0fb6d0               movzx    edx, al
006c31ae  85d2                 test     edx, edx
006c31b0  0f8595000000         jne      0x6c324b
006c31b6  8d4da4               lea      ecx, [ebp - 0x5c]
006c31b9  e80202d4ff           call     0x4033c0
006c31be  50                   push     eax
006c31bf  68d4067500           push     0x7506d4
006c31c4  6a02                 push     2
006c31c6  a120f47400           mov      eax, dword ptr [0x74f420]
006c31cb  50                   push     eax
006c31cc  e8df8cd4ff           call     0x40beb0
006c31d1  50                   push     eax
006c31d2  e819a6dbff           call     0x47d7f0
006c31d7  83c414               add      esp, 0x14
006c31da  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006c31dd  898d7cffffff         mov      dword ptr [ebp - 0x84], ecx
006c31e3  8b957cffffff         mov      edx, dword ptr [ebp - 0x84]
006c31e9  895580               mov      dword ptr [ebp - 0x80], edx
006c31ec  837d8000             cmp      dword ptr [ebp - 0x80], 0
006c31f0  7416                 je       0x6c3208
006c31f2  6a01                 push     1
006c31f4  8b4580               mov      eax, dword ptr [ebp - 0x80]
006c31f7  8b10                 mov      edx, dword ptr [eax]
006c31f9  8b4d80               mov      ecx, dword ptr [ebp - 0x80]
006c31fc  8b02                 mov      eax, dword ptr [edx]
006c31fe  ffd0                 call     eax
006c3200  89854cffffff         mov      dword ptr [ebp - 0xb4], eax
006c3206  eb0a                 jmp      0x6c3212
006c3208  c7854cffffff00000000 mov      dword ptr [ebp - 0xb4], 0
006c3212  c78578ffffff00000000 mov      dword ptr [ebp - 0x88], 0
006c321c  c645fc04             mov      byte ptr [ebp - 4], 4
006c3220  8d4dc0               lea      ecx, [ebp - 0x40]
006c3223  e83802d4ff           call     0x403460
006c3228  c645fc03             mov      byte ptr [ebp - 4], 3
006c322c  8d4de4               lea      ecx, [ebp - 0x1c]
006c322f  e81c04f6ff           call     0x623650
006c3234  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006c323b  8d4da4               lea      ecx, [ebp - 0x5c]
006c323e  e81d02d4ff           call     0x403460
006c3243  8b8578ffffff         mov      eax, dword ptr [ebp - 0x88]
006c3249  eb36                 jmp      0x6c3281
006c324b  8b4de0               mov      ecx, dword ptr [ebp - 0x20]
006c324e  898d74ffffff         mov      dword ptr [ebp - 0x8c], ecx
006c3254  c645fc04             mov      byte ptr [ebp - 4], 4
006c3258  8d4dc0               lea      ecx, [ebp - 0x40]
006c325b  e80002d4ff           call     0x403460
006c3260  c645fc03             mov      byte ptr [ebp - 4], 3
006c3264  8d4de4               lea      ecx, [ebp - 0x1c]
006c3267  e8e403f6ff           call     0x623650
006c326c  c745fcffffffff       mov      dword ptr [ebp - 4], 0xffffffff
006c3273  8d4da4               lea      ecx, [ebp - 0x5c]
006c3276  e8e501d4ff           call     0x403460
006c327b  8b8574ffffff         mov      eax, dword ptr [ebp - 0x8c]
006c3281  8b4df4               mov      ecx, dword ptr [ebp - 0xc]
006c3284  64890d00000000       mov      dword ptr fs:[0], ecx
006c328b  59                   pop      ecx
006c328c  5e                   pop      esi
006c328d  8b4ddc               mov      ecx, dword ptr [ebp - 0x24]
006c3290  33cd                 xor      ecx, ebp
006c3292  e80edef7ff           call     0x6410a5
006c3297  8be5                 mov      esp, ebp
006c3299  5d                   pop      ebp
006c329a  c20800               ret      8
006c329d  cc                   int3     
006c329e  cc                   int3     
006c329f  cc                   int3     
006c32a0  55                   push     ebp
006c32a1  8bec                 mov      ebp, esp
006c32a3  6aff                 push     -1
006c32a5  6806896c00           push     0x6c8906
006c32aa  64a100000000         mov      eax, dword ptr fs:[0]
006c32b0  50                   push     eax
006c32b1  83ec20               sub      esp, 0x20
006c32b4  56                   push     esi
006c32b5  a108957c00           mov      eax, dword ptr [0x7c9508]
006c32ba  33c5                 xor      eax, ebp
006c32bc  50                   push     eax
006c32bd  8d45f4               lea      eax, [ebp - 0xc]
006c32c0  64a300000000         mov      dword ptr fs:[0], eax
006c32c6  894dd8               mov      dword ptr [ebp - 0x28], ecx
006c32c9  8b45d8               mov      eax, dword ptr [ebp - 0x28]
006c32cc  c700e4057500         mov      dword ptr [eax], 0x7505e4
006c32d2  c745fc05000000       mov      dword ptr [ebp - 4], 5
006c32d9  8d4df0               lea      ecx, [ebp - 0x10]
006c32dc  51                   push     ecx
006c32dd  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
006c32e0  81c198000000         add      ecx, 0x98
006c32e6  e85568d5ff           call     0x419b40
006c32eb  eb08                 jmp      0x6c32f5
006c32ed  8d4df0               lea      ecx, [ebp - 0x10]
006c32f0  e8bbc0d5ff           call     0x41f3b0
006c32f5  8d55ec               lea      edx, [ebp - 0x14]
006c32f8  52                   push     edx
006c32f9  8b4dd8               mov      ecx, dword ptr [ebp - 0x28]
006c32fc  81c198000000         add      ecx, 0x98
006c3302  e88957d7ff           call     0x438a90
006c3307  50                   push     eax
006c3308  8d4df0               lea      ecx, [ebp - 0x10]
006c330b  e8c01cd5ff           call     0x414fd0
006c3310  0fb6c0               movzx    eax, al
006c3313  85c0                 test     eax, eax
006c3315  7425                 je       0x6c333c
006c3317  8d4df0               lea      ecx, [ebp - 0x10]
006c331a  e881cbdaff           call     0x46fea0
006c331f  51                   push     ecx
006c3320  8bcc                 mov      ecx, esp
006c3322  8965e8               mov      dword ptr [ebp - 0x18], esp
006c3325  50                   push     eax
006c3326  e81501d4ff           call     0x403440
006c332b  e870d5d4ff           call     0x4108a0
006c3330  83c004               add      eax, 4
006c3333  8bc8                 mov      ecx, eax
006c3335  e8e6d5d4ff           call     0x410920
006c333a  ebb1                 jmp      0x6c32ed
