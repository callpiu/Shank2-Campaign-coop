"""Initialize native page metadata before entering the character panel."""
import importlib.util
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'story-coop-v19-character-first'
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('role_first19',BASE/'flow19.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
CODE,DATA=previous.CODE,previous.DATA

def routines(asm,c=CODE,d=DATA,**kwargs):
    blocks=previous.routines(asm,c,d,**kwargs)
    def put(offset,text):blocks[c+offset]=asm(text,c+offset)
    # Do not redirect OnShow's Page(0): its tail subsequently overwrites the
    # panel's position. Enter role3 only AFTER native OnShow fully returned.
    put(0x1700,f'''cmp ecx,[{d+0x10}];jne native
        cmp dword ptr [{d+0x3c}],1;jne native
        cmp dword ptr [esp+4],3;jne native
        mov eax,ecx;call {c+0x600};ret 4
        native:jmp {c+0x17c0}''')
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
        mov ecx,ebx;call {c+0x1c00}
        add esp,28;pop esi;pop ebx;ret''')
    # Page0 was populated by OnShow. Pages1/2 populate their image maps and
    # source indexes; Page3 then updates all equipped icons and the skin panel.
    # These are view changes only: no native confirmation/event callback runs.
    put(0x1c00,f'''cmp ecx,[{d+0x10}];jne done
        cmp dword ptr [{d+0x3c}],0;jne done
        push ebx;mov ebx,ecx
        push 1;call {c+0x17c0}
        push 2;mov ecx,ebx;call {c+0x17c0}
        cmp dword ptr [ebx+0x20],3;je finished
        push 3;mov ecx,ebx;call {c+0x17c0}
        finished:pop ebx
        done:ret''')
    # Replace the literal hint address, keeping all instruction boundaries.
    old=(0x75328c).to_bytes(4,'little');new=(d+0x350).to_bytes(4,'little')
    assert blocks[c+0xb00].count(old)==1
    blocks[c+0xb00]=blocks[c+0xb00].replace(old,new)
    return blocks
