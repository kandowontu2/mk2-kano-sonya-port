"""Original last native drawing pass through each exact Pit display flip.

The native flash has DMA-free fields. Bind the last observed BEFORE-pass by
event order, including held intervals; never initialize from tested flip VRAM.
"""
from pathlib import Path
import numpy as np
from PIL import Image
import inspect_natural_arena_floor_v635_v4 as base
from verify_native_floor_display_v602 import check_latch

base.HEX=base.HEX|{'cursor','row','size','xy','b14','b10','a0','a1','a2','a3','a7','a8','a11','a13','entry'}
base.STR=base.STR|{'seconds'}
data=base.data
class Replay(base.Replay):
    def dma(self,d):
        xs,ys=d['scaleX']or 256,d['scaleY']or 256
        if xs==ys==256:return super().dma(d)
        # Native 8.8 source stepping for the uncompressed Pit backdrop and
        # post-Pit ladder. Deliberately reject unobserved scaled skip modes.
        assert not d['command']&128 and d['skip']==0,'Unsupported scaled compressed/skip path'
        source,c,w,h=d['source'],d['command'],d['width'],d['height']
        if not w or not h:return
        mode=c&15
        assert mode in (2,8,12),'Unsupported scaled pixel mode'
        indices=np.zeros((h,w),dtype=np.uint8)if mode==12 else self.decode(source,c,w,h)
        # Destination counts follow the native while(ix<width<<8) loops,
        # not the floor division used solely for the DMA busy-time estimate.
        dy,dx=np.indices(((h*256+ys-1)//ys,(w*256+xs-1)//xs))
        sy,sx=(dy*ys)//256,(dx*xs)//256
        pens=indices[sy,sx]
        x=(d['x']+(-dx if c&16 else dx))&1023
        y=(d['y']+(-dy if c&32 else dy))&511
        inside=(x>=d['left'])&(x<=d['right'])&(y>=d['top'])&(y<=d['bottom'])&(x<512)
        if mode!=12:inside&=pens!=0
        x,y,pens=x[inside],y[inside],pens[inside]
        if mode in (8,12):pens=np.full(len(x),d['color'],dtype=np.uint16)
        else:pens=pens.astype(np.uint16)
        self.words[y,x]=pens|d['palette']
        self.body[y,x]=d['slot']if mode==2 else 0
        self.shadow[y,x]=(0x10000000<=source<0x1a000000)and mode==8


def inspect(folder):
    folder=Path(folder)
    groups,buffers,_,_,owners=data(folder)
    pre=groups['FLOOR_PRE_FRAME']
    assert len({r['frame'] for r in pre})==len(pre),'One retained BEFORE-pass per actual drawing field'
    events=sorted([(tag,r) for tag in ('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU') for r in groups[tag]],
                  key=lambda e:e[1]['event'])
    flips={r['event']:r for r in groups['FLOOR_FLIP']}
    displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
    snaps={r['frame']:r for r in groups['FLOOR_SNAP']}
    records=[];replay=Replay(folder,groups,buffers,owners)
    for latch in groups['FLOOR_LATCH']:
        frame=latch['snapshot'];flip=flips[latch['event']]
        assert latch['flip_frame']==frame==flip['frame'],'Actual current native flip, no best buffer selection'
        prior=[r for r in pre if r['event']<flip['event']]
        assert prior,'An actual retained BEFORE-pass must exist'
        anchor=max(prior,key=lambda r:r['event'])
        assert anchor['frame']==latch['anchor_frame'] and anchor['phase']=='before_first_frame_dma','Original last BEFORE-pass binding'
        assert anchor['frame']<frame,'Last actual native drawing pass precedes the displayed flip'
        # Each sample is independent. Two held fields can legitimately share
        # the same prior pass; all intervening CPU writes still participate.
        replay.begin(anchor['epoch'])
        for tag,row in events:
            if anchor['event']<=row['event']<flip['event']:replay.apply(tag,row)
        actual=np.fromfile(folder/latch['file'],dtype='<u2').reshape(512,512)
        mismatch=replay.words!=actual
        display=displays[frame]
        assert all(latch[key]==display[key] for key in ('start','control','tap')),'Current display registers agree'
        image=np.asarray(Image.open(folder/'snap'/snaps[frame]['file']).convert('RGB'))
        bound=check_latch(image,actual.tobytes(),(folder/display['palette_file']).read_bytes(),
                          latch['start'],latch['control'],latch['tap'])
        row,col=bound['row'],bound['column']
        crop=lambda a:a[row:row+254,col:col+400]
        body=crop(replay.body)==1
        difference=crop(mismatch)
        records.append(dict(frame=frame,anchor_frame=anchor['frame'],event=flip['event'],file=snaps[frame]['file'],
                            display_pixels=bound['pixels'],vram_mismatches=int(mismatch.sum()),
                            displayed_mismatches=int(difference.sum()),body_pixels=int(body.sum()),
                            body_mismatches=int((body&difference).sum())))
    return dict(frames=len(records),records=records,fullPortAcceptance=False,
                scope='Each actual last BEFORE-pass through exact current flip, including native DMA-free flash/blank fields; not arbitrary inter-pass erasure or full artistic acceptance')
