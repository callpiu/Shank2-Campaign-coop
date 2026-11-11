"""Character -> melee -> ranged -> throwable for each pre-level player."""
import importlib.util
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'story-coop-v18-prelevel-duo'
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('prelevel18_flow',BASE/'flow.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
CODE,DATA=previous.CODE,previous.DATA

def routines(asm,c=CODE,d=DATA,diag=previous.DIAG,config=previous.CONFIG,catalog=previous.CATALOG):
    blocks=previous.routines(asm,c,d,diag,config,catalog)
    def put(offset,text):blocks[c+offset]=asm(text,c+offset)
    # +3c: role already confirmed for the currently selected player.
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
        mov dword ptr [{d+0x3c}],0
        mov eax,[{diag+32}];mov [{d+0x20}],eax
        mov esi,{config};mov edi,{d+0x40};mov ecx,32;cld
        rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        inc dword ptr [{d+0x24}]
        mov ecx,ebx;call {c+0x800}
        native:mov ecx,ebx;call 0x801ce0
        cmp ebx,[{d+0x10}];jne done
        mov ecx,ebx;call {c+0x1000}
        done:pop edi;pop esi;pop ebx;ret''')
    put(0x600,f'''push ebx;push esi;push edi
        mov ebx,eax
        cmp eax,[{d+0x10}];jne native
        cmp dword ptr [{d+0x3c}],0;jne equipment_done
        push dword ptr [ebx+0x1e8];push dword ptr [{d+0x14}]
        call {c+0x1400}
        test eax,eax;jz repeat_player
        mov dword ptr [{d+0x3c}],1
        jmp repeat_player
        equipment_done:
        mov ecx,ebx;call {c+0x900}
        cmp eax,1;jne repeat_player
        cmp dword ptr [{d+0x14}],0;jne commit
        inc dword ptr [{d+0x28}]
        mov dword ptr [{d+0x14}],1
        mov dword ptr [{d+0x3c}],0
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
    put(0x1000,f'''push ebx;push esi;sub esp,28
        mov ebx,ecx;mov esi,esp;mov ecx,esi;call 0x5e4540
        push esi;mov ecx,{d+0x240};mov eax,ebx;call 0x5e3e00
        mov ecx,{d+0x260}
        cmp dword ptr [{d+0x14}],0;je selected_player
        mov ecx,{d+0x290}
        selected_player:cmp dword ptr [{d+0x3c}],0;je title
        add ecx,0x60
        title:mov eax,esi;call 0x5e45a0
        mov ecx,esi;call 0x4604e0
        add esp,28;pop esi;pop ebx;ret''')
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
        cmp ebx,[{d+0x10}];jne done
        mov edi,{d+0x320}
        cmp dword ptr [{d+0x3c}],1;jne hint
        cmp dword ptr [{d+0x14}],1;jne hint
        cmp dword ptr [ebx+0x20],2;jne hint
        mov edi,0x75328c
        hint:lea ecx,[ebx+0x1f0];call 0x46fea0
        test eax,eax;jz done
        push edi;push 1;mov ecx,eax;call 0x697160
        done:pop edi;pop esi;pop ebx;mov esp,ebp;pop ebp;ret 4''')
    put(0x1200,f'''cmp ecx,[{d+0x10}];jne native
        cmp dword ptr [{d+0x3c}],0;je role_page
        cmp dword ptr [ecx+0x20],0;jne native
        push ecx;call {c+0x900};pop ecx
        mov dword ptr [{d+0x3c}],0
        jmp refresh
        role_page:cmp dword ptr [ecx+0x20],3;jne native
        cmp dword ptr [{d+0x14}],1;jne cancel
        mov dword ptr [{d+0x14}],0
        jmp refresh
        cancel:mov dword ptr [ecx+0x20],0
        jmp native
        refresh:mov dword ptr [{d+0x18}],1
        mov byte ptr [ecx+0x24],0
        ret 4
        native:jmp {c+0x1640}''')
    # Called with the original Page(int) ABI. Original OnShow requests page0
    # from sentinel4; make that the role page until that role is confirmed.
    # After the last weapon, native requests role3; this is now player-ready.
    put(0x1700,f'''cmp ecx,[{d+0x10}];jne native
        cmp dword ptr [{d+0x3c}],0;je initial
        cmp dword ptr [esp+4],3;jne native
        mov eax,ecx;call {c+0x600};ret 4
        initial:cmp dword ptr [esp+4],0;jne native
        cmp dword ptr [ecx+0x20],4;jne native
        mov dword ptr [esp+4],3
        native:jmp {c+0x17c0}''')
    put(0x17c0,'push ebp;mov ebp,esp;push -1;jmp 0x68d1c5')
    return blocks
