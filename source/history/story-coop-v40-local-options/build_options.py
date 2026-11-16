"""Build local options candidates from the frozen original and CHS releases."""
import argparse
import base64
import json
from pathlib import Path
import struct
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = HERE.parent
sys.path[:0] = [
    str(WORK / 'story-coop-v38-throwable-refill'),
    str(WORK / 'story-coop-v04'),
]
from build_candidate import load_build, reconstruct, sha
from chui import Reader
from keystone import Ks, KS_ARCH_X86, KS_MODE_32
import pefile

BASELINES = {
    'en': ('0.10.4-MOD', '353298a76da5cab4762a5629d9edab9028bf474061d3672e227458dc865f8a6c'),
    'chs': ('0.10.6-MOD-CHS', '9c40c9269777afcec3d96d7722894b716ba02ecd698b336357db550445dd4764'),
}
STATE = 0x72e294
APIS = (
    (0x6655ce, 0x2200, STATE, 8),
    (0x6655c2, 0x0820, 0x72e290, 12),
    (0x6655b6, 0x0840, 0x72e288, 8),
    (0x6655c8, 0x0860, 0x72e298, 12),
)


def hud(raw):
    reader = Reader(raw)
    assert reader.u32() == 2
    [reader.node() for _ in range(reader.u32())]
    roots = {n['name']: n for n in [reader.node() for _ in range(reader.u32())]}
    assert len(raw) == reader.pos
    p1, p2 = (roots[k] for k in ('playerui', 'playerui2'))
    first, second = [next(n for n in p['children'] if n['name'] == 'player') for p in (p1, p2)]
    assert first['type'] == second['type'] == 16
    position = lambda n: struct.unpack_from('<2f', raw, n['common'])
    assert position(first) == position(second)
    x, y = position(second)
    x1, y1 = position(p1)
    x2, y2 = position(p2)
    assert abs(x1 - x2) < 1e-6 and abs(y1 - y2 - .18) < 1e-5
    out = bytearray(raw)
    # Move only the status widget (portrait, HP, throwables, score).
    # Its old left edge is ~.02; the new one is ~.32. Leave the upper
    # right free for the Boss HUD.
    struct.pack_into('<2f', out, second['common'], x + .30, y + y1 - y2)
    return bytes(out)


