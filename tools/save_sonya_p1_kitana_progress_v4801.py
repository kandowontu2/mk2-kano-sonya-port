"""Additive full-goal checkpoint: actual Kitana guard input evidence, not release.

Retains the entire original five-group scope and inherited immutable chain.
Never pins a still-growing capture as a native terminal or claims a full clear.
"""
import ast,json,re,subprocess
from pathlib import Path
import save_actual_p1_campaign_progress_v4789 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4790_actual_p1_campaign_progress/progress.json']
OUT=ROOT/'audit_v4802_sonya_p1_kitana_progress'

def main():
    need(not OUT.exists(),'Fresh immutable additive full-goal checkpoint')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for path in PARENTS:
        for p,h in json.loads(path.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent inherited full-goal evidence');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'All prior actual source/native/public evidence unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();actual=sha(path);key=str(path)
        need((wanted is None or actual==wanted) and (key not in inherited or inherited[key]==actual)
             and (key not in pins or pins[key]==actual),'Exact additive immutable source/evidence byte')
        if key not in inherited:pins[key]=actual
    for path in [BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(path)
    reports={}
    for name,path in (
        ('bounded',ROOT/'audit_v4792_sonya_p1_bounded_kitana_diagnosis/report.json'),
        ('source',ROOT/'audit_v4796_sonya_p1_kitana_guard_source_checked/report.json'),
        ('prefix',ROOT/'audit_v4800_sonya_p1_kitana_guard_prefix_checked/report.json')):
        report=json.loads(path.read_text());need(report['passed'],'Actual finite boundary passed '+name)
        pin(path)
        for p,h in report['inputHashes'].items():pin(p,h)
        reports[name]=report
    bounded,source,prefix=(reports[n] for n in ('bounded','source','prefix'))
    need(not bounded['actualNaturalP1TowerClearAccepted'] and not bounded['completeMandatoryContextCheckerPassed']
         and bounded['failedCheckerPreserved'],'Actual bounded old terminal and context failure preserved')
    need(source['originalSourceFaultsRetained']==13 and len(source['actualSourceFaultsRejected'])==7
         and source['allOriginalOtherPhysicalPoliciesRetained'],'All prior physical/native boundaries plus seven new source faults')
    need(prefix['prefixProofOnly'] and len(prefix['actualRowFaultsRejected'])==11
         and prefix['case']['actualCompleteGuardFields']==3045 and prefix['case']['actualNativeLegActivations']==10
         and prefix['case']['actualNativeHumanUppercut107Stores']==0,
         'Every actual Kitana field/input replayed, real leg tasks and all faults; no planned uppercut activation credited')
    folder=ROOT/'audit_v4797_sonya_p1_kitana_guard_ram'
    for name in ('process.json','input_hashes_before.json','guest_memory_proof.json'):pin(folder/name)
    for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
    process=json.loads((folder/'process.json').read_text())
    # Fixed small prefix window, no unbounded/tail read and no live-log pin.
    with (folder/'run.log').open('rb') as stream:raw=stream.read(48*1024*1024)
    raw=raw[:raw.rfind(b'\n')+1]
    need(len(raw)>=prefix['nativeLogPrefixBytes'],'Actual executed prefix remains available')
    import hashlib
    need(hashlib.sha256(raw[:prefix['nativeLogPrefixBytes']]).hexdigest().upper()==prefix['nativeLogPrefixSHA256'],
         'Independent finite input prefix retained byte-for-byte in actual growing native capture')
    lines=raw.decode().splitlines()
    advance=next(l for l in lines if l.startswith('MK2_NAT_CAMPAIGN_STAGE ') and ' stage=3 ' in l)
    advance_frame=int(re.search(r'frame=(\d+)',advance)[1])
    wins=[l for l in lines if l.startswith('MK2_NAT_CAMPAIGN_WIN ') and ' slot=1 stage=2 id=18 ' in l
          and int(re.search(r'frame=(\d+)',l)[1])<advance_frame]
    need(advance_frame==31262 and len(wins)>=2,'Actual native own Kitana victories precede true next-stage observation')
    checker=ROOT/'tools/verify_sonya_p1_kitana_guard_whole_campaign_v4803.py'
    ast.parse(checker.read_text());pin(checker)
    observation_path=ROOT/'audit_v4798_sonya_p1_kitana_guard_observed/report.json'
    whole_path=ROOT/'audit_v4804_sonya_p1_kitana_guard_whole_campaign_checked/report.json'
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_sonya_p1_kitana_guard_ram_v4794.py|audit_v4797_|verify_sonya_p1_kitana_guard_whole_campaign_v4803.py' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact process/command census');live=json.loads(census.stdout) if census.stdout.strip() else []
    if isinstance(live,dict):live=[live]
    native_case=dict(execSession=95967,nativePID=process['pid'],capture=str(folder),observation=str(observation_path),
                     wholeCampaignProof=str(whole_path),actualNativeKitanaAdvanceObserved=True,
                     actualKitanaAdvanceRow=advance,actualNativeOwnKitanaRoundWinnerRows=wins,
                     wholeCampaignClearAccepted=False,endingPixelsAccepted=False,completeCampaignAudioAccepted=False)
    if observation_path.exists():
        terminal=json.loads(observation_path.read_text());pin(observation_path)
        need(terminal['passed'] and terminal['nativeExit']==0,'Actual native terminal, never elapsed time')
        for p,h in terminal['inputHashes'].items():pin(p,h)
        native_case.update(actualNativeTerminalExit=0,actualStages=terminal['actualStages'])
    else:
        need(any(r['ProcessId']==process['pid'] and str(folder) in r['CommandLine'] for r in live)
             and any(r['Name']=='python.exe' and '4794.py' in r['CommandLine'] and '--fighter sonya' in r['CommandLine'] for r in live),
             'Pending only after currently live exact native and collector confirmed')
        native_case.update(nativeLiveNow=True,collectorLiveNow=True)
    if whole_path.exists():
        whole=json.loads(whole_path.read_text());pin(whole_path)
        native_case['actualIndependentWholeCampaignProofPassed']=whole['passed']
        if whole['passed']:
            for p,h in whole['inputHashes'].items():pin(p,h)
            native_case['wholeCampaignClearAccepted']=whole['actualNaturalP1TowerOwnEndingAttractAccepted']
        else:native_case['actualWholeProofError']=whole['error']
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p) for p in PARENTS],
        mergeRule='Read with4557 and all parent journals. All five original requirements, evidence, exclusions and public artifacts persist; physical Kitana progress is not whole-port or release acceptance.',
        remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        previousGoalTurnClassification='progress: consumed actual Sonya P1 native terminal0 at322771, retained103paid losses and incomplete stages0/1/2. Full mandatory-context checker actually failed; preserved it and stream-diagnosed real Kitana4,1434native Ring activations and collision damage rather than claiming a proxy/selection lock or full clear.',
        thisGoalTurnClassification='progress: source-qualified a distinct Kitana4 guard controller cloned from existing physical mirror policy; all other native policies and guest unchanged.20retained/new source faults accepted. Launched fresh actual native P1; independently replayed3045first-Kitana fields and exact button edges,10real leg tasks and11actual faults. No native uppercut107 store was observed, so intended anti-air HP is not credited as activated. After a genuine paid loss the same actual run beat Kitana and advanced to stage3, then stage4. Full native campaign/ending checker prepared without relaxing any later mandatory context.',
        actualKitanaSourceProof=str(ROOT/'audit_v4796_sonya_p1_kitana_guard_source_checked/report.json'),
        actualKitanaInputPrefixProof=str(ROOT/'audit_v4800_sonya_p1_kitana_guard_prefix_checked/report.json'),
        actualKitanaNativeCase=native_case,liveJobsAuthoritativelyObservedNow=live,
        candidateAndPublicChanged=False,newBuilds=0,rawMediaFilesWritten=0,newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
        nextAction='Poll same95967/native19836/collector117108 while exact commands are live; never restart for losses or observation timeout. Only after real4798terminal execute4803 --fighter sonya into unused4804, preserving any genuine counterexample. Current observed retries are stage4 Jax11. Any next tactic must be physical-input-only and based on captured native action chronology. Broad Pit/Tomb victim/audio, move art/grounding/floor shadows/cleanup/CPU/KO/overlap, other finishers/morphs/secrets/cinematics, P1 ending pixels/audio, final selection/ladder/names/audio/cleanup/refreshed release remain.',
        cleanupAccounting='Compressed source/text/digests only. No new build, raw guest/VRAM/RGB/PCM, deletion or reclaimed-space recount.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Full original scope and all immutable additive evidence retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),actualKitanaFields=3045,actualNativeLegTasks=10,
        actualKitanaAdvanceFrame=advance_frame,nativeLiveNow=native_case.get('nativeLiveNow',False),
        wholeCampaignClearAccepted=native_case['wholeCampaignClearAccepted'],newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
