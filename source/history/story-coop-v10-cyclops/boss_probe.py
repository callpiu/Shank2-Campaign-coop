"""Read the latest scoped Cyclops attack attempt from the isolated trace build."""
import argparse
import json
import math
import struct
import time
import datetime
from pathlib import Path

from score_probe import memory


def number(word):
    value = struct.unpack('<f', struct.pack('<I', word))[0]
    return value if math.isfinite(value) else None


def sample(process):
    for _ in range(5):
        raw = process.read(0x7ff900, 60)
        if len(raw) != 60 or raw[:4] != b'CYCP':
            raise RuntimeError('The selected process is not the Cyclops trace build.')
        if raw == process.read(0x7ff900, 60):
            break
    else:
        raise RuntimeError('The trace changed while sampling; read again after pausing the game.')
    (_, attempts, actor, generation, resolves, resolved, hits, attacker, target,
     scaled_damage, hp_before, hp_after, _, resolve_attempt, damage_attempt) = struct.unpack('<15I', raw)
    row = dict(attempts=attempts, actor=hex(actor), generation=generation,
                target_resolutions=resolves, resolution_attempt=resolve_attempt, latest_resolved_target=hex(resolved),
                native_damage_calls=hits, damage_attempt=damage_attempt, latest_damage_attacker=hex(attacker),
                latest_damage_target=hex(target), scaled_damage=number(scaled_damage) if hits else None,
                hp_before=number(hp_before) if hits else None, hp_after=number(hp_after) if hits else None)
    # Sample delayed health outside the game. No calls are injected and a stale
    # actor/component from a prior retry is never accepted as a live Boss.
    component = struct.unpack('<15I', raw)[12]
    if (target and component and process.u32(0x7ff004) == 5
            and process.u32(0x7ff020) == generation
            and process.u32(component + 8) == target
            and process.u32(component) == 0x758e94):
        current = process.u32(component + 0xa0)
        if current is not None:
            row['sampled_hp'] = number(current)
    return row


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pid', type=int)
    parser.add_argument('--watch', type=Path)
    parser.add_argument('--seconds', type=int, default=1800)
    args = parser.parse_args()
    p = memory.Process(args.pid)
    try:
        if not args.watch:
            print(json.dumps(sample(p), indent=2))
        else:
            end, previous = time.monotonic() + args.seconds, None
            with args.watch.open('x', encoding='utf-8') as out:
                while time.monotonic() < end:
                    try:
                        row = sample(p)
                    except RuntimeError:
                        if not p.read(0x7ff900, 4):
                            break
                        time.sleep(.04)
                        continue
                    if row != previous:
                        out.write(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(), **row)) + '\n')
                        out.flush()
                        previous = row
                    time.sleep(.04)
    finally:
        p.close()
