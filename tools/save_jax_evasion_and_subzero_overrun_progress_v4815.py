"""Full-goal additive checkpoint: genuine Jax progress and new native defect.

Do not turn earlier finite successes into universal stability. The actual
Sub-Zero/zero-health Sonya cache write contradicts full-port acceptance.
Preserve the live run, mandatory checker failures and all original scope.
"""
import ast,hashlib,json,re,struct,subprocess
from pathlib import Path
import save_sonya_p1_kitana_progress_v4801 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4802_sonya_p1_kitana_progress/progress.json']
OUT=ROOT/'audit_v4816_jax_evasion_and_subzero_overrun_progress'

def main():
    need(not OUT.exists(),'Fresh immutable complete-scope checkpoint')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for path in PARENTS:
        for p,h in json.loads(path.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent inherited whole-goal evidence');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'Entire original native/source/public evidence chain unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted) and (key not in inherited or inherited[key]==actual)
             and (key not in pins or pins[key]==actual),'Exact immutable additive source/evidence byte')
        if key not in inherited:pins[key]=actual
    for path in [BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(path)
    paths={
        'oldTerminal':ROOT/'audit_v4798_sonya_p1_kitana_guard_observed/report.json',
        'oldWholeFailure':ROOT/'audit_v4804_sonya_p1_kitana_guard_whole_campaign_checked/report.json',
        'sourceGround':ROOT/'audit_v4806_jax_137_ground_damage_source/report.json',
        'source':ROOT/'audit_v4810_sonya_p1_jax_jump_guard_source_checked/report.json',
        'prefix':ROOT/'audit_v4814_sonya_p1_jax_jump_guard_prefix_checked/report.json'}
    reports={}
    for name,path in paths.items():
        r=json.loads(path.read_text());pin(path);reports[name]=r
        for p,h in r.get('inputHashes',{}).items():pin(p,h)
    old,failed,ground,source,prefix=(reports[n] for n in ('oldTerminal','oldWholeFailure','sourceGround','source','prefix'))
    need(old['passed'] and old['nativeExit']==0 and old['actualStages']==[0,1,2,3,4]
         and old['endingStarts']==old['endingCompletions']==0 and not failed['passed']
         and 'One complete native field and physical decision per observed field' in failed['error'],
         'Actual old terminal and genuine mandatory-context failure retained, not silently relaxed')
    need(ground['passed'] and len(ground['actualInstructionFaultsRejected'])==9
         and source['passed'] and source['originalSourceFaultsRetained']==20
         and len(source['actualSourceFaultsRejected'])==7,'Original ground code and all27source faults retained')
    need(prefix['passed'] and prefix['prefixProofOnly'] and len(prefix['actualRowAndCallbackFaultsRejected'])==13
         and prefix['case']['actualCompleteGuardFields']==3234 and prefix['case']['actualNativeLegActivations']==10
         and prefix['nativeCallbacks']['actualNativeOwnedHumanJumpEntries']==1
         and prefix['nativeCallbacks']['actualNativeGroundResultsSkippingMovingOrAirborneTarget']==1
         and prefix['nativeCallbacks']['actualNativeGroundDamageInstructionsReached']==0,
         'Actual full Jax field/edge/native opcode/Carry/ownership replay and13faults; genuine opening evasion')
    folder=ROOT/'audit_v4811_sonya_p1_jax_jump_guard_ram'
    for name in ('process.json','input_hashes_before.json','guest_memory_proof.json'):pin(folder/name)
    for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
    process=json.loads((folder/'process.json').read_text())
    # Fixed prefix, complete lines only. Never hash-pin a growing whole log.
    with (folder/'run.log').open('rb') as stream:raw=stream.read(64*1024*1024)
    raw=raw[:raw.rfind(b'\n')+1]
    need(hashlib.sha256(raw[:prefix['nativeLogPrefixBytes']]).hexdigest().upper()==prefix['nativeLogPrefixSHA256'],
         'All actual independently accepted pre-defect Jax prefix bytes preserved')
    lines=raw.decode().splitlines();stages=[l for l in lines if l.startswith('MK2_NAT_CAMPAIGN_STAGE ')]
    overrun=[l for l in lines if l.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')]
    need(overrun,'Actual native global-cache write counterexample, never an inferred palette fault')
    first=dict(re.findall(r'(\w+)=([^\s]+)',overrun[0]));bad_frame=int(first['frame'])
    need(bad_frame==108255 and first['pc']=='FF838860' and first['a8']=='01034E90'
         and first['a9']=='FF07BAF0' and first['a13']=='0106C620' and first['id']=='18'
         and first['at']=='01060020' and first['mask']=='FFFF' and first['writes']=='0'
         and first['assistance']=='none','Actual original group-cache store, true Sonya actor/Main and global address')
    critical=[l for l in overrun if ' at=010601F0 ' in l]
    need(len(critical)==1 and 'data=0510' in critical[0],
         'Actual original cache overwrites physical P1 state word with non-state0510, not a theoretical address-range concern')
    recent=[l for l in lines if l.startswith('MK2_NAT_CAMPAIGN_LIVE ')
            and bad_frame-270<=int(re.search(r'frame=(\d+)',l)[1])<bad_frame]
    need(recent and all(' human=18:18 cpu=8:8 ' in l and 'stage=7' in l for l in recent)
         and any('health=0,105' in l for l in recent),
         'Actual Sub-Zero8 opponent and zero-health Sonya context before cache writes; freeze vs finisher cause not guessed')
    payload_path=ROOT/'diagnostic_v3836_native_mileena_rom_identity/roms/mk2ks/mk2ks.mdata'
    payload=payload_path.read_bytes();offset=(0xff07baf0-0xfe800000)//8
    need(payload[offset:offset+64]==b'\xff'*64,'Observed cursor falls in unpopulated payload bytes')
    target=struct.pack('<I',0xff07baf0)
    count=sum(payload[n:n+4]==target for n in range(0,len(payload)-3,2))
    need(count==0,'No literal payload pointer to observed later cursor; trace original cursor/lookup, do not assume direct table constant')
    pin(payload_path)
    bridge=ROOT/'tools/verify_sonya_p1_jax_jump_guard_whole_campaign_v4817.py'
    ast.parse(bridge.read_text());pin(bridge)
    observation_path=ROOT/'audit_v4812_sonya_p1_jax_jump_guard_observed/report.json'
    whole_path=ROOT/'audit_v4818_sonya_p1_jax_jump_guard_whole_campaign_checked/report.json'
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_sonya_p1_jax_jump_guard_ram_v4808.py|audit_v4811_|verify_sonya_p1_jax_jump_guard_whole_campaign_v4817.py' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact process/command census');live=json.loads(census.stdout) if census.stdout.strip() else []
    if isinstance(live,dict):live=[live]
    case=dict(execSession=40542,nativePID=process['pid'],capture=str(folder),observation=str(observation_path),
        wholeCampaignProof=str(whole_path),actualNativeStageRowsFromFixedPrefix=stages,
        actualNaturalTowerClearAccepted=False,fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False)
    if observation_path.exists():
        terminal=json.loads(observation_path.read_text());pin(observation_path)
        case.update(actualTerminalObservationPassed=terminal['passed'])
        if terminal['passed']:
            for p,h in terminal['inputHashes'].items():pin(p,h)
            case.update(actualNativeTerminalExit=terminal['nativeExit'],actualStages=terminal['actualStages'])
        else:case['actualTerminalObservationError']=terminal['error']
    else:
        need(any(r['ProcessId']==process['pid'] and str(folder) in r['CommandLine'] for r in live)
             and any(r['Name']=='python.exe' and '4808.py' in r['CommandLine'] and '--fighter sonya' in r['CommandLine'] for r in live),
             'Pending only after native and collector exact commands currently confirmed live')
        case.update(nativeLiveNow=True,collectorLiveNow=True)
    if whole_path.exists():
        whole=json.loads(whole_path.read_text());pin(whole_path)
        need(not whole['passed'],'A global-state-overrun campaign cannot be accepted as whole stable campaign')
        case['actualWholeCampaignCheckerError']=whole['error']
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p) for p in PARENTS],
        mergeRule='Read with4557 and every parent. All five requirements, finite prior evidence, public artifacts and exclusions persist. New actual Sub-Zero/zero-health Sonya global-state writes contradict universal stability; do not reuse prior finite campaign or prefix passes to declare completion.',
        remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        previousGoalTurnClassification='progress: actual Sonya P1 Kitana guard/control prefix accepted3045fields/10native leg tasks/11faults; genuine native advancement to stages3and4 observed; full original campaign checker prepared without relaxing missing later contexts.',
        thisGoalTurnClassification='progress: consumed old native terminal0/381RAMframes at322771, stages0..4only and93paid losses; real mandatory-context checker failed and preserved. Original Jax137 velocity/floor/21damage code source-qualified with9actual instruction faults. Fresh physical jump/guard wrapper retained all other policies and27source faults. Actual current P1 run independently accepted3234Jax fields/10leg tasks/13row-native faults, native jump at52707 and source-bound ground-helper Carry1 at52720 with no damage instruction reached; Jax was beaten and actual stages5/6/7 reached. At108255 a true zero-health Sonya versus Sub-Zero8 produced actual original group-cache writes into global state, including P1state0510. This is a real native defect, not control weakness, and changes next priority to original lookup/cursor/descriptor root-cause tracing.',
        actualJaxPhysicalAndNativePrefixProof=str(paths['prefix']),actualNativeCase=case,
        nativeDefect=dict(firstFrame=bad_frame,sourceInstruction='FF838850 MOVE A6,*A1+,1; store witness PCFF838860',
            actualFirstGlobalWrite=overrun[0],actualPhysicalP1StateCorruption=critical[0],
            nativeLoggedGlobalOverrunRows=len(overrun),actualPreDefectSonyaSubzeroWindow=recent,
            observedCursor='FF07BAF0',observedCursorPayload64BytesUnpopulated=True,literalPayloadPointersToCursor=0,
            causeNotYetQualified=True,ordinaryFreezeVersusFinisherNotYetDistinguished=True,
            newNativeFixBuilt=False,stableAllContextsContradicted=True),
        liveJobsAuthoritativelyObservedNow=live,candidateAndPublicChanged=False,newBuilds=0,rawMediaFilesWritten=0,
        newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
        nextAction='Poll same40542/native143080/collector75588 while exact commands remain live; do not restart or stop merely for an observation timeout or post-corruption silence. Consume actual4812terminal and preserve any4817/4818 rejection. Prioritize deterministic native root-cause diagnosis at108255: true Sonya18zero-health/Sub-Zero8stage7, original cache MOVE atFF838850 into globalP1state010601F0=0510, cursorFF07BAF0is unpopulated with no literal payload reference. Add readonly original main-animation lookup, cursor and group/descriptor/cache-entry witnesses to the same physical controller and RAM collector before any native fix/build. Trace the earlier first invalid input; distinguish freeze/KO/finisher path. Do not use ID proxies, artificial group-copy caps, state restoration, health/AI/RNG writes or a control strategy that evades the broken native branch as its fix. Full original Pit/Tomb/audio/art/grounding/floor-shadow/CPU/KO/overlap/finishers/victims/morphs/secrets/cinematics/endings/selection/ladder/names/cleanup/refreshed-release requirements remain.',
        cleanupAccounting='Compressed source/text/digests only. No new build, raw guest/VRAM/RGB/PCM, deletion or reclaimed-space recount.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Full original scope and immutable evidence retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),actualJaxFields=3234,
        actualOriginalGroundAttackSkipped=True,actualNativeGlobalStateDefectFrame=bad_frame,
        nativeLiveNow=case.get('nativeLiveNow',False),fullPortAcceptance=False,newBuilds=0,rawMediaFilesWritten=0),indent=2),flush=True)

if __name__=='__main__':main()
