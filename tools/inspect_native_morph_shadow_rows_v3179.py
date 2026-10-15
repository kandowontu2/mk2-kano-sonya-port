"""Independent compressed-row/native-shadow stepping diagnostic, not full acceptance."""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from inspect_current_cpu_knife_raster_v1975 import data
import verify_native_cpu_ring_erase_v2985


def inspect(folder):
    groups, buffers, *_ = data(folder)
    dmas = {r['event']: r for r in groups['FLOOR_DMA']}
    components = defaultdict(list)
    for component in groups['SHADOW_COMPONENT']:
        assert component['id'] in (6,17,18) and component['owner'] == component['actor'], 'Actual imported native fighter owns shadow component'
        assert component['row'] == component['cache'] + component['component']*112, 'Actual component belongs to native actor cache'
        components[component['frame'], component['row']].append(component)
    shadow_events = {r['event'] for r in groups['FLOOR_DMA'] if r['pc'] in (0xff8015a0,0xff801610) and r['command'] & 15 == 8}
    assert shadow_events == {r['event'] for r in groups['SHADOW_COMPONENT']}, 'Every imported shadow copy has exact owned component evidence'
    checked = 0
    failures = []
    oversized_rows = []
    identities = set()
    for (frame, row), copies in components.items():
        first = copies[0]
        source, command, width, height = (first[k] for k in ('first_source', 'command', 'width', 'height'))
        identities.add((first['slot'], first['id']))
        key = f'{source:08X}_{command | 0x8002:04X}_{width}_{height}'
        record = buffers.get(key)
        if record is None:
            failures.append(dict(frame=frame, row=row, reason='Missing independently observed complete body stream', key=key))
            continue
        raw = bytes.fromhex(record['data'])
        bit = record['offset'] % 8
        start = bit
        starts = []
        bpp = (command >> 12) & 7 or 8
        assert bpp == 6 and command & 0x80, 'Original native routine assumes six-bit compressed imported rows'
        for y in range(height):
            starts.append(source + bit - start)
            assert bit + 8 <= len(raw)*8, 'Complete row header observation'
            header = (int.from_bytes(raw[bit//8:bit//8+2], 'little') >> (bit%8)) & 255
            pre = (header & 15) << ((command >> 8) & 3)
            post = (header >> 4) << ((command >> 10) & 3)
            if pre + post > width:
                oversized_rows.append(dict(frame=frame, row=row, y=y, width=width, pre=pre, post=post))
            bit += 8 + bpp * max(0, width-pre-post)
            assert bit <= len(raw)*8, 'Complete body stream observation'
        indices = list(range(0, 4*(height//4), 4))
        indices.append(indices[-1])
        expected_sources = [starts[y] for y in indices]
        actual = [dmas[r['event']] for r in copies]
        expected_command = command | 0x8008
        first_y = actual[0]['y']
        expected = [(s, expected_command, width, 1, actual[0]['x'], (first_y+i)&511,
                     0, 15, 0xff801610 if i == len(indices)-1 else 0xff8015a0)
                    for i, s in enumerate(expected_sources)]
        observed = [tuple(d[k] for k in ('source','command','width','height','x','y','palette','color','pc')) for d in actual]
        if observed != expected:
            failures.append(dict(frame=frame,row=row,reason='Native row sources/count/coordinates/command differ',
                                 expected=expected,observed=observed))
        else:
            checked += len(actual)
    return dict(scope='Native compressed-row stepping and copy cadence only; full geometry/grounding acceptance pending',
                components=len(components), checked_copies=checked, identities=sorted(identities),
                oversized_rows=oversized_rows, failures=failures,
                rowStreamVerified=bool(components) and not failures and not oversized_rows,
                fullPortAcceptance=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.folder), indent=2))
