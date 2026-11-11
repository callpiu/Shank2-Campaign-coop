"""Read campaign HUD score inputs from the isolated v0.9 test build."""
import argparse
import datetime
import importlib.util
import json
from pathlib import Path
import struct
import time


WORK = Path(r'G:\DeepSeekData\Workspaces\Codex\2026-10-28\shank2-mod-e-steamlibrary-steamapps-common\work')
spec = importlib.util.spec_from_file_location('memory_probe', WORK / 'shank2-story-coop/memory_probe.py')
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)
DIAG = 0x7ff000


def inventory(p, actor):
    head = p.u32(actor + 0x160)
    node = p.u32(head + 4) if head else None
    key = p.u32(0x7db2d4)
    for _ in range(64):
        if not node or node == head or not key:
            break
        value = p.u32(node + 12)
        if value is None:
            break
        if value == key:
            handle = p.u32(node + 16)
            if not handle:
                break
            flag, value = p.u32(handle), p.u32(handle + 4)
            return p.u32(value + 12) if value and flag and p.read(flag, 1) not in (b'', b'\0') else value
        node = p.u32(node + (0 if key < value else 8))
    return None


def sample(p):
    raw = p.read(DIAG, 0x68)
    if len(raw) != 0x68:
        return None
    data = struct.unpack('<26I', raw)
    row = dict(stage=data[1], generation=data[8], players=[])
    if data[1] != 5:
        return row
    for actor in data[3:5]:
        inv = inventory(p, actor) if actor else None
        row['players'].append(dict(actor=hex(actor), inventory=hex(inv or 0),
                                   score=p.u32(inv + 0x50) if inv else None))
    # Avoid treating mixed snapshots during initialization as valid evidence.
    if p.read(DIAG, 0x24) != raw[:0x24]:
        return None
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pid', type=int)
    parser.add_argument('--watch', type=Path)
    parser.add_argument('--seconds', type=int, default=600)
    args = parser.parse_args()
    p = memory.Process(args.pid)
    try:
        if not args.watch:
            print(json.dumps(sample(p), indent=2))
            return
        deadline, previous = time.monotonic() + args.seconds, None
        with args.watch.open('x', encoding='utf-8') as out:
            while time.monotonic() < deadline:
                row = sample(p)
                if row is not None and row != previous:
                    stamp = datetime.datetime.now().astimezone().isoformat()
                    out.write(json.dumps(dict(time=stamp, **row)) + '\n')
                    out.flush()
                    previous = row
                time.sleep(0.10)
    finally:
        p.close()


if __name__ == '__main__':
    main()
