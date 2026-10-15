"""Preserve full scope while recording bounded original-MK2 frame evidence."""
import json
import subprocess
from pathlib import Path
import verify_original_ending_black_strip_v3551 as frame

ROOT, need, sha = frame.ROOT, frame.need, frame.sha
PREVIOUS = ROOT / 'audit_v3545_current_natural_ending_text_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v3554_current_original_ending_frame_full_scope_checkpoint'


def main():
    need(not OUT.exists(), 'Fresh immutable checkpoint')
    state = json.loads(PREVIOUS.read_text())
    remaining = state['remaining']
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'] and
         state['current3172BothNaturalP1EndingVisibleOriginalPhotosAccepted'] and
         state['current3172BothNaturalP1StoryOriginalGlyphSpacingPunctuationBlackShadowsAccepted'] and
         state['currentKnifeBossChildParentGuardAndNativeDamageAndRetirementAccepted'] and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Keep completed native P1 gates and unfinished whole objective')
    fresh = {}

    def pin(path, wanted=None):
        key = str(Path(path).resolve())
        actual = sha(path)
        need(wanted is None or actual == wanted, 'Actual evidence/public bytes unchanged')
        need(key not in fresh or fresh[key] == actual, 'Consistent fresh pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == actual,
             'Inherited evidence never relabeled')
        fresh[key] = actual

    report_path = frame.OUT / 'report.json'
    report = json.loads(report_path.read_text())
    faults = report['actualQualifiedFrameBackgroundPixelFaults']
    black = [f for f in faults if f['name'] == 'one_actual_original_black_strip_pixel_changed']
    need(report['passed'] and report['entireOriginalGuestByteExact'] and
         report['originalReferenceGame'] == 'mk2' and
         report['originalReferenceAssistance'] == 'stage14_combat_health_only' and
         not report['originalReferenceUnassistedCampaignAccepted'] and
         report['originalReferenceFinalFrame'] == 6188 and
         report['actualOriginalNativeSceneIndices'] == [19, 18] and
         len(report['sourceBoundaryQualifiedFaults']) == 3 and
         len(report['currentNaturalEndingFrameCases']) == 8 and
         report['exactOriginalFrameAndCommonVisibleBackgroundPixels'] == 481176 and
         len(faults) == 16 and len(black) == 4 and
         all(f['beforeRGB'] == [0, 0, 0] and f['position'] == [341, 0] for f in black) and
         report['originalTopRightPage2BlackStripNotPortSpecificAccepted'] and
         report['bothNaturalP1NativePhotoFrameOverpaintAndCommonBackgroundAccepted'] and
         not report['foregroundOrHiddenBackgroundAllExtraBlackPensAudioP2OrAllCinematicsAccepted'] and
         report['newExecutableROMRawAudioOrRecoveredOracleCopies'] == 0 and
         not report['fullPortAcceptance'], 'Bounded frame evidence, genuine black faults, no broader claim')
    pin(report_path)
    for file, wanted in report['inputHashes'].items():
        pin(file, wanted)
    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        path = ROOT / relative
        pin(path, state['inputHashes'][str(path.resolve())])
    superseded = ROOT / 'audit_v3550_original_native_ending_background_checked/report.json'
    pin(superseded)
    pin(ROOT / 'tools/verify_original_ending_background_v3549.py')
    pin(PREVIOUS)
    pin(__file__)
    state['inputHashes'] = fresh
    state['currentScopeEvidenceAudit']['group4'] = (
        'Both current3172 true-character P1 natural Kintaro/Shao clears, own endings and attract are accepted. '
        '3536 proves210920visible original own-photo pixels;3543 proves46454native face and22670black text-shadow pixels '
        'with original spacing/punctuation at eight early/late scanouts.3552 additionally proves481176common visible '
        'original-MK2 frame/background pixels at the same eight current scanouts, including photo-frame overpaint and '
        'the genuine native page2top-right black strip. The untouched-original MK2 comparison uses explicit stage14/live '
        'combat health fixtures, not a natural clear. Foreground/hidden background/all extra black pens/audio/P2/all '
        'cinematics remain separate gates. Do not rerun completed P1 campaign/photo/text/common-frame gates for continuity.')
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: fresh small compressed original-MK2 stock ending reference3548 runs existing3172executable with actual mk2 parent ROM; whole captured guest byte-exact original. Explicit preconstruction stage14 and live-combat HP fixtures stop before native ending; never natural-clear evidence.3552 checks original physical control/source boundary, original scenes19/18 and independent original-font masks; all8current natural ending early/late scanouts match481176common visible native frame/background pixels, including photo overpaint edges and actual page2black strip.16qualified actual pixel faults include4genuine black pixels, plus3source faults, all same-path positives.3550nearby-corner fault label superseded without altering executed evidence. No game/public/build/ROM/WAV/recovered-oracle changes; one small compressed original reference capture. Whole five groups remain unfinished.',
        current3172BothNaturalP1NativePhotoFrameOverpaintAndCommonBackgroundAccepted=True,
        current3172NativeEndingFrameBackgroundReport=str(report_path),
        current3172NativeEndingExactOriginalCommonFrameBackgroundPixels=481176,
        current3172NativeEndingFrameEarlyLateScanouts=8,
        current3172NativeEndingQualifiedFramePixelFaults=16,
        current3172NativeEndingQualifiedActualBlackStripPixelFaults=4,
        originalMK2EndingReferenceWholeGuestByteExact=True,
        originalMK2EndingReferenceAssistance='stage14_combat_health_only; stops before ending',
        originalMK2EndingReferenceNaturalCampaignAccepted=False,
        nativeEndingPage2BlackStripNotPortSpecificAccepted=True,
        originalEndingFrameSupersededFaultLabelReport=str(superseded),
        originalEndingFrameSupersededFaultLabelReason='3550 labeled nearby corner-background faults black_strip;3552 qualifies actual black pixel[341,0] beforeRGB0,0,0. Preserve old executed evidence.',
        current3172AllEndingPixelsAudioContextsAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        newRuntimeCapturesThisTurn=1,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        historicalPinMapCopiedAgain=False,
        nextAction='Choose a real remaining bounded current3172 audio/finisher/arena gate after auditing actual1836/2753 source-transfer scope. Do not rerun accepted natural P1 campaign,Knife3534,photo3536,text3543,or common native frame3552 gates merely for continuity. Ending audio,P2/all cinematic contexts and foreground/hidden background/extra black pens remain unaccepted. Final combined selection/ladder/names/audio regression and refreshed releaseZIP pending; public1836CMD/ZIP unchanged. Preserve original five requirement groups, current source/assets/builds and retired storage exclusions; no recovered historical oracles or new EXE/ROM/WAV copies for ordinary testing.')
    need(state['remaining'] == remaining, 'Five original requirement groups retained verbatim')
    OUT.mkdir()
    path = OUT / 'checkpoint.json'
    path.write_text(json.dumps(state, indent=2) + '\n')
    digest = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == digest, 'Lossless compact checkpoint')
    print(json.dumps(dict(saved=str(path), goalStatus='active', commonNativeFramePixels=481176,
        actualBlackStripFaults=4, freshPins=len(fresh), gameOrPublicBytesChanged=False,
        fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
