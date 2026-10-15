"""Preserve full port scope; add actual finisher-state evidence and live video repair."""
import ctypes,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PARENT=ROOT/'audit_v4532_ending_video_live_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint'
CASE=ROOT/'audit_v4547_kano_p2_ending_display_ram'

def need(value,message):
    if not value:raise AssertionError(message)

def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()

def main():
    need(not OUT.exists(),'Fresh checkpoint only')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'All inherited evidence/public/source unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=sha(path);key=str(path)
        need((wanted is None or actual==wanted) and (key not in pins or pins[key]==actual),'Exact immutable source/evidence pin')
        pins[key]=actual
    pin(PARENT);pin(__file__)
    reports={}
    for key,leaf in [('checked','audit_v4555_current_scorpion_secondary_state_checked'),
                     ('observed','audit_v4553_current_scorpion_secondary_state_observed'),
                     ('source','audit_v4551_current_scorpion_secondary_source_checked'),
                     ('video','audit_v4546_ending_display_source_preflight')]:
        path=ROOT/leaf/'report.json';report=json.loads(path.read_text());pin(path)
        need(report['passed'] and not report['fullPortAcceptance'],'Scoped real proof only')
        for p,h in report['inputHashes'].items():pin(p,h)
        reports[key]=report
    proof=reports['checked']
    need(proof['actualCurrentNativeContexts']==6 and proof['actualQualifiedFaultsRejected']==66 and
         proof['completePhysicalStateFields']==5760 and proof['actualCollisionKOs']==12 and
         proof['currentBothTrueAddedVictimsBothSlotsScorpionSecondaryNativeStateAccepted'] and
         not proof['fullNativeArtFloorShadowAlternateArenasOrAudioAccepted'],
         'Six real contexts, complete state and actual faults; no art/audio scope substitution')
    need({(r['fighter'],r['physicalVictimSlot'],r['identity']) for r in proof['cases']}==
         {('kitana',1,4),('liu_kang',2,1),('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18)} and
         all(len(r['actualRowFaultsRejected'])==11 and r['wholePositiveRestoredAfterEveryFault'] for r in proof['cases']),
         'Actual both physical slots/true identities and stock controls')
    video=reports['video']
    need(video['generatedCollectorStderrAndModelErrorLocalsAreDistinct'] and
         len(video['actualObserverSourceFaultsRejected'])==4 and not video['nativeEndingVideoAcceptance'],
         'Fresh repaired pre-boot source proof is not native video acceptance')
    failure_path=ROOT/'audit_v4525_kano_p2_ending_display_checked/report.json'
    failure=json.loads(failure_path.read_text());pin(failure_path)
    need(not failure['passed'] and 'TextIOWrapper' in failure['error'],'Preserve actual terminal collector failure')
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_display_campaign_ram_v4540.py|audit_v4547_|run_current_scorpion_secondary_state_v4549.py|audit_v4552_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(census.returncode==0 and census.stdout.strip(),'Actual fresh process census')
    jobs=json.loads(census.stdout);jobs=jobs if isinstance(jobs,list) else[jobs]
    need({r['ProcessId'] for r in jobs}=={36624,135848} and
         any(r['ProcessId']==135848 and r['ParentProcessId']==36624 and CASE.name in r['CommandLine'] for r in jobs) and
         any(r['ProcessId']==36624 and 'run_ending_display_campaign_ram_v4540.py --fighter kano' in r['CommandLine'] for r in jobs),
         'Exact original fresh repaired live ending handles; six state jobs terminal')
    need(not (CASE/'result.json').exists(),'Live missing video window, not accepted terminal capture')
    process=json.loads((CASE/'process.json').read_text());need(process['pid']==135848,'Actual native capture PID')
    for name in ('process.json','input_hashes_before.json','source_snapshot_paths.json'):pin(CASE/name)
    before=json.loads((CASE/'input_hashes_before.json').read_text())
    for p,h in before.items():pin(p,h)
    for original,frozen in json.loads((CASE/'source_snapshot_paths.json').read_text()).items():pin(frozen,before[original])
    files=[]
    leaves=['audit_v4551_current_scorpion_secondary_source_checked','audit_v4553_current_scorpion_secondary_state_observed',
            'audit_v4555_current_scorpion_secondary_state_checked','audit_v4546_ending_display_source_preflight',
            'audit_v4524_kano_p2_ending_display_ram','audit_v4525_kano_p2_ending_display_checked']
    leaves.extend(p.name for p in ROOT.glob('audit_v4552_scorpion_secondary_*_native_state_ram'))
    for leaf in leaves:
        files.extend(p for p in (ROOT/leaf).rglob('*') if p.is_file())
    files.extend(ROOT/p for p in ['tools/run_current_scorpion_secondary_state_v4537.py',
      'tools/check_scorpion_secondary_source_v4535.py','tools/run_current_scorpion_secondary_state_v4549.py',
      'tools/check_scorpion_secondary_source_v4550.py','tools/verify_current_scorpion_secondary_state_v4554.py',
      'tools/run_ending_display_campaign_ram_v4540.py','tools/qualify_ending_display_source_v4541.py',
      'mk2ks_ending_display_ram_v4542.lua','mk2ks_kano_ending_display_campaign_ram_v4543.lua',
      'mk2ks_sonya_ending_display_campaign_ram_v4544.lua','mk2ks_scorpion_secondary_state_ram_v4534.lua'])
    files=list(dict.fromkeys(files));allocated=0
    alloc=ctypes.windll.kernel32.GetCompressedFileSizeW
    alloc.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];alloc.restype=ctypes.c_uint32
    for p in files:
        pin(p);hi=ctypes.c_uint32();lo=alloc(str(p),ctypes.byref(hi));need(lo!=0xffffffff,'Exact completed compressed allocation')
        allocated+=(hi.value<<32)|lo
    next_action=('Poll exact exec82454/collector36624/native135848, never restart on observation timeout. '
      'Inspect actual4547 result and4548 report only after terminal; full video remains unaccepted. '
      'If first complete video passes, observe fresh Sonya window with frozen4540. '
      'Scorpion secondary state now verified for both true added victims in both slots plus stock controls; '
      'do not repeat these same state-only contexts as new coverage. Still require full finisher art/ground/'
      'shadows/audio/alternate/arenas and all other original requirement groups: broader Pit/Tomb victims/'
      'branches/audio; move-phase/CPU/repeat/KO/overlap; finishers/morphs/secrets/cinematics; required natural '
      'towers/endings/attract; final combined selection/ladder/names/audio/dependency cleanup/release.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every inherited full scope/evidence/exclusion retained; actual six-context state proof and repaired live ending observer added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: six actual current native Scorpion-secondary state contexts and66 real-row faults passed; disabled ending collector diagnosed and repaired into fresh preflight and genuinely live new observation.',
      currentScorpionSecondaryBothTrueAddedVictimsBothSlotsNativeStateAccepted=True,
      currentScorpionSecondaryStateReport=str(ROOT/'audit_v4555_current_scorpion_secondary_state_checked/report.json'),
      currentScorpionSecondaryStateContexts=proof['cases'],
      currentScorpionSecondaryFullArtFloorShadowAlternateArenasAudioAccepted=False,
      priorEndingVideoCollectorFailure=dict(report=str(failure_path),error=failure['error'],
        collectorExit=1,nativeExitCodePersisted=False,fullVideoAccepted=False,
        cause='Original stderr context local errors overwrote the model error list, disabled replay, then failed JSON serialization.',
        correction='Fresh4540 uses scene_errors; fresh4541 asserts distinct generated locals before boot. Executed originals frozen.'),
      unexecutedScorpionPrototypeCorrection=dict(source=str(ROOT/'tools/run_current_scorpion_secondary_state_v4537.py'),
        executed=False,nativeJobsLaunched=False,condition='Pre-boot AST parse rejected three ternary spacing mistakes.',
        correction='Fresh4549 spacing-only repair and fresh4550 AST preflight; originals frozen; no retired capture resurrection.'),
      current3836EndingContinuousVideoSourcePreflightAccepted=True,
      current3836BothP2CompleteEndingNativeRendererVideoAccepted=False,
      currentKanoP2EndingVideoObservationPending=dict(execSession=82454,collectorPID=36624,nativePID=135848,
        actualLiveCIMProcesses=jobs,capture=str(CASE),sourcePreflight=str(ROOT/'audit_v4546_ending_display_source_preflight/report.json'),
        nativeVideoAcceptance=False,noRestartOnObservationTimeout=True),
      currentTurnDeletedFiles=0,currentTurnReclaimedAllocatedBytes=0,currentTurnCompletedEvidenceAllocatedBytes=allocated,
      currentTurnCompletedEvidenceLogicalBytes=sum(p.stat().st_size for p in files),liveDiagnosticAllocationExcludedFromCompletedCount=True,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,
      cleanupAccounting='Zero new deletions/reclaim; prior18,701,301B cache savings not recounted; live4547 excluded from completed allocation.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All five original groups unchanged')
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited/current/public source pin unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),actualNativeContexts=6,
      rejectedActualFaults=66,endingVideoLive=True,fullPortAcceptance=False,completedEvidenceAllocatedBytes=allocated),indent=2),flush=True)

if __name__=='__main__':main()
