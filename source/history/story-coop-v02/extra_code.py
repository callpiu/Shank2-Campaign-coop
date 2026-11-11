"""Authored x86 glue for campaign tethering and two keyboard-backed gamepads."""
import struct

def build_player_count(asm,codebase,diag):
    # cGameScreen::ReadControls (693730) broadcasts aggregate input when this
    # count is 1, and fetches each descriptor's input profile when it is 2.
    return asm(f'''
cmp dword ptr [{diag+4:#x}], 5
jne original
cmp ecx, dword ptr [{diag+36:#x}]
jne original
mov eax, dword ptr [ecx+0x150]
cmp eax, dword ptr [{diag+28:#x}]
jne original
cmp dword ptr [eax+0x164], 1
jne original
mov eax, 2
ret
original:
jmp 0x6a9560
''',codebase+0x2800)

def build_follow(asm,codebase,diag):
    return asm(f'''
push ebp
mov ebp, esp
push esi
push edi
push ebx
sub esp, 4
mov esi, ecx
inc dword ptr [{diag+184:#x}]
push dword ptr [ebp+8]
call 0x4ac550
cmp dword ptr [{diag+4:#x}], 5
jne done
cmp esi, dword ptr [{diag+36:#x}]
jne done
mov eax, dword ptr [esi+0x150]
cmp eax, dword ptr [{diag+28:#x}]
jne done
cmp dword ptr [eax+0x164], 1
jne done
inc dword ptr [{diag+44:#x}]
mov eax, dword ptr [esi]
push 0
mov ecx, esi
call dword ptr [eax+0x2c]
test eax, eax
jz done
mov edi, eax
mov eax, dword ptr [esi]
push 1
mov ecx, esi
call dword ptr [eax+0x2c]
test eax, eax
jz done
mov ebx, eax
mov dword ptr [{diag+12:#x}], edi
mov dword ptr [{diag+16:#x}], ebx
mov ecx, edi
call 0x40bb40
test eax, eax
jz done
push {diag+48:#x}
push eax
call 0x4e77c0
mov ecx, ebx
call 0x40bb40
test eax, eax
jz done
push {diag+56:#x}
push eax
call 0x4e77c0
mov dword ptr [ebp-16], 0x44160000
fld dword ptr [{diag+48:#x}]
fsub dword ptr [{diag+56:#x}]
fabs
fcomp dword ptr [ebp-16]
fnstsw ax
test ah, 0x45
jz teleport
mov dword ptr [ebp-16], 0x43960000
fld dword ptr [{diag+52:#x}]
fsub dword ptr [{diag+60:#x}]
fabs
fcomp dword ptr [ebp-16]
fnstsw ax
test ah, 0x45
jnz done
teleport:
push 0
push {diag+48:#x}
mov eax, ebx
call 0x4d25e0
inc dword ptr [{diag+40:#x}]
done:
add esp, 4
pop ebx
pop edi
pop esi
pop ebp
ret 4
''',codebase+0x2500)

