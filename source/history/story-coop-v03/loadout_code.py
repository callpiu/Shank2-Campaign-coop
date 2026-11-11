import struct
def hash_name(s):
 v=0
 for c in s.lower().encode('ascii'):v=(v*0x1003f+c)&0xffffffff
 return v

def defaults():
 out=bytearray(128)
 for i,(family,skin,melee,ranged) in enumerate([('shank','shank','machete','throwingknives'),('corina','corina','sword','revolver')]):
  o=i*64;struct.pack_into('<I',out,o,1);s=family.encode()+b'\0';out[o+4:o+4+len(s)]=s
  struct.pack_into('<5I',out,o+20,*map(hash_name,[skin,melee,ranged,'weapon_grenade']),3)
 return bytes(out)

def build_loadouts(asm,codebase,diag,p1=1,p2=2):
 wrapper=asm(f'''
push ebx
push esi
push edi
mov ebx, ecx
lea edi, [ebx+8]
mov esi, {diag+0x800:#x}
call {codebase+0x4600:#x}
lea edi, [ebx+0x78]
mov esi, {diag+0x840:#x}
call {codebase+0x4600:#x}
pop edi
pop esi
pop ebx
ret
''',codebase+0x4500)
 one=asm('''
cmp dword ptr [esi], 1
jne done
lea eax, [esi+4]
push eax
lea ecx, [edi+0x20]
call 0x4048f0
mov eax, dword ptr [esi+20]
mov dword ptr [edi+0x3c], eax
mov eax, dword ptr [esi+24]
mov dword ptr [edi+0x40], eax
mov eax, dword ptr [esi+28]
mov dword ptr [edi+0x44], eax
mov eax, dword ptr [esi+32]
mov dword ptr [edi+0x48], eax
mov eax, dword ptr [esi+36]
mov dword ptr [edi+0x58], eax
done:
ret
''',codebase+0x4600)
 # Resource loading reads its own copy of GameSimStartParams before campaign
 # initialization. Populate both descriptors there, so a second archetype and
 # skin reach the existing 434710/69a820 asset-loading path.
 loader=asm(f'''
push ebp
mov ebp, esp
push ebx
push esi
push edi
mov esi, ecx
push dword ptr [ebp+8]
call 0x434c00
mov ebx, esi
cmp dword ptr [ebx+0x164], 1
jne done
mov ecx, ebx
call 0x404960
test eax, eax
jz done
mov edi, eax
mov dword ptr [edi+0x60], {p1}
mov dword ptr [edi+0x64], {p1}
push {p2}
push {p2}
lea eax, [edi+0x3c]
push eax
lea ecx, [edi+0x20]
call 0x4033c0
push eax
lea ecx, [edi+4]
call 0x4033c0
push eax
mov ecx, ebx
call 0x6aa7b0
mov ecx, ebx
call {codebase+0x4500:#x}
inc dword ptr [{diag+212:#x}]
mov dword ptr [{diag+216:#x}], ebx
done:
mov eax, esi
pop edi
pop esi
pop ebx
pop ebp
ret 4
''',codebase+0x4700)
 patch=(0x4346a0,b'\xe8'+struct.pack('<i',0x434c00-0x4346a0-5),b'\xe8'+struct.pack('<i',codebase+0x4700-0x4346a0-5))
 return {0x4500:wrapper,0x4600:one,0x4700:loader},[patch]
