"""Additive full-goal journal: complete native timing ledger, fresh RAM video."""
import json,subprocess
from pathlib import Path
import save_actual_cpu_cycle_raster_progress_v4744 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4745_actual_cpu_cycle_raster_progress/progress.json']
OUT=ROOT/'audit_v4756_complete_ending_clock_progress'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent original full-goal pin chain');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'All original source/native/playable evidence bytes unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or wanted==actual)and(key not in inherited or inherited[key]==actual)and
             (key not in pins or pins[key]==actual),'Exact immutable additive source/evidence byte')
        if key not in inherited:pins[key]=actual
    for p in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(p)
    old=ROOT/'audit_v4733_kano_p2_ending_raster_io_ram'
    failed=ROOT/'audit_v4734_kano_p2_ending_raster_io_checked/report.json'
    error=json.loads(failed.read_text());meta=json.loads((old/'result.json').read_text())
    need(not error['passed']and meta['exit_code']==0 and meta['observedEndingRGBFields']==3040 and
         meta['exactContinuousEndingFields']==13 and meta['actualNativeFrameCallbacks']==58 and
         len(meta['endingModelErrors'])==1 and len(meta['endingNativePipelineFaults'])==2 and
         'frame=56309 'in meta['endingModelErrors'][0]['line']and
         'Actual CPU beam follows source-scheduled native scanline'in meta['endingModelErrors'][0]['error'],
         'Actual Kano terminal0, all3040observed fields,13exact whole VRAM/RGB fields, both real bit faults; failed timing gate retained')
    pin(failed)
    for p,h in meta['input_hashes'].items():pin(p,h)
    for p in old.rglob('*'):
        if p.is_file():pin(p)
    reference=ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log'
    prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_',
              'MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
    def selected(path):
        with path.open()as stream:
            return[l.rstrip()for l in stream if l.startswith(prefixes)and not l.startswith(
              ('MK2_NAT_CAMPAIGN_FLOOR_','MK2_NAT_CAMPAIGN_SHADOW_','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_'))]
    need(selected(old/'run.log')==selected(reference),'All original actual cold controls/states/boss/ending/guest/58RGB unchanged')
    pin(reference)
    failedledger=ROOT/'audit_v4747_kano_complete_cpu_cycle_ending_ledger_checked/report.json'
    original_failure=json.loads(failedledger.read_text());pin(failedledger)
    need(not original_failure['passed']and 'All actual native ending/attract fields complete and consecutive'in original_failure['error'],
         'Actual unrendered-next-notifier terminal-seed checker failure preserved')
    ledgerpath=ROOT/'audit_v4749_kano_complete_cpu_cycle_ending_terminal_ledger_checked/report.json'
    ledger=json.loads(ledgerpath.read_text());pin(ledgerpath)
    need(ledger['passed']and ledger['completeActualMetadataFields']==3040 and ledger['actualNativeClockRecords']==139566 and
         ledger['completedRendererClockRecords']==139565 and ledger['actualNativeDisplayIOStores']==4407 and
         ledger['actualAttractFields']==300 and len(ledger['actualMetadataFaultsRejected'])==27 and
         len(ledger['actualTerminalFaultsRejected'])==8 and ledger['metadataNeverSubstitutedForPixels']and
         not ledger['fullEndingVRAMRGBPixelsAccepted']and not ledger['dummyVRAMUsed'],
         'Complete actual native clock/IO/instruction/shutdown ledger and35real metadata faults, not pixel acceptance')
    for p,h in ledger['inputHashes'].items():pin(p,h)
    preflight=ROOT/'audit_v4751_ending_cpu_cycle_source_checked/report.json'
    proof=json.loads(preflight.read_text());pin(preflight)
    need(proof['passed']and proof['wholeOriginalNativeOneBasePipelineRetained']and
         proof['actualSourceDefinedCPUClockBoundaryQualified']and proof['wholeKanoMetadataLedgerAccepted']and
         proof['originalNativeIOStoreInstructionSemanticsQualified']and proof['all27MetadataAnd8TerminalFaultsRetained']and
         not proof['fullEndingRendererVideoAccepted']and not proof['fullPortAcceptance'],
         'Original complete source/controls/transport with qualified timing/opcode semantics, no native pixel substitution')
    for p,h in proof['inputHashes'].items():pin(p,h)
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_cpu_cycle_campaign_ram_v4752.py|audit_v4753_|run_ending_raster_io_blackpen_campaign_ram_v4731.py|audit_v4733_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh actual native/collector process commands')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any(str(old)in row['CommandLine']or '4731.py --fighter kano'in row['CommandLine']for row in live),
         'Prior Kano truly terminal, not restarted for timeout')
    cases=[]
    for fighter,folder,session,result,runner in(
      ('kano',ROOT/'audit_v4753_kano_p2_ending_cpu_cycle_ram',22694,ROOT/'audit_v4754_kano_p2_ending_cpu_cycle_checked/report.json','4752.py'),
      ('sonya',ROOT/'audit_v4733_sonya_p2_ending_raster_io_ram',3663,ROOT/'audit_v4734_sonya_p2_ending_raster_io_checked/report.json','4731.py')):
        process=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        entry=dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,execSession=session,
          nativePID=process['pid'],capture=str(folder),report=str(result),nativeFullVideoAccepted=False,
          nativeLiveNow=any(row['ProcessId']==process['pid']and str(folder)in row['CommandLine']for row in live),
          collectorLiveNow=any(row['Name']=='python.exe'and runner in row['CommandLine']and f'--fighter {fighter}'in row['CommandLine']for row in live))
        if result.exists():
            actual=json.loads(result.read_text());pin(result);entry['actualTerminalReportPassed']=actual['passed']
            if actual['passed']:
                for p,h in actual['inputHashes'].items():pin(p,h)
            else:entry['error']=actual['error'][:500]
        else:need(entry['nativeLiveNow']and entry['collectorLiveNow'],'Pending only after exact authoritative process/command check')
        cases.append(entry)
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read with4557 and every additive journal. All five original full-goal groups, native finite evidence, input hashes, exclusions and current playable artifacts remain. This consumes actual Kano4731 terminal and verifies the entire CPU-clock/IO ledger before a fresh full RAM pixel run.',
      remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousGoalTurnClassification='progress: actual Sonya old terminal and source-defined actual CPU clock counterexample diagnosed;14metadata fields and real boundary faults qualified; full source model corrected without image tolerance.',
      thisGoalTurnClassification='progress: consumed actual Kano4731 native terminal0/all3040observed fields/13exact full RAM fields/2rawbit faults; independently verified every original cold state/guest/58RGB event. Entire4740hardware ledger accepted all3040fields with139566actualclocks,4407originalIOstores and846223operations. Original absolute register-store opcode/destination/register windows qualified;27first-field metadata faults and8actual shutdown-boundary faults rejected. Preserved failed4747terminal-seed assumption; source-qualified original next-notifier unrendered final seed without omitting a completed field. Passed whole4751source preflight and launched fresh4752Kano full raw-RAM replay only after actual prior terminal+complete ledger.',
      priorKanoTerminal=dict(execSession=37407,execTerminalConsumed=True,nativeExit=0,observedFields=3040,
        wholeExactVRAMRGBFields=13,actualNativePixelBitFaultsRejected=2,originalColdControlsStatesGuestAnd58RGBUnchanged=True,
        completeVideoAccepted=False,failedFrame=56309),
      completeActualKanoHardwareLedger=dict(report=str(ledgerpath),fields=3040,attractFields=300,
        actualClocks=139566,completedRendererClocks=139565,actualIOStores=4407,originalTimedOperations=846223,
        sourceQualifiedOriginalStoreCallers=ledger['sourceQualifiedOriginalIOInstructions'],
        actualMetadataFaultsRejected=27,actualTerminalFaultsRejected=8,unrenderedTerminalSeeds=1,
        sourceDefinedCPUCycleSeconds=1.6e-7,metadataNeverReplacesPixels=True,completePixelAcceptance=False),
      wholeNativeRAMSourcePreflight=dict(report=str(preflight),passed=True,
        wholeOriginalOneBaseCPUShiftDMAGraphicsVRAMRGBRetained=True,originalPhysicalControllersUnchanged=True,
        actualNativeStoreOpcodeSemanticsQualified=True,noSpecificCharacterFrameOrPixelException=True,
        pixelToleranceAdded=False,noComparisonTargetReanchor=True),
      pendingRuns=cases,liveJobsAuthoritativelyObservedNow=live,candidateAndPublicBuildChanged=False,
      newBuilds=0,rawMediaFilesWritten=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      nextAction='Poll exact22694 freshKano4752/4753 and3663 Sonya4731/4733 first. Consume actual terminal reports, never restart on observation timeout. Sonya already reached actual84378ending and failed the old4720timestamp gate; allow all ending+300attract naturally, then run fresh4748 --fighter sonya into unused4749S to verify complete ledger, original instructions and35actual faults. Only after actual Sonya terminal+passed ledger, launch4752 --fighter sonya into unused4753/4754S. From passed new full RAM video, require complete new capture metadata/terminal/caller proof, original cold equivalence and all four ending pages plus every VRAM/RGB field and both raw bit faults; do not use4737 unchanged because it excludes final unrendered seed and old timestamp model. Entire broader P1/endings/stock choreography/art/floor shadows/audio/allfinisher/morph/arena/CPU/repeated/KO/selection/release scope remains.',
      cleanupAccounting='Only compressed source/text/digests. New raw guest/VRAM/RGB/PCM are RAM-only; no playable/ROM copy, build, recovery archive or deletion. Prior32.49GiB cleanup is not recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Entire original scope and every additive evidence/source byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),priorKanoNativeExit=0,
      completeActualKanoMetadataFields=3040,actualOriginalIOStores=4407,metadataFaults=35,
      freshWholeRAMSourcePassed=True,pendingRuns=[c['fighter']for c in cases if c['nativeLiveNow']],
      newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
