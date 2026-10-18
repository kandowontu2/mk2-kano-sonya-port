"""Encode selected generated morph cells as editable native indexed sources."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PORT=Path(__file__).resolve().parent
OUT=PORT/'assets/morph'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

def main():
    assert not OUT.exists(),'Never overwrite authored indexed sources'
    paths=[PORT/'assets/morph_draft'/name for name in ('morph-atlas.png','morph-atlas-v2.png')]
    images=[Image.open(path).convert('RGBA') for path in paths]
    assert all(image.size==(1536,1024) for image in images)
    outputs={};frames=[];palettes={}
    preview=Image.new('RGB',(480,320),(35,35,40))
    for row,(actor,ground) in enumerate((('kano',131),('sonya',132))):
        tiles=[]
        for phase in range(3):
            selected=1 if phase==0 else 0
            box=(phase*512,row*512,(phase+1)*512,(row+1)*512)
            tile=images[selected].crop(box)
            bounds=tile.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
            assert bounds and 0<bounds[0]<bounds[2]<512 and 0<bounds[1]<bounds[3]<512
            tiles.append((tile.crop(bounds),selected,box,bounds))
        scale=ground/tiles[-1][0].height
        samples=[tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS) for tile,_,_,_ in tiles]
        opaque=[(r,g,b) for sample in samples for r,g,b,a in sample.getdata() if a>=128]
        strip=Image.new('RGB',(len(opaque),1));strip.putdata(opaque)
        quantized=strip.quantize(colors=63,method=Image.Quantize.MEDIANCUT)
        raw=quantized.getpalette()
        # Store exact hardware 5-bit RGB words; quantize against those words.
        colors=[0]+[((raw[i*3]>>3)<<10)|((raw[i*3+1]>>3)<<5)|(raw[i*3+2]>>3) for i in range(63)]
        rgb=[((c>>10&31)*255//31,(c>>5&31)*255//31,(c&31)*255//31) for c in colors]
        palettes[actor]=colors
        cache={}
        for phase,(sample,(_,selected,box,bounds)) in enumerate(zip(samples,tiles)):
            w,h=sample.size;indices=[]
            for r,g,b,a in sample.getdata():
                if a<128:indices.append(0);continue
                key=(r,g,b)
                if key not in cache:cache[key]=min(range(1,64),key=lambda i:sum((key[c]-rgb[i][c])**2 for c in range(3)))
                indices.append(cache[key])
            name=f'{actor}_morph{phase}.pgm'
            payload=(f'P2\n# Native morph palette indices; zero transparent.\n{w} {h}\n63\n'+'\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n').encode('ascii')
            outputs[name]=payload
            rendered=Image.new('RGB',(w,h));rendered.putdata([rgb[i] if i else (35,35,40) for i in indices])
            preview.paste(rendered,(phase*160+(160-w)//2,row*160+150-h))
            frames.append(dict(actor=actor,phase=phase,file=name,SHA256=sha(payload),width=w,height=h,
                xOffset=w//2,yOffset=h-ground,ground=ground,sourceScale=scale,
                sourceAsset=str(paths[selected].relative_to(PORT)),sourceAssetSHA256=sha(paths[selected].read_bytes()),
                cellRectangle=box,alpha128Bounds=bounds,sourceRGBA_SHA256=sha(images[selected].crop(box).tobytes()),
                paletteLabel=f'ks_{actor}_morph_palette',nativeFacingQualified=False))
    OUT.mkdir()
    for name,payload in outputs.items():(OUT/name).write_bytes(payload)
    preview.save(OUT/'indexed-preview.png')
    report=dict(frames=frames,palettes=palettes,transparentIndex=0,maximumIndex=63,
        originalFourLaterFramesRetained=True,firstFramesFromTargetedRevision=True,
        commonScalePerActor=True,groundByActor=dict(kano=131,sonya=132),linkedIntoROM=False,
        finalVisualAcceptance=False,runtimeVerified=False,releaseReady=False)
    (OUT/'MORPH_SOURCES.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Encoded six candidate morph frames; not linked or runtime accepted.')

if __name__=='__main__':main()
