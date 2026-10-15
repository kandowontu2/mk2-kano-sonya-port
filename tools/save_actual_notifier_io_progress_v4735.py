"""Additive whole-goal progress: actual notifier failure and generic IO replay."""
import json,subprocess
from pathlib import Path
import save_generic_raster_clock_progress_v4717 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4718_generic_raster_clock_progress/progress.json']
OUT=ROOT/'audit_v4736_actual_notifier_io_progress'

def main():
    need(not OUT.exists(),'Fresh immutable compact full-scope journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent full-scope source/native pin chain');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every inherited full-goal native/source/public byte unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);h=sha(path)
        need((wanted is None or h==wanted)and(key not in inherited or inherited[key]==h)and
             (key not in pins or pins[key]==h),'Exact unchanged additive evidence/source pin')
        if key not in inherited:pins[key]=h
    for p in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(p)
    prior=ROOT/'audit_v4713_kano_p2_ending_raster_clock_ram'
    failed_path=ROOT/'audit_v4714_kano_p2_ending_raster_clock_checked/report.json'
    failed=json.loads(failed_path.read_text());meta=json.loads((prior/'result.json').read_text());pin(failed_path)
    need(not failed['passed']and meta['exit_code']==0 and meta['observedEndingRGBFields']==3040 and
         meta['exactContinuousEndingFields']==0 and meta['actualNativeFrameCallbacks']==58 and
         len(meta['endingModelErrors'])==1 and 'frame=56296 'in meta['endingModelErrors'][0]['line']and
         'Actual field starts after prior273partial update, before next274latch'in meta['endingModelErrors'][0]['error'],
         'Actual full native terminal0 with all3040renderer fields, failed first source timing assumption, not video acceptance')
    for p,h in meta['input_hashes'].items():pin(p,h)
    for p in prior.rglob('*'):
        if p.is_file():pin(p)
    # Independently preserve every cold native event, even though model failed
    # before the normal whole-campaign equivalence gate could be executed.
    reference=ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log'
    prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_',
              'MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
    def selected(path):
        with path.open()as stream:
            return[l.rstrip()for l in stream if l.startswith(prefixes)and
              not l.startswith(('MK2_NAT_CAMPAIGN_FLOOR_','MK2_NAT_CAMPAIGN_SHADOW_',
                                'MK2_NAT_CAMPAIGN_ENDING_DISPLAY_'))]
    need(selected(prior/'run.log')==selected(reference),'Every original actual cold input/state/boss/ending/guest/58RGB event unchanged');pin(reference)
    preflight=ROOT/'audit_v4732_ending_raster_io_blackpen_source_checked/report.json'
    proof=json.loads(preflight.read_text());pin(preflight)
    phase=proof['actualNotifierPhaseControl']
    need(proof['passed']and proof['wholeOriginalNativeOneBasePipelineRetained']and
         phase['actualSourceBoundNotifierPhaseAccepted']and len(phase['actualNotifierMetadataFaultsRejected'])==8 and
         len(proof['observerSourceFaultsRejected'])==6 and not proof['explicitDisplayIOObservationsAccepted']and
         not proof['fullEndingRendererVideoAccepted']and not proof['fullPortAcceptance'],
         'Whole generic actual notifier/register source, real8notifier faults and6observer source faults; no native IO/pixel acceptance yet')
    for p,h in proof['inputHashes'].items():pin(p,h)
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_raster_clock_campaign_ram_v4712.py|audit_v4713_|run_ending_raster_io_blackpen_campaign_ram_v4731.py|audit_v4733_' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact authoritative process census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    need(not any(r['Name']=='python.exe'and '4712.py --fighter kano'in r['CommandLine']for r in live)and
         not any(r['Name']=='mkport_candidate.exe'and str(prior)in r['CommandLine']for r in live),
         'Prior failed Kano actual terminal, not restarted for an observation timeout')
    cases=[]
    for fighter,folder,session,result in(
      ('kano',ROOT/'audit_v4733_kano_p2_ending_raster_io_ram',37407,ROOT/'audit_v4734_kano_p2_ending_raster_io_checked/report.json'),
      ('sonya',ROOT/'audit_v4713_sonya_p2_ending_raster_clock_ram',74307,ROOT/'audit_v4714_sonya_p2_ending_raster_clock_checked/report.json')):
        process=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        entry=dict(fighter=fighter,physicalSlot=2,identity=17 if fighter=='kano'else 18,execSession=session,
          nativePID=process['pid'],capture=str(folder),report=str(result),nativeVideoAccepted=False,
          nativeLiveNow=any(r['ProcessId']==process['pid']and str(folder)in r['CommandLine']for r in live),
          collectorLiveNow=any(r['Name']=='python.exe'and f'--fighter {fighter}'in r['CommandLine']for r in live))
        if result.exists():
            terminal=json.loads(result.read_text());pin(result);entry['actualTerminalReportPassed']=terminal['passed']
            if terminal['passed']:
                for p,h in terminal['inputHashes'].items():pin(p,h)
                entry['wholeRAMVideoPassedPendingActualClockIOFaultQualification']=True
            else:entry['error']=terminal['error'][:700]
        else:need(entry['nativeLiveNow']and entry['collectorLiveNow'],'Pending only called live after exact current command verification')
        cases.append(entry)
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with the original4557 and all listed additive journals. All five original full-goal requirement groups, prior finite evidence, exclusions and input pins persist. This resolves prior live Kano4712 to its real failed terminal and adds actual notifier phase and fresh IO state-machine work.',
      remaining=base['remaining'],newInputHashes=pins,
      priorGenericKanoActualTerminal=dict(report=str(failed_path),execSession=92884,execTerminalConsumed=True,
        nativeExit=0,actualRendererFields=3040,wholeExactPixelFields=0,firstFailedFrame=56296,
        originalColdNativeInputsStatesGuestAnd58RGBUnchanged=True,wholeVideoAccepted=False,
        cause='Native screen VBLANK starts before ordinary notifier while CPUVCOUNT still273. time_until_pos(274) gives one full future field, not the imminent latch. Original CPU also changes display control/address during clear; those must be observed and replayed, not assumed absent.'),
      correctedGenericNativeRegisterModel=dict(observer=str(ROOT/'mk2ks_ending_raster_io_ram_v4719.lua'),
        model=str(ROOT/'tools/ending_raster_io_model_v4720.py'),sourceProof=str(preflight),
        wholeOriginalOneBaseCPUShiftDMAGraphicsPreFlipHeldVRAMPipelineRetained=True,
        originalPhysicalControllersExactlyUnchanged=True,actualNotifierMetadataQualified=True,
        actualNotifierMetadataFaultsRejected=8,actualObserverSourceFaultsRejected=6,
        genericExplicitIOAndAutomaticLatchDUDATEReplay=True,originalDisabledDisplayBlackPenSourceQualified=True,
        actualNativeExplicitIOObservationsAccepted=False,wholeNativePixelsAccepted=False,
        noSpecificFrameOrCharacterOrPixelException=True,noComparisonTargetReanchor=True),
      firstIOPreflightLiteralFailurePreserved=dict(source=str(ROOT/'tools/qualify_ending_raster_io_source_v4721.py'),
        error='Wrong expected C++ type literal uint16_t; actual original declaration is pen_t. Fresh4730 preserves whole preflight with exact actual type. No native launch or acceptance resulted from the failed source check.'),
      pendingRuns=cases,liveJobsAuthoritativelyObservedNow=live,
      candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,newlyDeletedFiles=0,
      newlyReclaimedAllocatedBytes=0,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      thisGoalTurnClassification='progress: consumed actual full3040field Kano terminal0 exposing generic notifier assumption at first field; independently verified whole original cold stream unchanged. Actual source-order phase qualified against real first-field metadata with8real faults. Implemented full generic CPU IO/native latch/DUDATE/indexed row state machine and source-qualified permanent black-pen semantics; fresh Kano whole run dispatched only after actual prior terminal failure. Original Sonya observed same real first-field timing counterexample and remains live through its natural endpoint.',
      nextAction='Poll exact37407 fresh Kano4731/4733 and74307 original Sonya4712/4713 first, using current exact commands. Never restart for timeout or edit frozen sources. Consume actual terminals. After Sonya old run is actually terminal, preserve its real failed result/metadata and dispatch fresh4731 --fighter sonya using same old physical controls. From successful fresh native full VRAM/RGB results, source-qualify real display-register store PCs/data/masks/before values, all actual clocks/scanout agreement, original VRAM/RGB bit faults and real IO/timing row faults using RAM as required. Do not use4715 unchanged: it expects old predicted-latch timing and excludes new explicitIO. All original broader P1/endings/art/audio/finisher/morph/arena/CPU/KO/selection/release scope remains open.',
      cleanupAccounting='Only compressed source/text/digest/additive journal. New raw guest/VRAM/RGB/PCM RAM-only. Failed native text evidence is retained compressed, no new playable build/copy/archive or historical reclaim recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Original scope and every new source/evidence pin unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),oldKanoNativeExit=0,
      oldKanoObservedVideoFields=3040,sourceQualifiedNotifierPhase=True,
      pendingNativeRuns=[c['fighter']for c in cases if c['nativeLiveNow']],wholeNativeVideoAccepted=False,
      newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
