"""Sparse visible body/shadow points bound to qualified cross-throw state."""
import json
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace

def main():
    out=sync.ROOT/'audit_bounded_cross_throw_presentation_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_cross_added_ground_throws_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter in ('sonya','kano'):
        baseline=sync.ROOT/f'audit_bounded_{fighter}_cross_added_ground_throw_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_cross_throw_presentation_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder);oldfields,oldhits,_=trace(baseline)
        assert fields==oldfields and hits==oldhits and len(points)>2000
        visible=[];clipped=[];failures=[]
        for r in points:
            x,y=int(r['dma_x']),int(r['dma_y'])
            if not (0<=x<400 and 0<=y<254):
                assert r['actual']=='FFFFFFFFFFFFFFFF' and r['display_matches']=='0'
                clipped.append(r);continue
            visible.append(r)
            if not (r['source_vram']==r['display_vram'] and r['vram_rgb']==r['actual']
                    and r['display_matches']=='1' and int(r['frame'])==int(r['source_frame'])+1):
                failures.append(r)
        results[fighter]=dict(identicalQualifiedCrossThrowGameplay=True,
            visiblePoints=len(visible),offscreenQueries=clipped,visibleFailures=failures,
            allDrawPredictionGaps=sum(r['source_matches']=='0' for r in visible),
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    passed=all(not r['visibleFailures'] for r in results.values())
    report=dict(passed=passed,results=results,sourceSync=sync.verify(),
        priorSha256=sync.sha(prior),checkerSha256=sync.sha(Path(__file__)),
        fullThrowArtAccepted=False,allThrowContextsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=passed,cases={k:dict(visible=v['visiblePoints'],
        offscreen=len(v['offscreenQueries']),failures=len(v['visibleFailures']),
        predictionGaps=v['allDrawPredictionGaps']) for k,v in results.items()})))
    raise SystemExit(0 if passed else 1)

if __name__=='__main__':main()
