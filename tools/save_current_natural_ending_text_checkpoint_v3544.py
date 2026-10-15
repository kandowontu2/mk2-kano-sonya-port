"""Current natural original-font story evidence; whole objective retained."""
import json
import subprocess
from pathlib import Path
import verify_current_natural_ending_text_v3542 as text

ROOT, need, sha = text.ROOT, text.need, text.sha
PREVIOUS = ROOT / 'audit_v3538_current_natural_ending_photo_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v3545_current_natural_ending_text_full_scope_checkpoint'


def main():
    need(not OUT.exists(), 'Immutable fresh full-scope checkpoint')
    state = json.loads(PREVIOUS.read_text())
    remaining = state['remaining']
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'] and
         state['current3172BothNaturalP1EndingVisibleOriginalPhotosAccepted'] and
         state['currentKnifeBossChildParentGuardAndNativeDamageAndRetirementAccepted'] and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Preserve both natural clears, native Knife contact, own photo proof and full objective')
    fresh = {}
    def pin(path, wanted=None):
        key = str(Path(path).resolve())
        actual = sha(path)
        need(wanted is None or actual == wanted, 'Actual source/capture/public bytes unchanged')
        need(key not in fresh or fresh[key] == actual, 'Consistent current source/capture pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == actual,
             'Never relabel inherited actual evidence')
        fresh[key] = actual

    report_path = text.OUT / 'report.json'
    report = json.loads(report_path.read_text())
    need(report['passed'] and report['bothNaturalP1StoryGlyphSpacingPunctuationAndBlackShadowsAccepted'] and
         report['actualNaturalP1EarlyLateStoryScanouts'] == 8 and
         report['exactOriginalNativeGlyphFacePixels'] == 46454 and
         report['exactOriginalNativeBlackTextShadowPixels'] == 22670 and
         report['actualQualifiedTextPixelFaults'] == 32 and
         report['initialProbePunctuationOffsetAndSpaceWidthAssumptionsNotAccepted'] and
         not report['allFrameBackgroundPixelsCinematicsAudioP2OrAllContextsAccepted'] and
         not report['fullPortAcceptance'] and report['newRuntimeBuildROMRawAudioOrRecoveredOracleCopies'] == 0,
         'Exact original-font native stories/shadows only, not untested background/audio/contexts')
    pin(report_path)
    for file, wanted in report['inputHashes'].items():
        pin(file, wanted)
    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        path = ROOT / relative
        pin(path, state['inputHashes'][str(path.resolve())])
    pin(PREVIOUS)
    pin(__file__)
    state['inputHashes'] = fresh
    state['currentScopeEvidenceAudit']['group4'] = (
        'Both current3172 natural true-character P1 Kintaro/Shao clears, own stories and attract are accepted. '
        '3536 closes210920visible own photo pixels at eight early/late scanouts. '
        '3543 closes46454original-font face pixels,22670native black-shadow pixels, original spacing/punctuation/full own story words '
        'and no extra white lettering in native panel interiors. '
        'Native frame/background/extra black pens/audio/P2 and other cinematic contexts remain separate gates. '
        'Do not call completed P1 natural clears or these photo/font checks still pending.')
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: inspect3538checkpoint/actual3172compiled ending source/native original text renderer/unchanged dirty checkout.3539probe rejects wrongly assumed zero punctuation offsets;3540probe shows incorrect space width. Original FF809F10/FF80A490 preserves signed punctuation offsets; FFA2CA20 uses H width7/height11, space3+2=5 and line11+5=16, not assumed M width.3541original source-derived probes match both own native P1 pages exactly.3542/3543bind actual four-chip original font bank to MAME parent ZIP and compiled3172driver CRC/SHA1; full guest identity/unchanged native renderer/palette/table/descriptor bytes, genuine stock24byte story headers, complete own independent strings. All8early/late natural scanouts match46454native glyph face pixels and22670black one-pixel shadows, no extra white lettering in full native text-panel interiors.32qualified actual letter/shadow/extra-letter/palette pixel faults reject intended invariants; same-path positives. No game/public/build/capture/ROM/WAV/recovered oracle changes. Frame/background/extra black pens/audio/P2/all cinematics explicitly remain unaccepted.',
        current3172BothNaturalP1StoryOriginalGlyphSpacingPunctuationBlackShadowsAccepted=True,
        current3172NaturalEndingStoryTextReport=str(report_path),
        current3172NaturalEndingExactOriginalGlyphFacePixels=46454,
        current3172NaturalEndingExactNativeBlackTextShadowPixels=22670,
        current3172NaturalEndingActualEarlyLateStoryScanouts=8,
        current3172NaturalEndingQualifiedStoryTextPixelFaults=32,
        current3172NaturalEndingOriginalFontGlyphSpacingAndShadowRules='Original native one-bit glyphs, signed punctuation offsets, H-derived space3+original spacing2=5, line11+half5=16, white pen14 and black pen15 at native+1,+1.',
        current3172NaturalEndingTextPanelExtraWhiteLettersAcceptedAbsent=True,
        current3172NaturalEndingFrameBackgroundExtraBlackPensCinematicsAudioP2AllContextsAccepted=False,
        current3172AllEndingPixelsAudioContextsAccepted=False,
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        newRuntimeCapturesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        historicalPinMapCopiedAgain=False,
        nextAction='Do not rerun completed natural campaign, Knife3534, photo3536 or text3543 gates for continuity. Inspect original native scene18/19 frame/background contract against current existing natural ending scanouts. In particular page2top-right black strip should be explained by actual original scene/scanout evidence, not assumed native or a game bug. Old680stock control files are absent after storage cleanup; never recover/recreate old retired folders. If original native controls are needed, a small fresh explicitly assisted stock-ending diagnostic may establish background comparison only, never natural-clear acceptance, no WAV/newbuild/ROM duplication. Alternatively choose a targeted missing current3172finisher/arena proof after auditing actual1836/2753 source-transfer scope. Both native P1 clears/own photo/font/shadow proofs remain accepted. Preserve whole original five groups, public1836CMD/ZIP, current dev/source/assets and retired storage exclusions.')
    need(state['remaining'] == remaining, 'Original full objective retained')
    OUT.mkdir()
    path = OUT / 'checkpoint.json'
    path.write_text(json.dumps(state, indent=2) + '\n')
    digest = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == digest, 'Lossless compact full-scope checkpoint')
    print(json.dumps(dict(saved=str(path), goalStatus='active', bothNaturalClearsAndPhotosRetained=True,
        originalGlyphFacePixels=46454, nativeBlackTextShadowPixels=22670,
        freshPins=len(fresh), gameOrPublicBytesChanged=False, fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
