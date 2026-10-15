"""Original native selection objects retire before ladder, without reappearing."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    groups={}
    for line in (folder/'run.log').read_text().splitlines():
        assert '[LUA ERROR]' not in line
        if line.startswith('MK2_UI_'):
            tag=line.split()[0][7:]
            groups.setdefault(tag,[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return groups

def gate(rows,exitframe,liveframe):
    frames=[int(r['frame']) for r in rows]
    assert frames==list(range(frames[0],liveframe))
    photos=[int(r['frame']) for r in rows if int(r['cssphotos'])>0]
    poses=[int(r['frame']) for r in rows if int(r['addedposes'])>0]
    assert photos and poses and max(photos)==max(poses)<exitframe
    final=[r for r in rows if int(r['frame'])>max(photos)]
    assert len(final)>500 and all(r['cssphotos']==r['addedposes']=='0' for r in final)
    owners={r['cssactor'] for r in rows if int(r['frame'])>=exitframe}
    assert len(owners)==1 and '00000000' not in owners
    return dict(lastCSSPhotoAndPoseDrawField=max(photos),detectedLadderField=exitframe,zeroSubmissionFieldsAfterRetirement=len(final),originalCSSActor=next(iter(owners)))

out=sync.ROOT/'audit_bounded_css_teardown_owner_checked';assert not out.exists();results={}
proof_path=sync.ROOT/'audit_bounded_css_cadence_checked/report.json';proof=json.loads(proof_path.read_text());assert proof['passed']
for fighter in ('kano','sonya'):
    for side in (1,2):
        key=f'{fighter}P{side}';folder=sync.ROOT/f'audit_bounded_css_teardown_owner_{fighter}_p{side}_runtime'
        base=sync.ROOT/f'audit_bounded_css_cadence_{fighter}_p{side}_runtime'
        assert sync.sha(base/'run.log')==proof['results'][key]['logSHA256']
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['rawMedia']=='none'
        actual,old=load(folder),load(base)
        for tag in ('SELECT','INPUT','FIELD','CADENCE','RESULT'):assert actual[tag]==old[tag]
        exitframe=int(actual['EXIT'][0]['frame']);liveframe=int(actual['LIVE'][0]['frame'])
        positive=gate(actual['TEARDOWN'],exitframe,liveframe)
        bad=copy.deepcopy(actual['TEARDOWN']);next(r for r in bad if int(r['frame'])==exitframe)['cssphotos']='1'
        try:gate(bad,exitframe,liveframe)
        except AssertionError:pass
        else:raise AssertionError('Lingering selection photo accepted')
        bad=copy.deepcopy(actual['TEARDOWN']);next(r for r in bad if int(r['frame'])==exitframe+40)['addedposes']='1'
        try:gate(bad,exitframe,liveframe)
        except AssertionError:pass
        else:raise AssertionError('Late selection pose accepted')
        results[key]=dict(**positive,terminal=terminal,rejectedFaults=['lingering_photo','late_selection_pose'],physicalGameplayUnchanged=True,logSHA256=sync.sha(folder/'run.log'))
report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSHA256=sync.sha(Path(__file__)),priorProofSHA256=sync.sha(proof_path),scope='Complete native FIFO submission census of both CSS portraits and original added selection pose through ladder and battle construction. Does not prove every scanout/VRAM pixel cleared or whole-port completion.',fullGoalComplete=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,contexts=4,selectionObjectsRetireBeforeLadder=True)))
