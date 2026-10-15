"""Full original goal scope, fresh Bicycle evidence and explicit history retirement."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_cpu_launch_jump_v3319 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v3334_current_bicycle_full_scope_checkpoint'
PREVIOUS=ROOT/'audit_v3288_current_cpu_square_full_scope_checkpoint/checkpoint.json'
need=current.need

def main():
    need(not OUT.exists(),'Never overwrite full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=state['remaining']
    need(state['goalStatus']=='active' and len(remaining)==5 and state['candidateUnderTest']=='diagnostic_v3172_native_morph_shadow' and
         not state['fullPortAcceptance'] and not state['finishedRelease'] and not state['actualEndingsAccepted'] and state['currentRealShaoKahnMatchClears']==0,'Original full natural-port objective remains unfinished')
    cleanup_path=ROOT/'workspace_cleanup_followup_2026-10-05/verified_summary.json'
    cleanup=json.loads(cleanup_path.read_text())
    need(cleanup['passed'] and cleanup['removedObsoleteFolders']==267 and cleanup['removedOldRawTestRecordings']==84 and
         cleanup['removedObsoleteRecoveryArchives']==1 and cleanup['reclaimedAllocatedBytes']==34889808066 and cleanup['currentCMDBootPassed'] and
         cleanup['retainedInputsUnchanged']==138021,'Actual requested cleanup independently completed')
    retired=cleanup['retiredHistoricalEvidencePins']
    for file in retired:
        need(not Path(file).exists() and file in state['inputHashes'],'Explicitly retired inherited historical input, never a missing current game dependency')
        state['inputHashes'].pop(file)
    fresh={}
    def pin(path,digest=None):
        path=Path(path).resolve();key=str(path);actual=current.current.assembly.sha(path)if digest is None else digest
        need(key not in fresh or fresh[key]==actual,'Consistent fresh evidence hash')
        need(key not in state['inputHashes'] or state['inputHashes'][key]==actual,'Existing retained proof bytes never relabelled')
        fresh[key]=actual
    def proof(relative):
        path=ROOT/relative;result=json.loads(path.read_text(encoding='utf-8-sig'));need(result['passed'] and not result.get('fullPortAcceptance',False),'Completed bounded proof required')
        pin(path)
        for file,digest in result.get('inputHashes',{}).items():pin(file,digest)
        return result
    miss=proof('audit_v3313_current_cpu_bicycle_launch_response_checked/report.json')
    contact=proof('audit_v3320_current_cpu_bicycle_launch_jump_checked/report.json')
    visual=proof('audit_v3323_current_cpu_bicycle_hit_render_erase_checked/report.json')
    phase_units=proof('audit_v3328_current_cpu_bicycle_hit_phase_counterexamples/report.json')
    render_units=proof('audit_v3330_current_cpu_bicycle_hit_render_counterexamples/report.json')
    erase_units=proof('audit_v3332_current_cpu_bicycle_hit_erase_counterexamples/report.json')
    need(miss['actualBicycleMissAccepted'] and not miss['candidateBicycleHitOrBlockedAccepted'],'Real forward-step miss retained, not converted to a hit')
    need(contact['case']['health']['allModePhysicalFields']==3602 and contact['case']['selection']['errors']==0 and
         contact['actualNativeBicycleContactDamageAndSeparateRecoveryAccepted'] and contact['startupSeekPairedLiftFloatReleaseAndVerticalFallAccepted'] and
         not contact['fullHorizontalNativePushReplayAccepted'] and not contact['fullMovePhaseRasterShadowEraseAudioAccepted'],'Precisely bounded true-ID owned native contact/phase evidence')
    typed=contact['case']['phase']
    need((typed['start'],typed['hit'],typed['damage'],typed['ready'],typed['victimReady'])==(2663,2680,22,2742,2767) and
         contact['case']['nativeChoices'][0]['firstRandomResult']==134 and contact['case']['actualForwardJumpInputFields']==3,'Actual native chance, normal buttons, true original damage and separate physical recoveries')
    need(visual['sampledFrames']==109 and visual['exactScreenPixels']==11074400 and visual['nativeShadowCopies']==8067 and
         visual['sourceBoundProjections']==337 and visual['continuousExactFlips']==109 and visual['originalOwnAndVictimBicyclePosesVisible'] and
         visual['fullCapturedNativeBodyPaletteShadowAndChronologicalEraseAccepted'] and not visual['fullMovePhaseAndHorizontalPushAccepted'],'Complete actual paired original art/palette/shadow/erase, no broad phase claim')
    need(phase_units['actualCounterexamplesRejected']==28 and render_units['actualCounterexamplesRejected']==16 and erase_units['actualCounterexamplesRejected']==18 and
         phase_units['samePathPositiveControlsAccepted'] and render_units['sameMockedPathPositiveControlAccepted'] and erase_units['sameMockedPathPositiveControlsAccepted'] and
         all(p['unrelatedMissingEventExceptionsNeverAccepted']for p in (phase_units,render_units,erase_units)),'All62 actual corruptions specifically rejected with same-path passing controls')
    pin(cleanup_path);pin(ROOT/'workspace_cleanup_followup_2026-10-05/deletion_plan.json');pin(ROOT/'WORKSPACE_CLEANUP_CURRENT.md')
    failures=[]
    for report,script,cause in (
        ('audit_v3311_current_cpu_bicycle_launch_response_checked/report.json','tools/verify_current_cpu_launch_response_v3299.py','Old generic parser lacked explicit policy string and CPU action hex fields. Successor adds only strict launch-response schema parsing.'),
        ('audit_v3325_current_cpu_bicycle_hit_phase_counterexamples/report.json','tools/test_current_bicycle_hit_v3324.py','Raw-coordinate mutation first failed its redundant signed view. Successor changes both consistent views and requires the intended deeper phase invariant.')):
        path=ROOT/report;value=json.loads(path.read_text());need(not value['passed'],'Harness failure remains failed')
        pin(path);pin(ROOT/script);failures.append(dict(report=str(path),error=value['error'],cause=cause))
    pin(ROOT/'tools/native_cpu_bicycle_hit_contract_v3316.py')
    failures.append(dict(script='tools/native_cpu_bicycle_hit_contract_v3316.py',error='All twelve original reverse-intro release fields',
                         cause='Original draft forgot 32-bit wrap after negative world Y. Observed signed crossing preserved; successor uses the exact native 32-bit mask. No game or capture edited.'))
    pin(PREVIOUS);pin(__file__)
    print('Rehashing current evidence/source inputs:',len(fresh),flush=True)
    with ThreadPoolExecutor(max_workers=4)as pool:
        for (file,digest),actual in zip(fresh.items(),pool.map(current.current.assembly.sha,fresh)):
            need(actual==digest,'All actually executed input/capture bytes unchanged')
    state['inputHashes'].update(fresh)
    state.update(previousCheckpoint=str(PREVIOUS),
                 previousGoalTurnClassification='progress: explicit requested follow-up removed267obsoletefolders/84failedcampaignrawmixes/oneoldrecoveryarchive;32.49GiBallocatedreclaimed;138021retainedinputsunchanged/50SHAguards/CMDbootpass. Historical85pins explicitly retired, not regenerated.',
                 thisGoalTurnClassification='progress: existing3172normalinputforwardstepmissandforwardjumpBicyclehit independently verified wholeguest/correctedpayload/full3602HPstatefields/nativechoice134. TrueID18CPUdeals22HPtohuman17;ownedstartup/seek/pairedlift/16float/reverseintro/verticalfall/separateready2742/2767. Full109scenes/11074400pixels/8067nativeblackshadowcopies/337sourceprojections/109onebaseflips.62specificphase/raster/erasecorruptionsrejectedwithsamepathpositivecontrols. No newbuild/ROM/capture/audio/gameedit/promotion; horizontaloriginalclosebodypushreplaynotaccepted; allfivefullportgroupsremain.',
                 goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
                 currentNativeBicycleContactDamageAndSeparateRecoveryAccepted=True,
                 currentNativeBicycleCapturedOriginalArtPaletteShadowEraseAccepted=True,
                 currentNativeBicycleStateReport=str(current.OUT/'report.json'),
                 currentNativeBicycleRenderEraseReport=str(ROOT/'audit_v3323_current_cpu_bicycle_hit_render_erase_checked/report.json'),
                 currentNativeBicyclePhysicalCase=current.CASE,currentNativeBicycleDamage=22,
                 currentNativeBicycleOwnReady=2742,currentNativeBicycleVictimReady=2767,
                 currentNativeBicycleExactScenes=109,currentNativeBicycleShadowCopies=8067,
                 currentNativeBicycleQualifiedCounterexamples=62,
                 candidateUnderTestNativeBicycleHitOrBlockedAccepted=False,
                 currentNativeBicycleFullHorizontalPushReplayAccepted=False,
                 currentNativeBicycleBlockedAllArenasAudioKOOverlapAccepted=False,
                 currentCPUHarnessFailuresPreserved=failures,
                 latestRequestedCleanupReport=str(cleanup_path),latestRequestedCleanupReclaimedAllocatedBytes=34889808066,
                 latestRequestedCleanupRemovedObsoleteFolders=267,latestRequestedCleanupHistoryPermanentlyDiscarded=True,
                 explicitlyRetiredHistoricalInputPins=retired,currentRequestedCleanupRecoveryArchive=None,
                 retiredArchiveAndFailedCampaignAudioMustNotBeRecreated=True,
                 inheritedHistoricalGraphRevalidatedInFullThisTurn=False,revalidatedFreshRelevantFilePins=len(fresh),
                 gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
                 publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
                 nextAction='Keep3172isolated. Independently account for original horizontal close-body push during Bicycle release; then ordinary-input blocked/contact/CPU/KO/overlap/morph contexts and remaining native art/arena/finisher/audio gates. Do not recreate retired raw failed-campaign mixes/archive. Natural Kintaro/Shao match clears, own endings/attract, full combined selection/ladder/names/audio and refreshed release remain required. Reuse existing builds and bounded compressed captures. All five original remaining groups unchanged.')
    need(state['remaining']==remaining and len(remaining)==5 and not state['actualEndingsAccepted'] and state['currentRealShaoKahnMatchClears']==0 and
         not state['candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted'],'Original scope and unfinished gates never reduced')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n');digest=current.current.assembly.sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and current.current.assembly.sha(path)==digest,'Lossless full checkpoint compression verified')
    print(json.dumps(dict(saved=str(path),goalStatus='active',originalRemainingGroups=5,nativeBicycleDamage=22,
                         exactScenes=109,qualifiedCorruptionsRejected=62,fullHorizontalPushAndAllCPUAccepted=False,
                         freshPinsRehashed=len(fresh),retiredHistoricalPins=85,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
