"""Preserve full scope, actual rare native drop, and rejected held RGB premises."""
import json
import subprocess
from pathlib import Path

import verify_current_tomb_drop_physics_v3618 as drop
import verify_current_stage_hook_caller_states_v3620 as hooks

ROOT,need,sha=drop.ROOT,drop.need,drop.sha
PREVIOUS=ROOT/'audit_v3593_current_native_feature_coverage_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3623_current_tomb_drop_full_scope_checkpoint'


def main():
    need(not OUT.exists(),'Fresh full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and
         not state['finishedRelease']and state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted']and
         state['current3172BothHumanSlotsFullRetainedFriendshipAudioAccepted']and
         state['current3172BothHumanSlotFullVisibleFriendshipSceneAndTransitionAccepted'],
         'Full original objective and actual completed current gates retained')
    fresh={}
    def pin(file,wanted=None):
        key=str(Path(file).resolve());actual=sha(file)
        need(wanted is None or wanted==actual,'Relevant actual evidence/source/public bytes unchanged')
        need(key not in fresh or fresh[key]==actual,'Consistent new dependency')
        need(key not in state['inputHashes']or state['inputHashes'][key]==actual,'Never relabel inherited evidence')
        fresh[key]=actual
    drop_path=drop.OUT/'report.json';proof=json.loads(drop_path.read_text())
    need(proof['passed']and proof['actualNativeKanoP1TombRandomDropPhysicsAndCleanupAccepted']and
         proof['actualNativeRandomValue']==7 and proof['nativeThreshold']==50 and
         proof['phase']['checkedConsecutiveCallbacks']==269 and proof['phase']['nativeLandingField']==8486 and
         len(proof['qualifiedActualFieldFaults'])==4 and proof['allOriginalPhysicalInputsAndEarnedDamageRecordsUnchanged']and
         proof['completeOriginalNativeSourceRangesUnchanged']and
         not proof['standaloneCurrentForensicChildExitCodeMetadataAvailable']and
         not proof['actualCurrentVisibleSceneArtShadowsEraseAndAudioAccepted']and
         not proof['actualHeldSceneRGBReferenceApplicableToThisRandomDrop']and not proof['fullPortAcceptance'],
         'Actual current original branch physics, not held images/missing child metadata/full raster acceptance')
    hook_path=hooks.OUT/'report.json';hook=json.loads(hook_path.read_text())
    need(hook['passed']and hook['actualNonmatchingPaletteRequests']==1723 and hook['actualNativePoolResets']==5 and
         hook['completeCallerStatusSPA0A14StatePairs']==1728 and len(hook['actualQualifiedRegisterFaults'])==4 and
         hook['nativeSharedHookNonmatchCallerPreservationAccepted']and
         hook['exactTypedFriendshipPaletteOrOwnedBubbleRetirementPathNeverEntered']and
         not hook['actualGameplayEquivalenceToNoHookObservationAccepted']and
         not hook['currentVisibleSceneAcceptance']and not hook['universalPassThroughOtherScenesOrStageAudioAccepted'],
         'Observed native caller states do not imply observer-independent complete gameplay/raster')
    for path,report in ((drop_path,proof),(hook_path,hook)):
        pin(path)
        for file,wanted in report['inputHashes'].items():pin(file,wanted)
    # Original1836 control independently reproduces the complete retained held
    # reference without heavy VRAM/audio/image recording. Its parent aggregate
    # invocation failed on the different CURRENT drop, which remains failed.
    legacy=ROOT/'audit_v3611_legacy_tomb_snapshot_forensic'
    legacy_path=legacy/'result.json';positive=json.loads(legacy_path.read_text())
    fields=json.loads((legacy/'visible_frames.json').read_text())
    need(positive['captureCompleted']and positive['exit_code']==0 and positive['frames']==537 and
         positive['mismatchFrames']==0 and positive['allPhysicalNativeProvenanceRecordsUnchanged']and
         len(fields)==537 and all(row['currentRGB_SHA256']==row['referenceRGB_SHA256']and row['differingPixels']==0 for row in fields),
         'Actual untouched-build full visible positive control, not current-build transfer')
    for file,wanted in json.loads((legacy/'input_hashes_before.json').read_text()).items():pin(file,wanted)
    for file in legacy.rglob('*'):
        if file.is_file():pin(file)
    rejected=[]
    for relative in ('audit_v3599_current_tomb_palette_pixels_checked/report.json',
                     'audit_v3603_current_tomb_palette_pixels_checked/report.json',
                     'audit_v3607_stage_snapshot_forensic/report.json',
                     'audit_v3612_stage_snapshot_forensic/report.json'):
        path=ROOT/relative;report=json.loads(path.read_text())
        need(not report['passed']and not report['fullPortAcceptance'],'Preserve all rejected actual invocations')
        pin(path);rejected.append(str(path))
    capture_leaves=(drop.stage.CASE,ROOT/'audit_v3606_legacy_tomb_snapshot_forensic',
                    ROOT/'audit_v3606_current_tomb_snapshot_forensic',legacy,drop.CASE)
    storage_files=[]
    for folder in capture_leaves:
        for file in folder.rglob('*'):
            if file.is_file():storage_files.append(file);pin(file)
    need(len(capture_leaves)==5 and not any(file.suffix.lower()in('.exe','.wav','.png','.jpg','.bmp')for file in storage_files),
         'Small compressed diagnostic leaves only, no executable/PCM/pixel-image copies')
    for relative in (state['currentCMD'],state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        file=ROOT/relative;pin(file,state['inputHashes'][str(file.resolve())])
    for relative in ('tools/run_stage_snapshot_forensic_v3605.py','tools/run_stage_snapshot_forensic_v3610.py',
                     'tools/verify_current_stage_hook_nonmatch_v3608.py','tools/verify_current_tomb_drop_physics_v3614.py',
                     'tools/verify_current_tomb_drop_physics_v3616.py','mk2ks_stage_snapshot_forensic_v3604.lua'):
        pin(ROOT/relative)
    pin(PREVIOUS);pin(__file__)
    state['inputHashes']=fresh
    state['currentScopeEvidenceAudit']['group1']=(
        '3619now proves actual3172 naturalKanoP1->Sonya18 Tomb random-drop branch from real unassisted inputs, '
        'two earned matches/full-health damage, original RNG7<50 and unchanged original Tomb/RNG/fall/teardown '
        'bytes.269actual callbacks prove128hold/112slow descent/native16.16fall/own-floor landing and native '
        'actor teardown/next arena,4qualified actual field faults. Prior1836held RGB reference was an incorrect '
        'branch oracle for this current drop; preserve failed3603/3607/3612invocations, no visual/audio promotion. '
        'Untouched1836RAM control3611reproduces all537heldRGB fields exactly and all native physical/provenance '
        'records.3621observes1723nonmatching allocator requests/5pool resets,1728exact caller status/SP/A0-A14 '
        'pairs and4register faults; hook observer versus no-hook observation gameplay equivalence NOT accepted. '
        'Current whole-stage art/shadow/erase, stock/new victim/mirror branches, Pit and stage-audio fidelity '
        'remain broader gates, not automatically inherited or certified by exact stock table bytes.')
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: inspect3593typed feature matrix/current dirty state/retained1836Tomb observer and original native branch. Preserve806physical driver with only2read-only PNG calls omitted; current RAM pixels/register observers, no game edits.3597pre-capture trailing blank comparison fails; corrected3602runs3598terminal0/all537RGBfields but502mismatch held oracle.3608old-held full state comparison fails. Fresh3605legacy/current no-hook diagnostic runs both to native terminal but aggregate checker includesFORENSICrecords wrongly and produces no standalone metadata.3610corrects prefix and preserves physical differences; actuallegacy3611terminal0/all537RGBexact and full native provenance exact; current naturallyselects original RNG7drop, hardcoded old SonyaP2-only drop gate rejects parent3612, current standalone exit metadata missing. Do not force RNG/positions, normalize fields, change game for different native random branch, or rerun completed captures just to repair metadata. Fresh3614syntax error and3616pre-action owner qualification preserved;3618correctly scopes original action callback window.3619independently proves actual true17->18 original native drop269callbacks,128hold/112slow descent/nativefall/ownfloor/cleanup and4qualified faults.3621separately accepts1728actual nonmatching hook caller-state pairs/4faults, explicitly not complete observer-independent gameplay/visual acceptance. Full original5groups/currentprior gates preserved; new5smallcompressed diagnostic leaves46files13.7MBlogical, zeroEXE/WAV/PNG/VRAMcopies. No source/playable/public changes.',
        current3172NativeKanoP1TombDropPhysicsReport=str(drop_path),
        current3172NativeKanoP1TombDropPhysicsAndCleanupAccepted=True,
        current3172NativeKanoP1TombDropActualRandomValue=7,
        current3172NativeKanoP1TombDropCheckedCallbacks=269,
        current3172NativeKanoP1TombDropSceneVisualArtShadowEraseAudioAccepted=False,
        current3172TombStandaloneCurrentForensicChildExitCodeMetadataAvailable=False,
        current3172StageHookCallerStatesReport=str(hook_path),
        current3172SharedPaletteResetObservedNonmatchCallerStatePreservationAccepted=True,
        current3172SharedPaletteResetUniversalPassThroughRuntimeAccepted=False,
        current3172StageHookObservationGameplayEquivalenceToNoHookObservationAccepted=False,
        untouched1836TombHeldRAMPositiveControl=str(legacy_path),
        untouched1836TombHeldExactCurrentControlVisibleFields=537,
        untouched1836TombHeldExactCurrentControlRGBPixels=54559200,
        rejectedCurrentTombHeldAndForensicVerifierReports=rejected,
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,newRuntimeCaptureLeavesThisTurn=5,
        acceptedVisibleScenarioCapturesThisTurn=0,rawPixelImageVRAMCopiesThisTurn=0,
        diagnosticGuestProgramDumpsThisTurn=5,
        freshDiagnosticCaptureFilesThisTurn=len(storage_files),
        freshDiagnosticCaptureLogicalBytesThisTurn=sum(file.stat().st_size for file in storage_files),
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),historicalPinMapCopiedAgain=False,
        nextAction='Do not rerun completed P1 campaigns/endings/Friendship/3619native drop physics/3611legacyheldRGB or current forensic windows merely for metadata. Current RNG7drop is legitimate original native5-percent branch; old held RGB oracle is inapplicable. Next actual visual gate should source-replay current actual native FIFO/DMA/palettes/ground/shadow/erase for this drop, streaming diagnostics in RAM rather than assuming identical blood/RNG/held outcome or duplicating PNG/VRAM/WAVfiles. Explain observer-sensitive state facts before accepting noninterference;1728caller-state pairs alone are not universal gameplay equivalence. Use3591typed move/finisher/victim matrix to consolidate finite missing feature/branch gates and final combined currentselection/ladder/names/audio gate, then refreshed releaseZIP. Preserve all5groups/public1836CMD/ZIP/retired exclusions; no speculative global game hook fixes solely for alternate original random outcome.')
    need(state['remaining']==remaining,'Original five requirements unchanged')
    OUT.mkdir();saved=OUT/'checkpoint.json';saved.write_text(json.dumps(state,indent=2)+'\n')
    before=sha(saved);result=subprocess.run(['compact.exe','/C','/I','/Q',str(saved)],capture_output=True,text=True)
    need(result.returncode==0 and sha(saved)==before,'Lossless compact full-scope checkpoint')
    print(json.dumps(dict(saved=str(saved),goalStatus='active',newActualNativeDropCallbacks=269,
                         exactObservedHookCallerPairs=1728,qualifiedActualFieldRegisterFaults=8,
                         freshRelevantPins=len(fresh),newExecutableROMWAVPixelVRAMCopies=0,fullPortAcceptance=False),indent=2))


if __name__=='__main__':main()
