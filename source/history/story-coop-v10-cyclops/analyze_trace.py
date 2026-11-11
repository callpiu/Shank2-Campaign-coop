"""Summarize evidence from execution traces without treating bar animation as HP."""
import argparse
import json
from pathlib import Path


def analyze(rows):
    attempts = {}
    for row in rows:
        number = row.get('attempts', 0)
        if number:
            attempts[number] = row
    results = []
    for number, row in sorted(attempts.items()):
        resolved = row.get('resolution_attempt') == number
        damage = row.get('damage_attempt') == number and row.get('native_damage_calls', 0) > 0
        before, after = row.get('hp_before'), row.get('hp_after')
        if not resolved:
            status = 'native_target_lookup_not_observed'
        elif row.get('latest_resolved_target') == '0x0':
            status = 'native_target_lookup_returned_null'
        elif not damage:
            status = 'target_resolved_but_normal_damage_call_not_observed'
        elif before is None or after is None:
            status = 'native_damage_call_observed_without_complete_health_pair'
        elif after < before:
            status = 'native_health_decreased'
        elif after > before:
            status = 'native_health_increased'
        else:
            status = 'native_damage_call_observed_without_immediate_health_change'
        result = dict(attempt=number, status=status, time=row.get('time'))
        if damage:
            result.update(target=row.get('latest_damage_target'), scaled_damage=row.get('scaled_damage'),
                          hp_before=before, hp_after=after, sampled_hp=row.get('sampled_hp'))
        results.append(result)
    return dict(attempts=len(attempts), results=results,
                note='A native HP decrease does not establish that this grab was intended to kill. '
                     'Missing callbacks can also mean an incomplete trace; compare against the observed animation.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.log.read_text(encoding='utf-8').splitlines() if line]
    print(json.dumps(analyze(rows), indent=2))
