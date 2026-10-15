"""Contact sheets of unaltered actual mirror finisher captures."""
import json
from PIL import Image,ImageDraw
import verify_natural_mirror_finish_v1169 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1170_natural_mirror_finish_contacts'
assert not OUT.exists(),'Preserve contacts'
report_path=ROOT/'audit_v1169_natural_mirror_finish_checked/report.json'
report=json.loads(report_path.read_text());assert report['passed']
ages=tuple(range(0,241,10))+(300,400,500,600,660,700)
pins={str(report_path):proof.digest(report_path)};contacts={};OUT.mkdir()
for case,data in report['cases'].items():
 sheet=Image.new('RGB',(1600,274*((len(ages)+3)//4)),(25,25,25));draw=ImageDraw.Draw(sheet)
 for i,age in enumerate(ages):
  path=ROOT/case/'snap'/f"mirror_finish_{data['action']}_{age:03d}.png"
  assert proof.digest(path)==report['inputHashes'][str(path)]
  scene=Image.open(path).convert('RGB');assert scene.size==(400,254)
  x,y=(i%4)*400,(i//4)*274;draw.text((x+3,y+3),'actual native age'+str(age),fill='white');sheet.paste(scene,(x,y+20))
  pins[str(path)]=proof.digest(path)
 target=OUT/(case.removeprefix('audit_v1167_')+'.png');sheet.save(target);pins[str(target)]=proof.digest(target)
 contacts[case]=dict(path=str(target),scenes=len(ages))
record=dict(sceneCount=len(ages)*4,contacts=contacts,actualScenePixelsChanged=False,
 manualVisualReviewComplete=False,allFatalityArtAccepted=False,fullPortAccepted=False,inputHashes=pins)
(OUT/'inventory.json').write_text(json.dumps(record,indent=2)+'\n')
print('Saved 4 actual sheets /',record['sceneCount'],'scenes')
