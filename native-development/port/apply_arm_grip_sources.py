"""Convert only two revised grip poses; preserve all other indexed sources."""
import hashlib
import json
from pathlib import Path
from PIL import Image
from generate_arm_rip_sources import palette

PORT=Path(__file__).resolve().parent;SOURCE=PORT/'assets/arm_rip'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
manifest_path=SOURCE/'ARM_RIP_SOURCES.json';old=manifest_path.read_bytes();manifest=json.loads(old)
assert 'gripRevision' not in manifest
draft=PORT/'assets/arm_rip_draft/body-grip-atlas.png'
for frame in manifest['frames']:assert sha((SOURCE/frame['file']).read_bytes())==frame['SHA256']
revised=[]
with Image.open(draft) as atlas:
    assert atlas.mode=='RGBA' and atlas.size==(1774,887)
    for row,actor in enumerate(('kano','sonya')):
        cell=(0,0,460,443) if row==0 else (0,443,460,887)
        image=atlas.crop(cell);bounds=image.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
        assert bounds and min(bounds[:2])>=4 and bounds[2]<456 and bounds[3]<440
        crop=image.crop(bounds);ground=131 if actor=='kano' else 132;scale=ground/crop.height
        w,h=round(crop.width*scale),ground
        colors,palette_hash=palette(actor)
        rgb=[((value>>10&31)*255//31,(value>>5&31)*255//31,(value&31)*255//31) for value in colors]
        rgba=crop.resize((w,h),Image.Resampling.LANCZOS).tobytes();indices=[];nearest={}
        for at in range(0,len(rgba),4):
            r,g,b,a=rgba[at:at+4]
            if a<128:indices.append(0);continue
            key=r,g,b
            if key not in nearest:nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-rgb[i][c])**2 for c in range(3)))
            indices.append(nearest[key])
        feet=[i%w for i in range((h-4)*w,h*w) if indices[i]];assert feet
        xo=round((min(feet)+max(feet))/2);filename=f'{actor}_body0_grip.pgm'
        path=SOURCE/filename;assert not path.exists()
        pgm=f'P2\n# Own revised grip-pose palette indices; zero transparent.\n{w} {h}\n63\n'
        pgm+='\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
        path.write_text(pgm,encoding='ascii')
        frame=next(frame for frame in manifest['frames'] if frame['actor']==actor and frame['role']=='body' and frame['phase']==0)
        prior=dict(frame)
        frame.update(file=filename,SHA256=sha(path.read_bytes()),width=w,height=h,xOffset=xo,yOffset=0,
            sourceAsset=draft.name,sourceCell=list(cell),sourceBounds=list(bounds),scale=scale,
            opaquePixels=sum(index!=0 for index in indices),paletteSourceSHA256=palette_hash,
            priorFrame=prior,gripPoseRevised=True)
        frame.pop('paletteSquaredErrorPerOpaquePixel',None)
        revised.append(dict(actor=actor,width=w,height=h,xOffset=xo,sourceBounds=list(bounds)))
manifest.update(gripRevision=dict(priorManifestSHA256=sha(old),draftSHA256=sha(draft.read_bytes()),
    changedFrames=2,unchangedFrames=18,pose='Both arms toward opponent, hands lowered to waist',
    runtimeVisualAcceptance=False))
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(revised=revised,otherIndexedSourcesUnchanged=18,runtimeVerified=False)))