def build_keyboard(asm,codebase,diag,data,off):
    # Only executable-local XInput import thunks change. No virtual driver,
    # global keyboard hook, or system input injection is installed.
    state=codebase+0x3000;caps=codebase+0x3b00;rumble=codebase+0x3c00;stroke=codebase+0x3d00
    lines=[f'''
push ebp
mov ebp, esp
push esi
push edi
push ebx
mov esi, dword ptr [ebp+12]
cmp dword ptr [ebp+8], 2
jae real_state
test esi, esi
jz bad_state
xor eax, eax
mov dword ptr [esi], eax
mov dword ptr [esi+4], eax
mov dword ptr [esi+8], eax
mov dword ptr [esi+12], eax
inc dword ptr [{diag+128:#x}]
mov eax, dword ptr [{diag+128:#x}]
mov dword ptr [esi], eax
inc dword ptr [{diag+148:#x}]
call dword ptr [0x72e234]
cmp eax, dword ptr [0x7d7ed4]
jne connected
cmp dword ptr [ebp+8], 0
jne player_two
''']
    # Button labels are native Xbox buttons, with action names documented only
    # after observing the game's control display.
    mappings=[
        {'left':0x41,'right':0x44,'up':0x57,'down':0x53,'buttons':[(0x20,0x1000),(0x4a,0x4000),(0x4b,0x8000),(0x4c,0x2000),(0x55,0x200),(0x49,0x100),(0x0d,0x10)],'lt':0x51,'rt':0x4f},
        {'left':0x25,'right':0x27,'up':0x26,'down':0x28,'buttons':[(0x60,0x1000),(0x61,0x4000),(0x62,0x8000),(0x63,0x2000),(0x64,0x200),(0x65,0x100)],'lt':0x67,'rt':0x66},
    ]
    for player,m in enumerate(mappings):
        if player:lines.append('player_two:')
        for key,axis,value in [(m['left'],8,-32767),(m['right'],8,32767),(m['up'],10,32767),(m['down'],10,-32767)]:
            label=f'p{player}_axis_{key:x}'
            lines.append(f'push {key}\ncall dword ptr [0x72e224]\ntest ax, 0x8000\njz {label}\nmov word ptr [esi+{axis}], {value}\n{label}:')
        for key,mask in m['buttons']:
            label=f'p{player}_button_{key:x}'
            lines.append(f'push {key}\ncall dword ptr [0x72e224]\ntest ax, 0x8000\njz {label}\nor word ptr [esi+4], {mask}\n{label}:')
        for key,axis in [(m['lt'],6),(m['rt'],7)]:
            label=f'p{player}_trigger_{key:x}'
            lines.append(f'push {key}\ncall dword ptr [0x72e224]\ntest ax, 0x8000\njz {label}\nmov byte ptr [esi+{axis}], 255\n{label}:')
        lines.append(f'mov eax, dword ptr [esi+4]\nmov dword ptr [{diag+140+player*4:#x}], eax\nmov eax, dword ptr [esi+8]\nmov dword ptr [{diag+152+player*4:#x}], eax\njmp connected')
    lines.append('''
connected:
xor eax, eax
jmp state_return
bad_state:
mov eax, 87
state_return:
pop ebx
pop edi
pop esi
pop ebp
ret 8
real_state:
pop ebx
pop edi
pop esi
pop ebp
jmp dword ptr [0x72e294]
''')
    state_blob=asm('\n'.join(lines),state)
    assert len(state_blob)<0xb00
    caps_blob=asm('''
cmp dword ptr [esp+4], 2
jae real_caps
mov edx, dword ptr [esp+12]
test edx, edx
jz bad_caps
xor eax, eax
mov dword ptr [edx], eax
mov dword ptr [edx+4], eax
mov dword ptr [edx+8], eax
mov dword ptr [edx+12], eax
mov dword ptr [edx+16], eax
mov word ptr [edx], 0x0101
mov dword ptr [edx+4], 0xffffffff
mov dword ptr [edx+8], 0x7fff7fff
mov dword ptr [edx+12], 0x7fff7fff
ret 12
bad_caps:
mov eax, 87
ret 12
real_caps:
jmp dword ptr [0x72e290]
''',caps)
    rumble_blob=asm('''
cmp dword ptr [esp+4], 2
jae real_rumble
xor eax, eax
ret 8
real_rumble:
jmp dword ptr [0x72e288]
''',rumble)
    stroke_blob=asm('''
cmp dword ptr [esp+4], 2
jae real_stroke
mov eax, 4306
ret 12
real_stroke:
jmp dword ptr [0x72e298]
''',stroke)
    patches=[]
    for addr,iat,target in [(0x6655ce,0x72e294,state),(0x6655c2,0x72e290,caps),(0x6655b6,0x72e288,rumble),(0x6655c8,0x72e298,stroke)]:
        before=b'\xff\x25'+struct.pack('<I',iat)
        assert data[off(addr):off(addr)+6]==before
        after=b'\xe9'+struct.pack('<i',target-addr-5)+b'\x90'
        patches.append((addr,before,after))
    return {0x3000:state_blob,0x3b00:caps_blob,0x3c00:rumble_blob,0x3d00:stroke_blob},patches

def build_input_probe(asm,codebase,diag):
    # Observe the native per-controller command fetch without changing its result.
    return asm(f'''
push ebp
mov ebp, esp
push ebx
mov ebx, ecx
push dword ptr [ebp+8]
call 0x5d1940
cmp ebx, 1
je first
cmp ebx, 2
jne done
mov dword ptr [{diag+168:#x}], eax
mov dword ptr [{diag+172:#x}], edx
inc dword ptr [{diag+180:#x}]
jmp done
first:
mov dword ptr [{diag+160:#x}], eax
mov dword ptr [{diag+164:#x}], edx
inc dword ptr [{diag+176:#x}]
done:
pop ebx
pop ebp
ret 4
''',codebase+0x3e00)
