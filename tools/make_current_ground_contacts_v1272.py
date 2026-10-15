"""Diagnostic contact sheets: unchanged actual v1250 mobility captures only."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
import inspect_current_ground_shadow_v811 as ground
import verify_native_metadata_build_v1254 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1272_current_ground_contacts';assert not OUT.exists();OUT.mkdir()
cases={}
for fighter in ('kano','sonya'):
    for side in (1,2):
        key=f'{fighter}_p{side}';folder=ROOT/f'audit_v1268_ground_shadow_{key}'
        rows=ground.rows((folder/'run.log').read_text(encoding='utf-8-sig'),'SNAP')
        # All37 captured samples are included, no pose cherry-picking/cropping.
        sheet=Image.new('RGB',(1200,((len(rows)+2)//3)*278),(25,25,25));draw=ImageDraw.Draw(sheet);entries=[]
        for n,row in enumerate(rows):
            path=folder/'snap'/row['file'];image=Image.open(path).convert('RGB');assert image.size==(400,254)
            x,y=(n%3)*400,(n//3)*278;sheet.paste(image,(x,y+24))
            draw.text((x+5,y+5),f'{key} age {row["age"]} field {row["frame"]}',fill=(255,255,255))
            entries.append(dict(file=str(path),sha256=current.digest(path),age=row['age'],frame=row['frame']))
        filename=OUT/f'{key}.png';sheet.save(filename)
        cases[key]=dict(sheet=str(filename),sha256=current.digest(filename),entries=entries)
(OUT/'report.json').write_text(json.dumps(dict(candidate=current.CANDIDATE,cases=cases,allActualCapturedScenesIncluded=True,productionArtChanged=False,manualReviewPending=True),indent=2)+'\n')
print('Four contact sheets, all148 actual mobility captures; manual review pending',flush=True)
