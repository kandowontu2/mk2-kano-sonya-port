"""Compact additive whole-goal progress; exact live jobs, never timeout terminal.

Preserve all original scope/pins/exclusions. Add independently hardware-bound
ending source qualification and actual stock renderer outcome or live handle.
No raw files, build/public changes, deletion, or historical reclaim recount.
"""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint/checkpoint.json'
PARENTS=[ROOT/'audit_v4591_render_failure_scene_progress/progress.json',
         ROOT/'audit_v4611_secondary_render_latch_probe_progress/progress.json',
         ROOT/'audit_v4619_latch_cause_four_renderer_progress/progress.json']
OUT=ROOT/'audit_v4636_ending_hardware_stock_renderer_progress'

def sha(path):
    with Path(path).open('rb')as stream:return hashlib.file_digest(stream,'sha256').hexdigest().upper()

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    need(not OUT.exists(),'Fresh immutable compact whole-scope additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for p in PARENTS:
        for path,h in json.loads(p.read_text())['newInputHashes'].items():
            need(path not in inherited or inherited[path]==h,'No inherited proof graph conflict')
            inherited[path]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Every original full-goal scope/source/capture/public input unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or wanted==actual)and(key not in inherited or inherited[key]==actual),'Consistent original/current exact byte pin')
        if key not in inherited:pins[key]=actual
    for p in [BASE,*PARENTS,Path(__file__).resolve()]:pin(p)
    preflight_path=ROOT/'audit_v4624_ending_display_latch_source_checked/report.json'
    preflight=json.loads(preflight_path.read_text());pin(preflight_path)
    need(preflight['passed']and len(preflight['contexts'])==2 and len(preflight['actualObserverSourceFaultsRejected'])==7 and
         preflight['hardwareBindingControl']['actualFields']==41 and len(preflight['hardwareBindingControl']['actualHardwareFaultsRejected'])==4 and
         preflight['generatedCollectorStderrAndModelErrorLocalsAreDistinct']and not preflight['nativeEndingVideoAcceptance'],
         'Whole source/control/actual hardware/transport qualification, never full native video from preflight')
    for p,h in preflight['inputHashes'].items():pin(p,h)
    for name in ('verify_stock_scorpion_secondary_renderer_v4625.py','verify_stock_scorpion_secondary_renderer_v4629.py',
                 'verify_stock_scorpion_secondary_renderer_v4631.py','verify_stock_scorpion_secondary_renderer_v4633.py',
                 'verify_stock_scorpion_secondary_renderer_v4637.py'):
        pin(ROOT/'tools'/name)
    failures=[]
    for leaf in ('audit_v4626_stock_kitana_scorpion_secondary_renderer_checked',
                 'audit_v4630_stock_kitana_scorpion_secondary_renderer_checked',
                 'audit_v4632_stock_kitana_scorpion_secondary_renderer_checked',
                 'audit_v4634_stock_kitana_scorpion_secondary_renderer_checked'):
        path=ROOT/leaf/'report.json';r=json.loads(path.read_text());pin(path)
        need(not r['passed'],'Frozen failed stock harness assumptions never credited as game success')
        failures.append(dict(report=str(path),error=r['error']))
    census_command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_ending_display_latch_campaign_ram_v4617.py|audit_v4622_kano_p2_ending_display_latch_ram|verify_stock_scorpion_secondary_renderer_v4637.py' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',census_command],capture_output=True,text=True)
    need(census.returncode==0,'Authoritative current exact process census, no timeout assumption')
    live=json.loads(census.stdout)if census.stdout.strip()else []
    if isinstance(live,dict):live=[live]
    stock_live=any('verify_stock_scorpion_secondary_renderer_v4637.py'in r['CommandLine']for r in live)
    ending_live=any('run_ending_display_latch_campaign_ram_v4617.py'in r['CommandLine']or
                    'audit_v4622_kano_p2_ending_display_latch_ram'in r['CommandLine']for r in live)
    stock_path=ROOT/'audit_v4638_stock_kitana_scorpion_secondary_renderer_checked/report.json'
    stock=dict(report=str(stock_path),liveNow=stock_live,execSession=61030,completeNativeRendererWindowAccepted=False)
    if not stock_live and stock_path.exists():
        proof=json.loads(stock_path.read_text());pin(stock_path)
        stock.update(terminalReportPresent=True,passed=proof['passed'])
        if proof['passed']:
            need(proof['completeNativeRendererWindowAccepted']and proof['exactConsecutiveNativeRendererFields']==557 and
                 proof['originalFinalDuplicateRowRegisterPhaseSourceProven']and proof['originalCommandPostSkipRegisterSourceProven']and
                 proof['allStockSolidDMAOperationsExplicitlyAccounted']and len(proof['actualPipelineAndStockShadowFaultsRejected'])==13 and
                 not proof['completeCurrentVsStockRendererMatrixAccepted']and not proof['fullPortAcceptance'],
                 'Entire real stock window, original row/font register semantics, actual faults and full matrix exclusions retained')
            for p,h in proof['inputHashes'].items():pin(p,h)
            stock.update(completeNativeRendererWindowAccepted=True,exactFields=557,originalStockShadowRows=proof['originalStockShadowRowDMAs'],
                         originalSolidFontDraws=proof['actualOriginalFontSolidDMAs'])
        else:stock['error']=proof['error']
    ending_path=ROOT/'audit_v4623_kano_p2_ending_display_latch_checked/report.json'
    ending=dict(report=str(ending_path),capture=str(ROOT/'audit_v4622_kano_p2_ending_display_latch_ram'),liveNow=ending_live,
                execSession=93988,completeNativeRendererWindowAccepted=False)
    if not ending_live and ending_path.exists():
        proof=json.loads(ending_path.read_text());pin(ending_path)
        ending.update(terminalReportPresent=True,passed=proof['passed'])
        if proof['passed']:
            need(proof['completeCurrentP2EndingAttractNativeRendererVideoAccepted']and proof['everyVisibleStartDerivedFromActualHardware']and
                 not proof['fullPortAcceptance'],'Whole real ending video and original broad exclusions')
            for p,h in proof['inputHashes'].items():pin(p,h)
            ending.update(completeNativeRendererWindowAccepted=True,exactFields=proof['exactConsecutiveNativeVideoFields'])
        else:ending['error']=proof['error']
    capture=ROOT/'audit_v4622_kano_p2_ending_display_latch_ram'
    if (capture/'input_hashes_before.json').exists():
        pin(capture/'input_hashes_before.json')
        for p,h in json.loads((capture/'input_hashes_before.json').read_text()).items():pin(p,h)
        pin(capture/'process.json')
    result=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read together with4557/4591/4611/4619. All original five groups/pins/requirements/exclusions persist; only current job and scoped source/stock status changes.',
      remaining=base['remaining'],newInputHashes=pins,endingHardwareSourceQualification=str(preflight_path),
      actualNativeHardwareBindingFaults=4,actualObserverSourceFaults=7,
      wholeEndingVideo=ending,stockKitanaRenderer=stock,frozenFailedStockAssumptions=failures,
      liveJobsAuthoritativelyObservedNow=live,liveExecSessions=[r for r,on in [(93988,ending_live),(61030,stock_live)]if on],
      nextAction='Poll the exact existing ending93988 and stock61030 sessions/processes first; never restart for elapsed observation time. Preserve terminal failures and first real counterexamples. If Kano whole ending passes, run missing Sonya using qualified4617/fresh4622/4623Sonya leaves. Do not repeat accepted Scorpion added-victim windows. After stock Kitana qualification, adapt fresh source/collector for missing stock LiuP2 row-vs-font contract and qualify whole matrix actual faults. Continue full move/art/ground/shadow/arena/CPU/repeat/KO/overlap, broader native finishers/victims/morph/secret/cinematic/audio, all required natural towers/own endings/attract contexts, final selection/ladder/names/audio regression, dependency-aware cleanup and refreshed final release.',
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
      thisGoalTurnClassification='progress: actual hardware-bound complete ending observer/model implemented and source/41actual-field faults qualified; current actual native ending job launched. Stock renderer evidence type and original final-row/post-skip/font register semantics investigated without game changes; failed assumptions preserved.',
      gameCodeOrPublicReleaseChanged=False,newBuilds=0,rawMediaGuestROMCopies=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      cleanupAccounting='Compressed small source/text evidence and compact additive journal only. No duplicated raw frames/VRAM/audio/builds, no previous cleanup saving recounted.')
    need(len(result['remaining'])==5,'All original full-goal requirement groups preserved')
    need(all(sha(p)==h for p,h in pins.items()),'All newly frozen source/evidence/public bytes unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before journal writes')
    (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),stockAccepted=stock['completeNativeRendererWindowAccepted'],
                         endingAccepted=ending['completeNativeRendererWindowAccepted'],liveSessions=result['liveExecSessions'],newPins=len(pins),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
