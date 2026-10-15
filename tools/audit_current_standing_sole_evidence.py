"""Current-state scope audit: geometry evidence is not visible sole parity."""
import json
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
OUT=ROOT/'audit_current_standing_sole_scope_checked'
def main():
    assert not OUT.exists()
    historical=ROOT/'audit_v6022_current_ordinary_kitana_raw_checked/report.json'
    proof=json.loads(historical.read_text())
    assert proof['passed'] and not proof['fullArtAcceptance']
    assert not proof['continuousWholeRGBSceneReplayAccepted']
    payload=sync.BUILD/'roms/mk2ks/mk2ks.mdata'
    assert sync.sha(payload)==proof['payloadSHA256']
    cases=proof['cases']
    assert {(c['fighter'],c['side']) for c in cases}=={(f,s) for f in ('kano','sonya') for s in (1,2)}
    assert all(c['currentOrdinaryBodyAndOriginalFloorShadowGeometryAccepted'] for c in cases)
    assert all(not c['fullArtAcceptance'] for c in cases)
    current_exe=sync.sha(sync.BUILD/'mkport_candidate.exe')
    assert current_exe!=proof['executableSHA256'],'Historical runtime is not the current executable'
    result=dict(passed=True,classification='verified_acceptance_gap',
        currentPayloadIdenticalToHistoricalGeometryPayload=True,
        historicalFourCharacterSlotGeometryCases=True,
        historicalRuntimeRequalifiedOnCurrentExecutable=False,
        currentStandingVisibleSoleParityProven=False,
        fullGoalComplete=False,sourceSync=sync.verify(),
        nextRequiredEvidence='Actual ready standing opaque body pixels for Kano/Sonya and a stock control, linked to camera, stage baseline, pose and displayed frame; do not substitute floor table equality or descriptor rectangles',
        historicalProof=str(historical),historicalProofSha256=sync.sha(historical),
        currentPayloadSha256=sync.sha(payload),currentExecutableSha256=current_exe,
        historicalExecutableSha256=proof['executableSHA256'],
        checkerSha256=sync.sha(Path(__file__)))
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('classification','currentPayloadIdenticalToHistoricalGeometryPayload','currentStandingVisibleSoleParityProven','historicalRuntimeRequalifiedOnCurrentExecutable')}))
if __name__=='__main__':main()
