"""P2 head footprints; bucket1 refers to the selected head, not P1."""
import json
from pathlib import Path
from qualify_bounded_p2_stock_head_body_pixels import driver
from qualify_bounded_stock_head_finisher import gate as control_gate
from qualify_bounded_stock_head_effect_pixels import gate as pixel_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_head_head_pixels_checked';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_control_checked/report.json').read_text())
    census=json.loads((sync.ROOT/'audit_bounded_stock_head_effect_census_checked/report.json').read_text())
    assert proof['passed'] and census['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_head_pixels_runtime'
        baseline=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=driver(folder,fighter);assert rows==driver(baseline,fighter)
        control=control_gate(rows,fighter,ident)
        actors=census['results'][fighter]['candidateNonBodyActors'];assert len(actors)==1
        sources=set(next(iter(actors.values()))['sources'])
        coverage=pixel_gate(summaries_at(folder),control['nativeActionFrame'],ident,sources)
        results[fighter]=dict(**coverage,physicalVictimSlot=2,observerBucket=1,
            terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        reusedPixelGateSha256=sync.sha(sync.ROOT/'tools/qualify_bounded_stock_head_effect_pixels.py'),
        stockEffectsAccepted=False,subjectiveArtAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
