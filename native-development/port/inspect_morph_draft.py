"""Read-only alpha/cell audit of the unlinked morph atlas candidate."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PORT=Path(__file__).resolve().parent
path=PORT/'assets/morph_draft/morph-atlas.png'
image=Image.open(path)
assert image.mode=='RGBA' and image.size==(1536,1024)
alpha=image.getchannel('A')
assert alpha.getextrema()[0]==0
frames=[]
for row,actor in enumerate(('kano','sonya')):
    for phase in range(3):
        box=(phase*512,row*512,(phase+1)*512,(row+1)*512)
        mask=alpha.crop(box).point(lambda a:255 if a>=128 else 0)
        bounds=mask.getbbox()
        assert bounds and all((bounds[0]>0,bounds[1]>0,bounds[2]<512,bounds[3]<512))
        frames.append(dict(actor=actor,phase=phase,cellRectangle=box,alpha128Bounds=bounds,
            croppedWidth=bounds[2]-bounds[0],croppedHeight=bounds[3]-bounds[1],
            transparentMarginVerified=True))
report=dict(sourceSHA256=hashlib.sha256(path.read_bytes()).hexdigest().upper(),
    dimensions=list(image.size),genuineTransparency=True,frames=frames,
    cellClippingDetected=False,nativePaletteConversionComplete=False,
    firstIntermediateTransformationAccepted=False,finalCostumeContinuityAccepted=False,
    linkedIntoROM=False,runtimeVerified=False,releaseReady=False)
(path.parent/'MORPH_DRAFT_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
