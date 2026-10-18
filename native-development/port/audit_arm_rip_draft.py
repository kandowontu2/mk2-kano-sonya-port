"""Read-only PNG validation and bounded draft frame inventory, not ROM art."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PORT=Path(__file__).resolve().parent;OUT=PORT/'assets/arm_rip_draft'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
records=[]
for filename,columns in (('body-atlas.png',(0,460,780,1110,1450,1774)),
                         ('arm-atlas.png',(0,400,770,1120,1470,1774))):
    path=OUT/filename
    with Image.open(path) as image:
        assert image.mode=='RGBA' and image.size==(1774,887)
        alpha=image.getchannel('A');assert alpha.getextrema()==(0,255)
        frames=[]
        for row,actor in enumerate(('kano','sonya')):
            y0,y1=(0,443) if row==0 else (443,887)
            for phase in range(5):
                cell=(columns[phase],y0,columns[phase+1],y1)
                mask=alpha.crop(cell).point(lambda value:255 if value>=128 else 0)
                bounds=mask.getbbox();assert bounds
                margin=min(bounds[0],bounds[1],mask.width-bounds[2],mask.height-bounds[3])
                assert margin>=4,(filename,actor,phase,bounds,cell)
                frames.append(dict(actor=actor,phase=phase,cell=list(cell),alpha128Bounds=list(bounds),
                    opaquePixelCount=mask.histogram()[255],minimumCellMargin=margin,
                    touchesCellEdge=False))
        records.append(dict(file=filename,SHA256=sha(path.read_bytes()),mode='RGBA',size=list(image.size),
            generatedAlphaPreserved=True,frames=frames))
report=dict(format='MK2KS-ARM-RIP-DRAFT-1',assets=records,
    bodyPoses=['stretched arms','arms absent','recoil','knees buckling','collapsed on knees'],
    armPoses=['horizontal','elbow bending','raised diagonal','elbow raised','hanging'],
    generation='built-in image_gen; corrected body costume before saving',
    actorIdentitiesVisuallyReviewed=True,sourceReferenceCostumesCorrected=True,
    expectedNativeBodyPoseCount=5,expectedNativeSingleArmFrameCount=5,
    allTwentyFramesHaveTransparentMargins=True,paletteConversionDone=False,
    nativePixelScaleAccepted=False,animationAlignmentAccepted=False,
    gameCodeChanged=False,runtimeVerified=False,releaseReady=False,fullPortVerified=False)
(OUT/'DRAFT_MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(assets=len(records),frames=sum(len(item['frames']) for item in records),
    totalPNGBytes=sum((OUT/item['file']).stat().st_size for item in records),runtimeVerified=False)))
