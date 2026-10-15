"""Assemble unaltered actual selection/live screenshots for visual review."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
import verify_natural_mirror_v1144 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1145_natural_mirror_actual_contacts'
if OUT.exists():raise ValueError('Never replace actual-scene contact evidence')
report_path=ROOT/'audit_v1144_natural_mirror_selection_checked/report.json'
report=json.loads(report_path.read_text());assert report['passed'] and len(report['cases'])==6
pins={str(report_path):proof.digest(report_path)};contacts={};count=0
OUT.mkdir()
for case in report['cases']:
 scenes=sorted((ROOT/case/'snap').glob('*.png'))
 assert len(scenes)==5
 contact=Image.new('RGB',(1200,548),(25,25,25));draw=ImageDraw.Draw(contact)
 for n,path in enumerate(scenes):
  assert proof.digest(path)==report['inputHashes'][str(path)]
  image=Image.open(path).convert('RGB');assert image.size==(400,254)
  x,y=n%3*400,n//3*274
  draw.text((x+3,y+3),path.name,fill='white')
  contact.paste(image,(x,y+20));pins[str(path)]=proof.digest(path);count+=1
 out=OUT/(case.removeprefix('audit_v1143_')+'.png')
 contact.save(out);contacts[case]=str(out);pins[str(out)]=proof.digest(out)
record=dict(candidate=proof.split.CANDIDATE,scope='Thirty unaltered actual cold mirror selection and gameplay captures; all six cases',
 sceneCount=count,contacts=contacts,actualScenePixelsChanged=False,manualVisualReviewComplete=False,fullPortAccepted=False,inputHashes=pins)
(OUT/'inventory.json').write_text(json.dumps(record,indent=2)+'\n')
print('Saved 6 actual-scene contacts, 30 scenes; visual review pending')
