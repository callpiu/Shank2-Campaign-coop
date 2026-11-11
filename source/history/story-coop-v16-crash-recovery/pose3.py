"""Render-only female grapple adaptation, preserving deferred-packet lifetimes.

511c15 enqueues the packet pointer; 4a0195 renders it later, after this hook
returns. A stack clone MUST NOT escape into that queue. Redirect only those
new references to the unchanged, snapshot-owned source before returning.
The later boss draw re-enters this hook; the hidden victim entry is a no-op.
"""
import sys
import math
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'story-coop-v15-boss-transitions'))
from pose2 import BOSS, FEMALE, POSE, PACKET_SIZE


def routine(asm, code, diag=0x7ff000, native=0x7fcf80, lookup=0x513170, metrics=None, anchor=None):
    qualified = f'inc dword ptr [{metrics}]' if metrics else ''
    retained = f'inc dword ptr [{metrics+4}]' if metrics else ''
    align = ''
    if anchor is not None:
        assert len(anchor)==2 and all(math.isfinite(x) for x in anchor)
        px,py=struct.unpack('<2I',struct.pack('<2f',*anchor))
        # The copied 2x3 world transform starts at 3c: a,b,tx,c,d,ty.
        # Map the selected pose's pelvis to the original grapple anchor.
        # 54 is the separate ground/shadow transform and stays untouched.
        align=f'''mov eax,{px};movd xmm2,eax;mov eax,{py};movd xmm3,eax
            movss xmm0,[ebx+0x3c];mulss xmm0,xmm2
            movss xmm1,[ebx+0x40];mulss xmm1,xmm3;addss xmm0,xmm1
            movss xmm1,[ebx+0x44];subss xmm1,xmm0;movss [ebx+0x44],xmm1
            movss xmm0,[ebx+0x48];mulss xmm0,xmm2
            movss xmm1,[ebx+0x4c];mulss xmm1,xmm3;addss xmm0,xmm1
            movss xmm1,[ebx+0x50];subss xmm1,xmm0;movss [ebx+0x50],xmm1'''
    return asm(f'''push ebp;mov ebp,esp;sub esp,0x4e0
        push ebx;push esi;push edi
        mov ebx,[ebp+12]
        cmp dword ptr [{diag+4}],5
        jne original
        test ebx,ebx
        jz original
        cmp dword ptr [ebx],0x759294
        jne original
        cmp dword ptr [ebx+0x7c],{BOSS}
        jne original
        mov eax,[ebx+0x70]
        cmp eax,-1
        je original
        mov ecx,[ebp+8]
        test ecx,ecx
        jz original
        cmp dword ptr [ecx],0
        je original
        mov edx,[ebp+16]
        test edx,edx
        jz original
        cmp dword ptr [edx+0x200],62
        ja original
        push dword ptr [ecx]
        call {lookup}
        test eax,eax
        jz original
        cmp dword ptr [eax],0x759294
        jne original
        cmp dword ptr [eax+0x7c],{FEMALE}
        jne original
        cmp byte ptr [eax+0x6c],0
        je original
        {qualified}
        mov [ebp-4],eax
        lea edi,[ebp-0x4e0];mov esi,ebx;mov ecx,{PACKET_SIZE//4};cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        lea ebx,[ebp-0x4e0]
        mov dword ptr [ebx+0x70],-1
        push dword ptr [ebp+16];push ebx;push dword ptr [ebp+8];call {native};add esp,12
        mov [ebp-0x274],eax
        mov edi,ebx
        mov eax,[ebp+12]
        call retain_source
        mov esi,[ebp-4];lea edi,[ebp-0x270];mov ecx,{PACKET_SIZE//4};cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        lea ebx,[ebp-0x270]
        mov dword ptr [ebx+0x70],-1
        mov dword ptr [ebx+0x90],{POSE}
        mov dword ptr [ebx+0x98],0x3dcccccd
        mov byte ptr [ebx+0x6c],0
        {align}
        push dword ptr [ebp+16];push ebx;push dword ptr [ebp+8];call {native};add esp,12
        mov edi,ebx
        mov eax,[ebp-4]
        call retain_source
        mov eax,[ebp-0x274]
        jmp done
        original:
        push dword ptr [ebp+16];push ebx;push dword ptr [ebp+8];call {native};add esp,12
        done:pop edi;pop esi;pop ebx;mov esp,ebp;pop ebp;ret
        retain_source:
        mov ecx,[ebp+16]
        mov edx,[ecx+0x200]
        cmp edx,64
        ja retained
        test edx,edx
        jz retained
        scan:
        cmp [ecx],edi
        jne next_entry
        mov [ecx],eax
        {retained}
        next_entry:add ecx,8;dec edx;jnz scan
        retained:ret''', code)
