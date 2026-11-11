"""Read-only native costume rows for the campaign co-op equipment selector."""
from collections import Counter
import json
from pathlib import Path
import struct
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'story-coop-v04'))
from loadout_code import hash_name

CATALOG = json.loads((HERE.parent / 'story-coop-v04/catalog.json').read_text())['skins']
FAMILIES = ('shank', 'corina')
STRIDE = 0x90
FAMILY_HASHES = tuple(hash_name(name) for name in FAMILIES)
COUNTS = Counter(item['family'] for item in CATALOG)
IDS = {item['hash']: item['family'] for item in CATALOG}
assert len(CATALOG) == len(IDS) == 17 and COUNTS == {'shank': 12, 'corina': 5}
assert all(item['hash'] == hash_name(item['id']) for item in CATALOG)


def constants(base):
    """A table of {skin hash, family ordinal}, followed by a native family header."""
    families = struct.pack('<2I', *FAMILY_HASHES)
    table = b''.join(struct.pack('<2I', item['hash'], FAMILIES.index(item['family'])) for item in CATALOG)
    raw = bytearray(0xc00)
    raw[:len(families)] = families
    raw[0x10:0x10+len(table)] = table
    begin = base + 0x140
    struct.pack_into('<3I', raw, 0x120+4, begin, begin, begin + STRIDE * len(CATALOG))
    return bytes(raw)


def routines(asm, code, data, native_lookup=0x506980):
    """Build a bounded menu vector without touching native family records or profiles.

    ECX is not an argument; this routine follows the family's custom ABI:
    EDI points to a family hash and the single stack argument is the root table.
    Its input family is ignored only for this already-scoped menu call. Original
    rows are copied by value for display; borrowed text/assets remain owned by
    the native loader. Return 0 if a configured list is incomplete, and never
    reuse a partial list.
    """
    count = len(CATALOG)
    begin = data + 0x140
    result = data + 0x100
    lookup = asm(f'''push ebp
    mov ebp,esp
    sub esp,12
    push ebx
    push esi
    push edi
    mov dword ptr [{result+0x28}],{begin}
    xor ebx,ebx
    next_family:
    lea edi,[{data}+ebx*4]
    push dword ptr [ebp+8]
    call {native_lookup}
    test eax,eax
    jz missing
    mov esi,[eax+0x24]
    mov edx,[eax+0x28]
    test esi,esi
    jz missing
    cmp edx,esi
    jb missing
    mov eax,edx
    sub eax,esi
    cmp eax,{0x40 * STRIDE}
    ja missing
    mov [ebp-4],edx
    mov eax,[{result+0x28}]
    mov [ebp-8],eax
    row:
    mov edx,[ebp-4]
    cmp esi,edx
    je family_end
    sub edx,esi
    cmp edx,{STRIDE}
    jb missing
    mov eax,[esi]
    mov ecx,{data+0x10}
    find:
    cmp ecx,{data+0x10+count*8}
    jae skip_row
    cmp eax,[ecx]
    jne next_key
    cmp ebx,[ecx+4]
    je eligible
    next_key:
    add ecx,8
    jmp find
    eligible:
    mov edi,[ebp-8]
    unique:
    cmp edi,[{result+0x28}]
    jae append
    cmp [edi],eax
    je skip_row
    add edi,{STRIDE}
    jmp unique
    append:
    cmp edi,[{result+0x2c}]
    jae missing
    mov ecx,{STRIDE//4}
    rep movsd dword ptr es:[edi], dword ptr [esi]
    mov byte ptr [edi-{STRIDE-0x69}],0
    mov [{result+0x28}],edi
    jmp row
    skip_row:
    add esi,{STRIDE}
    jmp row
    family_end:
    mov eax,[{result+0x28}]
    sub eax,[ebp-8]
    mov edx,{COUNTS['shank']*STRIDE}
    test ebx,ebx
    jz compare
    mov edx,{COUNTS['corina']*STRIDE}
    compare:
    cmp eax,edx
    jne missing
    inc ebx
    cmp ebx,2
    jb next_family
    mov eax,{result}
    jmp done
    missing:
    mov dword ptr [{result+0x28}],{begin}
    xor eax,eax
    done:
    pop edi
    pop esi
    pop ebx
    mov esp,ebp
    pop ebp
    ret 4''', code)
    return lookup
