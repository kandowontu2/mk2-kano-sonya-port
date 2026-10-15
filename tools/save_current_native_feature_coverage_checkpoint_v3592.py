"""Preserve full objective and current table/branch inventory without new builds."""
import json
import subprocess
from pathlib import Path

import map_current_native_feature_coverage_v3590 as inventory

ROOT, need, sha = inventory.ROOT, inventory.need, inventory.sha
PREVIOUS = inventory.PREVIOUS
OUT = ROOT / 'audit_v3593_current_native_feature_coverage_full_scope_checkpoint'


def main():
    need(not OUT.exists(), 'Never overwrite full-scope checkpoint')
    state = json.loads(PREVIOUS.read_text())
    remaining = list(state['remaining'])
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'] and
         state['current3172BothHumanSlotsFullRetainedFriendshipAudioAccepted'] and
         state['current3172BothHumanSlotFullVisibleFriendshipSceneAndTransitionAccepted'] and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Preserve original scope and completed actual current gates')
    report_path = inventory.OUT / 'report.json'
    report = json.loads(report_path.read_text())
    need(report['passed'] and report['candidate'] == inventory.NAME and
         report['wholeCurrentGuestIndependentlyReconstructed'] and
         report['wholeCurrentPayloadIndependentlyReconstructed'] and
         report['guestDeltaFrom1836']['changedBytes'] == 254 and
         report['payloadDeltaFrom1836']['changedBytes'] == 68 and
         report['payloadDeltaFrom1836']['descriptors'] == 12 and
         len(report['tables']) == 18 and len(report['coverage']) == 14 and
         len(report['actualFinalCPUVarietyBranches']) == 2 and
         len(report['actualQualifiedInventoryFaults']) == 3 and
         not report['guestDeltaFrom1836']['universalRuntimePassThroughProven'] and
         not report['completeIncludedHeaderGraphDirectlyComparedTo2753'] and
         not report['finisherSetInventoryExhaustive'] and
         not report['secondIndividualFatalityRequirementInferred'] and
         report['newRuntimeCaptures'] == report['newExecutableROMWAVPixelImageCopies'] == 0 and
         not report['gameOrPublicBytesChanged'] and not report['fullPortAcceptance'],
         'Actual narrow source/table/delta inventory is not new or universal runtime acceptance')
    fresh = {}

    def pin(path, wanted=None):
        key = str(Path(path).resolve())
        actual = sha(path)
        need(wanted is None or actual == wanted, 'Relevant actual input unchanged')
        need(key not in fresh or fresh[key] == actual, 'Consistent fresh pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == actual,
             'Do not relabel inherited actual evidence')
        fresh[key] = actual

    pin(report_path)
    for file, wanted in report['inputHashes'].items():
        pin(file, wanted)
    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        item = ROOT / relative
        pin(item, state['inputHashes'][str(item.resolve())])
    pin(PREVIOUS)
    pin(__file__)
    state['inputHashes'] = fresh
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: current native feature/branch matrix from actual3172 whole initialized guest and independently reconstructed guest/payload, actual compiled graph and correct typed table strides. Only254guest bytes differ from1836 in known Friendship palette/reset spans; only68payload bytes in12morph source/format descriptors differ. Whole current machine/tms34010.cpp/video.cpp identical2753; driver only payload metadata. Included gfx/ops headers current compile-bound but old2753direct snapshots absent, explicitly no full included-header comparison.18native tables preserve stock rows and own entries, correct24action-vs19fighter schemas; native stage/individual input tuples and final event wrappers checked. Actual CPU random variety routes independently encoded:KanoKnife/Ball/Blade,SonyaRing/Square/Bicycle.14bounded feature rows retain actual tested builds; no automatic1836stage runtime promotion.3qualified inventory faults. Failed3584invented prior header path and3586early AI initialization assumptions preserved; corrected3588passed and refined3590passed, terminal0. No new runtime/EXE/ROM/WAV/pixel/VRAM copies, no game/public/source edits. Full5groups/retired exclusions retained.',
        current3172NativeFeatureCoverageMatrixReport=str(report_path),
        current3172NativeFeatureCoverageMatrixTableCount=18,
        current3172NativeFeatureCoverageMatrixBoundedFeatureRows=14,
        current3172GuestDeltaFrom1836ChangedBytes=254,
        current3172PayloadDeltaFrom1836ChangedBytes=68,
        current3172PayloadDeltaOnlyTwelveMorphSourceFormatDescriptors=True,
        current3172CompiledMachineAndMainCPURendererSourceIdentical2753=True,
        current3172CompleteIncludedHeaderGraphComparedTo2753=False,
        current3172CurrentTableInvariantsAutomaticallyPromote1836StageRuntime=False,
        current3172SharedPaletteResetUniversalPassThroughRuntimeAccepted=False,
        current3172NativeFinisherSetInventoryExhaustive=False,
        secondIndividualFatalityRequirementInferredThisTurn=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        newRuntimeCaptureLeavesThisTurn=0,
        acceptedVisibleScenarioCapturesThisTurn=0,
        rawPixelImageVRAMCopiesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        historicalPinMapCopiedAgain=False,
        nextAction='Use3591typed table/feature matrix. Next targeted current3172 representative non-Friendship full stage scene should cover exact global palette allocator/reset nonmatching path; compare native physical state/actual visible RGB to retained1836 source-bound reference without new images/VRAM/WAV/executable copies. Do not rerun completed P1 campaigns/own photo/text/common-frame/Friendship sequences. Consolidate explicitly missing native move/finisher/victim/secret branches and final combined selection/ladder/names/audio gate, then refreshed releaseZIP. Stock19fighter/24action table invariants and identical source are not universal runtime coverage; included header historical gap explicit. Preserve all5original groups/public1836CMD/ZIP/retired exclusions. Do not infer second individual fatality scope from recalled names.')
    need(state['remaining'] == remaining, 'All five original requirements unchanged')
    OUT.mkdir()
    saved = OUT / 'checkpoint.json'
    saved.write_text(json.dumps(state, indent=2) + '\n')
    before = sha(saved)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(saved)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(saved) == before, 'Lossless compact checkpoint')
    print(json.dumps(dict(saved=str(saved), goalStatus='active', nativeTables=18,
                         boundedFeatureRows=14, freshPins=len(fresh),
                         newRuntimeOrPlayableCopies=0, fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
