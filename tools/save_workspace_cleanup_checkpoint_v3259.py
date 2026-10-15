"""Retain the full unfinished port goal after requested cleanup and bounded morph proof."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import archive_obsolete_workspace_v3243 as common
ROOT=common.ROOT; OUT=ROOT/'audit_v3260_cleanup_and_adversity_full_scope_checkpoint'
def main():
    common.need(not OUT.exists(),'Immutable full-scope checkpoint')
    previous=ROOT/'audit_v3208_corrected_morph_shadow_full_scope_checkpoint/checkpoint.json'
    state=json.loads(previous.read_text())
    common.need(state['goalStatus']=='active' and len(state['remaining'])==5 and
        not state['fullPortAcceptance'] and not state['finishedRelease'] and
        state['candidateUnderTest']=='diagnostic_v3172_native_morph_shadow','All original unfinished requirements retained')
    proof_path=ROOT/'audit_v3236_morph_adversity_checked/report.json'
    proof=json.loads(proof_path.read_text())
    common.need(proof['passed'] and proof['physicalCases']==24 and
        proof['completeCallbackFields']==57624 and proof['completeRepeatedMorphCycles']==12 and
        proof['newActualMorphedKOFixtures']==4 and not proof['fullPortAcceptance'] and
        not proof['directArtShadowEraseArenaAudioAndCPUAcceptance'],'Exact bounded actual proof, no broad acceptance transfer')
    leaves=['audit_v3238_workspace_space_inventory','audit_v3242_unreferenced_workspace_cleanup_plan',
        'audit_v3246_workspace_fast_file_compaction','audit_v3248_bounded_audio_compaction_checked',
        'audit_v3262_obsolete_workspace_zstd_recovery','audit_v3256_obsolete_workspace_parallel_removal_checked',
        'audit_v3252_obsolete_workspace_removed','audit_v3258_current_launcher_after_workspace_cleanup']
    reports={name:json.loads((ROOT/name/'report.json').read_text(encoding='utf-8-sig')) for name in leaves}
    for name,report in reports.items():
        if 'passed' in report: common.need(report['passed'],'Actual completed cleanup/launcher evidence: '+name)
    removal=reports['audit_v3252_obsolete_workspace_removed']
    common.need(removal['removedFolderCount']==470 and not removal['allOldBuildFoldersRemoved'] and
        not removal['fullPortAcceptance'],'Exact bounded recoverable cleanup')
    inherited=state['inputHashes']; fresh=dict(proof['inputHashes'])
    fresh[str(previous)]=common.sha(previous); fresh[str(proof_path)]=common.sha(proof_path)
    for name in leaves:
        path=ROOT/name/'report.json'; fresh[str(path)]=common.sha(path)
    for name in ['inventory_workspace_space_v3237.py','compact_workspace_large_files_v3239.py',
        'plan_unreferenced_workspace_cleanup_v3241.py','archive_obsolete_workspace_v3243.py',
        'compact_workspace_fast_files_v3245.py','verify_bounded_audio_compaction_v3247.py',
        'remove_verified_obsolete_workspace_v3251.ps1','archive_obsolete_workspace_parallel_v3253.py',
        'verify_obsolete_workspace_parallel_v3255.py','check_launcher_after_workspace_cleanup_v3257.ps1',
        'save_workspace_cleanup_checkpoint_v3259.py','archive_obsolete_workspace_zstd_v3261.py',
        'prefetch_obsolete_archive_sources_v3263.py']:
        path=ROOT/'tools'/name; fresh[str(path)]=common.sha(path)
    recovery=reports['audit_v3262_obsolete_workspace_zstd_recovery']
    fresh[recovery['recoveryArchive']]=recovery['recoveryArchiveSHA256']
    fresh[str(ROOT/'audit_v3262_obsolete_workspace_zstd_recovery/inventory.json')]=recovery['inventorySHA256']
    fresh[recovery['originalParallelHashedInventory']]=recovery['originalParallelHashedInventorySHA256']
    checked=reports['audit_v3256_obsolete_workspace_parallel_removal_checked']
    fresh[checked['sourceManifestPath']]=checked['sourceManifestSHA256']
    for path,digest in reports['audit_v3258_current_launcher_after_workspace_cleanup']['preservedHashes'].items(): fresh[path]=digest
    with ThreadPoolExecutor(max_workers=12) as pool:
        actual=dict(zip(fresh,pool.map(common.sha,fresh)))
    common.need(actual==fresh,'Every fresh gameplay proof/cleanup/launcher dependency independently rehashed')
    for path,digest in fresh.items():
        common.need(path not in inherited or inherited[path]==digest,'Never rewrite historical source/evidence pins')
    inherited.update(fresh)
    state.update(previousCheckpoint=str(previous),thisGoalTurnClassification='Requested dependency-aware workspace cleanup; bounded actual human morph interruption/repetition/KO proof saved',
        gameSourceAndPlayableBytesChangedThisTurn=False,nativeGuestProgramChangedThisTurn=False,
        foldersDeletedThisTurn=removal['removedDirectories'],obsoleteFoldersDeletedThisTurn=True,
        allOldBuildFoldersRemoved=False,fullPortAcceptance=False,finishedRelease=False,
        currentNativeMorphAdversityReport=str(proof_path),currentNativeMorphAdversityPhysicalCases=24,
        currentNativeMorphAdversityCompleteCallbackFields=57624,
        currentNativeMorphAdversityCompleteRepeatedCycles=12,currentNativeMorphAdversityTrueMorphedKOResets=4,
        currentNativeMorphAdversityBothSlotsBoundedAccepted=True,
        currentNativeMorphAdversityAllCPUArtShadowsEraseArenaAudioAccepted=False,
        currentRequestedCleanupReports={name:str(ROOT/name/'report.json') for name in leaves},
        currentRequestedCleanupRemovedFolders=470,
        currentRequestedCleanupNetAllocatedBytes=removal['netAllocatedSavings']+
            reports['audit_v3246_workspace_fast_file_compaction']['reclaimedAllocatedBytes']+
            reports['audit_v3248_bounded_audio_compaction_checked']['reclaimedAllocatedBytes'],
        currentRequestedCleanupRecoveryArchive=removal['recoveryArchive'],
        currentRequestedCleanupCurrentCMDAndSettingsVerified=True,
        cleanupIncompleteTemporaryArchiveRetained=dict(
            path=str(ROOT/'audit_v3254_obsolete_workspace_parallel_recovery/obsolete_470_folders_complete_recovery.tar.xz'),
            bytes=64267399,reason='Its follow-up removal command was rejected by tool policy. No alternative deletion route was attempted; the complete verified Zstandard recovery is retained.'),
        workspaceStorageConstraint='User explicitly requested reduced drive usage. Reuse current isolated builds; avoid disposable executable/ROM copies. Compress finalized large captures promptly and remove obsolete unreferenced outputs with verified recovery, rather than accumulating new old-build folders.',
        nextAction='Resume the original five remaining acceptance groups. The current both-slot human morph adversity proof is bounded, not all CPU/art/shadow/audio/finisher/arena acceptance; native Shao clears and own endings remain unproven. No additional capture/build work was started for this cleanup request.')
    common.need(len(state['remaining'])==5 and state['currentRealShaoKahnMatchClears']==0 and
        not state['actualEndingsAccepted'] and not state['candidateUnderTestNativeBicycleHitOrBlockedAccepted'],
        'No weakened original requirements or invented clear/contact/endings acceptance')
    OUT.mkdir(); path=OUT/'checkpoint.json'; path.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(saved=str(path),goalStatus=state['goalStatus'],fullPortAcceptance=False,
        cleanupNetGiB=round(state['currentRequestedCleanupNetAllocatedBytes']/2**30,2),freshPinsRehashed=len(fresh)),indent=2))
if __name__=='__main__': main()
