"""Freeze completed native palette/geometry evidence and truthful arena-check status."""
import hashlib,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
import verify_active_launch_timer_v1520 as source

ROOT=source.ROOT;OUT=ROOT/'audit_v1584_native_arena_context_checkpoint'
CASES=(('audit_v1564_native_arenas_kano_p1','audit_v1583_native_arenas_kano_checked','kano',1),
       ('audit_v1564_native_arenas_sonya_p2','audit_v1583_native_arenas_sonya_checked','sonya',2),
       ('audit_v1576_native_arenas_kano_p2','audit_v1583_native_arenas_kano_p2_checked','kano',2),
       ('audit_v1576_native_arenas_sonya_p1','audit_v1583_native_arenas_sonya_p1_checked','sonya',1))

def verify():
    pins={}
    def pin(path,wanted=None):
        path=Path(path);key=str(path.resolve())
        if key not in pins:pins[key]=source.sha(path)
        assert wanted is None or pins[key]==wanted,'Changed immutable evidence '+key
    previous=ROOT/'audit_v1565_native_arena_capture_checkpoint/checkpoint.json';pin(previous)
    old=json.loads(previous.read_text());assert not old['fullPortAccepted']
    completed=[]
    for name in('audit_v1570_geometry_smoke_kano_checked','audit_v1570_geometry_smoke_sonya_checked',
                'audit_v1575_drawing_scope_regression_checked','audit_v1582_native_palette_contexts_checked'):
        path=ROOT/name/'report.json';r=json.loads(path.read_text());assert r['passed'];pin(path)
        for file,wanted in r['inputHashes'].items():pin(file,wanted)
        completed.append(str(path))
    failures=[]
    for name in('audit_v1572_native_arenas_sonya_checked','audit_v1574_native_arenas_sonya_checked',
                'audit_v1574_native_arenas_kano_checked','audit_v1581_native_arenas_sonya_checked'):
        path=ROOT/name/'report.json';r=json.loads(path.read_text());assert not r['passed'];pin(path)
        failures.append(dict(report=str(path),error=r['error'],accepted=False))
    for fighter in('kano','sonya'):
        path=ROOT/f'audit_v1579_{fighter}_campaign_palette_diagnostic/report.json';r=json.loads(path.read_text());pin(path)
        assert r['diagnosticCompleted']and len(r['actualFailures'])==(18 if fighter=='kano'else 14)
        for file,wanted in r['inputHashes'].items():pin(file,wanted)
    cases=[];accepted_count=0;frames=0;copies=0
    for folder_name,report_name,fighter,side in CASES:
        folder=ROOT/folder_name;launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        assert launch['exit_code']==0 and launch['candidate']==source.NAME and launch['seconds']==900 and launch['assistance']=='none'
        assert launch['player']==fighter and launch['human_slot']==side and launch['executable_sha256']==source.EXE_SHA
        # Captures are all terminal now. Pin actual complete retained bytes;
        # missing or still-running checker outputs never become acceptance.
        for path in folder.rglob('*'):
            if path.is_file():pin(path)
        path=ROOT/report_name/'report.json';accepted=False;report=None
        if path.is_file():
            report=json.loads(path.read_text());pin(path)
            if report['passed']:
                assert report['fighter']==fighter and report['human_slot']==side and report['allNineRegularArenasSampled']
                assert report['actualArenaIDs']==list(range(9))and not report['allMovePhaseFloorAccepted']and not report['fullPortAcceptance']
                for file,wanted in report['inputHashes'].items():pin(file,wanted)
                accepted=True;accepted_count+=1;frames+=report['exactScanouts'];copies+=report['nativeShadowCopies']
        cases.append(dict(capture=str(folder),fighter=fighter,humanSlot=side,terminalExit=0,
                          verifierReport=str(path),verifierReportExists=path.is_file(),accepted=accepted,
                          checkerFailure=report.get('error')if report and not accepted else None))
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -like '*tools/verify_native_arena_geometry_v1583.py*' } | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"
    observation=subprocess.run(['powershell','-NoProfile','-Command',command],capture_output=True,text=True,check=True)
    live=json.loads(observation.stdout)if observation.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    for name in('tools/verify_native_floor_campaign_v1573.py','tools/verify_native_arena_geometry_v1574.py',
                 'tools/verify_drawing_scope_regression_v1575.py','tools/inspect_campaign_palette_failure_v1577.py',
                 'tools/inspect_campaign_palette_failure_v1578.py','tools/inspect_campaign_palette_failure_v1579.py',
                 'tools/verify_native_campaign_palette_v1580.py','tools/verify_native_arena_geometry_v1581.py',
                 'tools/verify_native_palette_contexts_v1582.py','tools/verify_native_arena_geometry_v1583.py',
                 'mk2ks_natural_campaign_floor_v1566.lua','tools/run_natural_campaign_floor_v1566.ps1',
                 'PLAY_CURRENT_V1517_TEST_BUILD.cmd'):
        pin(ROOT/name)
    pin(Path(__file__));pin(ROOT/source.NAME/'mkport_candidate.exe',source.EXE_SHA)
    return dict(candidate=source.NAME,observedUTC=datetime.now(timezone.utc).isoformat(),
                previousCheckpoint=str(previous),previousCheckpointSHA256=source.sha(previous),
                previousPinsIndividuallyRehashedThisCheckpoint=False,completedBoundedReports=completed,
                retainedFailedCheckerReports=failures,terminalCampaignCases=cases,
                actualNativePaletteEffectCasesAccepted=32,badPaletteStateAndOwnerCasesRejected=96,
                scopeRegressionVerifiedCaptureCount=4,everyScopeRegressionDrawingRowBoundToActualHumanSlotAndFighter=True,
                additionalExactGeometrySmokeFrames=30,additionalCoordinatePublicationsChecked=1211,
                acceptedFullArenaCases=accepted_count,acceptedFullArenaNativeFrames=frames,
                acceptedFullArenaNativeShadowCopies=copies,allNineArenasBothCharactersBothSlotsAccepted=accepted_count==4,
                liveCheckerProcessesAtObservation=live,allMovePhaseGroundingAccepted=False,
                fullBossCampaignAndEndingsAccepted=False,playableGameChangedThisWork=False,
                oldBuildCleanupCompleted=False,releaseZIPUpdated=False,fullPortAccepted=False,
                remainingWork=['Remaining arena checks and all-move-phase grounding/shadows',
                    'Remaining CPU repertoire, opponents and audio overlap/KO/round contexts',
                    'Remaining finisher/victim/morph consumers and special transitions',
                    'Unassisted boss wins, full ladders, endings, secrets and cinematic teardown',
                    'Final release ZIP and safe obsolete-build cleanup'],inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','terminalCampaignCases','retainedFailedCheckerReports','remainingWork')},indent=2),flush=True)
