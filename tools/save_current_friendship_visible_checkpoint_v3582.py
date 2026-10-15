"""Save bounded current visible Friendship proof and preserve full port scope."""
import json
import subprocess
from pathlib import Path
import verify_current_friendship_snapshot_pixels_v3579 as visible

ROOT, need, sha = visible.ROOT, visible.need, visible.sha
PREVIOUS = ROOT / 'audit_v3565_current_friendship_ram_audio_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v3583_current_friendship_visible_full_scope_checkpoint'


def main():
    need(not OUT.exists(), 'Fresh immutable full-scope checkpoint')
    state = json.loads(PREVIOUS.read_text())
    remaining = state['remaining']
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         state['current3172BothHumanSlotsFullRetainedFriendshipAudioAccepted'] and
         state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'] and
         state['current3172BothNaturalP1NativePhotoFrameOverpaintAndCommonBackgroundAccepted'] and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Whole original objective and earlier actual accepted gates retained')
    fresh = {}

    def pin(path, wanted=None):
        key = str(Path(path).resolve())
        actual = sha(path)
        need(wanted is None or actual == wanted, 'Actual evidence/source/public bytes unchanged')
        need(key not in fresh or fresh[key] == actual, 'Consistent new proof pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == actual,
             'Never relabel inherited actual evidence')
        fresh[key] = actual

    report_path = visible.OUT / 'report.json'
    report = json.loads(report_path.read_text())
    need(report['passed'] and report['candidate'] == visible.CANDIDATE and
         report['actualCurrentVisibleFrames'] == 6400 and
         report['exactActualCurrentVisibleRGBPixels'] == 650240000 and
         report['actualQualifiedPixelFaults'] == 12 and
         report['currentBothHumanSlotFullVisibleFriendshipSceneAndTransitionAccepted'] and
         report['completedFullWindowCapturesReusedWithoutRerun'] == 3 and
         report['newPhysicalCaptures'] == 1 and
         report['old3574VerifierNamespaceFailurePreserved'] and
         not report['allStandaloneChildExitCodeRecordsAvailable'] and
         not report['completeCurrentHiddenVRAMWriteReplayAccepted'] and
         not report['allArenaAbsoluteGroundShadowAccepted'] and
         not report['allFriendshipMirrorVictimCPUOrFinisherContextsAccepted'] and
         not report['referenceRawAudioOrVRAMGraphRecreated'] and
         report['newExecutableROMWAVOrRawPixelImageCopies'] == 0 and
         not report['fullPortAcceptance'], 'Actual full visible fields, not missing metadata/hidden VRAM/all contexts')
    need({(c['winner'], c['side']) for c in report['cases']} ==
         {(fighter, side) for fighter in ('kano', 'sonya') for side in (1, 2)} and
         all(c['actualVisibleFrames'] == 1600 and c['samePathOriginalPositive'] and
             c['nativeScene']['observedOriginalOwnWinnerDispatches'] == 2 for c in report['cases']),
         'Both own characters/human slots, full source-bound visible sequences and native earned wins/cleanup')
    pin(report_path)
    for file, wanted in report['inputHashes'].items():
        pin(file, wanted)
    rejected_path = ROOT / 'audit_v3578_friendship_raw_screen_surface_diagnostic/report.json'
    rejected = json.loads(rejected_path.read_text())
    need(rejected['diagnosticRecorded'] and not rejected['passed'] and
         not rejected['currentVisualAcceptance'] and not rejected['fullPortAcceptance'],
         'Rejected alternate raw screen surface never relabeled accepted')
    pin(rejected_path)
    for file, wanted in rejected['inputHashes'].items():
        pin(file, wanted)
    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        item = ROOT / relative
        pin(item, state['inputHashes'][str(item.resolve())])
    pin(PREVIOUS)
    pin(__file__)
    state['inputHashes'] = fresh
    state['currentScopeEvidenceAudit']['group3'] = (
        '3563 accepts actual3172 both-character/both-human-slot retained original Friendship waveforms/tails/overlap '
        'and native allocation/owners/cleanup,80cues/8sample-paired captures.3581now proves all6400current visible '
        'RGB fields,650240000pixels, including full finish/fade/selection transition, exactly equal to immutable '
        '2753 independently source-bound native art/palette/shadow/erase reference.12qualified pixel faults. '
        'Three completed exact streaming comparisons were rechecked after3574post-capture Python namespace error; '
        'one previously uncapturedSonyaP2scenario ran fresh. Those three old leaves lack standalone child-exit '
        'metadata, explicitly not accepted as successful original verifier invocations. Raw-screen alternate '
        'bitmap3570probe remains rejected; corrected snapshot-rendering path is source-bound, not one-field '
        'timing normalization. Current hidden-VRAM write replay, absolute/all-arena grounding/shadows, mirrors, '
        'other victims/CPU and other finisher/secret/cinematic contexts are not automatically promoted.')
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: inspect3565checkpoint/current dirty worktree/old2753source-perfect native Friendship reference. Stream current native RGB without image/VRAM/WAV duplication.3570wrong screen:pixels surface shows alternate previous raw bitmap; preserve rejected actual1600Kano fields and incompleteSonya probe, stop exact verified wrong-surface processes,72393terminal1. Source screen.cpp/luaengine/video.cpp identifies actual snapshot rendering path; fresh3573/3574uses video.snapshot_pixels, not temporal normalization. Three corrected full1600scenes have zero pixel differences but post-capture module namespace error3576; retain failed invocation and immutable records. Fresh3579rechecks all recorded actual/reference RGB digests against source-bound PNGs, full source/exe/guest/input/native earned-win/cleanup records, explicitly missing standalone exit metadata; do not rerun completed RGB captures. Only missingSonyaP2 runs fresh3580terminal0.3581proves all4visible sequences6400frames/650240000pixels and12qualified exact pixel faults. Current hidden VRAM/all absolute-ground/arena/mirror/victim/CPU/other-finisher scope remains unaccepted. No game/public/newEXE/ROM/WAV/image/VRAM changes.',
        current3172BothHumanSlotFullVisibleFriendshipSceneAndTransitionAccepted=True,
        current3172FriendshipVisibleSceneReport=str(report_path),
        current3172FriendshipActualVisibleFields=6400,
        current3172FriendshipExactVisibleRGBPixels=650240000,
        current3172FriendshipQualifiedVisiblePixelFaults=12,
        current3172FriendshipVisibleScenesAllStandaloneChildExitCodeMetadataAvailable=False,
        current3172FriendshipCurrentHiddenVRAMWriteReplayAccepted=False,
        current3172FriendshipAllAbsoluteArenaGroundShadowMirrorVictimCPUContextsAccepted=False,
        rejectedFriendshipRawScreenSurfaceReport=str(rejected_path),
        rejectedFriendshipSnapshotReportNamespaceFailure=str(ROOT / 'audit_v3576_current_friendship_snapshot_pixels_checked/report.json'),
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        newRuntimeCaptureLeavesThisTurn=7,
        acceptedVisibleScenarioCapturesThisTurn=4,
        rawPixelImageVRAMCopiesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        historicalPinMapCopiedAgain=False,
        nextAction='Do not rerun completed native P1 campaigns/endings,Knife3534,photo/text/common frame,Friendship3563audio or3581visible pixel sequences for continuity. Build an explicit feature/branch coverage matrix from actual current3172 guest tables and changes versus1836/2753 before choosing the next real missing finisher/arena/secret gate. Distinguish source-proven unreachable changes and representative runtime coverage from untested contexts; no automatic old-build or universal promotion. Prioritize remaining functional/visual integration and final combined selection/ladder/names/audio regression, then refreshed releaseZIP. Preserve all5original groups, public1836CMD/ZIP, current source/assets/builds and retired storage exclusions. No recovered raw oracle graphs or new EXE/ROM/WAV/image dumps for ordinary regression.')
    need(state['remaining'] == remaining, 'Five original requirement groups unchanged')
    OUT.mkdir()
    saved = OUT / 'checkpoint.json'
    saved.write_text(json.dumps(state, indent=2) + '\n')
    digest = sha(saved)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(saved)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(saved) == digest, 'Lossless compact checkpoint')
    print(json.dumps(dict(saved=str(saved), goalStatus='active', exactCurrentVisibleFields=6400,
                         visiblePixels=650240000, freshPins=len(fresh),
                         gameOrPublicBytesChanged=False, fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
