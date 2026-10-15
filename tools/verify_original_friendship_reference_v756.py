"""Check the full original friendship body/bubble artwork against native frames.

These are opponent-health-assisted MK3 reference captures, never port tests.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import numpy as np
from PIL import Image
from native_babality_runtime_checks_v739 import image_match

def check(value,message):
    if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def nearest(actual,sprite):
    mask=sprite[:,:,3]!=0
    locations=np.argwhere(mask)
    y0,x0=locations[len(locations)//2]
    hits=np.argwhere(np.all(actual==sprite[y0,x0,:3],axis=2))
    h,w=mask.shape;best=None
    for y,x in hits:
        y,x=int(y-y0),int(x-x0)
        if 0<=x<=actual.shape[1]-w and 0<=y<=actual.shape[0]-h:
            cut=actual[y:y+h,x:x+w]
            delta=mask & np.any(cut!=sprite[:,:,:3],axis=2)
            count=int(delta.sum())
            if best is None or count<best['count']:
                best={'count':count,'origin':[x,y],'mismatch_positions':np.argwhere(delta)[:15].tolist()}
    return best

def rows(path):
    result=[]
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        match=re.match(r'MK3_FRIEND_(\w+) (.*)',line)
        if match:result.append((match[1],dict(re.findall(r'(\w+)=([^\s]+)',match[2]))))
    return result

def verify(root,art,cases):
    reference=json.loads((art/'reference.json').read_text())
    checked={}
    def track(path):
        check(path.is_file(),f'Missing executed input {path}')
        checked[str(path.resolve())]=sha(path)
    track(art/'reference.json');track(Path(__file__))
    import native_babality_runtime_checks_v739 as shared
    track(Path(shared.__file__))
    for path,wanted in reference['input_hashes'].items():
        check(sha(Path(path))==wanted,'Original artwork source changed');track(Path(path))
    report={}
    for fighter,case in cases.items():
        result=json.loads((case/'result.json').read_text(encoding='utf-8-sig'))
        check(result['exit_code']==0 and result['assistance']=='opponent_health_only','Nonterminal/wrong-scope oracle')
        track(case/'result.json');track(case/'run.log')
        for path,wanted in result['input_hashes'].items():
            check(sha(Path(path))==wanted,'Executed original-scene source changed');track(Path(path))
        events=rows(case/'run.log')
        final=[r for tag,r in events if tag=='RESULT']
        check(len(final)==1 and int(final[0]['kos'])==2 and int(final[0]['window'])>0 and int(final[0]['action'])>0,'Original scene not actually entered')
        check(final[0]['position_writes']=='0' and final[0]['identity_writes']=='0' and final[0]['state_writes']=='0' and final[0]['auto_cheat']=='false','Unsupported reference assistance')
        rec=reference['records'][fighter]
        entries=[r for tag,r in events if tag=='ENTRY' and int(r['entry'],16)==rec['native_action']]
        check(entries and all(int(r['id'])==rec['original_id'] for r in entries),'Scene not owned by true original character')
        poses=[r for tag,r in events if tag=='POSE']
        check(poses and all(int(r['id'])==rec['original_id'] for r in poses),'Original body identity changed')
        part_events=[r for tag,r in events if tag=='PART']
        samples=[]
        for group in rec['groups']:
            picture=art/group['file'];track(picture)
            sprite=np.asarray(Image.open(picture).convert('RGBA'))
            check(hashlib.sha256(sprite.tobytes()).hexdigest()==group['rgba_sha256'],'Artwork PNG changed')
            candidates=[]
            if group['effect']:
                for item in part_events:
                    if int(item['pose'],16)==group['group']:
                        age=int(item['age'])
                        # Frame-done palette RAM initially precedes deferred copy.
                        # Use saved native render(s) of this pose after that copy.
                        candidates.extend(case/'snap'/f'friendship_{a}.png'for a in range(age,age+5)if a%8==0)
                        candidates.extend(case/'snap'/f'pose_{a}.png'for a in range(age,age+5))
                        candidates.extend(case/'snap'/f'native_field_{a}.png'for a in range(age+1,age+5))
            else:
                for index,item in enumerate(poses):
                    if int(item['pose'],16)!=group['group']:continue
                    age=int(item['age'])
                    end=int(poses[index+1]['age'])if index+1<len(poses)else age+16
                    # CPU pose changes happen after the current screen's draw.
                    # Include the next pose-change snapshot (previous rendered
                    # body) and periodic saves strictly after construction.
                    candidates.extend(case/'snap'/f'friendship_{a}.png'for a in range(age+1,end+1)if a%8==0)
                    candidates.extend([case/'snap'/f'pose_{end}.png'])
                    candidates.extend(case/'snap'/f'native_field_{a}.png'for a in range(age+1,end+1))
            found=None
            best=None
            for path in candidates:
                if not path.is_file():continue
                actual=np.asarray(Image.open(path).convert('RGB'))
                for flip in (False,True):
                    try:
                        origin,pixels=image_match(actual,sprite[:,::-1] if flip else sprite)
                    except ValueError:
                        near=nearest(actual,sprite[:,::-1] if flip else sprite)
                        if near and(best is None or near['count']<best['count']):
                            best={**near,'file':str(path),'flip':flip}
                        continue
                    found={'group':group['group'],'file':str(path.resolve()),'flip':flip,'origin':origin,'pixels':pixels}
                    track(path);break
                if found:break
            check(found is not None,f'Original {fighter} group {group["group"]:08X} not pixel-exact in native capture; nearest={best}')
            samples.append(found)
        report[fighter]={'groups':len(samples),'pixels':sum(s['pixels']for s in samples),'samples':samples,'assistance':'opponent_health_only'}
    return {'scope':'original body/bubble artwork oracle, not native port or audio acceptance',
            'fullPortAcceptance':False,'fullFinisherAcceptance':False,'artwork':report,'checked_inputs':checked}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    check(not args.output.exists(),'Refusing to overwrite verified evidence')
    report=verify(args.root,args.root/'audit_v755_original_friendship_art',{
        'kano':args.root/'audit_v757_original_friendship_kano',
        'sonya':args.root/'audit_v758_original_friendship_sonya'})
    args.output.mkdir(parents=True)
    (args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({fighter:{key:rec[key]for key in('groups','pixels')}for fighter,rec in report['artwork'].items()},indent=2))

if __name__=='__main__':main()
