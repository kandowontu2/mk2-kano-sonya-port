"""Actual two-human idle/mobility soles bound to original display flips and VRAM."""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from inspect_natural_arena_floor_v602 import decoder
from inspect_ground_presentation import rows
from verify_native_floor_display_v602 import check_latch


def inspect(folder):
    folder=Path(folder)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    assert not re.search(r'\[LUA ERROR\]|fatal error|access violation|stack traceback',log,re.I)
    fields={(r['frame'],r['slot']):r for r in rows(log,'FIELD')}
    dmas=defaultdict(list)
    for r in rows(log,'DMA'):dmas[r['frame']].append(r)
    decode=decoder({r['key']:r for r in rows(log,'GFX')})
    records=[]
    for snap in rows(log,'SNAP'):
        frame=snap['frame']
        image=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))
        words=np.fromfile(folder/snap['vram_file'],dtype='<u2').reshape(512,512)
        number=lambda key:int(snap[key],16) if isinstance(snap[key],str) else snap[key]
        assert snap['flip_frame']==frame and snap['phase']=='frame_done'
        bound=check_latch(image,words.tobytes(),(folder/snap['palette_file']).read_bytes(),
                          number('start'),number('control'),number('tap'))
        page,col=bound['row'],bound['column']
        expected=np.zeros((512,512),dtype=np.uint16)
        owner=np.zeros((512,512),dtype=np.uint8)
        for d in dmas[frame-1]:
            if d['command']&15!=2:continue
            c,w,h=d['command'],d['width'],d['height']
            assert d['palette'] in (0x200,0x300) and d['skip']==0
            indices=decode(d['source'],c,w,h)
            sy,sx=np.where(indices!=0)
            x=(d['x']+(-sx if c&16 else sx))&1023
            y=(d['y']+(-sy if c&32 else sy))&511
            inside=(x>=d['left'])&(x<=d['right'])&(y>=d['top'])&(y<=d['bottom'])&(x<512)
            x,y,sy,sx=(a[inside]for a in(x,y,sy,sx))
            expected[y,x]=indices[sy,sx].astype(np.uint16)|d['palette']
            owner[y,x]=1 if d['palette']==0x200 else 2
        crop=lambda a:a[page:page+254,col:col+400]
        bodies={}
        for slot in (1,2):
            a=fields[frame-1,slot]
            assert a['id']==a['roster'] and a['owner']==a['actor'] and a['state']==1
            mask=crop(owner)==slot
            mismatch=mask&(crop(expected)!=crop(words))
            assert mask.any(),'Actual whole-body pixels in displayed field'
            y,x=np.where(mask)
            ground=a['stageY']+5+a['displayY']-a['cameraY']-page
            bodies[slot]=dict(id=a['id'],pixels=int(mask.sum()),mismatches=int(mismatch.sum()),
                sole=int(y.max()),native_ground=ground,sole_relative_native_ground=int(y.max())-ground,
                object_y=a['y'],floor=a['floor'],vx=a['vx'],vy=a['vy'],gravity=a['gravity'],action=a['action'],
                grounded=a['y']==a['floor'],stationary=a['vx']==a['vy']==a['gravity']==0,
                pose=f"{a['pose']:08X}")
        records.append(dict(frame=frame,age=snap['age'],stage=fields[frame-1,1]['stage'],
                            display_pixels=bound['pixels'],body=bodies))
    idle=[r for r in records if r['age']<=96 and all(a['grounded'] and a['stationary'] for a in r['body'].values())]
    sole_ranges={slot:sorted({r['body'][slot]['sole'] for r in idle}) for slot in (1,2)}
    return dict(scope='Fixed two-human idle/jump/crouch/walk actual body soles against stock Kitana; not all-arena grounding acceptance',
                samples=len(records),idle_samples=len(idle),idle_sole_rows=sole_ranges,
                idle_native_ground_offsets={slot:sorted({r['body'][slot]['sole_relative_native_ground'] for r in idle}) for slot in (1,2)},
                body_mismatches=sum(a['mismatches']for r in records for a in r['body'].values()),
                records=records,fullPortAcceptance=False,floorAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args=parser.parse_args()
    print(json.dumps(inspect(args.folder),indent=2))
