"""Paste unaltered real full-render captures for main-agent visual review."""
import json
from PIL import Image,ImageDraw
import verify_stock_secondary_display_v1234 as proof
OUT=proof.ROOT/'audit_v1237_secondary_native_contacts';assert not OUT.exists();OUT.mkdir()
inventory=[]
for key in proof.physical.CASES:
 folder=proof.ROOT/f'audit_v1230_secondary_{key}'
 report_path=proof.ROOT/f'audit_v1234_secondary_{key}_render_checked/report.json'
 report=json.loads(report_path.read_text());assert report['passed']
 records=report['replayed']['records'];start=report['originalDetachedAllocation']['frame']-71-report['victimSlot']
 chosen=[min(records,key=lambda r:abs(r['frame']-(start+age))) for age in (2,30,50,74,90,98,120,200,400,528,552)]
 sheet=Image.new('RGB',(1600,3*280),(18,18,18));draw=ImageDraw.Draw(sheet);scenes=[]
 for index,record in enumerate(chosen):
  path=folder/'snap'/record['file'];image=Image.open(path).convert('RGB');assert image.size==(400,254)
  x,y=index%4*400,index//4*280;sheet.paste(image,(x,y+24))
  draw.text((x+5,y+5),f"{key} field +{record['frame']-start}",fill='white')
  scenes.append(dict(path=str(path),sha256=proof.util.digest(path),actualFrame=record['frame']))
 path=folder/'snap/continue_4080.png';image=Image.open(path).convert('RGB');sheet.paste(image,(1200,584));draw.text((1205,565),key+' actual continue',fill='white')
 scenes.append(dict(path=str(path),sha256=proof.util.digest(path),actualFrame=4080))
 output=OUT/(key+'.png');sheet.save(output)
 inventory.append(dict(case=key,sheet=str(output),sha256=proof.util.digest(output),scenes=scenes,
  renderReport=str(report_path),renderReportSHA256=proof.util.digest(report_path)))
(OUT/'inventory.json').write_text(json.dumps(dict(sceneCount=72,cases=inventory,
 actualImagesAltered=False,manualReviewPending=True,fullPortAccepted=False),indent=2)+'\n')
print('72 unaltered actual full-render/continue captures prepared for review')
