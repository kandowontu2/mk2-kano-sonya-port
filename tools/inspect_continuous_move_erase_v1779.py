"""Attempt uninterrupted original CPU/DMA replay, never reset from later VRAM.

Every retained pre-pass is a comparison target, not an expected-state anchor.
Failure is diagnostic evidence of a missing event/model path, not a game bug.
"""
import argparse,json
from pathlib import Path
import numpy as np
import inspect_secondary_display_v1231 as raster
raster.HEX|={'world','camera','display','parent_main','native_actor_owner','victim','victim_main'}

def inspect(folder):
    groups,buffers,_,_,owners=raster.data(folder)
    replay=raster.Replay(folder,groups,buffers,owners)
    events=sorted([(kind,row)for kind in('FLOOR_PRE_FRAME','FLOOR_DMA','FLOOR_CPU','FLOOR_FLIP')for row in groups[kind]],key=lambda item:item[1]['event'])
    latches={r['event']:r for r in groups['FLOOR_LATCH']if r['flip_frame']==r['snapshot']}
    checked_pres=checked_flips=0
    for kind,row in events:
        if replay.epoch!=row['epoch']:replay.begin(row['epoch'])
        if kind=='FLOOR_PRE_FRAME':
            actual=np.fromfile(folder/row['file'],dtype='<u2').reshape(512,512)
            mismatch=replay.words!=actual
            if mismatch.any():
                y,x=np.where(mismatch)
                return dict(passed=False,failureKind='inter_pass_pre_buffer',frame=row['frame'],event=row['event'],
                  mismatchCount=int(mismatch.sum()),firstDifferences=[dict(x=int(xx),y=int(yy),model=int(replay.words[yy,xx]),actual=int(actual[yy,xx]))for yy,xx in zip(y[:16],x[:16])],
                  exactPriorPreBuffers=checked_pres,exactPriorFlips=checked_flips,laterBuffersUsedAsAnchors=False,fullPortAcceptance=False)
            assert row['event']>replay.last_event;replay.last_event=row['event'];checked_pres+=1
        elif kind=='FLOOR_FLIP':
            if row['event']not in latches:continue
            actual=np.fromfile(folder/latches[row['event']]['file'],dtype='<u2').reshape(512,512)
            mismatch=replay.words!=actual
            if mismatch.any():
                y,x=np.where(mismatch)
                return dict(passed=False,failureKind='continuous_flip_buffer',frame=row['frame'],event=row['event'],mismatchCount=int(mismatch.sum()),
                  firstDifferences=[dict(x=int(xx),y=int(yy),model=int(replay.words[yy,xx]),actual=int(actual[yy,xx]))for yy,xx in zip(y[:16],x[:16])],
                  exactPriorPreBuffers=checked_pres,exactPriorFlips=checked_flips,laterBuffersUsedAsAnchors=False,fullPortAcceptance=False)
            checked_flips+=1
        else:replay.apply(kind,row)
    assert checked_pres==len(groups['FLOOR_PRE_FRAME'])and checked_flips==len(latches)>0
    return dict(passed=True,continuousExactPreBuffers=checked_pres,continuousExactFlips=checked_flips,
                laterBuffersUsedAsAnchors=False,guestWrites=False,fullPortAcceptance=False,
                scope='Uninterrupted observed original CPU/DMA VRAM evolution from one initial base through every retained pre-pass and flip. Not universal art/audio/full-game acceptance.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    assert not args.output.exists(),'Never overwrite evidence'
    try:report=inspect(args.folder)
    except Exception as error:report=dict(passed=False,error=repr(error),laterBuffersUsedAsAnchors=False,fullPortAcceptance=False)
    args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
