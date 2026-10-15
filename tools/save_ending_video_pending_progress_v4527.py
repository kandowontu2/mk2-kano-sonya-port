"""Full scope retained; genuine missing ending-video observer live, not accepted."""
import ctypes,json,re,subprocess
from pathlib import Path
import qualify_ending_display_source_v4522 as video
ROOT,need,sha=video.ROOT,video.need,video.sha
PARENT=ROOT/'audit_v4517_native_ending_audio_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4528_ending_video_live_full_scope_checkpoint'
CASE=ROOT/'audit_v4524_kano_p2_ending_display_ram'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope live-video progress')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'All inherited actual source/proof/public bytes unchanged')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted)and(key not in pins or pins[key]==actual),'Every inherited/current exact byte pin')
        pins[key]=actual
    pin(PARENT);pin(__file__)
    preflight=video.OUT/'report.json';proof=json.loads(preflight.read_text());pin(preflight)
    need(proof['passed']and len(proof['contexts'])==2 and len(proof['actualObserverSourceFaultsRejected'])==4 and
      not proof['nativeEndingVideoAcceptance']and not proof['fullPortAcceptance'],
      'Actual complete read-only source/transport preflight, never called native video success')
    for p,h in proof['inputHashes'].items():pin(p,h)
    for f in ('kano','sonya'):video.source_boundary(f)
    manifest=CASE/'input_hashes_before.json';before=json.loads(manifest.read_text());pin(manifest)
    for p,h in before.items():pin(p,h)
    snapshots=json.loads((CASE/'source_snapshot_paths.json').read_text());pin(CASE/'source_snapshot_paths.json')
    for p,frozen in snapshots.items():pin(frozen,before[p])
    process=json.loads((CASE/'process.json').read_text());pin(CASE/'process.json')
    need(process['pid']==92488 and process['command'][0]==str(ROOT/'diagnostic_v3836_native_mileena_rom_identity/mkport_candidate.exe')and
      process['command'][-1]==str(ROOT/video.LUA['kano'])and not (CASE/'result.json').exists(),
      'Actual new native Kane17 P2 video observation still pending, not a reused terminal tower')
    query='Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(91580,92488) } | Select-Object ProcessId,ParentProcessId,Name,CreationDate,CommandLine | ConvertTo-Json -Compress'
    check=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(check.returncode==0 and check.stdout.strip(),'Fresh actual live process census, not inferred from files')
    jobs=json.loads(check.stdout);jobs=jobs if isinstance(jobs,list)else[jobs]
    need({r['ProcessId']for r in jobs}=={91580,92488}and
      any(r['ProcessId']==91580 and '-B' in r['CommandLine']and'run_ending_display_campaign_ram_v4526.py --fighter kano'in r['CommandLine']for r in jobs)and
      any(r['ProcessId']==92488 and r['ParentProcessId']==91580 and CASE.name in r['CommandLine']for r in jobs),
      'Exact still-live collector and its own native emulator; never restart on an observation timeout')
    with(CASE/'run.log').open('rb')as f:
        f.seek(max(0,(CASE/'run.log').stat().st_size-16384));tail=f.read(16384).decode('utf-8',errors='replace')
    live=[line for line in tail.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_LIVE ')]
    need(live and not re.search(r'LUA ERROR|Lua error|stack traceback|fatal error|access violation',tail),
      'Actually observed native ongoing campaign, no observed runtime error; not terminal acceptance')
    observed=dict(re.findall(r'(\w+)=([^\s]+)',live[-1]));need(observed['human']=='17:17'and observed['human_slot']=='2','Actual current true Kano17P2 live actor/roster')
    cleanup_path=ROOT/'audit_v4530_regenerable_python_cache_removed/report.json'
    cleanup=json.loads(cleanup_path.read_text(encoding='utf-8-sig'));pin(cleanup_path)
    pin(ROOT/'tools/remove_regenerable_python_cache_v4529.ps1')
    need(cleanup['passed']and cleanup['deletedFiles']==711 and cleanup['newlyReclaimedAllocatedBytes']==18701301 and
      cleanup['allOriginalSourceFilesPreserved']and cleanup['pinnedOrLiveInputFilesRemoved']==0 and
      cleanup['publicPlayableReleaseROMAndBuildFilesRemoved']==0 and not (ROOT/'tools/__pycache__').exists(),
      'Only actual unpinned regenerable bytecode removed; current new allocation savings, never historical recount')
    for record in cleanup['records']:
        need(not Path(record['cache']).exists(),'Actual exact cache file absent after terminal cleanup')
        pin(record['source'],record['sourceSHA256'])
    files=[p for folder in (video.OUT,ROOT/'audit_v4530_regenerable_python_cache_removed')for p in folder.rglob('*')if p.is_file()]
    files.extend(Path(p)for p in proof['inputHashes']if Path(p).name.endswith(('_v4518.lua','_v4519.py','_v4520.lua','_v4521.lua','_v4522.py','_v4526.py')))
    files.extend([Path(__file__),ROOT/'tools/remove_regenerable_python_cache_v4529.ps1'])
    files=list(dict.fromkeys(files))
    alloc=ctypes.windll.kernel32.GetCompressedFileSizeW
    alloc.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];alloc.restype=ctypes.c_uint32
    allocated=0
    for p in files:
        hi=ctypes.c_uint32();lo=alloc(str(p),ctypes.byref(hi));need(lo!=0xffffffff,'Actual new completed evidence allocation')
        allocated+=(hi.value<<32)|lo
    next_action=('First poll exec session75732 and exact collector91580/native92488 for new KanoP2 ending-video window. '
      'They were freshly confirmed live; timeout is not termination and must not cause restart. Source4526/4518/4519 '
      'and preflight4522/4523 are executed/pinned/frozen. The unchanged accepted cold campaign is reused solely to '
      'observe missing continuous ending transitions, not claim a new tower clear. On real terminal, inspect '
      'audit_v4524_kano_p2_ending_display_ram/result.json and audit_v4525_kano_p2_ending_display_checked/report.json. '
      'If a real model/observer failure appears, preserve it and repair only fresh unused source/output; never '
      'edit these executed inputs or fabricate native events. Do not accept video merely because preflight passes. '
      'Only after checking actual first context, run the already frozen4526 --fighter sonya for its fresh missing '
      'window. Require every native CPU/shift/DMA/source/pre-buffer/flip/held/VRAM/RGB field, full original campaign '
      'equality, original-source-qualified pages and actual faults; independent stock choreography/art/cinematic/'
      'audio/all-P1/full-port exclusions remain. Continue all five original groups, broader native Pit/Tomb stock '
      'victims/branches/audio, full move phases/ground/floor shadows/CPU/repeat/KO/overlap, other finishers/victims/'
      'morphs/secrets/cinematics, required current natural towers/endings/attract contexts and final combined '
      'selection/ladder/names/audio/dependency cleanup/refreshed release. The only cleanup now completed is711 '
      'regenerable .pyc files, actual18,701,301allocated bytes, all sources/pinned inputs/publics retained.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='All original groups/evidence/exclusions retained; missing ending-video preflight and actual live job, regenerable-cache cleanup added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: complete ending-audio checkpoint saved; new read-only continuous ending-video source and actual faults qualified; genuine new native KanoP2 job launched and freshly verified live; unpinned regenerable bytecode removed with all sources unchanged.',
      current3836EndingContinuousVideoSourcePreflightAccepted=True,
      current3836BothP2CompleteEndingNativeRendererVideoAccepted=False,
      current3836EndingIndependentStockChoreographyAccepted=False,
      current3836AllEndingTransitionArtCinematicsAudioContextsAccepted=False,
      currentKanoP2EndingVideoObservationPending=dict(execSession=75732,collectorPID=91580,nativePID=92488,
        actualLiveCIMProcesses=jobs,lastActuallyObservedNativeLive=observed,capture=str(CASE),
        sourcePreflight=str(preflight),nativeVideoAcceptance=False,noRestartOnObservationTimeout=True),
      currentTurnDeletedFiles=711,currentTurnReclaimedAllocatedBytes=18701301,
      currentTurnCompletedEvidenceAllocatedBytes=allocated,
      liveDiagnosticAllocationExcludedFromCompletedCount=True,
      cleanupReport=str(cleanup_path),cleanupAccounting='Actual new cache-file allocation only. All sources retained; no historical saving repeated; live compressed diagnostic allocation not called reclaimed space.',
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Entire original objective and all five remaining groups intact')
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited/current/public/preserved source byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),actualNewNativeJobPending=True,
      lastObservedFrame=int(observed['frame']),lastObservedStage=int(observed['stage']),
      completedEvidenceAllocatedBytes=allocated,newlyReclaimedAllocatedBytes=18701301,
      originalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
