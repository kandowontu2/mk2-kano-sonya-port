"""Convert own inflation atlas to editable indexed sources; never touches ROMs."""
import json
import sys
from pathlib import Path
from PIL import Image
from generate_arm_rip_sources import palette, sha

PORT = Path(__file__).resolve().parent
SOURCE = PORT / 'assets/inflation_draft/inflation-atlas-v2.png'
OUT = PORT / 'assets/inflation'


def main():
    repair = sys.argv[1:] == ['--kano-boundary-repair']
    assert not sys.argv[1:] or repair
    output = PORT/'assets/inflation_v3' if repair else OUT
    assert not output.exists(), 'Do not overwrite reviewed sources'
    frames = []
    outputs = {}
    preview = Image.new('RGB', (960, 300), (35, 35, 40))
    with Image.open(SOURCE) as atlas:
        assert atlas.mode == 'RGBA'
        for row, actor in enumerate(('kano', 'sonya')):
            colors, palette_hash = palette(actor)
            rgb = [((v >> 10 & 31)*255//31, (v >> 5 & 31)*255//31,
                    (v & 31)*255//31) for v in colors]
            scale = None
            ground = 131 if actor == 'kano' else 132
            for phase in range(6):
                cell = (round(phase*atlas.width/6), round(row*atlas.height/2),
                        round((phase+1)*atlas.width/6), round((row+1)*atlas.height/2))
                tile = atlas.crop(cell)
                source_asset = SOURCE
                if repair and actor == 'kano' and phase >= 4:
                    source_asset = PORT/'assets/inflation_draft/kano-final-pair.png'
                    with Image.open(source_asset) as pair:
                        assert pair.mode == 'RGBA'
                        column = phase-4
                        cell = (round(column*pair.width/2), 0,
                                round((column+1)*pair.width/2), pair.height)
                        tile = pair.crop(cell)
                bounds = tile.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()
                assert bounds
                crop = tile.crop(bounds)
                if scale is None:
                    scale = ground/crop.height
                frame_scale = ground/crop.height if repair and actor == 'kano' and phase >= 4 else scale
                w, h = round(crop.width*frame_scale), round(crop.height*frame_scale)
                assert 0 < w <= 160 and 0 < h <= 160
                sample = crop.resize((w, h), Image.Resampling.LANCZOS)
                nearest = {}
                pixels = []
                for r, g, b, a in sample.getdata():
                    if a < 128:
                        pixels.append(0)
                        continue
                    key = (r, g, b)
                    if key not in nearest:
                        nearest[key] = min(range(1, 64), key=lambda i:
                            sum((key[c]-rgb[i][c])**2 for c in range(3)))
                    pixels.append(nearest[key])
                feet = [i % w for i in range(max(0, h-4)*w, h*w) if pixels[i]]
                assert feet
                filename = f'{actor}_inflate{phase}.pgm'
                data = (f'P2\n# Own palette indices, zero transparent.\n{w} {h}\n63\n' +
                        '\n'.join(' '.join(map(str, pixels[y*w:(y+1)*w]))
                                  for y in range(h))+'\n').encode('ascii')
                outputs[filename] = data
                rendered = Image.new('RGB', (w, h))
                rendered.putdata([rgb[i] if i else (35, 35, 40) for i in pixels])
                preview.paste(rendered, (phase*160+(160-w)//2, row*150+145-h))
                frames.append(dict(actor=actor, phase=phase, file=filename,
                    SHA256=sha(data), width=w, height=h,
                    xOffset=round((min(feet)+max(feet))/2), yOffset=h-ground,
                    paletteSourceSHA256=palette_hash, sourceCell=cell,
                    alpha128Bounds=bounds, scale=frame_scale,
                    sourceAsset=str(source_asset.relative_to(PORT)),
                    sourceAssetSHA256=sha(source_asset.read_bytes()),
                    touchesCellEdge=any((bounds[0] == 0, bounds[1] == 0,
                        bounds[2] == tile.width, bounds[3] == tile.height))))
    assert len(outputs) == 12
    if repair:
        prior = json.loads((OUT/'INFLATION_SOURCES.json').read_text())
        for frame in frames:
            old = next(f for f in prior['frames'] if (f['actor'], f['phase']) ==
                       (frame['actor'], frame['phase']))
            if not (frame['actor'] == 'kano' and frame['phase'] >= 4):
                assert frame['SHA256'] == old['SHA256'], 'Unrelated pixels changed'
        assert not any(f['touchesCellEdge'] for f in frames)
    output.mkdir()
    for filename, data in outputs.items():
        (output/filename).write_bytes(data)
    preview.save(output/'indexed-preview.png')
    report = dict(format='MK2KS-INFLATION-SOURCE-1', frames=frames,
        atlasSHA256=sha(SOURCE.read_bytes()), transparentIndex=0, maximumIndex=63,
        animationContract='five multipart inflation groups, zero, pop group, zero',
        runtimeVerified=False, pixelAcceptance=False, releaseReady=False)
    if repair:
        report.update(boundaryRepairOnly=True, unchangedOtherFrames=10,
                      priorManifestSHA256=sha((OUT/'INFLATION_SOURCES.json').read_bytes()))
    (output/'INFLATION_SOURCES.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(frames=len(frames), edgeCells=[(f['actor'], f['phase'])
        for f in frames if f['touchesCellEdge']], runtimeVerified=False)))


if __name__ == '__main__':
    main()
