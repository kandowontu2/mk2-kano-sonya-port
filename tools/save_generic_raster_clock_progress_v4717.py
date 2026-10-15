"""Additive full-goal journal: generic temporal model and live native endings."""
import json,subprocess
from pathlib import Path
import save_raster_cause_native_voice_progress_v4704 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4705_raster_cause_native_voice_progress/progress.json']
OUT=ROOT/'audit_v4718_generic_raster_clock_progress'

def main():
    need(not OUT.exists(),'Fresh immutable compact full-goal journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent entire source/native/full-scope chain');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited native/source/public playable logical byte unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted)and(key not in inherited or inherited[key]==actual)and
             (key not in pins or pins[key]==actual),'Exact unchanged new/inherited pin')
        if key not in inherited:pins[key]=actual
    for p in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(p)
    preflight=ROOT/'audit_v4711_ending_raster_clock_source_checked/report.json'
    proof=json.loads(preflight.read_text());pin(preflight)
    need(proof['passed']and proof['wholeOriginalNativePipelineRetained']and
         len(proof['observerSourceFaultsRejected'])==7 and not proof['nativeClockObservationsAccepted']and
         not proof['fullEndingRendererVideoAccepted']and not proof['fullPortAcceptance'],
         'Whole generic clock model/observer/original source gates passed, never native pixel acceptance from source checks')
    for p,h in proof['inputHashes'].items():pin(p,h)
    pin(ROOT/'tools/verify_actual_ending_raster_clock_ledger_v4715.py')
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_raster_clock_campaign_ram_v4712.py|audit_v4713_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact authoritative native-process census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    cases=[]
    for fighter,session in(('kano',92884),('sonya',74307)):
        folder=ROOT/f'audit_v4713_{fighter}_p2_ending_raster_clock_ram'
        result=ROOT/f'audit_v4714_{fighter}_p2_ending_raster_clock_checked/report.json'
        proc=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        native=[r for r in live if r['ProcessId']==proc['pid']and r['Name']=='mkport_candidate.exe'and str(folder)in r['CommandLine']]
        python=[r for r in live if r['Name']=='python.exe'and f'--fighter {fighter}'in r['CommandLine']]
        entry=dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,execSession=session,
                   nativePID=proc['pid'],nativeLiveNow=bool(native),collectorLiveNow=bool(python),
                   capture=str(folder),report=str(result),nativeVideoAccepted=False,clockMetadataFaultQualificationPending=True)
        if result.exists():
            terminal=json.loads(result.read_text());pin(result);entry['terminalReportPassed']=terminal['passed']
            if terminal['passed']:
                for p,h in terminal['inputHashes'].items():pin(p,h)
                entry['wholeRAMRendererPassObserved']=True
                entry['actualFields']=terminal['exactConsecutiveNativeVideoFields']
                entry['nativeVideoAccepted']=False # Still require independent actual metadata fault ledger.
            else:entry['error']=terminal['error']
        else:
            need(native and python,'Pending renderer only called live after exact current process/command verification')
        cases.append(entry)
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with4557 and every listed additive journal. All original requirements, finite results, exclusions and pins persist. Generic timing implementation and actual live runs replace the former unexecuted generic-scanline plan only.',
      remaining=base['remaining'],newInputHashes=pins,
      genericRasterImplementation=dict(observer=str(ROOT/'mk2ks_ending_raster_clock_ram_v4706.lua'),
        model=str(ROOT/'tools/ending_raster_clock_model_v4709.py'),sourceProof=str(preflight),
        wholeOriginalOneBaseCPUShiftDMAGraphicsPreFlipHeldVRAMPipelineRetained=True,
        actualNotifierAndPreOperationAndFinishClocks=True,actualNativeVblankDeadlineAndScanPeriods=True,
        nativeScreenFrameDeduplicationDistinguishesEqualBeamInNextCycle=True,
        eachIndexedRowSampledBeforeLaterNativeWrites=True,currentPaletteConversionMatchesScreenPixelsSource=True,
        noSpecificFrameOrCharacterOrPixelFallback=True,noComparisonTargetReanchor=True,
        sourceQualified=True,nativeWholeVideoQualified=False),
      pendingNativeCompleteEndingRuns=cases,liveJobsAuthoritativelyObservedNow=live,
      nextActualClockQualifier=dict(source=str(ROOT/'tools/verify_actual_ending_raster_clock_ledger_v4715.py'),
        ASTAndModuleImportPassed=True,executedOnNativeCapture=False,pixelPositivesFabricated=False,
        requiresActualTerminalWholePixelReport=True,qualifiesSeparateRealClockScanoutAgreementAnd24ActualRowFaults=True),
      candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,newlyDeletedFiles=0,
      newlyReclaimedAllocatedBytes=0,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      thisGoalTurnClassification='progress: implemented generic source-timed indexed scanline reconstruction retaining the entire one-base integer native pipeline and original physical controllers. Actual source preflight passed with7observer faults. Both native whole ending/attract campaigns dispatched into fresh compressed leaves and confirmed live by exact commands. No specific58183/image/identity fallback, game patch, raw media or new build.',
      nextAction='Poll exact92884(Kano) and74307(Sonya) handles and fresh exact4712/4713 process commands before any action. Never restart on observation timeout or edit frozen capture sources. Once each is actually terminal, consume its real result. If whole pixels/VRAM pass, execute4715 against that real capture for independent complete clock/scanout agreement and real24row faults; retain original actual VRAM/RGB bit faults. If actual failure occurs, preserve it and diagnose the real source/timing counterexample into fresh sources and leaves. Full P1/broader ending/art/cinematic/audio and all other original five remaining groups stay open, including final integrated selection/ladder/names/audio regression and dependency-aware final cleanup/release.',
      cleanupAccounting='All new source and text/digests compressed; raw guest/VRAM/RGB/PCM remain in RAM. Live log bytes are not reported as completed reclaim or immutable pins. No new playable copies, old-build restoration, deletion or historical reclaim recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'All full-scope requirements and new logical-byte pins unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),
       liveNativeContexts=[c['fighter']for c in cases if c['nativeLiveNow']],genericTimingSourceQualified=True,
       wholeNativeVideoQualified=False,newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
