"""Native down/revive graphs for both players; lose only when both are down."""
import struct
def build_death(asm,codebase,diag):
 blob=asm(f'''
cmp dword ptr [{diag+4:#x}], 5
jne original
cmp ecx, dword ptr [{diag+36:#x}]
jne original
cmp ebx, dword ptr [{diag+12:#x}]
je cooperative
cmp ebx, dword ptr [{diag+16:#x}]
jne original
cooperative:
inc dword ptr [{diag+248:#x}]
mov eax, 1
ret
original:
mov eax, dword ptr [edx+0x34]
call eax
ret
''',codebase+0x4e00)
 patch=(0x4d09df,bytes.fromhex('8b4234ffd0'),b'\xe8'+struct.pack('<i',codebase+0x4e00-0x4d09df-5))
 defeat=asm(f'''
call 0x4d2460
test al, al
jz done
cmp dword ptr [{diag+4:#x}], 5
jne done
cmp esi, dword ptr [{diag+12:#x}]
jne done
mov ecx, dword ptr [ebp-0x14]
mov ecx, dword ptr [ecx+8]
cmp ecx, dword ptr [{diag+36:#x}]
jne done
inc dword ptr [{diag+260:#x}]
push esi
mov eax, dword ptr [ecx]
push 1
call dword ptr [eax+0x2c]
test eax, eax
jz missing
mov esi, eax
call 0x4d2460
pop esi
test al, al
jnz both_down
inc dword ptr [{diag+264:#x}]
ret
both_down:
inc dword ptr [{diag+268:#x}]
ret
missing:
pop esi
mov al, 1
done:
ret
''',codebase+0x4d00)
 address=0x6a8736
 old=b'\xe8'+struct.pack('<i',0x4d2460-address-5)
 both_patch=(address,old,b'\xe8'+struct.pack('<i',codebase+0x4d00-address-5))
 return {0x4e00:blob,0x4d00:defeat},[patch,both_patch]
