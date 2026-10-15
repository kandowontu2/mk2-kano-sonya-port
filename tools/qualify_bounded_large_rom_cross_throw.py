"""Recheck same trace with native large-ROM source mapping in observer."""
import json
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace,point_gate

def main():
    out=sync.ROOT/'audit_bounded_large_rom_cross_throw_checked';assert not out.exists()
    prior=sync.ROOT/'audit_bounded_cross_throw_presentation_checked/report.json'
    proof=json.loads(prior.read_text());assert proof['passed']
    results={}
    for fighter in ('sonya','kano'):
        old=sync.ROOT/f'audit_bounded_{fighter}_cross_throw_presentation_runtime'
        assert sync.sha(old/'run.log')==proof['results'][fighter]['logSha256']
        folder=sync.ROOT/f'audit_bounded_{fighter}_large_rom_cross_throw_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder);oldfields,oldhits,oldpoints=trace(old)
        assert fields==oldfields and hits==oldhits and len(points)==len(oldpoints)
        assert all(0<=int(r['dma_x'])<400 and 0<=int(r['dma_y'])<254 for r in points)
        point_gate(points)
        gaps=[r for r in points if r['source_matches']=='0']
        previousgaps=proof['results'][fighter]['allDrawPredictionGaps']
        assert len(gaps)<previousgaps,'Observer fix did not improve its native-source predictions'
        results[fighter]=dict(identicalQualifiedGameplay=True,visiblePoints=len(points),
            priorPredictionGaps=previousgaps,remainingPredictionGaps=gaps,
            remainingPredictionGapCount=len(gaps),terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),priorSha256=sync.sha(prior),
        checkerSha256=sync.sha(Path(__file__)),entireArtReplayAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:dict(points=v['visiblePoints'],priorGaps=v['priorPredictionGaps'],
        remainingGaps=v['remainingPredictionGapCount']) for k,v in results.items()}))

if __name__=='__main__':main()
