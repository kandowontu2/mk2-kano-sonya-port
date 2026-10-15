"""Unmodified actual scene contacts, plus exact normal image transfer."""
import json,re
from PIL import Image,ImageDraw
import verify_native_arm_palette_v1074 as normal
import verify_arm_palette_controlled_v1075 as alternate
import verify_arm_palette_stock_v1079 as stock
ROOT=normal.ROOT;OUT=ROOT/'audit_v1080_arm_palette_visual_review'
if OUT.exists():raise ValueError('Preserve visual evidence')
OUT.mkdir();pins={};counts={}
for case in alternate.CASES+stock.CASES:
 folder=ROOT/case;text=(folder/'run.log').read_text(encoding='utf-8-sig')
 action=int(re.search(r'_ACTION frame=(\d+)',text)[1])
 sheet=Image.new('RGB',(1200,1056),(35,35,40));draw=ImageDraw.Draw(sheet)
 for index,age in enumerate((0,40,50,90,100,120,140,160,200,260,400,600)):
  path=folder/f'snap/stock_head_{action}_{age:03d}.png'
  picture=Image.open(path).convert('RGB');assert picture.size==(400,254)
  x=index%3*400;y=index//3*264
  sheet.paste(picture,(x,y+10));draw.text((x,y),f'{case} age{age}',fill='white');pins[str(path)]=normal.digest(path)
 sheet.save(OUT/(case+'.png'));counts[case]=12
identical=0
for name in ('kano','sonya'):
 for side in (1,2):
  old=ROOT/f'audit_v1062_jax_{name}_p{side}_invariant_blood/snap'
  current=ROOT/f'audit_v1072_jax_{name}_p{side}_native_palette/snap'
  a={str(p.relative_to(old)):p for p in old.rglob('*.png')};b={str(p.relative_to(current)):p for p in current.rglob('*.png')}
  assert a.keys()==b.keys()
  for key,path in b.items():assert path.read_bytes()==a[key].read_bytes();identical+=1;pins[str(path)]=normal.digest(path)
assert identical==616
(OUT/'inputHashes.json').write_text(json.dumps(pins,indent=2)+'\n')
print(json.dumps({'currentContactScenes':sum(counts.values()),'normalActualPNGsIdenticalToPriorReviewedCases':identical,'contacts':counts},indent=2))
