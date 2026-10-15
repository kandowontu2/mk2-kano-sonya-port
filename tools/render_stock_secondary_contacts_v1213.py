"""Contact sheets of unaltered real captures; no synthesized game pixels."""
import json
from PIL import Image,ImageDraw
import verify_stock_scorpion_secondary_v1212 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1213_stock_secondary_contacts';assert not OUT.exists()
report=json.loads((proof.OUT/'report.json').read_text());assert report['passed']
OUT.mkdir();records=[]
ages=(0,20,30,40,60,70,80,90,100,120,160,200,300,400,500,600)
for key,case in report['cases'].items():
 folder=ROOT/f'audit_v1211_secondary_{key}';start=case['actionFrame']
 scenes=[(f'age {age}',folder/'snap'/f'stock_head_{start}_{age:03d}.png') for age in ages]
 scenes.append(('actual continue at 4080',folder/'snap/continue_4080.png'))
 sheet=Image.new('RGB',(1600,5*274+32),(24,24,24));draw=ImageDraw.Draw(sheet)
 draw.text((8,8),key+' — actual native secondary fatality captures',fill='white')
 entries=[]
 for i,(label,path) in enumerate(scenes):
  x=(i%4)*400;y=32+(i//4)*274
  image=Image.open(path).convert('RGB');assert image.size==(400,254)
  sheet.paste(image,(x,y));draw.text((x+5,y+256),label,fill='white')
  entries.append(dict(label=label,path=str(path),sha256=proof.state.digest(path)))
 file=OUT/(key+'.png');sheet.save(file)
 records.append(dict(case=key,sheet=str(file),sha256=proof.state.digest(file),scenes=entries))
(OUT/'inventory.json').write_text(json.dumps(dict(sceneCount=102,cases=records,actualUnalteredCaptures=True,
 manualVisualReviewComplete=False,fullPortAccepted=False),indent=2)+'\n')
print('Six contact sheets, 102 unaltered actual scenes; manual review pending')
