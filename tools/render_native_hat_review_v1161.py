"""Unaltered actual native hat timeline and source-bound body/head captures."""
import json
from PIL import Image,ImageDraw
import verify_native_hat_kill_v1158 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1161_native_hat_actual_contacts'
if OUT.exists():raise ValueError('Preserve actual-scene review evidence')
path=ROOT/'audit_v1158_native_hat_kill_checked/report.json';report=json.loads(path.read_text())
assert report['passed'] and len(report['cases'])==6
OUT.mkdir();pins={str(path):proof.digest(path)};contacts={};count=0
for case,data in report['cases'].items():
 log=(ROOT/case/'run.log').read_text(encoding='utf-8-sig')
 start=int(next(r for tag,r in proof.rows(log,'MK2_STOCK_HEAD_V921') if tag=='ACTION')['frame'])
 scenes=[(f"native {m['kind']} pose{m['pose']} score{m['score']:.3f}",proof.Path(m['picture'])) for m in data['pixelMatches']]
 for age in (0,20,30,40,50,60,100,150,200,300,400,500,600):
  scenes.append(('actual timeline age'+str(age),ROOT/case/'snap'/f'stock_head_{start}_{age:03d}.png'))
 height=((len(scenes)+3)//4)*274
 contact=Image.new('RGB',(1600,height),(25,25,25));draw=ImageDraw.Draw(contact)
 for n,(caption,picture) in enumerate(scenes):
  assert proof.digest(picture)==report['inputHashes'][str(picture)]
  image=Image.open(picture).convert('RGB');assert image.size==(400,254)
  x,y=n%4*400,n//4*274;draw.text((x+3,y+3),caption,fill='white');contact.paste(image,(x,y+20))
  pins[str(picture)]=proof.digest(picture);count+=1
 target=OUT/(case.removeprefix('audit_v1156_')+'.png');contact.save(target);pins[str(target)]=proof.digest(target)
 contacts[case]=dict(path=str(target),scenes=len(scenes),sourceBoundScenes=len(data['pixelMatches']),selectedTimelineScenes=13)
record=dict(candidate=proof.split.CANDIDATE,scope='All 50 own source-bound native head/body captures plus 78 selected actual timelines, six normal Dead Pool cases',
 sceneCount=count,contacts=contacts,actualScenePixelsChanged=False,manualVisualReviewComplete=False,fullPortAccepted=False,inputHashes=pins)
assert count==128
(OUT/'inventory.json').write_text(json.dumps(record,indent=2)+'\n');print('Saved 6 actual contacts / 128 scenes; manual review pending')
