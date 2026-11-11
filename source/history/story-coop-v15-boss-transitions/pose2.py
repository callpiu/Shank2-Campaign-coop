"""Correct direction: the boss packet references its hidden female victim."""
from build_pose import hash_name,PACKET_SIZE
BOSS=hash_name('boss_militia');FEMALE=hash_name('corina');POSE=hash_name('hit_mid1')

def routine(asm,code,diag=0x7ff000,native=0x7fcd80,lookup=0x513170):
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
        mov [ebp-4],eax
        lea edi,[ebp-0x4e0];mov esi,ebx;mov ecx,{PACKET_SIZE//4};cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        lea ebx,[ebp-0x4e0]
        mov dword ptr [ebx+0x70],-1
        push dword ptr [ebp+16];push ebx;push dword ptr [ebp+8];call {native};add esp,12
        mov [ebp-0x274],eax
        mov esi,[ebp-4];lea edi,[ebp-0x270];mov ecx,{PACKET_SIZE//4};cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        lea ebx,[ebp-0x270]
        mov dword ptr [ebx+0x70],-1
        mov dword ptr [ebx+0x90],{POSE}
        mov dword ptr [ebx+0x98],0x3dcccccd
        mov byte ptr [ebx+0x6c],0
        push dword ptr [ebp+16];push ebx;push dword ptr [ebp+8];call {native};add esp,12
        mov eax,[ebp-0x274]
        jmp done
        original:
        push dword ptr [ebp+16];push ebx;push dword ptr [ebp+8];call {native};add esp,12
        done:pop edi;pop esi;pop ebx;mov esp,ebp;pop ebp;ret''',code)
