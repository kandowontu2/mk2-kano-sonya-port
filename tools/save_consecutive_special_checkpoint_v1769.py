"""Retain the full natural-integration goal and bounded current-state evidence."""
import json
from pathlib import Path
from verify_human_special_phases_v1767 import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1769_consecutive_special_frontier_checkpoint'

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite a checkpoint'
    priorpath=ROOT/'audit_v1730_original_tomb_frontier_checkpoint/checkpoint.json'
    prior=json.loads(priorpath.read_text());assert prior['goalStatus']=='active'
    pins={str(priorpath):sha(priorpath)};accepted=dict(prior['acceptedReports'])
    names=['audit_v1732_current_stage_variants_checked','audit_v1733_current_stage_variant_units',
           'audit_v1744_portable_playtest_zip_checked','audit_v1746_current_sonya_defensive_leg_campaign_checked',
           'audit_v1747_current_kano_boss_tactics_campaign_checked','audit_v1749_current_sonya_boss_evasion_checked',
           'audit_v1750_current_kano_boss_evasion_checked','audit_v1767_human_special_phases_checked',
           'audit_v1768_human_special_phase_units_checked']
    reports={}
    for name in names:
        path=ROOT/name/('verification.json'if name=='audit_v1733_current_stage_variant_units'else'report.json')
        report=json.loads(path.read_text(encoding='utf-8-sig'));assert report['passed'];reports[name]=report
        pins[str(path)]=sha(path)
        for p,h in report.get('inputHashes',{}).items():
            assert sha(p)==h,'Changed accepted evidence '+p;pins[p]=h
        accepted[name]=dict(reportSHA=pins[str(path)],scope=report.get('scope','Exact declared test scope only'),fullPortAcceptance=False)
    for p,h in{
      'diagnostic_v1597_native_ground_throw/mkport_candidate.exe':'9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695',
      'diagnostic_v1597_native_ground_throw/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'PLAY_CURRENT_V1597_TEST_BUILD.cmd':'85962962ADA430B706B4052A28A8809D1E53EF3D98FE3C44831D709898375DAB',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():
        path=ROOT/p;assert sha(path)==h;pins[str(path)]=h
    portable=reports['audit_v1744_portable_playtest_zip_checked'];package=Path(portable['zip'])
    assert sha(package)==portable['zipSHA256'];pins[str(package)]=portable['zipSHA256']
    phase=reports['audit_v1767_human_special_phases_checked']
    assert phase['totalConsecutiveScenes']==1975 and phase['nativeCompositeParts']==8070
    for case in phase['cases']:
        for entry in case['contactSheets']:
            assert sha(entry['file'])==entry['sha256'];pins[entry['file']]=entry['sha256']
    # This records only images actually inspected, not every retained phase.
    reviewed=['leg_p1_1.png','ball_p1_1.png','choke_p1_1.png','square_air_p1_1.png','bicycle_p1_1.png',
              'ball_p1_2.png','leg_p1_2.png','leg_p1_3.png','blade_p1_1.png','knife_p1_1.png','ring_p1_1.png']
    for name in reviewed:
        path=ROOT/'audit_v1767_human_special_phases_checked'/name;assert path.is_file();pins[str(path)]=sha(path)
    report={k:v for k,v in prior.items()if k!='inputHashes'}
    report.update(goalStatus='active',fullPortAcceptance=False,acceptedReports=accepted,
      previousGoalTurnClassification='no progress: user requested status only; actual terminal campaign outputs revalidated before fresh work',
      thisGoalTurnClassification='progress: independently verified two terminal native campaigns; captured and verified 18 consecutive special-phase fixtures, native original clipping, unchanged physical events and 14 negative cases',
      currentFullStageMatrixAccepted=True,stageMatrixScope='Eight original held/drop Tomb/Pit positives plus twelve physical invalid-command/range/arena rejections. Does not certify full stage-finisher scene art/audio.',
      currentAllEightMoveConsecutiveScenesAccepted=True,currentConsecutiveSpecialScenes=1975,currentNativeSpecialCompositeParts=8070,
      currentNativeSpecialClippedParts=13,currentSpecialPhaseNegativeCasesRejected=14,
      fullMovePhaseRasterShadowEraseAccepted=False,fullMoveChoreographyAccepted=False,
      manuallyViewedContactSheets=reviewed,
      manualReviewScope='Eleven unchanged full-frame P1 sheets viewed: bodies and shadows visible, no obvious headless living actor in viewed tiles. Not all P2/fields, independent pixel/erasure/audio proof, all victim/arena or universal artistic acceptance.',
      nativeCampaigns={name:{k:reports[name][k]for k in('player','human_slot','stages_reached','native_own_round_wins','paid_continue_losses','unassisted_clear_proven','ending_starts','ending_completions')}for name in names if'boss_evasion_checked'in name},
      pendingCaptures=[],playtestZip=str(package),portablePlaytestZipVerified=True,finishedRelease=False,
      cleanupAllocatedBytesReclaimed=prior['cleanupAllocatedBytesReclaimed'],cleanupAdditionalBytesReclaimedThisTurn=0,
      deletedFilesThisTurn=0,allOldBuildFoldersRemoved=False,
      preservedFailedNewEvidence=['audit_v1753_human_leg_p1: wrapper print start trigger absent; no move scenes recorded',
       'audit_v1761_human_special_phases_checked: exact source checker encountered one omitted terminal empty line',
       'audit_v1762_human_special_phases_checked: failed full-publication assumption on original clipped ball victim components',
       'audit_v1766_human_special_phases_checked: verifier-local display Y variable shadowed actor lookup; fresh1767 fixes variable only'],
      nextAction='Use current consecutive phase evidence for complete native pixel/shadow/erase continuity validation; expand finisher/victim/morph/audio/cinematic coverage and genuine full boss clears/endings. Preserve current playable build and full original goal.',
      remainingFullScope=['Full move-phase raster/art/shadow/erase continuity and broader repeated/interrupt/KO/CPU/audio cases',
       'All remaining finisher/victim/morph/friendship/secrets/cinematics including stage-finisher presentation',
       'Genuine full boss/campaign clears for both true-ID fighters, own complete endings and return to attract',
       'Final combined native CSS, ladder, names, grounding, audio and gameplay acceptance',
       'Remaining dependency-aware obsolete build folder cleanup and finished release'],
      inputHashes=pins,previousCheckpointSHA=pins[str(priorpath)])
    pins[str(Path(__file__))]=sha(__file__)
    OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(pins),goalStatus='active',fullPortAcceptance=False,
                         consecutiveSpecialScenes=1975,currentPlayableBuildUnchanged=True),indent=2),flush=True)
