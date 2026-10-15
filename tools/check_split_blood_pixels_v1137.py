"""Measured native cut-pixel scores, unaltered actual scene contacts.

Explicitly retain original native foreground occlusion/viewport clipping.
Never create a simulated scene, relocate sprites or infer unseen pixels.
"""
import hashlib,json,struct
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import verify_native_split_blood_v1133 as proof

ROOT=proof.ROOT
OUT=ROOT/'audit_v1137_actual_split_blood_pixels'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def blood_score(picture,mask,indices,palette,dma):
    pixels=np.asarray(Image.open(picture).convert('RGB'))
    flip=bool(int(dma['command'],16)&16)
    if flip:indices,mask=indices[:,::-1],mask[:,::-1]
    h,w=indices.shape
    x=int(dma['x'])-56-(w-1 if flip else 0);y=int(dma['y'])&255
    x0,y0,x1,y1=max(0,x),max(0,y),min(pixels.shape[1],x+w),min(pixels.shape[0],y+h)
    if x1<=x0 or y1<=y0:return dict(score=None,inViewportPixels=0)
    tile=indices[y0-y:y1-y,x0-x:x1-x]
    visible=mask[y0-y:y1-y,x0-x:x1-x]
    count=int(visible.sum())
    expected=palette[tile]
    actual=pixels[y0:y1,x0:x1]
    equal=np.max(np.abs(actual.astype(int)-expected.astype(int)),axis=2)<=3
    return dict(score=float(equal[visible].mean()) if count else None,inViewportPixels=count)

if OUT.exists():raise ValueError('Preserve pixel-review evidence')
guest,graphics,assets,payload=proof.reconstruct()
report_paths=(ROOT/'audit_v1133_owned_split_blood_normal_checked/report.json',ROOT/'audit_v1135_controlled_split_alternate_checked/report.json')
reports=[json.loads(path.read_text()) for path in report_paths]
assert all(report['passed'] for report in reports)
OUT.mkdir()
pins={str(path):digest(path) for path in report_paths}
scores,contacts={},{}
for mode,report in zip(('normal','controlled-alternate'),reports):
    for case,data in report['cases'].items():
        directory=ROOT/case
        text=(directory/'run.log').read_text(encoding='utf-8-sig')
        art=proof.previous.prior.rows(text,'MK2_ROLLING_HEAD_V1003')
        dmas=[r for tag,r in art if tag=='DMA']
        snapshots=[r for tag,r in art if tag=='POSE_SNAPSHOT']
        dumps={int(r['source'],16):r for tag,r in art if tag=='PALETTE_DUMP'}
        scenes=sorted(data['pixelMatches'],key=lambda r:(r['pose'],r['actor']))
        assert len(scenes)==17
        contact=Image.new('RGB',(1600,1370),(25,25,25));draw=ImageDraw.Draw(contact)
        case_scores=[]
        for n,scene in enumerate(scenes):
            path=Path(scene['picture']);image=Image.open(path).convert('RGB')
            assert image.size==(400,254)
            snap=next(r for r in snapshots if f"head_pose_{r['actor_pose']}_{r['frame']}.png"==path.name)
            source=int(snap['source'],16)
            dma=next(r for r in dmas if r['frame']==snap['queued_frame'] and r['source']==snap['source'] and r['fifo_actor']==scene['actor'])
            asset=assets[source]
            palette_path=directory/dumps[source]['file']
            raw=np.asarray(struct.unpack('<64I',palette_path.read_bytes()),dtype=np.uint32)
            palette=np.stack(((raw>>16)&255,(raw>>8)&255,raw&255),axis=1)
            measured=blood_score(path,asset['bloodMask'],asset['indices'],palette,dma)
            case_scores.append(dict(pose=scene['pose'],actor=scene['actor'],picture=str(path),**measured))
            x,y=(n%4)*400,(n//4)*274
            label=f"{data['victim']} P{data['slot']} {mode} pose{scene['pose']}"
            if measured['score'] is not None:label+=f" cutmatch{measured['score']:.3f} n{measured['inViewportPixels']}"
            draw.text((x+3,y+3),label,fill='white')
            contact.paste(image,(x,y+20))
            pins[str(path)],pins[str(palette_path)]=digest(path),digest(palette_path)
        output=OUT/f"{data['victim']}-p{data['slot']}-{mode}-actual-17-scenes.png"
        contact.save(output);pins[str(output)]=digest(output)
        contacts[case]=str(output);scores[case]=case_scores
# Presence criterion is deliberately visible, not a claim that occluded blood
# is visible: at least 8 in-viewport classified pixels and 50% measured match
# at each actual actor/pose sample. Inspect failure data, never waive it.
errors=[]
for case,rows in scores.items():
    if '_kano_' not in case:continue
    for row in rows:
        if row['inViewportPixels']<8 or row['score'] is None or row['score']<0.5:
            errors.append(dict(case=case,pose=row['pose'],actor=row['actor'],score=row['score'],count=row['inViewportPixels']))
record=dict(passed=not errors,errors=errors,scope='visible classified Kano cut pixels at measured native positions; normal and explicit controlled alternate Dead Pool, original occlusions retained',
    sceneCount=136,kanoCutActorPoseSamples=68,pixelScores=scores,contacts=contacts,
    actualScenePixelsChanged=False,manualVisualReviewComplete=False,naturalAlternateSelectionAccepted=False,
    allArenasAccepted=False,fullPortAccepted=False,inputHashes=pins)
(OUT/'report.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(passed=record['passed'],errors=errors,sceneCount=136,kanoCutSamples=68),indent=2))
raise SystemExit(0 if record['passed'] else 1)