def sections(raw):
    pe = pefile.PE(data=raw, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    named = {s.Name.rstrip(b'\x00'): base+s.VirtualAddress for s in pe.sections}
    return named[b'.direct'], named[b'.dirdata'], lambda a: pe.get_offset_from_rva(a-base)


def native(stock, recipe, lang):
    raw = bytes(reconstruct(stock, recipe))
    assert sha(raw) == BASELINES[lang][1]
    c, d, off = sections(raw)
    image = bytearray(raw)
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda s, a: bytes(ks.asm(s, a)[0])

    def write(addr, before, after):
        p = off(addr)
        assert len(before) == len(after) and image[p:p+len(before)] == before, hex(addr)
        image[p:p+len(after)] = after

    def put(addr, source):
        blob = asm(source, addr)
        write(addr, b'\xcc'*len(blob), blob)

    layout, mode, cfg_mode = d+0x64, d+4, d+0x84
    hudname = f'campaignhud40{lang}.chui'
    name = hudname.encode('ascii') + b'\0'
    write(d+0x7c0, bytes(len(name)), name)
    assert raw[off(layout):off(layout)+4] == bytes(4)
    validate = c+0x2800
    selector = c+0x2900
    resolve = c+0x2950
    # Keep the existing 116-byte settings format. Bit 2 selects vertical;
    # decode it separately so legacy consumers still see just input mode.
    put(validate, f'''cmp dword ptr [{d+0x620}],0x314b3253;jne invalid
        mov edx,[{d+0x624}];cmp edx,6;ja invalid;cmp edx,3;je invalid
        mov ecx,27;mov esi,{d+0x628}
        keycheck:mov eax,[esi];add esi,4;dec eax;cmp eax,253;ja invalid;loop keycheck
        mov ecx,29;mov esi,{d+0x620};mov edi,{d+0x80};rep movsd dword ptr es:[edi],dword ptr ds:[esi]
        mov eax,edx;and eax,4;mov [{layout}],eax
        and edx,3;mov [{cfg_mode}],edx
        invalid:ret''')
    start = c+0x2700
    write(start, asm(f'cmp dword ptr [{d+0x620}],0x314b3253', start)[:5],
          asm(f'jmp {validate}', start))

    put(selector, f'''pushfd;cmp dword ptr [{mode}],1;jne solo
        cmp dword ptr [{layout}],0;jne vertical
        popfd;push {d+0x7c0};jmp 0x6968dd
        vertical:popfd;push 0x7ff400;jmp 0x6968dd
        solo:popfd;push {d+0x300};jmp 0x6968dd''')
    start = c+0x1100
    write(start, asm(f'pushfd;cmp dword ptr [{mode}],1', start)[:5],
          asm(f'jmp {selector}', start))

    # Resolve the first connected XInput device, including configurations
    # where Steam Input allocated a nonzero hardware index. Query into a
    # private stack buffer; synthetic 1P can never claim the physical pad.
    put(resolve, f'''push ebx;sub esp,16;xor ebx,ebx
        probe:mov edx,esp;push edx;push ebx;call dword ptr [{STATE}]
        test eax,eax;jz found;inc ebx;cmp ebx,4;jb probe
        mov ebx,-1
        found:mov eax,ebx;add esp,16;pop ebx;ret''')

    for i, (site, old, iat, pop) in enumerate(APIS):
        entry = c+0x29b0+i*0x60
        put(entry, f'''cmp dword ptr [{cfg_mode}],2;jne previous
            cmp dword ptr [{mode}],1;jne native
            cmp dword ptr [esp+4],0;je previous
            cmp dword ptr [esp+4],1;jne absent
            call {resolve};test eax,eax;js absent;mov [esp+4],eax
            native:jmp dword ptr [{iat}]
            absent:mov eax,1167;ret {pop}
            previous:jmp {c+old}''')
        write(site, asm(f'jmp {c+old};nop', site), asm(f'jmp {entry};nop', site))

    # Allow the existing P1 dodge mapper after mixed input has already
    # excluded every physical-device call from the synthetic path.
    at = c+0x2200
    p = off(at)
    check = asm(f'cmp dword ptr [{cfg_mode}],0', at) + b'\x75'
    start = raw.index(check, p, p+0x50)
    image[start+len(check)-2:start+len(check)] = b'\x01\x74'

    # Rebuild changed original-file runs directly from the supported stock.
    edits = []
    i = 0
    for j, (a, b) in enumerate(zip(stock, image)):
        if a != b:
            if not i:
                i = j+1
        elif i:
            k = i-1
            edits.append(dict(offset=k, before=stock[k:j].hex(), after=image[k:j].hex()))
            i = 0
    if i:
        k = i-1
        edits.append(dict(offset=k, before=stock[k:].hex(), after=image[k:len(stock)].hex()))
    recipe.update(patches=edits, append=base64.b64encode(image[len(stock):]).decode(),
                  output_sha256=sha(image))
    assert reconstruct(stock, recipe) == image
    return hudname, bytes(image)


def create(stock, lang):
    release, _ = BASELINES[lang]
    with zipfile.ZipFile(ROOT/'outputs'/f'Shank2-v{release}.zip') as archive:
        files = {p: archive.read(p) for p in archive.namelist() if p != 'patch/SHA256SUMS.txt'}
    recipe, manifest = (json.loads(files['patch/'+p+'.json']) for p in ('exe-recipe', 'manifest'))
    hudname, image = native(stock, recipe, lang)
    prefix = 'data-pc/ui/'
    path = prefix+hudname
    asset = hud(files[f'patch/payload/{prefix}campaigncoopv20{lang}.chui'])
    files['patch/payload/'+path] = asset
    manifest['files'].append(dict(path=path, targetRelative=path, relative='payload/'+path,
                                  size=len(asset), sha256=sha(asset), original_sha256=None))
    settings = 'Coop-Key-Settings.ps1'
    from settings import extend
    for p in (f'patch/{settings}', f'patch/payload/patch/{settings}'):
        files[p] = extend(files[p], lang)
    for row in manifest['files']:
        if row.get('recipe'):
            row['sha256'] = sha(image)
        if row['path'] == 'patch/'+settings:
            data = files['patch/'+row['relative']]
            row.update(size=len(data), sha256=sha(data))
        if 'relative' in row:
            data = files['patch/'+row['relative']]
            assert (len(data), sha(data)) == (row['size'], row['sha256']), row['path']
    for p, value in [('manifest', manifest), ('exe-recipe', recipe), ('VALIDATION', {
        'scope': 'Local HUD and mixed input development build; in-game verification pending',
        'base_release': release, 'online_campaign': False,
    })]:
        files[f'patch/{p}.json'] = (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode()
    files['patch/SHA256SUMS.txt'] = ''.join(
        f'{sha(data)}  {p}\n' for p, data in sorted(files.items())).encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-dir', type=Path, required=True, help='Supported unmodified game')
    parser.add_argument('--out', type=Path, required=True, help='New development output directory')
    parser.add_argument('--lang', choices=BASELINES, required=True)
    args = parser.parse_args()
    files = create((args.game_dir/'bin/shank2.exe').read_bytes(), args.lang)
    builder = load_build()
    builder.verify_game(args.game_dir, json.loads(files['patch/manifest.json']),
                        json.loads(files['patch/exe-recipe.json']))
    builder.package(args.out, f'Shank2-Local-Options-Test-{args.lang}', files)


if __name__ == '__main__':
    main()
