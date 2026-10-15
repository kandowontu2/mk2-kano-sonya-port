"""Entry through persistent paired idle: finite P1 cross-added throw pixels."""
import json
from pathlib import Path
import verify_native_source_sync as sync
from qualify_bounded_sweep_presentation import trace,point_gate
from qualify_bounded_viewport_throw_footprints import summaries_at
from qualify_bounded_queued_throw_footprints import gate

def main():
    out=sync.ROOT/'audit_bounded_complete_cross_throw_footprints_sealed';assert not out.exists()
    windowpath=sync.ROOT/'audit_bounded_cross_throw_windows_sealed/report.json'
    window=json.loads(windowpath.read_text());assert window['passed']
    assert all(sync.sha(Path(p))==h for p,h in window['pins'].items())
    endpath=sync.ROOT/'audit_bounded_cross_throw_recovery_end/report.json'
    ends=json.loads(endpath.read_text());assert ends['passed']
    results={};pins={str(windowpath):sync.sha(windowpath),str(endpath):sync.sha(endpath)}
    for fighter in ('sonya','kano'):
        expected=ends['results'][fighter]
        assert expected['nativeThrowEntryAge']==114 and expected['firstPersistentPairedIdleAge']==183
        folder=sync.ROOT/f'audit_bounded_{fighter}_complete_throw_recovery_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        fields,hits,points=trace(folder)
        baseline=sync.ROOT/f'audit_bounded_{fighter}_cross_added_ground_throw_runtime'
        assert sync.sha(baseline/'run.log')==expected['logSha256']
        oldfields,oldhits,_=trace(baseline);assert fields==oldfields and hits==oldhits
        point_gate(points);assert all(r['source_matches']=='1' for r in points)
        groups=summaries_at(folder);summaries=groups['COMPLETE_FOOTPRINT']
        recovery=gate(summaries,groups['IDLE_OPAQUE'],groups['IDLE_FIFO'],expected['readyFrame'],177,183)
        assert all(0<=int(r['offscreen'])<int(r['points']) for r in summaries)
        cropped=sum(int(r['offscreen']) for r in summaries)
        old=window['cases'][fighter]
        assert old['drawFields']==63 and old['sourceAgeRange']==[114,176]
        results[fighter]=dict(completeActualThrowSourceAgeRange=[114,183],
            nativeDrawFields=old['drawFields']+recovery['nativeDrawFields'],
            opaqueComponentPixels=old['opaqueComponentPixels']+recovery['opaquePixels'],
            visibleComponentPixels=old['visibleComponentPixels']+recovery['opaquePixels']-cropped,
            offscreenComponentPixels=old['offscreenComponentPixels']+cropped,
            finalStableStateFields=expected['finalStableFields'],
            recoveryTerminal=terminal,identicalQualifiedGameplay=True)
        assert results[fighter]['nativeDrawFields']==70
        pins[str(folder/'run.log')]=sync.sha(folder/'run.log')
    report=dict(passed=True,results=results,pins=pins,sourceSync=sync.verify(),
        sealSha256=sync.sha(Path(__file__)),
        scope='Every opaque body-component pixel at every native draw from P1 cross-added ground-throw entry through first persistent paired idle; includes explicit actual camera crop',
        entireFramebufferAccepted=False,subjectiveChoreographyAccepted=False,
        fullThrowAudioAccepted=False,allVictimsSlotsAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
