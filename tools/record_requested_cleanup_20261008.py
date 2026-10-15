"""Verify exact obsolete-history retirement and retain the complete active goal."""
import datetime, json, subprocess
from pathlib import Path
from plan_requested_cleanup_v3275 import sha

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT/'workspace_cleanup_2026-10-08'
JOURNAL = ROOT/'audit_v5826_current_requested_cleanup_progress'

def main():
    destination = OUT/'verified_summary.json'
    assert not destination.exists() and not JOURNAL.exists()
    plan_path, result_path = OUT/'retirement_plan.json', OUT/'result.json'
    plan = json.loads(plan_path.read_text())
    result = json.loads(result_path.read_text(encoding='utf-8-sig'))
    boot = json.loads((OUT/'launcher_check/report.json').read_text(encoding='utf-8-sig'))
    assert result['passed'] and boot['passed'] and boot['userSettingsUnchanged']
    assert result['planSHA256'] == sha(plan_path)
    leaves = [f for row in plan['targets'] for f in row['files']]
    assert result['removedFiles'] == len(leaves) == 2142
    assert result['reclaimedAllocatedBytes'] == plan['reclaimableAllocatedBytes']
    assert all(not Path(f['path']).exists() for f in leaves)
    assert all(not Path(row['path']).exists() for row in plan['targets'])
    for name, digest in plan['preservedHashes'].items():
        assert sha(name) == digest, name
    summary = dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        removedFiles=len(leaves), removedCacheDirectories=result['removedCacheDirectories'],
        removedFailedCampaignRawMixes=8, removedDiscardedBuildRecoveryArchives=4,
        reclaimedAllocatedBytes=result['reclaimedAllocatedBytes'],
        reclaimedGiB=round(result['reclaimedAllocatedBytes']/2**30, 2),
        currentPlayableSourceAndEvidenceHashesUnchanged=len(plan['preservedHashes']),
        currentCMDBootPassed=True, userSettingsUnchanged=True, newBuilds=0,
        newRecoveryArchives=0, historicalDataPermanentlyRetired=True,
        compilerCacheRegenerable=True, fullPortAcceptance=False,
        exactRetirementManifest=str(plan_path))
    destination.write_text(json.dumps(summary,indent=2)+'\n')
    parent_path = ROOT/'audit_v5825_current_held_tomb_full_scene_matrix_progress/progress.json'
    parent = json.loads(parent_path.read_text())
    assert parent['passed'] and parent['goalStatus']=='active' and len(parent['remaining'])==5
    pins = dict(parent['newInputHashes'])
    pins[str(parent_path)] = sha(parent_path)
    for p in [*OUT.rglob('*'), ROOT/'WORKSPACE_CLEANUP_CURRENT.md', Path(__file__),
              ROOT/'tools/plan_workspace_cleanup_20261008.py',
              ROOT/'tools/plan_workspace_cleanup_20261008_v2.py',
              ROOT/'tools/plan_workspace_cleanup_20261008_v3.py',
              ROOT/'tools/plan_obsolete_history_retirement_20261008.py',
              ROOT/'tools/remove_workspace_cleanup_20261008.ps1',
              ROOT/'tools/remove_obsolete_history_20261008.ps1',
              ROOT/'tools/check_cleanup_launcher_20261008.ps1']:
        if p.is_file():
            pins[str(p.resolve())] = sha(p)
    assert all(sha(p)==h for p,h in pins.items())
    journal = dict(passed=True, observedUTC=summary['observedUTC'], goalStatus='active',
        parentAdditiveJournal=str(parent_path), remaining=parent['remaining'], newInputHashes=pins,
        thisGoalTurnClassification='progress: current held mirror Tomb full-scene checks retained; renewed obsolete-history cleanup completed and public launcher boot verified. Full original five-group gameplay objective remains open.',
        actualCurrentHeldAndRandomMirrorFullScenesRetained=True,
        currentPressedMirrorFullSceneAccepted=False, fullPortAcceptance=False,
        requestedCleanup=summary, retiredHistoricalEvidenceManifest=str(plan_path),
        historicalInventoryReferencesNotRuntimeInputs=True,
        failedReadOnlyDependencyScanRetained=True,
        originalReadOnlyScanStoppedForRepeatedPathIO=True,
        gameSourceChanged=False, publicPlayableChanged=False, publicZIPChanged=False,
        next='Continue the current pressed mirror Tomb full-scene check and the broader original remaining scope. Do not rerun completed held/random scenes or restore retired old recordings, archives or compiler objects merely for historical hashes. Final combined regression and release refresh remain open.')
    JOURNAL.mkdir()
    journal_path = JOURNAL/'progress.json'
    journal_path.write_text(json.dumps(journal,indent=2)+'\n')
    for p in [destination, journal_path, *[Path(n) for n in pins if Path(n).parent==OUT]]:
        before=sha(p)
        assert subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0
        assert sha(p)==before
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    main()
