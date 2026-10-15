"""Preserve the whole natural-integration objective and new rendering frontier."""
import json
from pathlib import Path
from verify_human_special_phases_v1767 import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1803_native_special_render_frontier_checkpoint'

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite a checkpoint'
    priorpath=ROOT/'audit_v1769_consecutive_special_frontier_checkpoint/checkpoint.json'
    prior=json.loads(priorpath.read_text());assert prior['goalStatus']=='active'
    matrixpath=ROOT/'audit_v1813_special_full_render_matrix_checked/report.json'
    matrix=json.loads(matrixpath.read_text());assert matrix['passed']and matrix['fixtureCount']==18
    pins={str(priorpath):sha(priorpath),str(matrixpath):sha(matrixpath)}
    for report in(prior,matrix):
        for p,h in report['inputHashes'].items():
            assert sha(p)==h,'Changed authoritative evidence '+p
            assert p not in pins or pins[p]==h;pins[p]=h
    accepted=dict(prior['acceptedReports'])
    accepted['audit_v1813_special_full_render_matrix_checked']=dict(reportSHA=sha(matrixpath),scope=matrix['scope'],fullPortAcceptance=False)
    report={k:v for k,v in prior.items()if k!='inputHashes'}
    viewed=['audit_v1796_human_leg_p1_render/snap/display_1620.png',
            'audit_v1800_human_bicycle_p2_render/snap/display_1640.png',
            'audit_v1800_human_blade_p1_render/snap/display_1595.png',
            'audit_v1800_human_choke_p2_render/snap/display_1610.png',
            'audit_v1806_human_ball_p2_render/snap/display_1709.png',
            'audit_v1806_human_ball_p2_render/snap/display_1710.png',
            'audit_v1806_human_ball_p2_render/snap/display_1711.png']
    for name in viewed:pins[str(ROOT/name)]=sha(ROOT/name)
    report.update(goalStatus='active',fullPortAcceptance=False,acceptedReports=accepted,
      previousGoalTurnClassification='no progress: status-only request inspected latest evidence; next safe rendering action was available',
      thisGoalTurnClassification='progress: original native shift-register clearing observed read-only; independently verified 18 cold physical special fixtures for full consecutive source/body/palette/shadow/erase continuity and 18 in-memory negative tests',
      gameSourceAndPlayableBytesChangedThisTurn=False,currentPlayableBuildUnchanged=True,
      boundedPositiveSpecialNativeRasterShadowAndEraseAccepted=True,
      boundedPositiveSpecialRasterScope=matrix['scope'],boundedPositiveSpecialFixtures=matrix['fixtureCount'],
      boundedPositiveSpecialConsecutiveFullScenes=matrix['consecutiveFullScenes'],
      boundedPositiveSpecialNativeBodyDraws=matrix['sourceBoundBodyDraws'],
      boundedPositiveSpecialExactNativeShadowCopies=matrix['exactNativeShadowCopies'],
      boundedPositiveSpecialNativeClearTransfers=matrix['nativeShiftTransfers'],
      continuousEraseNegativeCasesRejected=18,fullMovePhaseRasterShadowEraseAccepted=False,
      fullMoveChoreographyAccepted=False,universalArtisticGroundingAcceptance=False,
      ballBoundaryDepartureNativeFeelingAccepted=False,
      ballBoundaryEvidence='P2 rebound render fields 1709:29 body pixels, 1710/1711:0 body pixels. Actual source-bound viewport clipping and matching shadow departure proven. Movement/native-feeling acceptance remains unproven; do not count pixel agreement as choreography acceptance.',
      newlyManuallyViewedFullScenes=viewed,
      manualReviewScope='Seven actual new full scenes viewed, including leg handstand, airborne bicycle, blade, choke and three P2 ball boundary frames. Kano briefly leaves the right viewport during rebound; movement review/fix remains open. Not universal artistic, victim, arena or cinematic review.',
      pendingCaptures=[],newReleaseZIPCreated=False,finishedRelease=False,
      deletedFilesThisTurn=0,cleanupAdditionalBytesReclaimedThisTurn=0,allOldBuildFoldersRemoved=False,
      inspectedCompilerCache='x32 contains no files; x64 has 2906 current regenerable outputs totaling 420009240 logical bytes. Current useful cache preserved; no compiler process was live when inspected.',
      preservedFailedNewEvidence=prior.get('preservedFailedNewEvidence',[])+[
       'audit_v1779_human_leg_p1_continuity_diagnostic: ordinary write/DMA recorder omitted original TMS shift-register clear',
       'audit_v1782_human_leg_p1_render: newly generated observer string escaping syntax error, no game execution',
       'audit_v1791_human_leg_p1_continuity_checked: verifier path separators did not normalize source manifest',
       'audit_v1792_human_leg_p1_continuity_checked and audit_v1793_human_leg_p1_render_checked: native fill offset name collided with decimal graphics-stream offset parser; new capture1796 uses native_offset',
       'audit_v1798_human_leg_p1_continuity_checked: verifier dispatched before capture terminal manifest existed; existing live capture awaited, never restarted',
       'audit_v1800_human_ball_p2_render_checked: blanket body visibility assumption failed at legitimate viewport departure; new full capture1806 retains original pre-clip candidates',
       'audit_v1807_human_ball_p2_render_checked: clipping arithmetic reused unsigned publication coordinates; fresh1808 uses signed pre-clip coordinates',
       'audit_v1808_human_ball_p2_render_checked: low-pixel native boundary frame has partial source rectangles, not full component culls; fresh1811 proves the actual partial and complete viewport clipping',
       'audit_v1811_human_ball_p2_render_checked: blanket visible-shadow assumption failed during actual viewport departure; fresh1812 source-matches body/shadow clipping but leaves native movement acceptance false',
       'audit_v1807_human_ball_p1_continuity_checked and audit_v1807_human_ball_p2_continuity_checked: generic parser did not recognize new hexadecimal clipping-bound observation fields; fresh1809 adds metadata parsing only'],
      nextAction='Investigate and resolve Kano ball rebound boundary departure against native reference choreography, then broader special repeated/blocked/interrupted/KO/CPU victim/arena coverage, genuine full boss clears/endings, remaining finisher/morph/cinematic/audio acceptance; dependency-aware cleanup and final release. Full original natural-integration goal remains active.',
      remainingFullScope=[
       'Broader repeated/blocked/interrupted/KO/CPU special fixtures and all victim/arena rendering, audio, universal artistic grounding; review brief Kano ball boundary departure against native reference choreography',
       'All remaining finisher/victim/morph/friendship/secrets/cinematics including complete stage-finisher presentation',
       'Genuine full boss/campaign clears for both true-ID fighters, own complete endings and return to attract',
       'Final combined native CSS, ladder, names, grounding, audio and gameplay acceptance',
       'Remaining dependency-aware obsolete build folder cleanup and finished release'],
      previousCheckpointSHA=sha(priorpath),inputHashes=pins)
    pins[str(Path(__file__))]=sha(__file__)
    OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(pins),goalStatus='active',fullPortAcceptance=False,
                         boundedPositiveSpecialFixtures=18,fullScenes=matrix['consecutiveFullScenes'],currentPlayableBuildUnchanged=True),indent=2),flush=True)
