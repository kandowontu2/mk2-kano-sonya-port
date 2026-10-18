"""Extract native ingestion geometry and timing, never another actor's pixels."""
import json
import re
from pathlib import Path
from build_inflation_assets import sha
from inventory_character_tables import source_tables

PORT = Path(__file__).resolve().parent
SRC = PORT.parent/'baseline/mk2-rebuild-main/srcp'


def number(token):
    token = token.strip()
    return int(token[:-1], 16) if token.lower().endswith('h') else int(token)


def extract():
    assembly = (SRC/'MKDIE.ASM').read_text()
    tables = source_tables(assembly)
    headers = {}
    text = (SRC/'MKSUCK.TBL').read_text()
    for label, values in re.findall(r'(?m)^(\w+):\s*\n\s*\.word\s+([^\r\n]+)', text):
        values = [number(x) for x in values.split(';', 1)[0].split(',')]
        if len(values) == 4:
            headers[label] = values
    sequences = {}
    for actor, label in (('liu', 'a_lk_sucked_in'), ('female_ninja', 'a_fn_sucked_in')):
        values = [value for row in tables[label]['rows'] for value in row['values']]
        assert values[-1] == '0' and '0' not in values[:-1]
        frames = []
        for phase, group in enumerate(values[:-1]):
            components = [v for row in tables[group]['rows'] for v in row['values']]
            assert components[-1] == '0'
            pieces = [headers[v] for v in components[:-1]]
            assert all(0 < w <= 200 and 0 < h <= 200 for w, h, x, y in pieces)
            left = min(-x for w, h, x, y in pieces)
            top = min(-y for w, h, x, y in pieces)
            right = max(w-x for w, h, x, y in pieces)
            bottom = max(h-y for w, h, x, y in pieces)
            frames.append(dict(phase=phase, group=group, components=components[:-1],
                originalHeaders=pieces, unionBounds=[left, top, right, bottom],
                unionWidth=right-left, unionHeight=bottom-top,
                unionXOffset=-left, unionYOffset=-top))
        sequences[actor] = frames
    assert len(sequences['liu']) == 7 and len(sequences['female_ninja']) == 8
    return dict(format='MK2KS-INGESTION-NATIVE-CONTRACT-1', sequences=sequences,
        sourceSHA256={name: sha((SRC/name).read_bytes()) for name in ('MKDIE.ASM','MKSUCK.TBL')},
        renderer='multipart group pointers terminated by zero', frameDelay=4,
        preAnimationShakeFields=4*2*3,
        sourceGeometryOnly=True, donorPixelsCopied=False,
        ownFramesAuthored=False, ownRuntimeVerified=False)


if __name__ == '__main__':
    report = extract()
    (PORT/'INGESTION_NATIVE_CONTRACT.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(frameCounts={k:len(v) for k,v in report['sequences'].items()},
        firstFemaleBounds=report['sequences']['female_ninja'][0]['unionBounds'],
        lastFemaleBounds=report['sequences']['female_ninja'][-1]['unionBounds'],
        ownRuntimeVerified=False), indent=2))
