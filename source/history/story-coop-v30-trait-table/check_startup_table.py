"""Reproduce native boot ReadFile writes before inspecting all skin rows."""
import json
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
sys.path.insert(0,str(WORK/'story-coop-v28-trait-descriptions'))
from build_descriptions import summaries,name_hash,pefile,BASE,TABLE_OFFSET


def check(raw,row,table_offset):
    pe=pefile.PE(data=raw,fast_load=True);data=int(row['data'],16)
    offset=lambda a:pe.get_offset_from_rva(a-BASE)
    def read(a,size):return raw[offset(a):offset(a)+size]
    # Use the exact native bootstrap writes: bytesRead at +600 and the
    # 116-byte settings payload at +620. Buffer is deliberately 117 bytes
    # so a file with trailing bytes is rejected by the normal validator.
    defaults=(0x41,0x44,0x57,0x53,0x20,0x4a,0x4b,0x4c,0x55,0x49,0x0d,0x51,0x4f,
        0x25,0x27,0x26,0x28,0x60,0x61,0x62,0x63,0x64,0x65,0x67,0x66,0x75,0x76)
    valid=b'S2K1'+struct.pack('<I',0)+struct.pack('<27I',*defaults)
    cases={'missing':None,'valid_keyboard':valid,'valid_controllers':valid[:4]+struct.pack('<I',1)+valid[8:],
        'truncated':valid[:41],'wrong_magic':b'BAD!'+valid[4:],'trailing_byte':valid+b'!'}
    rows=summaries()[row['language']]
    reports=[]
    for label,packet in cases.items():
        changed=bytearray(raw)
        if packet is not None:
            struct.pack_into('<I',changed,offset(data+0x600),len(packet))
            changed[offset(data+0x620):offset(data+0x620)+len(packet)]=packet
        failed=[]
        for i,(name,item) in enumerate(rows.items()):
            h,ptr=struct.unpack_from('<II',changed,offset(data+table_offset)+i*8)
            if h!=name_hash(name):failed.append(name);continue
            try:
                po=offset(ptr)
                text=bytes(changed[po:po+512]).split(b'\0')[0].decode('utf8')
            except Exception:failed.append(name);continue
            if text!=item['text']:failed.append(name)
        reports.append(dict(settings=label,failed_skins=failed))
    return reports


def main():
    previous=json.loads((HERE/'prior-builds.json').read_text())
    result=[]
    for row in previous:
        reports=check((HERE/f'prior-{row["language"]}.exe').read_bytes(),row,0x600)
        valid=next(r for r in reports if r['settings']=='valid_keyboard')['failed_skins']
        assert valid==['shank','explorer','hobo','luchador','yakuza','boogie','horror','cesar','evil','corina','bubbles','superheroine','track','sunshine']
        result.append(dict(language=row['language'],old_reproduction=reports))
    (HERE/'startup-reproduction.json').write_text(json.dumps(dict(reproduced=True,cases=result),indent=2)+'\n')
    print('Old boot writes reproduce missing Shank, Explorer and every later/female skin in EN and CHS.')
    builds=WORK/'story-coop-v28-trait-descriptions'
    current=json.loads((builds/'builds.json').read_text())
    fixed=[]
    for row in current:
        reports=check((builds/'dev'/f'shank2-story-coop-{row["language"]}.exe').read_bytes(),row,TABLE_OFFSET)
        assert all(not r['failed_skins'] for r in reports)
        fixed.append(dict(language=row['language'],sha256=row['sha256'],table_offset=hex(TABLE_OFFSET),cases=reports))
    (HERE/'startup-validation.json').write_text(json.dumps(dict(passed=True,cases=fixed),indent=2)+'\n')
    print('Fixed EN/CHS tables survive all 6 settings-read scenarios, preserving all 17 rows.')


if __name__=='__main__':main()
