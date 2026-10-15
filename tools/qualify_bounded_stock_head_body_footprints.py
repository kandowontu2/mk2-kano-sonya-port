"""Opening physical bodies only; detached head/effects/audio remain unverified."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_stock_head_finisher import gate as state_gate
from qualify_bounded_queued_throw_footprints import gate as pixel_gate
from qualify_bounded_viewport_throw_footprints import summaries_at

PREFIX=re.compile(r'^MK2_STOCK_HEAD_V921_(\w+) frame=(\d+) victim=(\w+) side=(\d+) killer=(\w+) writes=(\d+) assistance=(\w+)(?: |$)')

def states(folder,fighter):
    rows=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line and len(line)<1048576
            if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
            match=PREFIX.match(line);assert match
            tag,frame,name,side,killer,writes,assistance=match.groups()
            assert (name,side,killer,writes,assistance)==(fighter,'1','baraka','0','none')
            row=dict(re.findall(r'(\w+)=([^\s]+)',line));assert row['frame']==frame
            rows.append((tag,row))
    return rows

def main():
    out=sync.ROOT/'audit_bounded_stock_head_body_footprints_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        baseline=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_body_footprint_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=states(folder,fighter);assert rows==states(baseline,fighter)
        control=state_gate(rows,fighter,ident)
        groups=summaries_at(folder);summaries=groups['COMPLETE_FOOTPRINT']
        ready=control['nativeActionFrame']
        coverage=pixel_gate(summaries,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],ready,0,30)
        faults=[]
        for fault in ('display','source','missing_field','count'):
            bad=copy.deepcopy(summaries)
            if fault=='display':bad[0]['display_fail']='1'
            elif fault=='source':bad[0]['source_fail']='1'
            elif fault=='missing_field':bad.pop()
            else:bad[0]['points']=str(int(bad[0]['points'])+1)
            try:pixel_gate(bad,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],ready,0,30)
            except AssertionError:faults.append(fault)
            else:raise AssertionError('Fault accepted '+fault)
        assert all(0<=int(r['offscreen'])<int(r['points']) for r in summaries)
        cropped=sum(int(r['offscreen']) for r in summaries)
        results[fighter]=dict(**control,**coverage,visibleComponentPixels=coverage['opaquePixels']-cropped,
            croppedComponentPixels=cropped,identicalQualifiedControlTrace=True,rejectedFaults=faults,
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),priorProofSha256=sync.sha(prior),
        checkerSha256=sync.sha(Path(__file__)),detachedHeadAccepted=False,goreEffectsAccepted=False,
        fullFinisherArtAccepted=False,fullFinisherAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
