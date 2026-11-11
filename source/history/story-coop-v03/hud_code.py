import struct

def build_hud(asm,codebase,diag):
 delta=0x13f0-0x638
 ctor=asm(f'''
push esi
mov esi, ecx
call 0x4430e0
lea ecx, [esi+{delta:#x}]
call 0x4430e0
mov eax, esi
pop esi
ret
''',codebase+0x4000)
 bind=asm(f'''
push ebp
mov ebp, esp
push esi
mov esi, ecx
push dword ptr [ebp+16]
push dword ptr [ebp+12]
push dword ptr [ebp+8]
call 0x672c00
push {diag+0x420:#x}
push 1
push dword ptr [ebp+8]
lea ecx, [esi+{delta:#x}]
mov dword ptr [{diag+204:#x}], ecx
call 0x672c00
mov eax, dword ptr [ebp+8]
mov dword ptr [{diag+200:#x}], eax
pop esi
pop ebp
ret 12
''',codebase+0x4100)
 destroy=asm(f'''
push esi
mov esi, ecx
lea ecx, [esi+{delta:#x}]
call 0x4431a0
mov dword ptr [{diag+200:#x}], 0
mov dword ptr [{diag+204:#x}], 0
mov ecx, esi
call 0x4431a0
pop esi
ret
''',codebase+0x4200)
 update=asm(f'''
push ebp
mov ebp, esp
push esi
push edi
mov esi, ecx
push dword ptr [ebp+12]
push dword ptr [ebp+8]
call 0x6966a0
mov ecx, esi
call 0x6936e0
test eax, eax
jz done
mov ecx, eax
mov edx, dword ptr [eax]
push 1
call dword ptr [edx+0x2c]
test eax, eax
jz done
mov edi, eax
push dword ptr [ebp+12]
push edi
push dword ptr [ebp+8]
lea ecx, [esi+0x13f0]
call 0x673870
inc dword ptr [{diag+208:#x}]
done:
pop edi
pop esi
pop ebp
ret 8
''',codebase+0x4300)
 visibility=asm(f'''
push ebp
mov ebp, esp
push esi
mov esi, ecx
push dword ptr [ebp+8]
call 0x66e820
push dword ptr [ebp+8]
lea ecx, [esi+{delta:#x}]
call 0x66e820
pop esi
pop ebp
ret 4
''',codebase+0x4400)
 patches=[]
 def call(addr,target,replacement):
  patches.append((addr,b'\xe8'+struct.pack('<i',target-addr-5),b'\xe8'+struct.pack('<i',replacement-addr-5)))
 call(0x696902,0x4430e0,codebase+0x4000)
 call(0x696a19,0x672c00,codebase+0x4100)
 call(0x695d99,0x4431a0,codebase+0x4200)
 call(0x6956fd,0x66e820,codebase+0x4400)
 patches.append((0x751e08,struct.pack('<I',0x6966a0),struct.pack('<I',codebase+0x4300)))
 patches.append((0x6adcc9,struct.pack('<I',0x13f0),struct.pack('<I',0x1e84)))
 patches.append((0x6968d9,struct.pack('<I',0x751c48),struct.pack('<I',diag+0x400)))
 return {0x4000:ctor,0x4100:bind,0x4200:destroy,0x4300:update,0x4400:visibility},patches
