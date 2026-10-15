"""Whole-goal additive progress: both real clock ledgers, live RAM video."""
import ast,json,subprocess
from pathlib import Path
import save_complete_ending_clock_progress_v4755 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4756_complete_ending_clock_progress/progress.json']
OUT=ROOT/'audit_v4760_both_ending_clock_progress'

def main():
    need(not OUT.exists(),'Fresh immutable whole-goal journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent original full-goal source/evidence chain');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited native/source/playable artifact byte unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or wanted==actual)and(key not in inherited or inherited[key]==actual)and
             (key not in pins or pins[key]==actual),'Exact immutable additive evidence/source byte')
        if key not in inherited:pins[key]=actual
    for path in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(path)
    old=ROOT/'audit_v4733_sonya_p2_ending_raster_io_ram'
    failed=ROOT/'audit_v4734_sonya_p2_ending_raster_io_checked/report.json'
    failure=json.loads(failed.read_text());meta=json.loads((old/'result.json').read_text());pin(failed)
    need(not failure['passed']and meta['exit_code']==0 and meta['observedEndingRGBFields']==3043 and
         meta['exactContinuousEndingFields']==8 and meta['actualNativeFrameCallbacks']==78 and
         len(meta['endingModelErrors'])==1 and len(meta['endingNativePipelineFaults'])==2 and
         'frame=84386 'in meta['endingModelErrors'][0]['line']and
         'Actual CPU beam follows source-scheduled native scanline'in meta['endingModelErrors'][0]['error'],
         'Actual Sonya terminal0/all3043observed fields/8exact raw fields/2real bit faults; timing failure preserved')
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
    need(selected(old/'run.log')==selected(reference),'All original Sonya physical controls/states/boss/ending/guest/78RGB byte-exact')
    pin(reference)
    ledgers=[]
    for fighter,fields,clocks,operations,stores in(('kano',3040,139566,846223,4407),('sonya',3043,141631,853304,4410)):
        p=ROOT/f'audit_v4749_{fighter}_complete_cpu_cycle_ending_terminal_ledger_checked/report.json'
        proof=json.loads(p.read_text());pin(p)
        need(proof['passed']and proof['completeActualMetadataFields']==fields and
             proof['actualNativeClockRecords']==clocks and proof['completedRendererClockRecords']==clocks-1 and
             proof['actualOriginalTimedOperations']==operations and proof['actualNativeDisplayIOStores']==stores and
             proof['actualAttractFields']==300 and len(proof['actualMetadataFaultsRejected'])==27 and
             len(proof['actualTerminalFaultsRejected'])==8 and proof['metadataNeverSubstitutedForPixels']and
             not proof['fullEndingVRAMRGBPixelsAccepted']and not proof['fullPortAcceptance'],
             'Both complete actual source/instruction/IO/clock/shutdown ledgers and real35faults; no metadata pixel substitute')
        for path,h in proof['inputHashes'].items():pin(path,h)
        ledgers.append(dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,report=str(p),
          fields=fields,clocks=clocks,originalOperations=operations,originalIOStores=stores,
          originalStoreCallers=proof['sourceQualifiedOriginalIOInstructions'],attractFields=300,actualMetadataFaults=35,
          fullNativePixelAcceptance=False))
    bridge=ROOT/'tools/verify_complete_native_ending_pixels_hardware_v4757.py';text=bridge.read_text();ast.parse(text);pin(bridge)
    for token in("need(failed['passed']and meta['exit_code']==0", "failed['oneInitialBaseOnly']",
                  "failed['comparisonTargetsNeverReanchor']", "len(failed['actualNativePixelFaultsRejected'])==2",
                  "failed['originalQualifiedEarlyLatePagesPresent']", "failed['actualRasterClocks']==positive['clocks']-1",
                  "r['exactVRAMWords']==262144 and r['exactRGBPixels']==101600"):
        need(token in text,'Prepared full pixel/hardware bridge retains mandatory actual whole proof '+token)
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_cpu_cycle_campaign_ram_v4752.py|audit_v4753_|run_ending_raster_io_blackpen_campaign_ram_v4731.py|audit_v4733_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh authoritative native/collector command census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any('4731.py --fighter sonya'in row['CommandLine']or str(old)in row['CommandLine']for row in live),
         'Original Sonya actually terminal before fresh dispatch, never restart on timeout')
    cases=[]
    for fighter,session in(('kano',22694),('sonya',53444)):
        folder=ROOT/f'audit_v4753_{fighter}_p2_ending_cpu_cycle_ram'
        result=ROOT/f'audit_v4754_{fighter}_p2_ending_cpu_cycle_checked/report.json'
        process=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        entry=dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,execSession=session,
          nativePID=process['pid'],capture=str(folder),report=str(result),nativeFullVideoAccepted=False,
          nativeLiveNow=any(row['ProcessId']==process['pid']and str(folder)in row['CommandLine']for row in live),
          collectorLiveNow=any(row['Name']=='python.exe'and '4752.py'in row['CommandLine']and f'--fighter {fighter}'in row['CommandLine']for row in live))
        if result.exists():
            actual=json.loads(result.read_text());pin(result);entry['actualTerminalReportPassed']=actual['passed']
            if actual['passed']:
                for p,h in actual['inputHashes'].items():pin(p,h)
                entry['wholeRAMVideoPassedPendingIndependentCompleteLedger']=True
            else:entry['error']=actual['error'][:500]
        else:need(entry['nativeLiveNow']and entry['collectorLiveNow'],'Pending only after exact current process/command confirmation')
        cases.append(entry)
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read with4557 and all additive journals. Every original scope group, finite native evidence, input hash, exclusion and public playable artifact persists. This consumes Sonya4731 terminal and verifies her complete hardware ledger before fresh full RAM video.',
      remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousGoalTurnClassification='progress: complete Kano3040field clock/IO/shutdown ledger,35actual metadata faults, native opcode semantics and whole source4751 preflight qualified; fresh4752Kano dispatched only after actual terminal and metadata proof.',
      thisGoalTurnClassification='progress: consumed actual Sonya4731 native terminal0 with all3043ending/attract fields,8exact full native RAM fields and both rawbit faults. Independently verified every cold physical input/state/boss/ending/guest/78RGB event. Same generic4740 model and4748 ledger passed all3043Sonya fields,141631clocks,4410originalIOstores,853304operations and35real metadata/shutdown faults. Fresh4752Sonya dispatched only after real prior terminal+complete ledger; both fresh full RAM runs confirmed live. Prepared4757full raw-pixel/hardware bridge preserving all original mandatory raw/cold/page/source/bit-fault/clock/terminal gates; parsed only, no invented whole pixel acceptance.',
      priorSonyaTerminal=dict(execSession=3663,execTerminalConsumed=True,nativeExit=0,observedRendererFields=3043,
        exactWholeVRAMRGBFields=8,actualRawBitFaultsRejected=2,failedFrame=84386,
        allOriginalColdControlsStatesGuestAnd78RGBUnchanged=True,completeNativeVideoAccepted=False),
      completeActualP2HardwareLedgers=ledgers,bothNativeMetadataLedgersAccepted=True,
      combinedMetadataFields=6083,combinedNativeClocks=281197,combinedOriginalIOStores=8817,
      fullNativeEndingVideoFromMetadataNeverInferred=True,
      preparedWholePixelHardwareBridge=dict(source=str(bridge),onlyASTAndRequiredGateChecksExecuted=True,
        futurePassedNativePixelReportRequired=True,wholeVRAMRGBAndRawBitFaultsRequired=True,
        perFieldRendererClockAndIOAgreementRequired=True,allOriginal35MetadataFaultsRequired=True,
        nativeWholePositiveExecuted=False),
      pendingRuns=cases,liveJobsAuthoritativelyObservedNow=live,candidateAndPublicBuildChanged=False,
      newBuilds=0,rawMediaFilesWritten=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      nextAction='Poll exact22694Kano and53444Sonya4752 first, never restart for timeout. Both complete old kernel ledgers are accepted with35actual faults each; no need repeat those runs. Fresh Kano has reached real56296ending and live collector reported at least300complete exact wholeRAM fields, not terminal acceptance. Require real complete4754reports: all3040K/all3043S whole VRAM/RGB fields, original cold states, all four qualified pages, both actual rawbit faults and complete natural ending+300attract. If4754passes, execute4757 --fighter into fresh4758 for independent new full clock/IO/instruction/shutdown ledger and complete per-field pixel bridge. If actual native counterexample arises, preserve capture/model, diagnose recorded source cause into fresh sources/leaves; no target reanchor/image tolerance/game-state writes. All broader original P1/endings/stock choreography/art/floor shadows/audio/finisher/morph/arena/CPU/repeated/KO/selection/release groups remain.',
      cleanupAccounting='Compressed source/text/digest/journal only. New raw guest/VRAM/RGB/PCM remains RAM-only; no new playable/ROM copies, build, archive or deletion. Prior32.49GiB reclamation is not recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Original full goal scope and all new source/evidence bytes unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),priorSonyaNativeExit=0,
      bothCompleteActualP2MetadataFields=6083,nativeOriginalIOStores=8817,actualMetadataFaults=70,
      freshWholeRAMRuns=[c['fighter']for c in cases if c['nativeLiveNow']],fullNativeVideoAccepted=False,
      newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
