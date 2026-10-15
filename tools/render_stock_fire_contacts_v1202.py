"""Unaltered actual native scenes; no synthesized gameplay art."""
import json
from PIL import Image,ImageDraw
import verify_stock_fire_display_v1201 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1202_stock_fire_contacts'
assert not OUT.exists(),'Preserve contact evidence'
names=(('control_kitana',1),('control_liu',2),('kano',1),('kano',2),('sonya',1),('sonya',2))
ages=tuple(range(0,261,10))+(300,400,500,600)
pins={};contacts={};OUT.mkdir()
for name,side in names:
 report_path=ROOT/f'audit_v1201_fire_{name}_p{side}_render_checked/report.json';report=json.loads(report_path.read_text());assert report['passed'];pins[str(report_path)]=proof.state.digest(report_path)
 case=report['case'];paths=[ROOT/case/'snap'/f"stock_head_{report['nativeAction']}_{age:03d}.png" for age in ages]+[ROOT/case/'snap/continue_4080.png']
 sheet=Image.new('RGB',(1600,274*8),(25,25,25));draw=ImageDraw.Draw(sheet)
 for index,path in enumerate(paths):
  assert proof.state.digest(path)==report['inputHashes'][str(path)];scene=Image.open(path).convert('RGB');assert scene.size==(400,254)
  x,y=(index%4)*400,(index//4)*274;label='actual native age '+str(ages[index]) if index<len(ages) else 'actual continue 4080'
  draw.text((x+3,y+3),label,fill='white');sheet.paste(scene,(x,y+20));pins[str(path)]=proof.state.digest(path)
 target=OUT/f'{name}_p{side}.png';sheet.save(target);pins[str(target)]=proof.state.digest(target);contacts[case]={'path':str(target),'scenes':len(paths)}
 record=None
record=dict(sceneCount=192,contacts=contacts,actualScenePixelsChanged=False,manualVisualReviewComplete=False,allFatalityArtAccepted=False,fullPortAccepted=False,inputHashes=pins)
(OUT/'inventory.json').write_text(json.dumps(record,indent=2)+'\n');print('Saved six actual contacts / 192 scenes')
