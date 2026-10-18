"""Author editable own-palette ingestion sources along native mouth geometry."""
import json
from pathlib import Path
from PIL import Image
from generate_arm_rip_sources import palette, sha
from ingestion_contract import extract

PORT = Path(__file__).resolve().parent
SOURCE = PORT/'assets/ingestion_draft/ingestion-atlas.png'
OUT = PORT/'assets/ingestion'


def main():
    assert not OUT.exists(), 'Never overwrite reviewed sources'
    geometry = extract()['sequences']['female_ninja']
    columns = [0, 310, 720, 1170, 1536]
    rows = [0, 340, 530, 845, 1024]
    preview = Image.new('RGB', (640, 560), (35,35,40))
    frames, outputs = [], {}
    with Image.open(SOURCE) as atlas:
        assert atlas.mode == 'RGBA' and atlas.size == (1536, 1024)
        for actor_index, actor in enumerate(('kano','sonya')):
            colors, palette_hash = palette(actor)
            rgb = [((v>>10&31)*255//31, (v>>5&31)*255//31, (v&31)*255//31) for v in colors]
            nearest = {}
            for phase in range(8):
                row, col = actor_index*2+phase//4, phase%4
                cell = (columns[col], rows[row], columns[col+1], rows[row+1])
                tile = atlas.crop(cell)
                bounds = tile.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                assert bounds and 0<bounds[0]<bounds[2]<tile.width
                assert 0<bounds[1]<bounds[3]<tile.height
                crop = tile.crop(bounds)
                ref = geometry[phase]
                scale = min(ref['unionWidth']/crop.width, ref['unionHeight']/crop.height)
                w, h = max(1,round(crop.width*scale)), max(1,round(crop.height*scale))
                sample = crop.resize((w,h), Image.Resampling.LANCZOS)
                indices = []
                for r,g,b,a in sample.getdata():
                    if a<128:
                        indices.append(0)
                        continue
                    key=(r,g,b)
                    if key not in nearest:
                        nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-rgb[i][c])**2 for c in range(3)))
                    indices.append(nearest[key])
                assert any(indices) and len(indices)==w*h
                left, top, right, bottom = ref['unionBounds']
                xo=w-right
                yo=round(h/2-(top+bottom)/2)
                filename=f'{actor}_ingest{phase}.pgm'
                data=(f'P2\n# Own palette indices, zero transparent.\n{w} {h}\n63\n'+
                      '\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n').encode('ascii')
                outputs[filename]=data
                rendered=Image.new('RGB',(w,h))
                rendered.putdata([rgb[i] if i else (35,35,40) for i in indices])
                preview.paste(rendered,(col*160+(160-w)//2,row*140+(140-h)//2))
                frames.append(dict(actor=actor,phase=phase,file=filename,SHA256=sha(data),
                    width=w,height=h,xOffset=xo,yOffset=yo,sourceCell=cell,
                    alpha128Bounds=bounds,sourceScale=scale,paletteSourceSHA256=palette_hash,
                    referenceGeometryOnly=ref,originMethod='preserve native right edge and vertical center',
                    nativeFacingNotYetQualified=True))
    assert len(outputs)==16
    OUT.mkdir()
    for filename,data in outputs.items():(OUT/filename).write_bytes(data)
    preview.save(OUT/'indexed-preview.png')
    report=dict(format='MK2KS-INGESTION-SOURCES-1',frames=frames,
        atlasSHA256=sha(SOURCE.read_bytes()),transparentIndex=0,maximumIndex=63,
        allCellsHaveTransparentMargins=True,originalCharacterPixelsCopied=False,
        ownFramesAuthored=True,runtimeVerified=False,visualAcceptance=False,releaseReady=False)
    (OUT/'INGESTION_SOURCES.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(frames=len(frames),transparentMargins=True,runtimeVerified=False)))


if __name__=='__main__':main()
