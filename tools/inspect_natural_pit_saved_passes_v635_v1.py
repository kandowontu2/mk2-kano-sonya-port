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
Replay=base.Replay


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
