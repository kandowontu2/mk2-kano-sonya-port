"""Recover authored head rasters as standalone, readable native palette indices.

No legacy driver payload, executable words, or runtime hooks are consumed.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys
from PIL import Image
import import_character_art as art

PORT = Path(__file__).resolve().parent
OUT = PORT / 'assets/heads'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()
SOURCES = {
    'kano': ('art_native_death_v893/kano-heads.png', '69A8B33DE3835AB33627627FDAD410FCB5F29836C1F248ACF5492167077043A2'),
    'sonya': ('art_native_death_v893/sonya-heads.png', 'F5D2E85765F366B4FD530B9F7C58097F5FB0953F9DB436F2D90DAB4A5408D3B9'),
    'diagonals': ('art_native_rolling_heads_v998/sonya-diagonals-135-225-315.png', '3ABABEDEA62905D75B161DC2D26A8424EEC19280B2A6FB9560D10C57B226E17E'),
}

def components(image):
    w, h = image.size
    alpha = image.getchannel('A').tobytes()
    unseen = bytearray(v >= 128 for v in alpha)
    result = []
    for origin in range(w*h):
        if not unseen[origin]:
            continue
        unseen[origin] = 0
        pending = [origin]
        pixels = []
        while pending:
            point = pending.pop()
            pixels.append(point)
            x, y = point % w, point // w
            for ny in range(max(0, y-1), min(h, y+2)):
                for nx in range(max(0, x-1), min(w, x+2)):
                    at = ny*w+nx
                    if unseen[at]:
                        unseen[at] = 0
                        pending.append(at)
        if len(pixels) < 10000:
            continue
        box = (min(p % w for p in pixels), min(p // w for p in pixels),
               max(p % w for p in pixels)+1, max(p // w for p in pixels)+1)
        mask = bytearray(w*h)
        for p in pixels:
            mask[p] = alpha[p]
        isolated = image.copy()
        isolated.putalpha(Image.frombytes('L', (w, h), bytes(mask)))
        result.append((box, isolated.crop(box), len(pixels)))
    return sorted(result, key=lambda p: (p[0][1] // (h//2), p[0][0]))

def main():
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    OUT.mkdir(exist_ok=True)
    parts = {}
    provenance = {}
    for key, (relative, expected) in SOURCES.items():
        raw = (art.ROOT / relative).read_bytes()
        assert sha(raw) == expected
        filename = key + '-source.png'
        (OUT / filename).write_bytes(raw)
        with Image.open(OUT / filename) as source:
            parts[key] = components(source.convert('RGBA'))
        assert len(parts[key]) == (3 if key == 'diagonals' else 7)
        provenance[key] = dict(file=filename, SHA256=expected, originalPath=relative)
    program = (art.ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    report = dict(format='MK2KS-HEAD-PALETTE-INDEX-PGM-1', sources=provenance,
                  transparentIndex=0, maxIndex=63, actors={}, visualAcceptance=False,
                  runtimeVerified=False, fullPortVerified=False)
    preview = Image.new('RGBA', (840, 280), (35, 35, 40, 255))
    for row, (actor, offset) in enumerate((('kano', 0x92bbc), ('sonya', 0x92cf2))):
        colors = struct.unpack_from('<64H', program, offset+4)
        palette = [(0, 0, 0)] + [((v>>10&31)*255//31, (v>>5&31)*255//31, (v&31)*255//31) for v in colors[:63]]
        factor = 27 / parts[actor][0][1].height
        area = parts[actor][0][2] * factor**2
        frames = []
        nearest = {}
        for phase, angle in enumerate((0, 90, 135, 180, 225, 270, 315)):
            if actor == 'kano':
                source_key, index = actor, (0, 6, 5, 4, 3, 2, 1)[phase]
            elif phase in (0, 1, 3, 5):
                source_key, index = actor, {0: 0, 1: 2, 3: 4, 5: 6}[phase]
            else:
                source_key, index = 'diagonals', {2: 0, 4: 1, 6: 2}[phase]
            box, image, source_area = parts[source_key][index]
            scale = (area/source_area)**0.5 if source_key == 'diagonals' else factor
            w, h = max(1, round(image.width*scale)), max(1, round(image.height*scale))
            image = image.resize((w, h), Image.Resampling.LANCZOS)
            indices = []
            for r, g, b, a in image.getdata():
                if a < 128:
                    indices.append(0)
                    continue
                key = (r, g, b)
                if key not in nearest:
                    nearest[key] = min(range(1, 64), key=lambda i: sum((key[c]-palette[i][c])**2 for c in range(3)))
                indices.append(nearest[key])
            filename = f'{actor}_{phase}.pgm'
            text = f'P2\n# Native palette indices, not grayscale luminance.\n{w} {h}\n63\n'
            text += '\n'.join(' '.join(map(str, indices[y*w:(y+1)*w])) for y in range(h))+'\n'
            (OUT / filename).write_text(text, encoding='ascii')
            frames.append(dict(phase=phase, angleClockwise=angle, file=filename,
                               width=w, height=h, xOffset=w//2, yOffset=h//2,
                               fileSHA256=sha((OUT/filename).read_bytes()),
                               indexSHA256=sha(bytes(indices)), source=source_key,
                               sourceComponent=index, sourceBox=box, uniformScale=scale))
            decoded = Image.new('RGBA', (w, h))
            decoded.putdata([(*palette[i], 255) if i else (0, 0, 0, 0) for i in indices])
            preview.alpha_composite(decoded.resize((w*3, h*3), Image.Resampling.NEAREST), (phase*120+5, row*140+10))
        report['actors'][actor] = dict(frames=frames)
    (OUT/'HEAD_SOURCE.json').write_text(json.dumps(report, indent=2)+'\n')
    preview.save(OUT/'palette_preview.png')
    print(json.dumps(dict(frames=14, visualAcceptance=False, runtimeVerified=False)))

if __name__ == '__main__':
    main()
