"""One-time lossless migration of portrait data out of the old player archive."""
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]
DEST=PORT/'assets/selector_source'
SEED=ROOT/'release_mk2_kano_sonya_20261015_player/MK2_Kano_Sonya_20261015_PLAYER.zip'
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
assert not DEST.exists(),'Never overwrite portrait source assets'
assert sha(SEED.read_bytes())=='3B6E59E9998EA2D3B03F0AFE8470DA4F98E417FFD2B6DFBE3D3C3DDC7C2ED342'
with zipfile.ZipFile(SEED) as archive:
    with zipfile.ZipFile(io.BytesIO(archive.read('MK2_Kano_Sonya/roms/mk2ks.zip'))) as rom:
        ui=rom.read('mk2ks.ui')
assert ui[:4]==b'KSU4'
width,height=ui[4:6];colors=struct.unpack_from('<H',ui,6)[0]
assert width and height and 0<colors<=128
DEST.mkdir()
actors={}
for index,actor in enumerate(('kano','sonya')):
    at=8+index*(colors*2+width*height)
    palette=list(struct.unpack_from(f'<{colors}H',ui,at))
    pixels=ui[at+colors*2:at+colors*2+width*height]
    assert len(pixels)==width*height and max(pixels)<colors
    pgm=f'P2\n# Palette indices, not luminance. Original portrait pixels unchanged.\n{width} {height}\n{colors-1}\n'
    pgm+='\n'.join(' '.join(map(str,pixels[y*width:(y+1)*width])) for y in range(height))+'\n'
    data=pgm.encode('ascii');(DEST/f'{actor}.pgm').write_bytes(data)
    actors[actor]=dict(file=f'{actor}.pgm',fileSHA256=sha(data),indicesSHA256=sha(pixels),paletteRGB15=palette)
report=dict(format='MK2KS-SELECTOR-INDEXED-1',width=width,height=height,colors=colors,actors=actors,
    legacyUI_SHA256=sha(ui),legacyPortraitPrefixSHA256=sha(ui[:8+2*(colors*2+width*height)]),
    losslessPixelMigration=True,newArtCreated=False)
(DEST/'SOURCE.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(width=width,height=height,colors=colors,actors=list(actors),losslessPixelMigration=True),indent=2))
