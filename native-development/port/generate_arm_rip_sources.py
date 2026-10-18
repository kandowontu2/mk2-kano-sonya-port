"""Compile authored arm-rip drafts into editable own-index PGM source data."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PORT=Path(__file__).resolve().parent
SOURCE=PORT/'assets/arm_rip_draft';OUT=PORT/'assets/arm_rip'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

def palette(actor):
    path=PORT/f'generated_packed/{actor.upper()}ART.ASM'
    text=path.read_text().split(f'ks_{actor}_primary_palette\n',1)[1].split(f'ks_{actor}_alternate_palette\n',1)[0]
    words=[]
    for line in text.splitlines():
        if '.word' not in line:continue
        for token in line.split('.word',1)[1].split(','):
            token=token.strip();words.append(int(token[:-1],16) if token.lower().endswith('h') else int(token))
    assert words[0]==65 and len(words)==66 and words[1]==0
    return words[1:65],sha(path.read_bytes())

def main():
    assert not OUT.exists(),'Do not overwrite authored/reviewed indexed sources'
    manifest=json.loads((SOURCE/'DRAFT_MANIFEST.json').read_text())
    assert manifest['allTwentyFramesHaveTransparentMargins']
    palettes={actor:palette(actor) for actor in ('kano','sonya')}
    scales={};frames=[];outputs={}
    preview=Image.new('RGB',(800,580),(35,35,40))
    for asset_index,asset in enumerate(manifest['assets']):
        path=SOURCE/asset['file'];assert sha(path.read_bytes())==asset['SHA256']
        role='body' if asset['file']=='body-atlas.png' else 'arm'
        with Image.open(path) as atlas:
            assert atlas.mode=='RGBA' and list(atlas.size)==asset['size']
            for frame in asset['frames']:
                actor=frame['actor'];phase=frame['phase'];ground=131 if actor=='kano' else 132
                crop=atlas.crop(frame['cell']).crop(frame['alpha128Bounds'])
                if phase==0:
                    # Whole bodies use own native ground height; detached
                    # components are independently sized, not atlas zoom.
                    scales[actor,role]=(ground/crop.height if role=='body' else (57 if actor=='kano' else 53)/crop.width)
                scale=scales[actor,role];w,h=round(crop.width*scale),round(crop.height*scale)
                assert 0<w<=160 and 0<h<=160
                sample=crop.resize((w,h),Image.Resampling.LANCZOS)
                colors,palette_hash=palettes[actor]
                rgb=[((value>>10&31)*255//31,(value>>5&31)*255//31,(value&31)*255//31) for value in colors]
                nearest={};indices=[];error=0;opaque=0
                rgba=sample.tobytes()
                for offset in range(0,len(rgba),4):
                    r,g,b,a=rgba[offset:offset+4]
                    if a<128:indices.append(0);continue
                    key=(r,g,b)
                    if key not in nearest:
                        nearest[key]=min(range(1,64),key=lambda index:sum((key[channel]-rgb[index][channel])**2 for channel in range(3)))
                    index=nearest[key];indices.append(index);opaque+=1
                    error+=sum((key[channel]-rgb[index][channel])**2 for channel in range(3))
                assert opaque and min(indices)>=0 and max(indices)<=63
                if role=='body':
                    feet=[index%w for index in range(max(0,h-4)*w,h*w) if indices[index]]
                    assert feet
                    xo=round((min(feet)+max(feet))/2);yo=h-ground
                else:
                    # Initial descriptor origins are calibration seeds based
                    # on the native held-arm coordinate convention only.
                    xo=-31;yo=-90 if actor=='kano' else -76
                filename=f'{actor}_{role}{phase}.pgm'
                pgm=f'P2\n# Own native palette indices; zero is transparent.\n{w} {h}\n63\n'
                pgm+='\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
                outputs[filename]=pgm.encode('ascii')
                row=(0 if actor=='kano' else 1)+(0 if role=='body' else 2)
                cell=Image.new('RGB',(w,h),(35,35,40))
                cell.putdata([rgb[index] if index else (35,35,40) for index in indices])
                preview.paste(cell,(phase*160+(160-w)//2,row*145+140-h))
                frames.append(dict(actor=actor,role=role,phase=phase,file=filename,SHA256=sha(outputs[filename]),
                    width=w,height=h,xOffset=xo,yOffset=yo,ground=ground,paletteSourceSHA256=palette_hash,
                    sourceAsset=asset['file'],sourceCell=frame['cell'],sourceBounds=frame['alpha128Bounds'],
                    scale=scale,opaquePixels=opaque,paletteSquaredErrorPerOpaquePixel=round(error/opaque,3),
                    requiresNativeVisualAndAlignmentReview=True))
    assert len(frames)==len(outputs)==20
    OUT.mkdir()
    for filename,data in outputs.items():(OUT/filename).write_bytes(data)
    preview.save(OUT/'indexed-preview.png')
    report=dict(format='MK2KS-ARM-RIP-PALETTE-INDEX-PGM-1',frames=frames,
        palettesRGB15={actor:values[0] for actor,values in palettes.items()},transparentIndex=0,maxIndex=63,
        draftManifestSHA256=sha((SOURCE/'DRAFT_MANIFEST.json').read_bytes()),
        nativeBodyGrounds={'kano':131,'sonya':132},bodyGroupFramesEach=5,singleArmFramesEach=5,
        paletteConversionDone=True,pixelPerfectVisualAcceptance=False,animationAlignmentAccepted=False,
        gameCodeChanged=False,runtimeVerified=False,releaseReady=False,fullPortVerified=False)
    (OUT/'ARM_RIP_SOURCES.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(files=len(outputs),sourceBytes=sum(map(len,outputs.values())),runtimeVerified=False)))

if __name__=='__main__':main()
