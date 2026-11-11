"""Allow native partner-context actions in the active two-player campaign."""
import struct

def build_revive(asm,codebase,diag):
    # SelectContext selector 15 first checks IsPlayer, then IsSurvival. Its
    # native continuation looks up the other registered player. Story mode
    # used to fail this guard, skipping the revive/ui_pickup StopFX actions.
    blob=asm(f'''
cmp dword ptr [{diag+4:#x}], 5
jne original
cmp ecx, dword ptr [{diag+36:#x}]
jne original
mov eax, dword ptr [esi+8]
cmp eax, dword ptr [{diag+12:#x}]
je cooperative
cmp eax, dword ptr [{diag+16:#x}]
jne original
cooperative:
inc dword ptr [{diag+252:#x}]
mov eax, 1
ret
original:
mov eax, dword ptr [edx+0x34]
call eax
ret
''',codebase+0x4b00)
    address=0x53b355
    patch=(address,bytes.fromhex('8b4234ffd0'),b'\xe8'+struct.pack('<i',codebase+0x4b00-address-5))
    # Multiplayer spawnPlayerIndicators starts an indefinite blue_glow.peg
    # identification tint. Campaign players did not get it at initial spawn;
    # it first appeared after onrevive. Keep low-health/dead blue_glow_loop,
    # but suppress this ordinary living tint for the campaign partner.
    tint=asm(f'''
cmp dword ptr [{diag+4:#x}], 5
jne original
cmp dword ptr [ecx+8], 0xbf79ee36
jne original
cmp dword ptr [ecx+0x50], 2
jne original
cmp byte ptr [ecx+0x58], 0
jne original
mov eax, dword ptr [esp+4]
test eax, eax
jz original
mov eax, dword ptr [eax+8]
cmp eax, dword ptr [{diag+16:#x}]
jne original
inc dword ptr [{diag+256:#x}]
ret 4
original:
sub esp, 8
push ebx
push ebp
jmp 0x53f1b5
''',codebase+0x4c00)
    address=0x53f1b0
    tint_patch=(address,bytes.fromhex('83ec085355'),b'\xe9'+struct.pack('<i',codebase+0x4c00-address-5))
    return {0x4b00:blob,0x4c00:tint},[patch,tint_patch]
