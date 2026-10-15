"""Save verified native ball-boundary progress without narrowing full-port scope."""
import json
from pathlib import Path
from verify_human_special_phases_v1767 import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v1853_ball_register_frontier_checkpoint'
def verify():
    previous=ROOT/'audit_v1803_native_special_render_frontier_checkpoint/checkpoint.json'
    prior=json.loads(previous.read_text());assert prior['goalStatus']=='active'
    pins={str(previous):sha(previous)};accepted=dict(prior['acceptedReports'])
    for path,value in prior['inputHashes'].items():
        assert sha(path)==value,'Changed prior evidence '+path
        pins[path]=value
    names=['audit_v1837_ball_register_source_checked','audit_v1840_human_ball_p1_register_checked','audit_v1840_human_ball_p2_register_checked',
           'audit_v1842_human_ball_p1_render_checked','audit_v1842_human_ball_p2_render_checked',
           'audit_v1843_human_ball_p1_erase_checked','audit_v1843_human_ball_p2_erase_checked',
           'audit_v1846_ball_register_special_matrix_checked','audit_v1848_ball_register_runtime_units_checked',
           'audit_v1852_ball_register_launcher_checked']
    reports={}
    for name in names:
        path=ROOT/name/'report.json';r=json.loads(path.read_text(encoding='utf-8-sig'))
        assert r['passed'],'Required current evidence '+name
        assert r.get('candidate','diagnostic_v1836_ball_register_boundary')=='diagnostic_v1836_ball_register_boundary'
        pins[str(path)]=sha(path);reports[name]=r
        accepted[name]=dict(reportSHA=sha(path),scope=r.get('scope'),fullPortAcceptance=False)
        for p,h in r['inputHashes'].items():
            p=str(Path(p).resolve());assert sha(p)==h,'Changed current evidence '+p
            assert p not in pins or pins[p]==h;pins[p]=h
    matrix=reports['audit_v1846_ball_register_special_matrix_checked']
    assert matrix['current52CaseHumanStateMatrixAccepted']and len(matrix['cases'])==52 and matrix['exactPriorActualFullScreensMatched']==152
    units=reports['audit_v1848_ball_register_runtime_units_checked']
    assert units['negativeCases']==28 and units['sameFixedBoundaryScenesBeforeAndAfterCallerPreservation']==361
    build=ROOT/'diagnostic_v1836_ball_register_boundary/build-info.json'
    meta=json.loads(build.read_text(encoding='utf-8-sig'));assert meta['executable_sha256']=='34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E'
    canonical={'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
               'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
               'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
               'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'}
    for name,wanted in canonical.items():
        path=ROOT/name;assert sha(path)==wanted; pins[str(path)]=wanted
    viewed=[f'audit_v1841_human_ball_p{s}_boundary/snap/display_1710.png'for s in(1,2)]
    for name in viewed:pins[str(ROOT/name)]=sha(ROOT/name)
    for name in ['audit_v1830_ball_boundary_special_matrix_checked/report.json','audit_v1847_ball_register_runtime_units_checked/report.json',
                 'audit_v1851_ball_register_launcher_checked/report.json','audit_v1851_ball_register_launcher_checked/run.log']:
        path=ROOT/name;pins[str(path)]=sha(path)
    pins[str(Path(__file__))]=sha(__file__)
    report={k:v for k,v in prior.items()if k!='inputHashes'}
    report.update(goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousGoalTurnClassification='no progress: status-only request inspected latest reports',
      thisGoalTurnClassification='progress: revised native callback preserves separation and all seven helper-clobbered caller registers; 52 current physical move fixtures, both-slot full raster/shadow/continuous-clear and 28 negative runtime cases passed; actual corrected CMD boot tested',
      currentCandidate='diagnostic_v1836_ball_register_boundary',currentCMD='PLAY_CURRENT_V1836_CHECKED.cmd',
      gameSourceAndPlayableBytesChangedThisTurn=True,currentPlayableBuildUnchanged=False,
      executableSHA256=meta['executable_sha256'],payloadSHA256=meta['payload_sha256'],
      acceptedReports=accepted,current52CaseHumanStateMatrixAccepted=True,
      currentBallBoundaryDepartureAcceptedInBoundedBothSlots=True,
      ballBoundaryDepartureNativeFeelingAccepted=True,
      ballBoundaryScope='Both cold physical human slots versus Sub-Zero in arena zero, one hit ball command each. 361 consecutive full scenes: owned body remains visible, original floor shadows source/pixel-exact, continuous native erase exact. Original 304 distance correction stops outward rebound, no late 54-pixel return. Not all ranges/victims/arenas/CPU/repeats/interrupts.',
      ballBoundaryEvidence='42 actual callbacks/returns each; all A1-A5/A8-A9 and SP restored, A0 retains original three. Native corrections at most nine/seven pixels, 24 damage and 42-field recoil unchanged, post-expiry separation 305/304. Blocked/missed balls retain every previous native event and endpoint scene.',
      currentBallFullScenes=361,currentBallShadowCopies=16087,currentBallNativeShiftClearTransfers=46101,
      callerRegisterRuntimeNegativeCasesRejected=28,
      ballBodyAndShadowAlwaysVisibleInObservedScenes=True,
      newReleaseZIPCreated=False,playtestZipCurrentCandidate=False,
      olderPlaytestZIPRetained='v1597 current-state ZIP remains unchanged; not refreshed to v1836',
      newlyManuallyViewedFullScenes=viewed,
      manualReviewScope='Actual P1/P2 rebound frames 1710 viewed after caller-preserving build; both owned bodies/shadows are visible. Not universal artwork review.',
      pendingCaptures=[],allOldBuildFoldersRemoved=False,cleanupAdditionalBytesReclaimedThisTurn=0,
      deletedPreExistingMaterialFilesThisTurn=0,deletedUnusedProvisionalFilesCreatedThisTurn=3,
      launcherBootScope='Actual hash-checked CMD, physical inputs absent, no diagnostic autoboot, eight seconds from a different working directory, video/sound none. Existing older launchers and control settings unchanged. Not GUI or complete interactive audio/game/campaign acceptance.',
      preservedFailedNewEvidence=prior.get('preservedFailedNewEvidence',[])+[
        'audit_v1830_ball_boundary_special_matrix_checked: original helper scratch A2/A3 changed in one blocked-ball parameter observation. Fresh candidate1836 preserves every helper-clobbered caller register; fresh1846 retains every unaffected event without relaxing old predicates.',
        'audit_v1847_ball_register_runtime_units_checked: mutation toggled unrelated status bit instead of carry. Fresh1848 corrupts the actual carry condition and actual callback timer store; all 28 in-memory negative cases rejected.',
        'audit_v1851_ball_register_launcher_checked: generated CMD used incorrect candidate directory suffix. Preserved; corrected fresh PLAY_CURRENT_V1836_CHECKED.cmd and fresh1852 boot passed.',
        'audit_v1820_human_ball_p1/p2_boundary: observer1818 extra-end Lua syntax error before game execution; fresh1822 and1838 observers used unchanged physical baseline'],
      remainingFullScope=[
        'Broader repeated/blocked/interrupted/KO/CPU special fixtures, all victim/arena rendering and audio, universal artistic grounding',
        'All remaining finisher/victim/morph/friendship/secrets/cinematics including complete stage-finisher presentation',
        'Genuine full boss/campaign clears for both true-ID fighters, own complete endings and return to attract',
        'Final combined native selection, ladder, names, grounding, audio and gameplay acceptance',
        'Dependency-aware obsolete-build folder cleanup and finished release ZIP'],
      nextAction='Revalidate combined UI and grounded gameplay on the new current candidate, then broader repeated/interrupted/CPU and victim/arena boundary cases, campaign/boss/endings and remaining whole-game natural integration; cleanup and refreshed final release. The complete original scope remains active.',
      previousCheckpointSHA=sha(previous),inputHashes=pins)
    return report
if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite checkpoint evidence'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),goalStatus=report['goalStatus'],candidate=report['currentCandidate'],
                         currentCMD=report['currentCMD'],pins=len(report['inputHashes']),fullPortAcceptance=False),indent=2),flush=True)
