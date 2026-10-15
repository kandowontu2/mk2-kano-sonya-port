"""Diagnostic contact sheets of actual native presented screenshots; no art edits."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
import verify_rolling_heads_v1010 as proof

ROOT=proof.ROOT
OUT=ROOT/'audit_v1011_owned_rolling_head_visual_review'


def main():
    if OUT.exists():raise ValueError('Never overwrite a visual review')
    report=json.loads((ROOT/'audit_v1010_owned_rolling_head_runtime_checked/verification.json').read_text())
    assert report['passed']
    OUT.mkdir();pins={};close=Image.new('RGB',(1568,768),(32,32,38))
    draw=ImageDraw.Draw(close)
    for row,(case,evidence) in enumerate(report['cases'].items()):
        sheet=Image.new('RGB',(1600,1088),(32,32,38));labels=ImageDraw.Draw(sheet)
        pictures=sorted(evidence['pixelMatches'],key=lambda r:(r['kind'],r['pose']))
        log=(ROOT/case/'run.log').read_text(encoding='utf-8-sig')
        action=next(r for tag,r in proof.records(log,'MK2_STOCK_HEAD_V921') if tag=='ACTION')
        start=int(action['frame'])
        pictures += [dict(snapshot=str(ROOT/case/'snap'/f'stock_head_{start}_{age:03d}.png'),kind=f'age{age}',pose='')
                     for age in (0,600)]
        for cell,item in enumerate(pictures):
            path=Path(item['snapshot']);pins[str(path)]=proof.digest(path)
            image=Image.open(path).convert('RGB')
            x,y=cell%4*400,cell//4*272
            sheet.paste(image,(x,y+18));labels.text((x+3,y+3),f'{case}: {item["kind"]}/{item["pose"]}',fill='white')
        sheet.save(OUT/f'{evidence["victim"]}_p{evidence["slot"]}_actual_scenes.png')
        for item in sorted((r for r in evidence['pixelMatches'] if r['kind']=='head'),key=lambda r:r['pose']):
            image=Image.open(item['snapshot']).convert('RGB')
            x,y=item['x'],item['y'];pose=item['pose']
            # Show measured head plus its original screen context, at integer
            # magnification only. These are review images, never game assets.
            box=(max(0,x-8),max(0,y-7),min(400,x+48),min(254,y+34))
            crop=image.crop(box)
            crop=crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST)
            close.paste(crop,(pose*224,row*192+22))
            draw.text((pose*224+2,row*192+3),f'{evidence["victim"]} P{evidence["slot"]} {pose} score{item["score"]:.3f}',fill='white')
    close.save(OUT/'all28_actual_rolling_heads_4x.png')
    (OUT/'input-hashes.json').write_text(json.dumps(pins,indent=2)+'\n')
    print(json.dumps(dict(actualScenes=64,actualHeadCloseups=28,output=str(OUT),fullPortAccepted=False)))


if __name__=='__main__':main()
