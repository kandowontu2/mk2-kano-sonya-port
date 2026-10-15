"""Current natural ending-photo gate and build-specific remaining scope."""
import json
import subprocess
from pathlib import Path
import verify_current_natural_ending_photos_v3535 as photos

ROOT = photos.ROOT
PREVIOUS = ROOT / 'audit_v3532_current_owned_knife_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v3538_current_natural_ending_photo_full_scope_checkpoint'
need, sha = photos.need, photos.sha


def main():
    need(not OUT.exists(), 'Immutable full-scope checkpoint')
    state = json.loads(PREVIOUS.read_text())
    original_remaining = state['remaining']
    need(state['goalStatus'] == 'active' and len(original_remaining) == 5 and
         state['current3172BothTrueCharacterP1NaturalCampaignClearsOwnStoryAndAttractAccepted'] and
         state['currentKnifeBossChildParentGuardAndNativeDamageAndRetirementAccepted'] and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Both natural clears and actual Knife child contact remain accepted; full goal remains active')
    fresh = {}
    def pin(path, expected=None):
        key = str(Path(path).resolve())
        digest = sha(path)
        need(expected is None or digest == expected, 'Actual scoped proof input unchanged')
        need(key not in fresh or fresh[key] == digest, 'Consistent fresh pin')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == digest,
             'Do not relabel an inherited actual input')
        fresh[key] = digest

    report_path = photos.OUT / 'report.json'
    report = json.loads(report_path.read_text())
    need(report['passed'] and report['bothNaturalP1EndingVisiblePhotosAccepted'] and
         report['actualNativeP1EndingScanouts'] == 8 and
         report['exactVisibleOriginalROMPhotoPixels'] == 210920 and
         report['actualQualifiedPhotoFaults'] == 32 and
         not report['frameOverpaintAllTextPixelsCinematicsAudioOrAllContextsAccepted'] and
         not report['fullPortAcceptance'] and report['newRuntimeBuildROMRawAudioOrPhotoOracleCopies'] == 0,
         'Bounded exact original-ROM photos, not all ending art/audio/contexts')
    pin(report_path)
    for file, digest in report['inputHashes'].items():
        pin(file, digest)

    inspected = [
        ('audit_v2080_current_kano_p1_tomb_matrix_checked/report.json', 'diagnostic_v1836_ball_register_boundary'),
        ('audit_v2100_current_kano_p1_pit_movie_checked/report.json', 'diagnostic_v1836_ball_register_boundary'),
        ('audit_v2922_candidate_friendship_audio_checked/report.json', 'diagnostic_v2753_native_friendship_palette'),
        ('audit_v2783_native_friendship_palette_shadow_rows_checked/report.json', 'diagnostic_v2753_native_friendship_palette'),
    ]
    evidence = []
    for relative, candidate in inspected:
        path = ROOT / relative
        value = json.loads(path.read_text())
        need(value['passed'] and value['candidate'] == candidate,
             'Inspect actual report candidate rather than inherited current label')
        pin(path)
        evidence.append(dict(report=str(path), candidate=value['candidate'], scope=value['scope'],
                             historicalDependenciesRevalidated=False,
                             current3172RuntimeAutomaticallyPromoted=False))

    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        path = ROOT / relative
        pin(path, state['inputHashes'][str(path.resolve())])
    pin(PREVIOUS)
    pin(__file__)
    state['inputHashes'] = fresh
    state.update(
        previousCheckpoint=str(PREVIOUS),
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PREVIOUS),
            parentCheckpointSHA256=fresh[str(PREVIOUS)],
            mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: inspected actual build bindings in older Pit/Tomb and Friendship reports; their current labels refer to1836/2753, not new3172runtime. Reused accepted current3516Kano/3490Sonya natural ending captures without rerunning combat.3535/3536 independently decode actual SHA-bound original donor graphics in memory; all8early/late native page scanouts exactly match210920visible original photo pixels at native positions. Actual real17/18 guest picture/story pointers and60/180field snapshot chronology checked.32actual pixel/one-pixel-position/wrong-fighter/row-direction faults reject exact intended gate, same-path positives. No retired oracle/rawPCM recovery or game/build/public changes. Frame overpaint/font/cinematic/audio and other contexts remain explicitly unaccepted.',
        current3172BothNaturalP1EndingVisibleOriginalPhotosAccepted=True,
        current3172NaturalEndingPhotoReport=str(report_path),
        current3172NaturalEndingExactVisibleOriginalPhotoPixels=210920,
        current3172NaturalEndingActualEarlyLatePhotoScanouts=8,
        current3172NaturalEndingQualifiedPhotoFaults=32,
        current3172NaturalEndingFrameOverpaintTextPixelsCinematicsAudioAllContextsAccepted=False,
        current3172AllEndingPixelsAudioContextsAccepted=False,
        currentScopeEvidenceAudit=dict(
            originalRequirementGroupsPreserved=True,
            inspectedBuildBoundReports=evidence,
            group1='Pit/Tomb representative whole scene proofs inspected here are1836. Full current3172 transfer/runtime coverage and broader victim/mirror/drop branches/stage voice/effects are not automatically accepted.',
            group2='Current3172 specific Square, Bicycle, Ring and human morph evidence is retained in inherited checkpoint, not rerun here. Complete move-phase/current arena/repeat/KO/overlap/CPU/audio coverage remains broader than those bounded cases.',
            group3='Representative complete Friendship audio/shadow evidence inspected here is2753 and bounded to four human cases/one arena. No automatic3172runtime promotion; all other finisher/victim/morph/secret/cinematic contexts remain a coverage gate.',
            group4='Both current3172 natural P1 Kintaro/Shao clears, true IDs, own story and attract are accepted. New3536 closes visible own photo pixels at eight early/late scanouts. Native frame-overpaint/font pixels/audio/P2 and other cinematic contexts are not yet fully accepted. Do not describe P1 natural clears as still pending.',
            group5='Current3172 bounded UI geometry/raster tests and completed storage cleanup are retained. Public CMD/ZIP still1836 and unchanged. Final combined current3172selection/ladder/lifebar/audio regression plus refreshed release package remain; do not promote development build merely for test progress.'),
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        newRuntimeCapturesThisTurn=0,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        historicalPinMapCopiedAgain=False,
        nextAction='Do not rerun completed natural campaigns,3534Knife or3536photo gates for continuity. Next inspect original native ending frame/text rendering contract against current existing scanouts, or implement a targeted missing current3172finisher/arena gate after auditing actual source transfer from1836/2753. Visible photographs now exact; no all-frame/font/audio acceptance. Preserve original five groups, completed native clears, public1836CMD/ZIP and storage exclusions. No retired audio/oracle/recovery regeneration, new build/ROM/WAV duplication, broad historical rehash or gameplay power/difficulty/AI/RNG/HP changes.')
    need(state['remaining'] == original_remaining, 'Original whole objective retained')
    OUT.mkdir()
    path = OUT / 'checkpoint.json'
    path.write_text(json.dumps(state, indent=2) + '\n')
    digest = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == digest, 'Lossless compact checkpoint')
    print(json.dumps(dict(saved=str(path), goalStatus='active', bothNaturalClearsRetained=True,
        exactOriginalVisiblePhotoPixels=210920, freshPins=len(fresh),
        gameOrPublicBytesChanged=False, fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
