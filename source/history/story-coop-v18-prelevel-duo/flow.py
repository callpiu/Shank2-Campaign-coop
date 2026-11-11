"""Scoped native pre-level P1/P2 selection; no live actor replacement."""
import importlib.util
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'story-coop-v12-live-character'))
spec=importlib.util.spec_from_file_location('character12_builder',HERE.parent/'story-coop-v12-live-character/build.py')
v12=importlib.util.module_from_spec(spec);spec.loader.exec_module(v12)

CODE,DATA=0x806000,0x808000
DIAG,CONFIG,CATALOG=0x7ff000,0x7ff800,0x800000

def routines(asm,c=CODE,d=DATA,diag=DIAG,config=CONFIG,catalog=CATALOG):
    blocks={}
    def put(offset,source):blocks[c+offset]=asm(source,c+offset)
    # State: registered initial/next-level screens; active, slot, refresh,
    # sync hold/generation. Staging at +40 contains both 64-byte configurations.
    put(0,f'''push eax;push edx
        mov eax,[esp+8]
        cmp eax,0x6b83b6;je initial
        cmp eax,0x6bde20;je next_level
        cmp ecx,[{d}];jne clear_next
        mov dword ptr [{d}],0
        clear_next:cmp ecx,[{d+4}];jne registered
        mov dword ptr [{d+4}],0
        jmp registered
        initial:mov [{d}],ecx;jmp registered
        next_level:mov [{d+4}],ecx
        registered:pop edx;pop eax;jmp {c+0x1600}''')
    put(0x180,f'''push ebx;push esi;push edi
        mov ebx,ecx
        cmp ecx,[{d}];je eligible
        cmp ecx,[{d+4}];jne native
        eligible:test ecx,ecx;jz native
        cmp dword ptr [ecx],0x7532b0;jne native
        cmp dword ptr [{config}],1;jne native
        cmp dword ptr [{config+64}],1;jne native
        mov [{d+0x10}],ecx
        mov dword ptr [{d+0x14}],0
        mov dword ptr [{d+0x18}],0
        mov dword ptr [{d+0x1c}],1
        mov eax,[{diag+32}];mov [{d+0x20}],eax
        mov esi,{config};mov edi,{d+0x40};mov ecx,32;cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        inc dword ptr [{d+0x24}]
        mov ecx,ebx;call {c+0x800}
        native:mov ecx,ebx;call 0x801ce0
        cmp ebx,[{d+0x10}];jne done
        mov ecx,ebx;call {c+0x1000}
        done:pop edi;pop esi;pop ebx;ret''')
    put(0x400,f'''push ecx
        cmp ecx,[{d+0x10}];jne native
        cmp byte ptr [ecx+0x24],0;jne confirmed
        mov dword ptr [{d+0x1c}],0
        inc dword ptr [{d+0x34}]
        confirmed:
        mov dword ptr [{d+0x10}],0
        mov dword ptr [{d+0x18}],0
        native:pop ecx;jmp 0x7fb680''')
    # Preserve the original pause selector's pointer+generation guard.
    put(0x500,f'''xor eax,eax
        test ecx,ecx;jz done
        cmp ecx,[{d+0x10}];jne pause
        mov eax,1;ret
        pause:cmp dword ptr [{diag+4}],5;jne done
        cmp ecx,[0x800c00];jne done
        mov eax,[{diag+32}];cmp eax,[0x800c04];sete al;movzx eax,al
        done:ret''')
    # Called exactly where a valid native costume choice would hide the UI.
    put(0x600,f'''push ebx;push esi;push edi
        mov ebx,eax
        cmp eax,[{d+0x10}];jne native
        mov ecx,ebx;call {c+0x900}
        cmp eax,1;jne repeat_player
        cmp dword ptr [{d+0x14}],0;jne commit
        inc dword ptr [{d+0x28}]
        mov dword ptr [{d+0x14}],1
        jmp repeat_player
        commit:inc dword ptr [{d+0x2c}]
        mov esi,{d+0x40};mov edi,{config};mov ecx,32;cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        mov dword ptr [{d+0x1c}],1
        mov eax,[{diag+32}];mov [{d+0x20}],eax
        inc dword ptr [{d+0x30}]
        mov dword ptr [{d+0x14}],0
        mov ecx,ebx;call {c+0x800}
        mov byte ptr [ebx+0x24],1
        jmp native
        repeat_player:mov byte ptr [ebx+0x24],0
        mov dword ptr [{d+0x18}],1
        pop edi;pop esi;pop ebx;ret
        native:mov eax,ebx;pop edi;pop esi;pop ebx;jmp 0x5e33c0''')
    put(0x800,f'''push esi
        mov esi,[{d+0x14}];shl esi,6;add esi,{d+0x40}
        push dword ptr [esi+20]
        push dword ptr [esi+32]
        push dword ptr [esi+28]
        push dword ptr [esi+24]
        add esi,4;push esi
        call 0x68c420
        pop esi;ret''')
    # 0=invalid, 1=ready, 2=changed archetype (must choose its own weapons).
    put(0x900,f'''push ebp;mov ebp,esp;sub esp,8;push ebx;push esi
        mov ebx,ecx
        mov esi,[{d+0x14}];shl esi,6;add esi,{d+0x40}
        mov eax,[esi+4];mov [ebp-4],eax
        push dword ptr [ebx+0x1e8];push dword ptr [{d+0x14}]
        call {c+0x1400}
        test eax,eax;jz done
        mov eax,[esi+4];cmp eax,[ebp-4];jne changed
        cmp dword ptr [ebx+0x1dc],0;je invalid
        cmp dword ptr [ebx+0x1e0],0;je invalid
        cmp dword ptr [ebx+0x1e4],0;je invalid
        mov eax,[ebx+0x1dc];mov [esi+24],eax
        mov eax,[ebx+0x1e0];mov [esi+28],eax
        mov eax,[ebx+0x1e4];mov [esi+32],eax
        mov eax,1;jmp done
        changed:mov eax,2;jmp done
        invalid:xor eax,eax
        done:pop esi;pop ebx;mov esp,ebp;pop ebp;ret''')
    # Refresh on the next UI tick, outside the active button signal callback.
    put(0xb00,f'''push ebp;mov ebp,esp;push ebx;push esi;push edi
        mov ebx,ecx
        cmp ecx,[{d+0x10}];jne native
        cmp dword ptr [{d+0x18}],0;je observe_skin
        mov dword ptr [{d+0x18}],0
        call {c+0x800}
        mov ecx,ebx;call 0x801ce0
        mov ecx,ebx;call {c+0x1000}
        observe_skin:
        cmp dword ptr [ebx+0x20],3;jne native
        cmp dword ptr [{catalog+0x128}],{catalog+0x140+0x90*17};jne native
        lea ecx,[ebx+0x148];call 0x5e49f0
        cmp eax,17;jae native
        imul eax,eax,0x90;mov edi,[{catalog+0x140}+eax]
        mov esi,[{d+0x14}];shl esi,6;add esi,{d+0x40}
        cmp edi,[esi+20];je native
        mov ecx,ebx;call {c+0x900}
        mov eax,[esi+4];push eax
        push edi;push dword ptr [{d+0x14}];call {c+0x1400}
        pop edx
        test eax,eax;jz native
        cmp edx,[esi+4];je native
        mov dword ptr [{d+0x18}],1
        inc dword ptr [{d+0x38}]
        native:push dword ptr [ebp+8];mov ecx,ebx;call 0x68c470
        pop edi;pop esi;pop ebx;mov esp,ebp;pop ebp;ret 4''')
    put(0xf00,f'''cmp dword ptr [{d+0x10}],0;jne held
        cmp dword ptr [{d+0x1c}],0;je native
        mov eax,[{diag+32}];cmp eax,[{d+0x20}];je held
        mov dword ptr [{d+0x1c}],0
        native:jmp 0x801700
        held:ret''')
    # A temporary native StringRef; teardown disconnects it before returning.
    put(0x1000,f'''push ebx;push esi;sub esp,28
        mov ebx,ecx;mov esi,esp;mov ecx,esi;call 0x5e4540
        push esi;mov ecx,{d+0x240};mov eax,ebx;call 0x5e3e00
        mov ecx,{d+0x260}
        cmp dword ptr [{d+0x14}],0;je title
        mov ecx,{d+0x290}
        title:mov eax,esi;call 0x5e45a0
        mov ecx,esi;call 0x4604e0
        add esp,28;pop esi;pop ebx;ret''')
    put(0x1200,f'''cmp ecx,[{d+0x10}];jne native
        cmp dword ptr [{d+0x14}],1;jne native
        cmp dword ptr [ecx+0x20],0;jne native
        mov dword ptr [{d+0x14}],0
        mov dword ptr [{d+0x18}],1
        mov byte ptr [ecx+0x24],0
        ret 4
        native:jmp {c+0x1640}''')
    blocks[c+0x1400]=v12.selection(asm,c+0x1400,data=catalog,config=d+0x40)
    put(0x1600,'push ebp;mov ebp,esp;push ecx;mov [ebp-4],ecx;jmp 0x68c2e7')
    put(0x1640,'push ebp;mov ebp,esp;sub esp,8;jmp 0x68dd66')
    # Replace only three existing weapon-filter CMPs, preserving their flags ABI.
    put(0x1680,f'''push eax
        cmp dword ptr [{diag+4}],5;je yes
        cmp dword ptr [{d+0x10}],0;jne yes
        mov eax,1;test eax,eax;pop eax;ret
        yes:xor eax,eax;test eax,eax;pop eax;ret''')
    return blocks
