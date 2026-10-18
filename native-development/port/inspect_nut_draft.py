"""Read-only alpha/cell inspection of generated nut-punch draft art."""
import json
from PIL import Image
from generate_head_sources import PORT,sha
folder=PORT/'assets/nut_draft';path=folder/'kano-nut-draft-v1.png'
assert sha(path.read_bytes())=='777E2840EC67B422754F5D8BB36D06BB893C86FE4212C47FF1F1F61AC1BFE028'
with Image.open(path) as image:
    assert image.mode=='RGBA'
    w,h=image.size;frames=[]
    for phase in range(2):
        cell=image.crop((phase*w//2,0,(phase+1)*w//2,h))
        box=cell.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
        assert box
        frames.append(dict(phase=phase,cell=[phase*w//2,0,(phase+1)*w//2,h],
            alpha128Bounds=box,touchesCellEdge=box[0]==0 or box[1]==0 or box[2]==cell.width or box[3]==h))
result=dict(format='MK2KS-NUT-DRAFT-1',asset=path.name,SHA256=sha(path.read_bytes()),
    generationMode='built-in image_gen',promptFile='NUT_PROMPT.txt',referenceAsset='../backbreak_draft/kano-backbreak-draft-v1.png',
    frames=frames,visualAcceptance=False,runtimeVerified=False,fullPortVerified=False)
(folder/'DRAFT_MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
