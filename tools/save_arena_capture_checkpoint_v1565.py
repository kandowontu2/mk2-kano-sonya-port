"""Freeze completed arena smoke evidence; never pin still-changing run outputs."""
import hashlib,json,re
from pathlib import Path
import verify_active_launch_timer_v1520 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1565_native_arena_capture_checkpoint'

def verify():
    pins={}
    def pin(path,wanted=None):
        path=Path(path);key=str(path.resolve())
        if key not in pins:pins[key]=source.sha(path)
        assert wanted is None or pins[key]==wanted,'Changed arena evidence '+key
    previous=ROOT/'audit_v1558_native_cpu_campaign_checkpoint/checkpoint.json'
    pin(previous);old=json.loads(previous.read_text());assert not old['fullPortAccepted']
    reports={};total_frames=0;copies=0;components=0
    for fighter in('kano','sonya'):
        for version in(1562,1563):
            path=ROOT/f'audit_v{version}_floor_smoke_{fighter}_checked/report.json'
            r=json.loads(path.read_text());assert r['passed'];pin(path)
            for p,h in r.get('inputHashes',{}).items():pin(p,h)
            reports[str(path)]=source.sha(path)
            if version==1563:
                assert r['exactScanouts']==15 and r['actualArenaIDs']==[0] and not r['allNineRegularArenasSampled']
                total_frames+=r['exactScanouts'];copies+=r['nativeShadowCopies'];components+=r['nativeShadowComponents']
                assert not r['allMovePhaseFloorAccepted'] and not r['fullPortAcceptance']
    assert(total_frames,copies,components)==(30,19729,790)
    for name in('audit_v1561_floor_smoke_kano_p1','audit_v1561_floor_smoke_sonya_p2'):
        for path in(ROOT/name).rglob('*'):
            if path.is_file():pin(path)
    pending=[]
    for name,session,process in(('audit_v1564_native_arenas_kano_p1',20824,40580),('audit_v1564_native_arenas_sonya_p2',37741,87428)):
        folder=ROOT/name;before=folder/'input_hashes_before.json';manifest=json.loads(before.read_text(encoding='utf-8-sig'))
        pin(before)
        for p,h in manifest.items():pin(p,h)
        for path in(folder/'input_sources').iterdir():
            if path.is_file():pin(path)
        pending.append(dict(folder=str(folder),commandSession=session,processIDObserved=process,
                            handlesRepolledLiveBeforeCheckpoint=True,observedArenaIDsAtPoll=[0,1,2,3],
                            terminalResultExistsAtCheckpoint=(folder/'result.json').exists(),
                            changingRuntimeOutputsExcludedFromImmutablePins=True))
    for p in(ROOT/'mk2ks_natural_campaign_floor_v1560.lua',ROOT/'tools/run_natural_campaign_floor_v1560.ps1',
             ROOT/'tools/verify_native_floor_campaign_v1562.py',ROOT/'tools/verify_current_native_arenas_v1563.py',
             ROOT/'STATUS_2026-10-03_V1517_NATIVE_ARENA_CAPTURE.md',ROOT/'PLAY_CURRENT_V1517_TEST_BUILD.cmd',Path(__file__)):
        pin(p)
    pin(ROOT/source.NAME/'mkport_candidate.exe',source.EXE_SHA)
    return dict(candidate=source.NAME,previousCheckpoint=str(previous),previousCheckpointSHA256=source.sha(previous),
                previousPinsBoundByManifest=len(old['inputHashes']),previousPinsIndividuallyRehashedThisCheckpoint=False,
                immutableCompletedReports=reports,completedSmokeNativeFrames=30,nativeShadowCopies=19729,
                nativeShadowComponents=790,originalPhysicalInputPolicyByteExact=True,
                pendingCaptures=pending,allNineRegularArenasAccepted=False,allMovePhaseGroundingAccepted=False,
                fullCampaignAccepted=False,playableGameChangedThisWork=False,additionalBuildCleanup=False,
                releaseZIPUpdated=False,fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(completedNativeFrames=30,freshPins=len(report['inputHashes']),pendingCampaigns=2,fullPortAccepted=False)),flush=True)
