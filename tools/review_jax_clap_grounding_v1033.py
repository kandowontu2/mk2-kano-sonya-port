"""Diagnostic contact sheets from actual presented frames, not replacement art."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
import verify_jax_clap_positions_v1030 as proof

OUT=proof.ROOT/'audit_v1033_jax_clap_visual_review'
if OUT.exists():raise ValueError('Preserve visual evidence')
OUT.mkdir()
review={'scope':'actual normal Dead Pool Jax primary against both true victims/slots',
        'manuallyReviewed':False,'fullPortAccepted':False,'sheets':[]}
for case in proof.CASES:
    text=(proof.ROOT/case/'run.log').read_text(encoding='utf-8-sig')
    action=next(r for t,r in proof.rows(text,'MK2_STOCK_HEAD_V921') if t=='ACTION')
    start=int(action['frame'])
    sheet=Image.new('RGB',(1600,810),(30,30,35));draw=ImageDraw.Draw(sheet)
    files=[]
    for index,age in enumerate((0,40,60,80,110,120,150,180,200,260,400,600)):
        path=proof.ROOT/case/'snap'/f'stock_head_{start}_{age:03d}.png'
        image=Image.open(path).convert('RGB');assert image.size==(400,254)
        x,y=index%4*400,index//4*270
        sheet.paste(image,(x,y+16));draw.text((x+3,y+2),f'{case}: age {age}',fill='white')
        files.append(str(path))
    filename=case+'.png';sheet.save(OUT/filename)
    review['sheets'].append({'case':case,'file':filename,'actualSceneFiles':files})
(OUT/'review.json').write_text(json.dumps(review,indent=2)+'\n')
print(json.dumps({'output':str(OUT),'actualScenes':48,'manuallyReviewed':False}))
