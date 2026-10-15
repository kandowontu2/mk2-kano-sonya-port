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
    pre={r['frame']:r for r in rows(log,'PRE')}
    owners={(r['frame'],r['slot']):r for r in rows(log,'OWNER')}
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
        assert pre[frame-1]['phase']=='before_first_dma'
        expected=np.fromfile(folder/pre[frame-1]['file'],dtype='<u2').reshape(512,512).copy()
        owner=np.zeros((512,512),dtype=np.uint8)
        for d in dmas[frame-1]:
            c,w,h=d['command'],d['width'],d['height']
            mode=c&15
            assert mode in (2,8,12) and d['skip']==0 and d['scaleX']in(0,256) and d['scaleY']in(0,256)
            if not w or not h:continue
            indices=np.zeros((h,w),dtype=np.uint8)if mode==12 else decode(d['source'],c,w,h)
            sy,sx=np.where(np.ones((h,w),dtype=bool)if mode==12 else indices!=0)
            x=(d['x']+(-sx if c&16 else sx))&1023
            y=(d['y']+(-sy if c&32 else sy))&511
            inside=(x>=d['left'])&(x<=d['right'])&(y>=d['top'])&(y<=d['bottom'])&(x<512)
            x,y,sy,sx=(a[inside]for a in(x,y,sy,sx))
            pens=np.full(len(x),d['color'],dtype=np.uint16)if mode in (8,12)else indices[sy,sx].astype(np.uint16)
            expected[y,x]=pens|d['palette']
            owner[y,x]=(1 if d['palette']==0x200 else 2)if mode==2 and d['palette']in(0x200,0x300)else 0
        crop=lambda a:a[page:page+254,col:col+400]
        bodies={}
        for slot in (1,2):
            a=fields[frame-1,slot]
            actual_owner=owners[frame-1,slot]
            assert a['id']==a['roster'] and a['owner']==a['actor'] and a['state']==1
            mask=crop(owner)==slot
            mismatch=mask&(crop(expected)!=crop(words))
            assert mask.any(),'Actual whole-body pixels in displayed field'
            y,x=np.where(mask)
            ground=actual_owner['stageY']+5+actual_owner['displayY']-actual_owner['cameraY']-page
            bodies[slot]=dict(id=a['id'],pixels=int(mask.sum()),mismatches=int(mismatch.sum()),
                sole=int(y.max()),native_ground=ground,sole_relative_native_ground=int(y.max())-ground,
                object_y=a['y'],floor=a['floor'],vx=a['vx'],vy=a['vy'],gravity=a['gravity'],action=a['action'],
                grounded=a['y']==a['floor'],stationary=a['vx']==a['vy']==a['gravity']==0,
                pose=f"{a['pose']:08X}")
        records.append(dict(frame=frame,age=snap['age'],stage=fields[frame-1,1]['stage'],vram_mismatches=int((expected!=words).sum()),
                            display_pixels=bound['pixels'],body=bodies))
    idle=[r for r in records if r['age']<=96 and all(a['grounded'] and a['stationary'] for a in r['body'].values())]
    sole_ranges={slot:sorted({r['body'][slot]['sole'] for r in idle}) for slot in (1,2)}
    return dict(scope='Fixed two-human idle/jump/crouch/walk actual body soles against stock Kitana; not all-arena grounding acceptance',
                samples=len(records),idle_samples=len(idle),idle_sole_rows=sole_ranges,
                idle_native_ground_offsets={slot:sorted({r['body'][slot]['sole_relative_native_ground'] for r in idle}) for slot in (1,2)},
                body_mismatches=sum(a['mismatches']for r in records for a in r['body'].values()),
                vram_mismatches=sum(r['vram_mismatches']for r in records),
                records=records,fullPortAcceptance=False,floorAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args=parser.parse_args()
    print(json.dumps(inspect(args.folder),indent=2))
