"""Unmodified actual normal/controlled/stock scenes, not synthetic game art."""
import json
import re
from PIL import Image,ImageDraw
import verify_native_arm_palette_v1074 as normal
import verify_arm_palette_controlled_v1083 as alternate
import verify_arm_palette_stock_v1079 as stock

ROOT=normal.ROOT;OUT=ROOT/'audit_v1088_arm_palette_visual_review'
if OUT.exists():raise ValueError('Preserve visual evidence')
proof=ROOT/'audit_v1087_arm_rng_differential_checked/report.json'
assert json.loads(proof.read_text())['passed']
OUT.mkdir();pins={str(proof):normal.digest(proof)};counts={}
for case in normal.CASES+alternate.CASES+stock.CASES:
    folder=ROOT/case;text=(folder/'run.log').read_text(encoding='utf-8-sig')
    action=int(re.search(r'_ACTION frame=(\d+)',text)[1])
    sheet=Image.new('RGB',(1200,1056),(35,35,40));draw=ImageDraw.Draw(sheet)
    for index,age in enumerate((0,40,50,90,100,120,140,160,200,260,400,600)):
        path=folder/f'snap/stock_head_{action}_{age:03d}.png'
        picture=Image.open(path).convert('RGB');assert picture.size==(400,254)
        x=index%3*400;y=index//3*264
        sheet.paste(picture,(x,y+10));draw.text((x,y),f'{case} age{age}',fill='white')
        pins[str(path)]=normal.digest(path)
    path=OUT/(case+'.png');sheet.save(path);pins[str(path)]=normal.digest(path);counts[case]=12
    if case not in normal.CASES:
        # Exact reuse of the six contacts already seen from failed1080. Its
        # failed full-image-transfer assertion is preserved, never relabelled.
        prior=ROOT/'audit_v1080_arm_palette_visual_review'/path.name
        assert path.read_bytes()==prior.read_bytes()
        pins[str(prior)]=normal.digest(prior)
(OUT/'inputHashes.json').write_text(json.dumps(pins,indent=2)+'\n')
(OUT/'review-inventory.json').write_text(json.dumps({
    'actualScenes':sum(counts.values()),'contacts':counts,
    'sixPreviouslyViewedContactsExactlyReused':True,
    'historicalNormalWholeImageEqualityClaimRejected':True,
    'manualReviewStillRequired':True,'fullPortAccepted':False},indent=2)+'\n')
print(json.dumps({'actualScenes':sum(counts.values()),'contacts':counts},indent=2))
