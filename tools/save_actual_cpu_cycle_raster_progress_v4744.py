"""Full-scope additive journal: terminal Sonya and actual CPU beam boundary."""
import json,subprocess
from pathlib import Path
import save_actual_notifier_io_progress_v4735 as previous
import qualify_actual_cpu_cycle_raster_boundary_v4742 as diagnostic
import verify_ending_native_io_clock_ledger_v4737 as ledger
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4736_actual_notifier_io_progress/progress.json']
OUT=ROOT/'audit_v4745_actual_cpu_cycle_raster_progress'

def main():
    need(not OUT.exists(),'Fresh immutable whole-goal journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Whole-goal source/evidence hash chain consistent');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'All inherited native/source/playable bytes unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or wanted==actual)and(key not in inherited or inherited[key]==actual)and
             (key not in pins or pins[key]==actual),'Exact immutable additive source/evidence input')
        if key not in inherited:pins[key]=actual
    for path in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(path)
    old=ROOT/'audit_v4713_sonya_p2_ending_raster_clock_ram'
    terminal=ROOT/'audit_v4714_sonya_p2_ending_raster_clock_checked/report.json'
    failed=json.loads(terminal.read_text());meta=json.loads((old/'result.json').read_text())
    need(not failed['passed']and meta['exit_code']==0 and meta['observedEndingRGBFields']==3043 and
         meta['exactContinuousEndingFields']==0 and meta['actualNativeFrameCallbacks']==78 and
         len(meta['endingModelErrors'])==1 and 'frame=84378 'in meta['endingModelErrors'][0]['line']and
         'Actual field starts after prior273partial update, before next274latch'in meta['endingModelErrors'][0]['error'],
         'Real Sonya native terminal0/all3043observed fields; no old full-video acceptance')
    pin(terminal)
    for p,h in meta['input_hashes'].items():pin(p,h)
    for p in old.rglob('*'):
        if p.is_file():pin(p)
    reference=ROOT/'audit_v4440_sonya_kintaro_pressure_guard_long_p2_campaign/run.log'
    prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_',
              'MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
    def selected(path):
        with path.open()as stream:
            return[l.rstrip()for l in stream if l.startswith(prefixes)and not l.startswith(
              ('MK2_NAT_CAMPAIGN_FLOOR_','MK2_NAT_CAMPAIGN_SHADOW_','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_'))]
    need(selected(old/'run.log')==selected(reference),'Every Sonya original cold input/state/boss/ending/guest/78RGB event byte-exact')
    pin(reference)
    proofpath=ROOT/'audit_v4743_actual_cpu_cycle_raster_boundary_checked/report.json'
    proof=json.loads(proofpath.read_text());pin(proofpath)
    need(proof['passed']and proof['actualFieldsMetadataAccepted']==14 and proof['actualIOStores']==42 and
         len(proof['actualTimingFaultsRejected'])==2 and not proof['nativeWholeEndingPixelsAccepted']and
         not proof['pixelToleranceAdded']and not proof['dummyVRAMUsed'],
         'Actual source-defined cycle boundary metadata only; full native pixel proof still required')
    for p,h in proof['inputHashes'].items():pin(p,h)
    import run_kintaro_pressure_guard_long_campaign_v4439 as guest_provider
    guest=guest_provider.expected();stockpath=ROOT/'mk2/mk2-maincpu.bin'
    prefix=diagnostic.make_ledger()(proof['actualClosedMetadataPrefix'],(13,17))
    callers=ledger.original_io_callers(prefix['io'],guest,stockpath.read_bytes())
    pin(stockpath);pin(guest_provider.__file__)
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_raster_io_blackpen_campaign_ram_v4731.py|audit_v4733_|run_ending_raster_clock_campaign_ram_v4712.py|audit_v4713_sonya_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact authoritative native/collector command census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any(str(old)in row['CommandLine']or '4712.py --fighter sonya'in row['CommandLine']for row in live),
         'Previous Sonya really terminal, not stopped or restarted for timeout')
    cases=[]
    for fighter,session in(('kano',37407),('sonya',3663)):
        folder=ROOT/f'audit_v4733_{fighter}_p2_ending_raster_io_ram'
        result=ROOT/f'audit_v4734_{fighter}_p2_ending_raster_io_checked/report.json'
        process=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        entry=dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,
          execSession=session,nativePID=process['pid'],capture=str(folder),report=str(result),nativeVideoAccepted=False,
          nativeLiveNow=any(row['ProcessId']==process['pid']and str(folder)in row['CommandLine']for row in live),
          collectorLiveNow=any(row['Name']=='python.exe'and '4731.py'in row['CommandLine']and f'--fighter {fighter}'in row['CommandLine']for row in live))
        if result.exists():
            actual=json.loads(result.read_text());pin(result);entry['actualTerminalReportPassed']=actual['passed']
            if actual['passed']:
                for p,h in actual['inputHashes'].items():pin(p,h)
            else:entry['error']=actual['error'][:500]
        else:need(entry['nativeLiveNow']and entry['collectorLiveNow'],'Pending only after exact current process/command confirmation')
        cases.append(entry)
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with4557 and all additive journals. Every original scope group, prior finite native proof, input hash and open exclusion persists. This records Sonya old terminal and the actual first new CPU-beam boundary counterexample without discarding the complete ending window.',
      remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousAcknowledgementWasNotWorkProgress=True,
      thisGoalTurnClassification='progress: revalidated exact live handles, consumed original Sonya4712 native terminal0 with all3043ending/attract fields and independently retained every original cold input/state/guest/78RGB event. Started fresh Sonya4731 only after actual prior terminal. Fresh Kano reached real ending and exposed timing mismatch after13fields. Reproduced exact actual sequence475/VCOUNT83 counterexample, source-qualified scheduler floor-cycle CPU-local time versus timer-global time, implemented fresh complete4740 model with one source-defined160ns early CPU boundary; real14field metadata and two actual out-of-source faults checked. No dummy pixels or full-ending acceptance.',
      oldSonyaTerminal=dict(execSession=74307,execTerminalConsumed=True,nativeExit=0,observedRendererFields=3043,
        exactContinuousFields=0,originalColdInputsStatesGuestAnd78RGBUnchanged=True,fullVideoAccepted=False),
      freshKanoCounterexample=dict(actualEndingStart=56296,firstFailedField=56309,priorCompleteFields=13,
        actualClockSequence=475,actualCPUBeam=83,error=proof['reproducedOriginalTimingFailure'],
        actualEarlyTimestampSeconds=proof['actualBoundaryEarlySeconds'],sourceDefinedNativeCycleSeconds=proof['originalSourceDefinedCPUCycleSeconds'],
        immutableDiagnostic=str(proofpath),completeNativeRunAllowedToFinish=True),
      correctedTimingModel=dict(source=str(ROOT/'tools/ending_raster_cpu_cycle_model_v4740.py'),
        wholeOriginalOneBaseCPUShiftDMAVRAMGraphicsRegisterRGBPipelineRetained=True,
        actualMetadataPrefixFields=14,actualClocks=504,actualExplicitIOStores=42,actualTimingFaultsRejected=2,
        actualFirstPrefixOriginalIOCallerWindows=callers,metadataNeverSubstitutedForPixels=True,
        wholeNativePixelAcceptance=False,comparisonTargetsNeverReanchor=True,pixelToleranceAdded=False),
      completeLedgerVerifier=dict(source=str(ROOT/'tools/verify_ending_native_io_clock_ledger_v4737.py'),
        importedSuccessfully=True,wholeNativeMainNotExecuted=True,requiresSeparatePassedFullRAMVideo=True,
        mustUseFreshAdapterFor4740=True),
      pendingRuns=cases,liveJobsAuthoritativelyObservedNow=live,
      candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      nextAction='Poll exact37407 Kano4731 and3663 Sonya4731 first. Never restart for timeout. Consume real native terminals/failed reports naturally. Once each complete4733log is immutable, verify the whole actual clock/register ledger with fresh4740 metadata adapter and real IO/time/source faults before spending another full native campaign. If complete metadata passes, source-qualify a fresh full RAM renderer runner using4740 and unchanged4719/4728/4729 read-only observers and original physical controls; require every VRAM/RGB field and original two raw bit faults. Keep all original broader P1/endings/art/floor-shadow/audio/finisher/morph/arena/CPU/KO/selection/release groups open.',
      cleanupAccounting='No new builds/ROM copies/raw media or recovery archive. Only compressed text/source/digests; earlier32.49GiB reclamation is not recounted. Preserve immutable failed native evidence and current playable artifacts.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Entire original scope and all additive source/evidence bytes unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),oldSonyaNativeExit=0,
      actualCPUBeamCounterexampleSourceQualified=True,metadataFields=14,actualOriginalIOStores=42,
      pendingRuns=[case['fighter']for case in cases if case['nativeLiveNow']],nativeWholeEndingPixelsAccepted=False,
      newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
