"""Physical body completion window; effects and audio excluded."""
import json
from pathlib import Path
import qualify_bounded_stock_head_body_footprints_driver as driver
from qualify_bounded_queued_throw_footprints import gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_stock_head_body_completion_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        baseline=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_body_completion_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=driver.driver_states(folder,fighter);assert rows==driver.driver_states(baseline,fighter)
        control=driver.scoped.original.state_gate(rows,fighter,ident)
        hi=control['nativeWrapFrame']-control['nativeActionFrame'];assert hi==174
        groups=summaries_at(folder);summaries=groups['COMPLETE_FOOTPRINT']
        coverage=gate(summaries,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],control['nativeActionFrame'],61,hi)
        assert all(0<=int(r['offscreen'])<int(r['points']) for r in summaries)
        results[fighter]=dict(**coverage,**control,croppedComponentPixels=sum(int(r['offscreen']) for r in summaries),
            terminal=terminal,logSha256=sync.sha(folder/'run.log'),identicalQualifiedControlTrace=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        dependencySha256={p:sync.sha(sync.ROOT/'tools'/p) for p in (
            'qualify_bounded_stock_head_body_footprints_driver.py','qualify_bounded_stock_head_body_footprints_scoped.py',
            'qualify_bounded_stock_head_body_footprints.py','qualify_bounded_queued_throw_footprints.py',
            'qualify_bounded_viewport_throw_footprints.py','qualify_bounded_stock_head_finisher.py')},
        detachedHeadAccepted=False,goreEffectsAccepted=False,fullFinisherArtAccepted=False,
        fullFinisherAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
