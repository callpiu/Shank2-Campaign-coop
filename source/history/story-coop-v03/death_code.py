"""Scope animation-graph multiplayer semantics to the co-op campaign partner."""
import struct
def build_death(asm,codebase,diag):
 blob=asm(f'''
cmp dword ptr [{diag+4:#x}], 5
jne original
cmp ecx, dword ptr [{diag+36:#x}]
jne original
cmp ebx, dword ptr [{diag+16:#x}]
jne original
inc dword ptr [{diag+248:#x}]
mov eax, 1
ret
original:
mov eax, dword ptr [edx+0x34]
call eax
ret
''',codebase+0x4e00)
 patch=(0x4d09df,bytes.fromhex('8b4234ffd0'),b'\xe8'+struct.pack('<i',codebase+0x4e00-0x4d09df-5))
 return {0x4e00:blob},[patch]
