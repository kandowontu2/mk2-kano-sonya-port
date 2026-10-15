"""Contact sheets of unmodified encoded art and actual native screenshots."""
import json,re,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v1049_arm_rip_visual_review'
if OUT.exists():raise ValueError('Preserve review evidence')
OUT.mkdir();pins={}
sheet=Image.new('RGBA',(1000,1440),(35,35,40,255));draw=ImageDraw.Draw(sheet)
for fighter,name in enumerate(('kano','sonya')):
 for kind_index,kind in enumerate(('body','arms')):
  for costume_index,costume in enumerate(('normal','alternate')):
   row=fighter*4+kind_index*2+costume_index
   for pose in range(5):
    path=ROOT/f'audit_v1043_owned_arm_rip_encoding/{name}-{kind}-{pose}-{costume}.png'
    image=Image.open(path).convert('RGBA');x=pose*200;y=row*180
    draw.text((x+2,y+2),f'{name} {kind}{pose} {costume}',fill='white')
    sheet.alpha_composite(image,(x+(200-image.width)//2,y+175-image.height))
    pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
sheet.save(OUT/'all-encoded-poses.png')
for name in ('kano','sonya'):
 for side in (1,2):
  folder=ROOT/f'audit_v1046_jax_{name}_p{side}_owned_arms'
  text=(folder/'run.log').read_text(encoding='utf-8-sig')
  action=int(re.search(r'_ACTION frame=(\d+)',text)[1])
  sheet=Image.new('RGB',(1200,1056),(35,35,40));draw=ImageDraw.Draw(sheet)
  for index,age in enumerate((0,40,50,90,100,120,140,160,200,260,400,600)):
   path=folder/f'snap/stock_head_{action}_{age:03d}.png'
   image=Image.open(path).convert('RGB');assert image.size==(400,254)
   x=index%3*400;y=index//3*264
   sheet.paste(image,(x,y+10));draw.text((x,y),f'{name} victimP{side} original age{age}',fill='white')
   pins[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest().upper()
  sheet.save(OUT/f'{name}-p{side}-actual.png')
(OUT/'inputHashes.json').write_text(json.dumps(pins,indent=2)+'\n')
print(OUT)
