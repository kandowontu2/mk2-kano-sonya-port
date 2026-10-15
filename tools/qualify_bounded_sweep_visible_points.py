"""Visible-only sweep points; explicitly account for off-screen sentinel."""
import json
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace, point_gate

def main():
    out=sync.ROOT/'audit_bounded_sweep_visible_points_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_spaced_sweep_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter in ('sonya','kano'):
        old=sync.ROOT/f'audit_bounded_{fighter}_spaced_sweep_runtime'
        folder=sync.ROOT/f'audit_bounded_{fighter}_sweep_presentation_runtime'
        assert sync.sha(old/'run.log')==proof['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        fields,hits,points=trace(folder);baseline,oldhits,_=trace(old)
        assert fields==baseline and hits==oldhits
        visible=[];clipped=[]
        for r in points:
            x,y=int(r['dma_x']),int(r['dma_y'])
            if 0<=x<400 and 0<=y<254:visible.append(r)
            else:
                assert r['actual']=='FFFFFFFFFFFFFFFF' and r['display_matches']=='0'
                assert r['kind']=='body' and r['slot']=='2' and r['id']=='4'
                assert r['source_frame']=='1440' and (x,y)==(331,259)
                clipped.append(r)
        assert len(clipped)==1
        point_gate(visible)
        results[fighter]=dict(identicalQualifiedSweepGameplay=True,
            exactVisiblePresentedPoints=len(visible),offscreenStockBodyQuery=clipped,
            unresolvedAllDrawPredictionPoints=sum(r['source_matches']=='0' for r in visible),
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),
        priorSha256=sync.sha(prior),checkerSha256=sync.sha(Path(__file__)),
        reusedCheckerSha256=sync.sha(sync.ROOT/'tools/qualify_bounded_sweep_presentation.py'),
        entireRenderedArtAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:dict(visible=v['exactVisiblePresentedPoints'],
        offscreen=len(v['offscreenStockBodyQuery']),predictionGaps=v['unresolvedAllDrawPredictionPoints']) for k,v in results.items()}))

if __name__=='__main__':main()
