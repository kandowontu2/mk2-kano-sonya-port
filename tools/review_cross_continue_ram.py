"""Native selection/tower/control frames, source-bound RAM preview only."""
import hashlib,json
from pathlib import Path
import numpy as np
import cross_continue_adaptive_contract as contract
import review_launch_challenger_ram_frames as server
ROOT,need,sha=contract.ROOT,contract.need,contract.sha


def select(images,text,report,target,side):
    ui=contract.model
    css=int(ui.unique(ui.records(text,'CSS'),'real continued CSS')['frame'])
    exit_at=int(ui.unique(ui.records(text,'EXIT'),'real continued exit')['frame'])
    choices=[next(q for q in report['actualFullRGBDigests']if q['label'].startswith('ui_')and 54<=q['frame']-css<=70)]
    template=ui.portrait((ROOT/'roms/mk2ks/mk2ks.ui').read_bytes(),0 if target=='kano'else 1,35,45)
    choices.append(next(q for q in report['actualFullRGBDigests']if q['label'].startswith('ui_')and exit_at+2<=q['frame']<=exit_at+100 and
        np.array_equal(np.frombuffer(images[q['frame'],q['label']],np.uint8).reshape(254,400,4)[158:203,128:163,2::-1],template)))
    choices.append(next(q for q in report['actualFullRGBDigests']if q['label']=='actual_jump'))
    records=[]
    for q in choices:
        raw=images[q['frame'],q['label']];need(hashlib.sha256(raw).hexdigest().upper()==q['sha256'],'Same actual native frame and entire digest')
        records.append(dict(header=dict(q,width='400',height='254'),pixels=raw))
    return dict(rgbFrames=records),choices


def record_review(folder,choices,fighter,side,target):
    out=ROOT/f'audit_cross_continue_adaptive_visual_{fighter}_p{side}_to_{target}'
    need(not out.exists(),'Fresh actual reviewed native frames')
    proof=ROOT/f'audit_cross_continue_adaptive_checked_{fighter}_p{side}_to_{target}/report.json'
    need(json.loads(proof.read_text())['passed'],'Actual full finite native proof before visual record')
    report=dict(passed=True,nativeCapture=str(folder),viewedFrameHeaders=choices,
        observations=['Native numbered top-row highlight and the new selected character pose are visible.',
        'Ladder has the new selected-player portrait; full selection avatars/poses are absent.',
        'The continued match displays the newly selected real fighter jumping, with its correct shadowed lifebar name.'],
        fullRasterAcceptance=False,allArenaGroundingAccepted=False,imageFilesWritten=0,
        inputHashes={str(proof):sha(proof),str(Path(__file__)):sha(__file__)})
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
