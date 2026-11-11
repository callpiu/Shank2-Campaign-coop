"""Local campaign HUD repair: one cinematic modifier may own the Boss bar."""
import base64
import json
from pathlib import Path
import struct
import sys
import zipfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'story-coop-v23-combo-fix'))
from build_update import BASE, BASE_SHA, DEV, dump, make_members, sha, pefile
from test_dispatch import PATCH_START, ORIGINAL, FIXED
from keystone import Ks, KS_ARCH_X86, KS_MODE_32

SET_UI = 0x674c46
UPDATE = 0x674a40
CAMPAIGN_VTABLE = 0x751ddc
DIAG = 0x7ff000
CODE_OFFSET = 0x1e00
DATA_OFFSET = 0x1f00
SET_BEFORE = bytes.fromhex('8b4240ffd0')
UPDATE_BEFORE = bytes.fromhex('558bec83ec14')


def routines(asm, code, diag, counter, update_continue, campaign_vtable=CAMPAIGN_VTABLE):
    setter = asm(f'''cmp dword ptr [{diag+4}],5
        jne original
        cmp dword ptr [ecx],{campaign_vtable:#x}
        jne original
        mov eax,[{diag+12}]
        test eax,eax
        jz original
        cmp dword ptr [{diag+16}],0
        je original
        cmp eax,[{diag+16}]
        je original
        lea eax,[ecx+0x113c]
        cmp eax,[ecx+0x11a0]
        jne original
        inc dword ptr [{counter:#x}]
        xor eax,eax
        ret 4
        original:
        mov eax,[edx+0x40]
        jmp eax''', code)
    update = asm(f'''cmp dword ptr [ecx+0xc],0
        je finished
        push ebp
        mov ebp,esp
        sub esp,0x14
        jmp {update_continue:#x}
        finished:
        xor eax,eax
        ret 4''', code + 0x80)
    assert len(setter) <= 0x80 and len(update) <= 0x80
    return setter, update


def build(mode, lang, recipe):
    stock = (DEV / f'{mode}-{lang}.exe').read_bytes()
    image = pefile.PE(data=stock)
    offset = lambda address: image.get_offset_from_rva(address - 0x400000)
    code = 0x400000 + next(s.VirtualAddress for s in image.sections if s.Name.rstrip(b'\0') == b'.precoop') + CODE_OFFSET
    data = 0x400000 + next(s.VirtualAddress for s in image.sections if s.Name.rstrip(b'\0') == b'.predat') + DATA_OFFSET
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda source, address: bytes(ks.asm(source, address)[0])
    original = bytearray(stock)
    combo = offset(PATCH_START)
    assert original[combo:combo+len(ORIGINAL)] == ORIGINAL
    original[combo:combo+len(ORIGINAL)] = FIXED
    assert sha(original) == recipe['output_sha256']
    baseline = bytes(original)
    setter, update = routines(asm, code, DIAG, data+4, UPDATE+6)
    changes = [(SET_UI, SET_BEFORE, asm(f'call {code:#x}', SET_UI)),
               (UPDATE, UPDATE_BEFORE, asm(f'jmp {code+0x80:#x};nop', UPDATE)),
               (code, b'\xcc' * len(setter), setter),
               (code+0x80, b'\xcc' * len(update), update),
               (data, bytes(8), b'BUI1'+bytes(4))]
    for address, before, after in changes:
        pos = offset(address)
        assert len(before) == len(after) and original[pos:pos+len(before)] == before, hex(address)
        if pos < recipe['source_size']:
            assert pos+len(before) <= recipe['source_size']
            assert all(entry['offset'] >= pos+len(before) or entry['offset']+len(bytes.fromhex(entry['after'])) <= pos for entry in recipe['patches'])
            recipe['patches'].append(dict(offset=pos, before=before.hex(), after=after.hex()))
        original[pos:pos+len(after)] = after
    for address, length in [(0x4ee3b0,0x80),(0x53de70,0x350),(0x6955f0,0xe8),(0x7ff800,128)]:
        pos = offset(address)
        assert original[pos:pos+length] == baseline[pos:pos+length], hex(address)
    recipe.update(output_sha256=sha(original), append=base64.b64encode(original[recipe['source_size']:]).decode('ascii'))
    recipe['patches'].sort(key=lambda entry: entry['offset'])
    return recipe, dict(mode=mode, lang=lang, baseline_sha256=sha(baseline), sha256=sha(original),
                        code=hex(code), overlap_counter=hex(data+4), sites=[hex(row[0]) for row in changes])


def main():
    assert sha(BASE.read_bytes()) == BASE_SHA
    with zipfile.ZipFile(BASE) as original:
        combo, _ = make_members(original)
    previous = json.loads(combo['patch/previous-baselines.json'])
    out = HERE / 'candidate' / 'patch'
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for mode in ('keyboard','pads'):
        for lang in ('en','chs'):
            name = f'{mode}-{lang}-addon.json'
            recipe = json.loads(combo['patch/'+name])
            previous[mode].append(recipe['output_sha256'])
            recipe, row = build(mode, lang, recipe)
            (out/name).write_bytes(dump(recipe))
            rows.append(row)
    (out/'previous-baselines.json').write_bytes(dump(previous))
    (HERE/'builds.json').write_bytes(dump(rows))
    print('Four local candidates prepared; no archive generated.')


if __name__ == '__main__':
    main()
