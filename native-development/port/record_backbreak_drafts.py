"""Read-only raster QA and provenance for unintegrated generated art drafts."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PORT=Path(__file__).resolve().parent
OUT=PORT/'assets/backbreak_draft'
records={}
for actor in ('kano','sonya'):
    path=OUT/f'{actor}-backbreak-draft-v1.png'
    with Image.open(path) as image:
        assert image.mode=='RGBA'
        alpha=image.getchannel('A')
        assert alpha.getextrema()==(0,255)
        projection=alpha.getprojection()[0]
        bands=[];start=None
        for x,present in enumerate(projection+[0]):
            if present and start is None:start=x
            if not present and start is not None:
                if x-start>60:bands.append((start,x))
                start=None
        assert len(bands)==3,(actor,bands)
        boxes=[]
        for left,right in bands:
            box=alpha.crop((left,0,right,image.height)).getbbox()
            boxes.append([left+box[0],box[1],left+box[2],box[3]])
        records[actor]={'asset':path.name,'SHA256':hashlib.sha256(path.read_bytes()).hexdigest().upper(),
            'rasterSize':list(image.size),'alphaRange':[0,255],'poseBoundingBoxes':boxes,
            'semiTransparentPixels':sum(alpha.histogram()[1:255]),
            'finalPrompt':'KANO_REFINEMENT_PROMPT.txt' if actor=='kano' else 'SONYA_PROMPT.txt',
            'identityReference':f'../../throw_pose_review/{actor}_throw.png',
            'nativePoseReference':'../../backbreak_part_review/backbreak_candidates.png',
            'nativePaletteVerified':False,'pivotVerified':False,'digitizedStyleAccepted':False}
roster=(PORT/'generated_roster_roots/KSROOT.ASM').read_text()
derived_enabled=all(f'.long ks_{actor}_back_broke ; main 3f' in roster for actor in ('kano','sonya'))
result={'generationMode':'built-in image_gen; no API/CLI fallback',
        'purpose':'Draft three-pose back-break art, not final ROM assets',
        'assets':records,'rasterStructureVerified':True,'rawAtlasUsedDirectly':False,
        'derivedNativeAssetsEnabledInCandidate':derived_enabled,
        'gameplayVerified':False,'fullPortVerified':False}
(OUT/'DRAFT_MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'drafts':list(records),'threeSeparatedAlphaSpritesEach':True,'derivedNativeAssetsEnabledInCandidate':derived_enabled}))
