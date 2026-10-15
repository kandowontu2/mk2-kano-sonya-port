"""Preserve the full natural-port objective after current CPU Square verification."""
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import verify_current_cpu_square_v3280 as current

ROOT = current.ROOT
OUT = ROOT / 'audit_v3288_current_cpu_square_full_scope_checkpoint'
PREVIOUS = ROOT / 'audit_v3260_cleanup_and_adversity_full_scope_checkpoint/checkpoint.json'

def main():
    need = current.need
    need(not OUT.exists(), 'Immutable full-scope checkpoint')
    state = json.loads(PREVIOUS.read_text())
    need(state['goalStatus'] == 'active' and len(state['remaining']) == 5 and
         state['candidateUnderTest'] == current.current.CANDIDATE and
         not state['fullPortAcceptance'] and not state['finishedRelease'] and
         not state['actualEndingsAccepted'] and state['currentRealShaoKahnMatchClears'] == 0 and
         not state['candidateUnderTestNativeBicycleHitOrBlockedAccepted'],
         'All original unfinished requirements retained')
    fresh = {}
    def pin(path, digest=None):
        path = Path(path).resolve()
        key = str(path)
        value = current.assembly.sha(path) if digest is None else digest
        need(key not in fresh or fresh[key] == value, 'Consistent fresh source/evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == value,
             'Never overwrite historical proof pins')
        fresh[key] = value
    def proof(path):
        value = json.loads(path.read_text(encoding='utf-8-sig'))
        need(value['passed'] and not value.get('fullPortAcceptance', False), 'Completed scoped proof')
        pin(path)
        for file, digest in value.get('inputHashes', {}).items():
            pin(file, digest)
        return value
    positive_path = current.OUT / 'report.json'
    positive = proof(positive_path)
    state_path = current.STATE_OUT / 'report.json'
    physical = proof(state_path)
    unit_path = ROOT / 'audit_v3286_current_cpu_square_counterexamples/report.json'
    units = proof(unit_path)
    need(positive['candidate'] == state['candidateUnderTest'] and positive['physicalFixtures'] == 1 and
         positive['actualSquareDamage'] == 27 and positive['sampledFrames'] == 69 and
         positive['exactScreenPixels'] == 7010400 and positive['nativeShadowCopies'] == 5733 and
         positive['sourceBoundProjections'] == 236 and positive['continuousExactFlips'] == 69 and
         positive['originalCPUHumanInputsAndGameplayTrajectoryUnchanged'] and
         positive['fullCurrentSquareHitPhaseArtShadowEraseAccepted'] and
         not positive['allCPUContextsArenasKOOverlapAudioAccepted'], 'Bounded current CPU contact/visual/erase proof')
    case = physical['cases']['current_kano']
    need(case['health']['allModePhysicalFields'] == 3602 and case['cold']['cpu_id'] == 18 and
         case['cold']['human_id'] == 17 and case['selection']['errors'] == 0 and
         case['originalPhysicalAndNativeEventsUnchanged'], 'Whole actual native identity/state/HP history, not proxy or sampled fields')
    need(units['actualGameplayRasterEraseCounterexamplesRejected'] == 78 and
         units['actualSnapshotMappingCounterexamplesRejected'] == 8 and
         units['sameMockedPathRenderAndErasePositiveControlsAccepted'] and
         units['unrelatedMissingEventExceptionsNeverAccepted'] and units['actualCapturesUnmodified'],
         'Original failures rejected specifically with same-path passing controls')
    cleanup_path = ROOT / 'workspace_cleanup_requested_2026-10-05/verified_summary.json'
    cleanup = proof(cleanup_path)
    need(cleanup['removedObsoleteFolders'] == 5631 and cleanup['removedOldPackageZIPs'] == 9 and
         cleanup['removedFiles'] == 205803 and cleanup['reclaimedWorkspaceAllocatedBytes'] == 28445519185 and
         cleanup['activeDependencyFrontiersDoNotIntersectDeletedTrees'] and
         cleanup['sourceCurrentBuildsROMsSettingsReleasePreserved'] and cleanup['launcherBootPassed'],
         'Requested actual cleanup and boot verified without deleting current dependencies')
    for file, digest in cleanup['evidenceHashes'].items():
        pin(file, digest)
    for file in ('tools/run_current_cpu_square_v3268.ps1', 'tools/current_cpu_capture_contract_v3270.py',
                 'tools/verify_current_cpu_square_v3280.py', 'tools/test_current_cpu_square_v3285.py',
                 'tools/inventory_requested_cleanup_v3274.py', 'tools/plan_requested_cleanup_v3275.py',
                 'tools/remove_requested_cleanup_v3276.ps1', 'tools/check_requested_cleanup_launcher_v3277.ps1',
                 'tools/remove_old_task_packages_v3278.ps1', 'tools/verify_requested_cleanup_v3279.py'):
        pin(ROOT/file)
    failures = []
    for report, script, cause in (
        ('audit_v3267_current_cpu_square_render_erase_checked/report.json', 'tools/verify_current_cpu_square_v3265.py',
         'Flat before-run report.json snapshots collided; fresh runner preserves the complete source hierarchy and eight specific corruptions are rejected.'),
        ('audit_v3284_current_cpu_square_counterexamples/report.json', 'tools/test_current_cpu_square_v3283.py',
         'Test wrapper referenced a nonexistent renderer assembly alias. Corrected successor also requires same mocked-path controls and specific corruption failures; no game/capture bytes were edited.')):
        path = ROOT/report
        failed = json.loads(path.read_text())
        need(not failed['passed'], 'Executed harness failure retained, not relabelled gameplay acceptance')
        pin(path); pin(ROOT/script)
        failures.append(dict(report=str(path), error=failed['error'], cause=cause))
    pin(PREVIOUS); pin(__file__)
    print('Rechecking fresh current CPU/cleanup/checkpoint dependencies:', len(fresh), flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file, digest), actual in zip(fresh.items(), pool.map(current.assembly.sha, fresh)):
            need(actual == digest, 'Every executed source/evidence byte unchanged')
    state['inputHashes'].update(fresh)
    state.update(previousCheckpoint=str(PREVIOUS),
                 previousGoalTurnClassification='progress: user-requested deletion of 5631 obsolete folders, nine ZIP copies and three old package-verification trees, independently checked; 26.49GiB allocated reclaimed plus package files; active source/builds/ROMs/settings/release unchanged and CMD boot passed.',
                 thisGoalTurnClassification='progress: existing fresh3172 actual native CPU Square hit capture independently verifies whole assembled guest/corrected payload, complete3602all-mode physical HP/state fields and unchanged original gameplay/CPU/RNG/input trajectory;27damage and distinct attacker/victim recovery;69complete scenes/7010400pixels/5733nativeblackshadowcopies/236sourceboundprojections and chronological one-base erase.78actual gameplay/render/erase corruptions plus8snapshot collision/hierarchy corruptions rejected with positive controls. No new build, ROM copy, capture, audio recording, game source edit or promotion; all five original full-port groups remain.',
                 candidateUnderTestNativeSquareHitAccepted=True,
                 candidateUnderTestNativeSquareHitOriginalArtPaletteShadowEraseAccepted=True,
                 candidateUnderTestNativeSquareHitPhaseReport=str(state_path),
                 candidateUnderTestNativeSquareHitRenderEraseReport=str(positive_path),
                 candidateUnderTestNativeSquareHitCounterexamplesReport=str(unit_path),
                 currentNativeCPUSquarePhysicalCase=current.CASE,
                 currentNativeCPUSquareAllModeFields=3602,
                 currentNativeCPUSquareDamage=27,
                 currentNativeCPUSquareExactScenes=69,
                 currentNativeCPUSquareShadowCopies=5733,
                 currentNativeCPUSquareGameplayRasterEraseCorruptionsRejected=78,
                 currentNativeCPUSourceSnapshotCorruptionsRejected=8,
                 currentNativeCPUSquareAllArenasAudioKOOverlapAccepted=False,
                 currentNativeCPUHarnessFailuresPreserved=failures,
                 latestRequestedCleanupReport=str(cleanup_path),
                 latestRequestedCleanupRemovedObsoleteFolders=5631,
                 latestRequestedCleanupRemovedOldZIPs=9,
                 latestRequestedCleanupReclaimedAllocatedBytes=28445519185,
                 latestRequestedCleanupHistoryPermanentlyDiscarded=True,
                 inheritedHistoricalGraphRevalidatedInFullThisTurn=False,
                 revalidatedFreshRelevantFilePins=len(fresh),
                 gameSourceAndPlayableBytesChangedThisTurn=False,
                 nativeGuestProgramChangedThisTurn=False,
                 publicLauncherChangedThisTurn=False,
                 publicReleaseZIPChangedThisTurn=False,
                 foldersDeletedThisTurn=[], obsoleteFoldersDeletedThisTurn=False,
                 allOldBuildFoldersRemoved=False,
                 fullPortAcceptance=False, finishedRelease=False, goalStatus='active',
                 nextAction='Keep3172isolated and retain the full original five remaining groups. Current bounded true-ID CPU Square hit now has full state/27HP/individual recovery/original art/palette/floor shadows/chronological erase and86qualified corruption checks. Next obtain source-directed normal-input Bicycle contact/blocked evidence, true CPU morph/KO/overlap and remaining affected special/finisher/arena/audio regression; a192pixel Bicycle miss is not contact proof or sufficient cause for a collision patch. Natural Kintaro/Shao clears, own endings/attract and final combined UI/ladder/names/audio plus refreshed release still required. Reuse current builds and compressed captures; no duplicate ROM/executable or large raw audio backlog.')
    need(len(state['remaining']) == 5 and state['currentRealShaoKahnMatchClears'] == 0 and
         not state['actualEndingsAccepted'] and not state['candidateUnderTestNativeBicycleHitOrBlockedAccepted'] and
         not state['candidateUnderTestBroadCPUOrKOOrMorphCoverageAccepted'], 'No invented broader acceptance or reduced original goal')
    OUT.mkdir()
    path = OUT/'checkpoint.json'
    path.write_text(json.dumps(state, indent=2)+'\n')
    digest = current.assembly.sha(path)
    result = subprocess.run(['compact.exe','/C','/I','/Q',str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and current.assembly.sha(path) == digest, 'Lossless full checkpoint compression verified')
    print(json.dumps(dict(saved=str(path), goalStatus='active', candidateUnderTest=state['candidateUnderTest'],
                          originalRemainingGroups=5, currentSquareHitAccepted=True, exactScenes=69,
                          actualCorruptionsRejected=86, candidateBicycleHitOrBlockedAccepted=False,
                          freshPinsRehashed=len(fresh), fullPortAcceptance=False), indent=2), flush=True)

if __name__ == '__main__':
    main()
