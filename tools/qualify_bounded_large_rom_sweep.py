"""Exact sweep queried-source and visible native/presented point agreement."""
import json
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace,point_gate

def main():
    out=sync.ROOT/'audit_bounded_large_rom_sweep_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_sweep_visible_points_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter in ('sonya','kano'):
        old=sync.ROOT/f'audit_bounded_{fighter}_sweep_presentation_runtime'
        assert sync.sha(old/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_large_rom_sweep_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder);oldfields,oldhits,oldpoints=trace(old)
        assert fields==oldfields and hits==oldhits and len(points)==len(oldpoints)
        visible=[];clipped=[]
        for r in points:
            if 0<=int(r['dma_x'])<400 and 0<=int(r['dma_y'])<254:visible.append(r)
            else:
                assert r['actual']=='FFFFFFFFFFFFFFFF' and r['kind']=='body'
                assert (r['dma_x'],r['dma_y'],r['id'],r['source_frame'])==('331','259','4','1440')
                clipped.append(r)
        assert len(clipped)==1
        point_gate(visible)
        gaps=[r for r in visible if r['source_matches']=='0']
        results[fighter]=dict(identicalQualifiedGameplay=True,visiblePoints=len(visible),
            priorPredictionGaps=proof['results'][fighter]['unresolvedAllDrawPredictionPoints'],
            remainingPredictionGaps=gaps,remainingPredictionGapCount=len(gaps),
            offscreenQueries=clipped,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    passed=all(not r['remainingPredictionGaps'] for r in results.values())
    report=dict(passed=passed,results=results,sourceSync=sync.verify(),priorSha256=sync.sha(prior),
        checkerSha256=sync.sha(Path(__file__)),entireArtReplayAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=passed,cases={k:dict(points=v['visiblePoints'],
        priorGaps=v['priorPredictionGaps'],remainingGaps=v['remainingPredictionGapCount']) for k,v in results.items()})))
    raise SystemExit(0 if passed else 1)

if __name__=='__main__':main()
