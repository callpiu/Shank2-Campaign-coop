"""Check full character biographies against actual font and card bounds."""
import json
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
sys.path.insert(0, str(WORK / 'story-coop-v28-trait-descriptions'))
from build_descriptions import parse_ui, summaries


def check(raw, lang, rows):
    reader, templates, roots = parse_ui(raw)
    skin = next(n for n in templates if n['name'] == 'SkinSpinnerTemplate')
    desc = next(n for n in skin['children'] if n['name'] == 'desc')
    trait = next(n for n in roots if n['name'] == 'coopTraitSummary')
    bounds = lambda n: struct.unpack_from('<4f', raw, n['common'])
    dx, dy, dw, dh = bounds(desc)
    _, _, sw, sh = bounds(skin)
    _, ty, _, th = bounds(trait)
    # Native Chinese wrapping has no word boundary inside these sentences.
    # Each unbroken run must fit; English may wrap at existing spaces.
    reader.pos = desc['extra']; reader.string()
    settings = reader.take(16); font_name = reader.string()
    size = struct.unpack('<f', reader.take(4))[0]
    assert settings == bytes.fromhex('000000000000000001000000ffffffff')
    assert font_name == 'antilles24' and size == 24
    font_root = (WORK / 'chs-compat/extracted/en/data-pc/bootstrap/fonts' if lang == 'en'
        else Path(r'E:\SteamLibrary\steamapps\common\Shank 2\data-pc\bootstrap\fonts'))
    font = ET.fromstring((font_root / 'antilles24.fnt').read_bytes())
    glyphs = {int(n.attrib['id']): int(n.attrib['xadvance']) for n in font.findall('./chars/char')}
    line_height = int(font.find('./common').attrib['lineHeight'])
    width = dw * 1280
    assert abs(dx) + dw / 2 <= sw / 2
    assert dy - dh / 2 >= -sh / 2 - 1e-6

    def origin(n, y=0):
        y += bounds(n)[1]
        if n['name'] == 'skinspinner': return y
        for child in n['children']:
            found = origin(child, y)
            if found is not None: return found
        return None
    center_y = next(y for n in roots if (y := origin(n)) is not None)
    desc_top = center_y + dy + dh / 2
    cases = []
    for name, row in rows.items():
        text = row['original_description']
        assert all(ord(c) in glyphs for c in text), (lang, name, 'missing glyph')
        runs = text.split(' ') if lang == 'en' else [text]
        assert all(sum(glyphs[ord(c)] for c in run) <= width for run in runs), (lang, name, 'horizontal clipping')
        lines, used = 1, 0
        for run in runs:
            advance = sum(glyphs[ord(c)] for c in run)
            space = glyphs[32] if used else 0
            if used + space + advance > width:
                lines += 1; used = advance
            else: used += space + advance
        assert lines * line_height <= dh * 720, (lang, name, 'vertical clipping')
        trait_bottom = ty + th / 2 - len(row['lines']) * line_height / 720
        # Full-width biography is below the right-hand bonuses, with a margin.
        assert trait_bottom >= desc_top + 8 / 720, (lang, name, 'trait overlap')
        assert ty + th / 2 <= center_y + sh / 2, 'trait above card'
        cases.append(dict(skin=name,biography_lines=lines,glyphs_present=True,
            full_text_fits=True,trait_gap_design_pixels=(trait_bottom-desc_top)*720))
    return dict(language=lang,description_bounds=[dx,dy,dw,dh],cases=cases)


def main():
    reports=[]
    for lang, rows in summaries().items():
        for prefix in ('cooppreselv28', 'coopsolo28sel'):
            path=WORK/f'story-coop-v28-trait-descriptions/dev/{prefix}{lang}.chui'
            reports.append(dict(resource=path.name,**check(path.read_bytes(),lang,rows)))
    # Freeze the user's failure as a regression: the old 230px box cannot fit Hobo.
    failed=False
    try: check((HERE/'prior-solo-chs.chui').read_bytes(),'chs',summaries()['chs'])
    except AssertionError: failed=True
    assert failed, 'Old screenshot failure must remain reproducible.'
    (HERE/'layout-validation.json').write_text(json.dumps(dict(passed=True,
        old_clipping_reproduced=True,characters=17,resources=reports,
        runtime_visual_verified=False),indent=2)+'\n')
    print('All 17 biographies fit four EN/CHS selectors; old clipping reproduced; bonus column stays separate.')


if __name__ == '__main__': main()
