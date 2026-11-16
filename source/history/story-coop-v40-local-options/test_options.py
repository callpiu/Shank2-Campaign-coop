"""Run the real boot/config, input thunks and HUD selector in isolated x86 fixtures."""
import os
import subprocess
import tempfile
from copy import deepcopy
from build_options import *

STOCK_GAME = WORK/'story-coop-v09-fixes/upgrade-fixture'
RUNTIME_BIN = WORK/'story-coop-v14-transitions/game/bin'


def fixture(image, lang):
    c, d, off = sections(image)
    out = bytearray(image)
    ks = Ks(KS_ARCH_X86, KS_MODE_32)
    asm = lambda s, a: bytes(ks.asm(s, a)[0])
    put = lambda a, data: out.__setitem__(slice(off(a), off(a)+len(data)), data)
    code = lambda a, s: put(a, asm(s, a))
    ctl, state = d+0x1c00, d+0x1d00

    # Simulate one controller in hardware index 2; reject all other slots.
    # Native distinct inputs (A + right stick) on that pad survive the wrapper.
    pad, keys, focus, other = (c+0x2c00+i*0x40 for i in range(4))
    code(pad, f'''mov eax,[esp+4];cmp eax,2;jne absent
        cmp dword ptr [{ctl}],0;je absent
        mov edx,[esp+8];mov dword ptr [edx],0x10203040
        mov dword ptr [edx+4],0x1000;mov dword ptr [edx+8],0
        mov dword ptr [edx+12],0x1234;xor eax,eax;ret 8
        absent:mov eax,1167;ret 8''')
    code(keys, '''mov eax,[esp+4];cmp eax,1;je pressed
        cmp eax,0x5a;je pressed;xor eax,eax;ret 4
        pressed:mov eax,0x8000;ret 4''')
    code(focus, 'mov eax,0x4321;ret')
    code(other, 'mov eax,[esp+4];ret 8')
    slots = {STATE: pad, 0x72e224: keys, 0x72e234: focus, 0x72e288: other}
    for i, (iat, target) in enumerate(slots.items()):
        slot = d+0x1e00+4*i
        put(slot, struct.pack('<I', target))
        for opcode in (b'\xff\x15', b'\xff\x25'):
            before = opcode+struct.pack('<I', iat)
            out = out.replace(before, opcode+struct.pack('<I', slot))

    hud_entry = c+0x1100
    code(0x6968dd, 'pop eax;ret')
    script = f'''cld;mov dword ptr [0x7d7ed4],0x4321
        call {hud_entry};cmp eax,{d+0x300};jne bad10
        mov dword ptr [{d+4}],1
        call {hud_entry}
        cmp dword ptr [{d+0x64}],0;jne stacked
        cmp eax,{d+0x7c0};jne bad11
        jmp input
        stacked:cmp eax,0x7ff400;jne bad11
        input:cmp dword ptr [{d+0x84}],2;jne finish
        mov dword ptr [{ctl}],1
        push {state};push 0;call 0x6655ce
        test eax,eax;jnz bad12
        cmp word ptr [{state+4}],0x4000;jne bad13
        cmp word ptr [{state+12}],0x8001;jne bad14
        push {state};push 1;call 0x6655ce
        test eax,eax;jnz bad15
        cmp dword ptr [{state}],0x10203040;jne bad15
        cmp word ptr [{state+4}],0x1000;jne bad16
        cmp word ptr [{state+12}],0x1234;jne bad16
        push {state};push 2;call 0x6655ce
        cmp eax,1167;jne bad17
        push 0;push 1;call 0x6655b6
        cmp eax,2;jne bad18
        push 0;push 0;call 0x6655b6
        test eax,eax;jnz bad19
        mov dword ptr [{ctl}],0
        push {state};push 1;call 0x6655ce
        cmp eax,1167;jne bad20
        mov dword ptr [{ctl}],1
        mov dword ptr [{d+4}],0
        push {state};push 0;call 0x6655ce
        cmp eax,1167;jne bad21
        push {state};push 2;call 0x6655ce
        test eax,eax;jnz bad21
        finish:mov eax,[{d+0x84}];or eax,[{d+0x64}];jmp exit
    '''
    script += '\n'.join(f'bad{i}:mov eax,{i};jmp exit' for i in range(10,22))
    script += '\nexit:push eax;call dword ptr [0x72e094]'
    boot_test = c+0x2d00
    assert len(asm(script, boot_test)) <= 0x300
    code(boot_test, script)
    # Swap the final jump after the original config + dodge files have loaded.
    jump = asm('jmp 0x6451e0', c+0x2100)
    pos = next(a for a in range(c+0x2100,c+0x2200-4)
               if out[off(a):off(a)+5] == asm('jmp 0x6451e0', a))
    assert len(jump) == 5
    code(pos, f'jmp {boot_test}')
    return bytes(out)


def test(game=STOCK_GAME):
    stock = (game/'bin/shank2.exe').read_bytes()
    env = dict(os.environ)
    # The stock fixture only includes the executable and its two hash guards.
    # Load FMOD and DirectX DLLs from the existing isolated runtime copy.
    env['PATH'] = str(RUNTIME_BIN)+os.pathsep+env.get('PATH','')
    keys = [0x41,0x44,0x57,0x53,0x20,1,0x4b,2,0x55,0x49,0x0d,0x51,0x4f,
            0x25,0x27,0x26,0x28,0x60,0x61,0x62,0x63,0x64,0x65,0x67,0x66,0x75,0x76]
    def packet(mode, values=keys):
        return b'S2K1'+struct.pack('<28I',mode,*values)

    with tempfile.TemporaryDirectory(prefix='options-native-', dir=HERE) as tmp:
        bin_dir = Path(tmp)/'bin'
        bin_dir.mkdir()
        exe, config = (bin_dir/name for name in ('options-native.exe', 'Shank2-Coop-Keys.dat'))
        for lang, (release, _) in BASELINES.items():
            with zipfile.ZipFile(ROOT/'outputs'/f'Shank2-v{release}.zip') as archive:
                recipe = json.loads(archive.read('patch/exe-recipe.json'))
                chui = archive.read(f'patch/payload/data-pc/ui/campaigncoopv20{lang}.chui')
            before = deepcopy(recipe)
            _, image = native(stock, recipe, lang)
            original = reconstruct(stock, before)
            assert stock[:1024] != image[:1024] and image != original
            assert len(hud(chui)) == len(chui) and hud(chui) != chui
            exe.write_bytes(fixture(image, lang))
            cases = [(None,0)]+[(packet(n),n) for n in (0,1,2,4,5,6)]
            cases += [(packet(n),0) for n in (3,7,0xffffffff)]
            cases += [(packet(6,[0]+keys[1:]),0),(packet(6)[:-1],0),(packet(6)+b'X',0)]
            for data, expected in cases:
                if data is None:
                    config.unlink(missing_ok=True)
                else:
                    config.write_bytes(data)
                p = subprocess.run([str(exe)], cwd=tmp, env=env,
                                   creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
                assert p.returncode == expected, (lang, expected, p.returncode)
            print(f'{lang}: {len(cases)} actual x86 boot and HUD checks passed; mixed mouse/dodge, single-pad routing and absent-pad cases passed.')


if __name__ == '__main__':
    test()
