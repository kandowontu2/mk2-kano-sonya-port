"""Current native UI/mobility/portable-playtest and recoverable cleanup checkpoint."""
import json
from pathlib import Path
from verify_human_special_phases_v1767 import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1868_current_presentation_release_checkpoint'
def verify():
    previous=ROOT/'audit_v1853_ball_register_frontier_checkpoint/checkpoint.json'
    prior=json.loads(previous.read_text());assert prior['goalStatus']=='active'
    pins={str(previous):sha(previous)};accepted=dict(prior['acceptedReports'])
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);value=sha(path)
        assert wanted is None or value==wanted,'Changed authoritative evidence '+key
        assert key not in pins or pins[key]==value;pins[key]=value
    for p,h in prior['inputHashes'].items():pin(p,h)
    names=['audit_v1856_current_native_ui_checked','audit_v1859_current_ground_shadow_checked',
           'audit_v1860_current_native_ui_units','audit_v1861_current_ground_shadow_counterexamples',
           'audit_v1864_portable_playtest_zip_checked','audit_v1865_superseded_ball_build_cleanup',
           'audit_v1867_duplicate_package_cleanup']
    reports={}
    for name in names:
        path=ROOT/name/'report.json';r=json.loads(path.read_text(encoding='utf-8-sig'))
        assert r['passed'],'Required evidence '+name;pin(path);reports[name]=r
        assert r.get('candidate','diagnostic_v1836_ball_register_boundary')=='diagnostic_v1836_ball_register_boundary'
        accepted[name]=dict(reportSHA=sha(path),scope=r.get('scope'),fullPortAcceptance=False)
        for p,h in r.get('inputHashes',{}).items():pin(p,h)
        for p,h in r.get('keptHashes',{}).items():pin(p,h)
    ui=reports['audit_v1856_current_native_ui_checked'];ground=reports['audit_v1859_current_ground_shadow_checked']
    assert ui['currentBothSlotSelectionLadderFirstMatchAccepted']and len(ui['cases'])==4
    assert ground['currentBoundedMobilityGroundShadowAccepted']and ground['samples']==148 and ground['nativeShadowCopies']==120162
    assert reports['audit_v1860_current_native_ui_units']['methods']==46
    assert reports['audit_v1861_current_ground_shadow_counterexamples']['count']==8
    package=ROOT/'release_v1863_current_playtest/package-report.json'
    info=json.loads(package.read_text(encoding='utf-8-sig'));assert info['passed'];pin(package)
    for p,h in info['sourceHashes'].items():pin(p,h)
    portable=reports['audit_v1864_portable_playtest_zip_checked']
    assert portable['romAuditExit']==portable['cmdColdBootExit']==0 and portable['developmentWorkspaceNotRequired']and not portable['finishedRelease']
    pin(portable['zip'],portable['zipSHA256'])
    assert portable['zipSHA256']=='994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'
    for name in ['tools/run_current_native_ui_v1854.ps1','tools/run_current_ground_shadow_v1857.ps1',
                 'tools/package_current_playtest_v1863.ps1','tools/verify_portable_playtest_zip_v1864.ps1',
                 'tools/archive_superseded_ball_build_v1865.ps1','tools/clean_duplicate_playtest_extractions_v1867.ps1',
                 'audit_v1864_portable_playtest_zip_checked/rom-audit.log','audit_v1864_portable_playtest_zip_checked/cmd-boot.log',
                 'release_v1863_current_playtest/RELEASE.json','release_v1863_current_playtest/sources_before.json',
                 'audit_v1865_superseded_ball_build_cleanup/inventory-before.json',
                 'audit_v1867_duplicate_package_cleanup/audit_v1744_portable_playtest_zip_checked-inventory.json',
                 'audit_v1867_duplicate_package_cleanup/audit_v1864_portable_playtest_zip_checked-inventory.json']:pin(ROOT/name)
    archive=reports['audit_v1865_superseded_ball_build_cleanup'];duplicate=reports['audit_v1867_duplicate_package_cleanup']
    assert not Path(archive['removedDirectory']).exists()and archive['archiveEveryEntryAndSourceHashVerified']
    pin(archive['recoveryZIP'],archive['recoveryZipSHA256'])
    for r in duplicate['removed']:
        assert not Path(r['removedDirectory']).exists();pin(r['retainedZIP'],r['zipSHA256'])
        for p,h in r['preservedHashes'].items():pin(p,h)
    reclaimed=archive['netBuildStorageReductionBytes']+duplicate['netDuplicateFileStorageReductionBytes']
    assert reclaimed==207452237
    viewed=['audit_v1855_ui_sonya_p1/snap/ui_0986.png','audit_v1855_ui_sonya_p1/snap/ui_1286.png',
            'audit_v1855_ui_kano_p2/snap/ui_1598.png','audit_v1858_ground_shadow_sonya_p1/snap/ground_1488.png']
    for name in viewed:pin(ROOT/name)
    pin(__file__)
    report={k:v for k,v in prior.items()if k!='inputHashes'}
    report.update(goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousGoalTurnClassification='progress: caller-preserving native rebound fix, both-slot full raster/shadow/erase, 52 current human move cases and corrected CMD boot',
      thisGoalTurnClassification='progress: fresh four character/slot native selection-to-first-match and sampled mobility/shadow checks, 46 UI and eight shadow counterexample tests, refreshed verified portable ZIP and recoverable removal of superseded/duplicate builds',
      gameSourceAndPlayableBytesChangedThisTurn=False,currentPlayableBuildUnchanged=True,
      acceptedReports=accepted,currentBothSlotSelectionLadderFirstMatchAccepted=True,
      currentSelectionScope=ui['scope'],currentUICharacterSlotCases=4,
      currentUISelectionFields=sum(r['selection_fields']for r in ui['cases'].values()),
      currentUIPostSelectionFields=sum(r['outside_fields']for r in ui['cases'].values()),
      currentUIInitialMatchParticipantFields=sum(r['first_match_participant_fields']for r in ui['cases'].values()),
      currentUIFailureCounterexampleMethods=46,
      currentBoundedMobilityGroundShadowAccepted=True,currentMobilityScope='Four cold true-ID human cases versus Kitana in Dead Pool; 481 paired fields each, 37 native sampled complete render passes each. Standing, walking, crouching, jumping and landing. Not all arenas/moves/art/CPU/audio or continuous inter-pass erase.',
      currentMobilityRenderedSamples=148,currentMobilityNativeShadowCopies=120162,currentMobilitySourceCounterexamplesRejected=8,
      newReleaseZIPCreated=True,portablePlaytestZipVerified=True,playtestZipCurrentCandidate=True,
      playtestZip=portable['zip'],playtestZipSHA256=portable['zipSHA256'],playtestZipBytes=portable['zipBytes'],
      portableReleaseScope=portable['scope'],olderPlaytestZIPRetained='v1597 ZIP remains unchanged as a historical playtest; v1836 ZIP is now current',
      cleanupAdditionalBytesReclaimedThisTurn=reclaimed,
      cleanupAllocatedBytesReclaimed=prior['cleanupAllocatedBytesReclaimed']+reclaimed,
      cleanupRemovedSupersededBuildFolders=1,cleanupRemovedDuplicateExtractionFolders=2,
      deletedPreExistingMaterialFilesThisTurn=147,
      deletedFilesThisTurn=147,allOldBuildFoldersRemoved=False,
      cleanupRecovery='Complete v1816 folder archived and every file hash checked; both disposable extraction copies regenerate from retained verified ZIPs; eight unique boot cfg/NVRAM/snapshot files preserved byte-for-byte.',
      cleanupRecoveryZIP=archive['recoveryZIP'],
      cleanupInventoryScope='Five early candidate folders inspected were small or still referenced by old source tests and were retained. One confirmed superseded unpinned v1816 build and two confirmed unpinned disposable portable-test extraction trees removed. Broader old-folder cleanup is unfinished.',
      pendingCaptures=[],newlyManuallyViewedFullScenes=viewed,
      manualReviewScope='Fresh Sonya highlighted selection, first teardown blank field, native Kano ladder icon reveal and Sonya standing/floor-shadow scene reviewed. Not universal artistic review.',
      preservedFailedNewEvidence=prior.get('preservedFailedNewEvidence',[])+[
        'tools/clean_duplicate_playtest_extractions_v1866.ps1 stopped before deletion: PowerShell property collection Count was not an array count. Fresh1867 uses explicit array counting and both exact 64-file extraction trees are verified, unique boot files preserved and disposable duplicates removed.'],
      nextAction='Broader repeated/interrupted/KO/CPU and victim/arena special integration, remaining finishers/morphs/cinematics/audio, natural boss clears and complete endings; then full final combined regression and dependency-aware remaining old-build cleanup. Current v1836 playtest ZIP is verified but is not the finished release.',
      previousCheckpointSHA=sha(previous),inputHashes=pins)
    return report
if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite checkpoint'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),goalStatus='active',pins=len(report['inputHashes']),
        currentCandidate=report['currentCandidate'],currentPlaytestZIP=report['playtestZip'],cleanupBytesReclaimedThisTurn=report['cleanupAdditionalBytesReclaimedThisTurn'],
        finishedRelease=False,fullPortAcceptance=False),indent=2),flush=True)
