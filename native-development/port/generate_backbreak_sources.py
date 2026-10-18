"""Compile selected draft rasters to readable native-palette index sources.

Deterministic ROM-format preparation, not a replacement for art/runtime QA.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys
from PIL import Image
import import_character_art as art

PORT=Path(__file__).resolve().parent
OUT=PORT/'assets/backbreak'
assert not OUT.exists() or '--refresh-generated' in sys.argv
OUT.mkdir(exist_ok=True)
draft=PORT/'assets/backbreak_draft'
manifest=json.loads((draft/'DRAFT_MANIFEST.json').read_text())
program=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
def rgb(word):return ((word>>10&31)*255//31,(word>>5&31)*255//31,(word&31)*255//31)
result={'format':'MK2KS-BACKBREAK-PALETTE-INDEX-PGM-1','transparentIndex':0,'maxIndex':63,
        'alphaThreshold':128,'uniformRasterScale':0.2,'nativePaletteVerified':False,
        'visualAcceptance':False,'runtimeVerified':False,'actors':{}}
preview=Image.new('RGBA',(480,200),(35,35,35,255))
for row,(actor,offset) in enumerate((('kano',0x92bbc),('sonya',0x92cf2))):
    record=manifest['assets'][actor]
    source=draft/record['asset']
    assert sha(source.read_bytes())==record['SHA256']
    colors=struct.unpack_from('<64H',program,offset+4)
    # The native imported body palette includes transparent index0, then colors.
    palette=[(0,0,0)]+[rgb(value) for value in colors[:63]]
    frames=[];nearest={}
    with Image.open(source) as atlas:
        for phase,box in enumerate(record['poseBoundingBoxes']):
            mask=atlas.getchannel('A').point(lambda value:255 if value>=128 else 0)
            visible=mask.crop(box).getbbox()
            assert visible
            box=[box[0]+visible[0],box[1]+visible[1],box[0]+visible[2],box[1]+visible[3]]
            w=max(1,round((box[2]-box[0])/5));h=max(1,round((box[3]-box[1])/5))
            pixels=atlas.crop(box).resize((w,h),Image.Resampling.NEAREST)
            indices=[]
            for red,green,blue,alpha in pixels.getdata():
                if alpha<128:indices.append(0);continue
                key=(red,green,blue)
                if key not in nearest:
                    nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-palette[i][c])**2 for c in range(3)))
                indices.append(nearest[key])
            assert max(indices)<=63 and any(indices)
            filename=f'{actor}_{phase}.pgm'
            text=f'P2\n# Native palette indices, not grayscale luminance.\n{w} {h}\n63\n'
            text+='\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
            (OUT/filename).write_text(text,encoding='ascii')
            frame={'phase':phase,'file':filename,'width':w,'height':h,
                   'xOffset':(28,46,50)[phase],'yOffset':(-30,-40,-64)[phase],
                   'fileSHA256':sha((OUT/filename).read_bytes()),'indexSHA256':sha(bytes(indices))}
            frame['opaqueSourceBox']=box
            frames.append(frame)
            image=Image.new('RGBA',(w,h))
            image.putdata([(*palette[i],255) if i else (0,0,0,0) for i in indices])
            preview.alpha_composite(image,(phase*160+10,row*100+10))
    result['actors'][actor]={'sourceDraftSHA256':record['SHA256'],'frames':frames,
                            'pivotBasis':'Native three-pose reference bounding origins; calibration pending'}
(OUT/'BACKBREAK_SOURCE.json').write_text(json.dumps(result,indent=2)+'\n')
preview.resize((960,400),Image.Resampling.NEAREST).save(OUT/'palette_preview.png')
print(json.dumps({'frames':6,'nativeIndexRange':[0,63],'runtimeVerified':False}))
