"""Save bounded launch/cry audio proof without narrowing the full port objective."""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_bicycle_block_push_v3382 as current

ROOT = current.ROOT
PREVIOUS = ROOT / 'audit_v3385_current_bicycle_block_push_full_scope_checkpoint/checkpoint.json'
REPORT = ROOT / 'audit_v3392_current_bicycle_block_audio_checked/report.json'
OUT = ROOT / 'audit_v3394_current_bicycle_block_audio_full_scope_checkpoint'
sha = current.prior.current.assembly.sha
need = current.need

def main():
    need(not OUT.exists(), 'Never overwrite executed checkpoint')
    state = json.loads(PREVIOUS.read_text())
    remaining = state['remaining']
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         not state['fullPortAcceptance'] and not state['finishedRelease'] and
         not state['actualEndingsAccepted'] and state['currentRealShaoKahnMatchClears'] == 0,
         'Keep original full natural-port objective')
    report = json.loads(REPORT.read_text())
    need(report['passed'] and report['physicalSlots'] == 2 and
         report['fullCapturedBlockedBicycleLaunchAudioAndOwnershipAccepted'] and
         report['rawAudioFilesWritten'] == 0 and report['newBuildsOrROMCopies'] == 0 and
         not report['allMoveOrCPUOrArenaAudioAccepted'] and not report['fullPortAcceptance'],
         'Actual bounded mixed audio proof, not broad acceptance')
    need([case['side'] for case in report['cases']] == [1, 2] and all(
         case['fullCapturedOriginalCuesAndFiniteOwnershipAccepted'] and
         case['mixedPCMUpdates'] == 207 and case['fullCueSamples'] == 66523 and
         case['correlation'] > .999 and .699 <= case['gain'] <= .701 and
         abs(case['onsetSeconds'] - case['markerSeconds']) < .0001
         for case in report['cases']), 'Both physical slots: complete retained cues, native timing and finite ownership')
    fresh = dict(report['inputHashes'])
    for path in (PREVIOUS, REPORT, Path(__file__).resolve()):
        fresh[str(path.resolve())] = sha(path)
    for relative in (state['currentCMD'], state['currentPlaytestZIP'],
                     'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
                     'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata'):
        key = str((ROOT / relative).resolve())
        need(key in state['inputHashes'], 'Retained public playable guard')
        fresh[key] = state['inputHashes'][key]
    failed_path = ROOT / 'audit_v3389_current_bicycle_block_audio_checked/report.json'
    failed = json.loads(failed_path.read_text())
    need(not failed['passed'], 'Preserve failed interleaved harness result')
    fresh[str(failed_path)] = sha(failed_path)
    removed = [ROOT / f'audit_v3388_current_bicycle_block_audio_p{side}_{mode}/run.log'
               for side in (1, 2) for mode in ('samples', 'nosamples')]
    need(all(not path.exists() for path in removed), 'Four failed verbose logs removed, no replacement copies')
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file, digest), actual in zip(fresh.items(), pool.map(sha, fresh)):
            need(actual == digest, 'Fresh source/capture/public bytes unchanged')
            need(file not in state['inputHashes'] or state['inputHashes'][file] == digest,
                 'Never relabel inherited evidence')
    state['inputHashes'].update(fresh)
    state.update(
        previousCheckpoint=str(PREVIOUS),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: existing3172 both-human stage0 blocked Bicycle launch/cry playback verified from actual mixed PCM in RAM against retained sample assets. Four sample-enabled/disabled captures preserve original input/state/push events. Both cues complete, approximately .70 gain, native launch timing, correct physical channels and finite owner lifetime. No game/build/public edits or raw audio copies. Full five-group port scope retained.',
        currentNativeBicycleBlockedLaunchCryPlaybackAccepted=True,
        currentNativeBicycleBlockedLaunchCryPlaybackReport=str(REPORT),
        currentNativeBicycleBlockedLaunchCryProofScope='Only genuine human Sonya in both physical slots versus standing-block Kano on stage0. Complete actual mixed playback of retained launch and cry assets, channel selection, timing, completion and owner cleanup. Not a fresh extraction/oracle of original DCS waveforms, native contact DCS effects, all move/CPU/arena/KO/overlap audio, or full port acceptance.',
        currentNativeBicycleBlockedAudioAccepted=False,
        currentNativeBicycleBlockedFullDefenderHorizontalRasterShadowAudioAccepted=False,
        currentNativeBicycleBlockedAllArenasAudioKOOverlapAccepted=False,
        currentNativeBicycleAudioHarnessFailure=dict(report=str(failed_path),
            cause='Verbose -oslog diagnostics interleaved stdout PCM. Successor3390 removes -oslog, separates stderr, rejects malformed PCM before disk, and retains raw PCM only in RAM.'),
        failedVerboseAudioLogsRemoved=[str(path) for path in removed],
        failedVerboseAudioLogsRecoverable=False,
        failedVerboseAudioLogRecoveryCopiesCreated=0,
        gameSourceAndPlayableBytesChangedThisTurn=False,
        nativeGuestProgramChangedThisTurn=False,
        newExecutableROMOrRawAudioCopiesThisTurn=0,
        publicLauncherChangedThisTurn=False,
        publicReleaseZIPChangedThisTurn=False,
        inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
        revalidatedFreshRelevantFilePins=len(fresh),
        goalStatus='active', fullPortAcceptance=False, finishedRelease=False,
        nextAction='Continue remaining native move/contact audio and CPU/arena/KO/overlap coverage, full arena/victim effects, finishers/morphs/secrets/cinematics, natural boss clears/own endings/attract, final integrated UI/audio/cleanup/refreshed release. Do not repeat completed bounded blocked state/push/raster/shadow/launch-cry tests or promote them to whole-game acceptance. Reuse existing builds; no raw-audio or retired archive recreation.')
    need(state['remaining'] == remaining and not state['actualEndingsAccepted'] and
         state['currentRealShaoKahnMatchClears'] == 0, 'Original requirements remain open')
    OUT.mkdir()
    path = OUT / 'checkpoint.json'
    path.write_text(json.dumps(state, indent=2) + '\n')
    digest = sha(path)
    compressed = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(compressed.returncode == 0 and sha(path) == digest, 'Lossless checkpoint compression')
    print(json.dumps(dict(saved=str(path), originalRemainingGroups=5,
        boundedLaunchCryPlaybackAccepted=True, fullBlockedAudioAccepted=False,
        freshPinsRehashed=len(fresh), failedLogsRemoved=4, rawAudioFilesWritten=0,
        fullPortAcceptance=False), indent=2), flush=True)

if __name__ == '__main__':
    main()
