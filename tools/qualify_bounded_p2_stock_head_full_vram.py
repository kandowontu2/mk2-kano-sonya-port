"""Strict full native VRAM source census, current P2 physical bodies."""
import json
from pathlib import Path
from qualify_bounded_p2_stock_head_body_pixels import driver
from qualify_bounded_stock_head_finisher import gate as control_gate
from qualify_bounded_queued_throw_footprints import gate as pixel_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_p2_stock_head_full_vram_checked';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_control_checked/report.json').read_text())
    assert proof['passed'];results={}
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_full_vram_runtime'
        baseline=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=driver(folder,fighter);assert rows==driver(baseline,fighter)
        control=control_gate(rows,fighter,ident)
        groups=summaries_at(folder);summaries=groups['COMPLETE_FOOTPRINT']
        coverage=pixel_gate(summaries,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],control['nativeActionFrame'],1,174)
        assert all(0<=int(r['offscreen'])<=int(r['points']) for r in summaries)
        cropped=sum(int(r['offscreen']) for r in summaries)
        results[fighter]=dict(**coverage,visibleComponentPixels=coverage['opaquePixels']-cropped,
            croppedComponentPixels=cropped,terminal=terminal,unchangedEarnedDriverTrace=True,
            logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        sourceColumns=512,detachedHeadAccepted=False,stockEffectsAccepted=False,subjectiveArtAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
