"""Whole-goal additive journal for actual current player-one campaigns.

Preserves all original scope, public artifacts and prior immutable evidence.
Native process observation, whole campaign grammar and pixel/audio acceptance
remain distinct. Never pin a still-growing log as terminal native evidence.
"""
import ast,json,re,subprocess
from pathlib import Path
import save_full_ending_and_packet_caller_progress_v4769 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=previous.BASE
PARENTS=previous.PARENTS+[ROOT/'audit_v4770_full_ending_and_packet_caller_progress/progress.json']
OUT=ROOT/'audit_v4790_actual_p1_campaign_progress'

def main():
    need(not OUT.exists(),'Fresh immutable whole-goal additive journal')
    base=json.loads(BASE.read_text());inherited=dict(base['inputHashes'])
    for parent in PARENTS:
        for p,h in json.loads(parent.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent original full-goal input chain');inherited[p]=h
    need(all(sha(p)==h for p,h in inherited.items()),'All inherited source/native/public playable evidence bytes unchanged')
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need((wanted is None or actual==wanted)and(key not in inherited or inherited[key]==actual)and
             (key not in pins or pins[key]==actual),'Exact additive immutable source/native evidence byte')
        if key not in inherited:pins[key]=actual
    for p in[BASE,*PARENTS,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(p)
    preflightpath=ROOT/'audit_v4784_current_p1_campaign_source_checked/report.json'
    source=json.loads(preflightpath.read_text());pin(preflightpath)
    need(source['passed']and source['physicalSlot']==1 and source['allOriginalPhysicalPoliciesRetained']and
         source['allSixRAMFramesAndWholeGuestSinkRetained']and source['bothActualPrebootFailuresRetained']and
         source['onlyOneLuaReturnAssignmentCorrected']and len(source['actualSourceFaultsRejected'])==5 and
         source['originalSourceFaultsRetained']==8 and not source['actualPlayerOneNativeCampaignClearAccepted'],
         'Actual exact single Lua correction, original input policies and13source faults; no source-only native victory claim')
    for p,h in source['inputHashes'].items():pin(p,h)
    failures=[]
    for fighter,session in(('kano',23377),('sonya',1637)):
        folder=ROOT/f'audit_v4775_{fighter}_current_p1_campaign_ram'
        reportpath=ROOT/f'audit_v4776_{fighter}_current_p1_campaign_observed/report.json'
        failed=json.loads(reportpath.read_text());meta=json.loads((folder/'result.json').read_text());pin(reportpath)
        need(not failed['passed']and meta['exit_code']==3 and meta['ramGuestSHA256']is None and
             meta['actualNativeFrameCallbacks']==0 and
             'attempt to perform arithmetic on a string value (local \'last\')'in(folder/'stderr.log').read_text(),
             'Both actual first preboot failures preserved; zero initialized guest or gameplay acceptance')
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
        failures.append(dict(fighter=fighter,execSession=session,execTerminalConsumed=True,nativeExit=3,
          guestCompared=False,actualNativeRGBFields=0,prebootOnly=True,nativeGameplayAccepted=False))
    command="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_current_p1_campaign_ram_v4782.py|audit_v4785_|verify_current_p1_whole_campaign_v4787.py' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    census=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True)
    need(census.returncode==0,'Fresh exact native and collector process/command census')
    live=json.loads(census.stdout)if census.stdout.strip()else[]
    if isinstance(live,dict):live=[live]
    cases=[]
    for fighter,identity,session in(('kano',17,1579),('sonya',18,9959)):
        folder=ROOT/f'audit_v4785_{fighter}_current_p1_campaign_ram'
        observationpath=ROOT/f'audit_v4786_{fighter}_current_p1_campaign_observed/report.json'
        wholepath=ROOT/f'audit_v4788_{fighter}_current_p1_whole_campaign_checked/report.json'
        process=json.loads((folder/'process.json').read_text());pin(folder/'process.json');pin(folder/'input_hashes_before.json')
        for p,h in json.loads((folder/'input_hashes_before.json').read_text()).items():pin(p,h)
        guestpath=folder/'guest_memory_proof.json';guest=json.loads(guestpath.read_text());pin(guestpath)
        need(guest['frame']==1 and guest['bytes']==1048576 and guest['everyActualByteComparedInRAM']and
             guest['sha256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
             guest['guestDumpFilesWritten']==0 and guest['captureSourceSHA256']==sha(ROOT/'tools/run_current_p1_campaign_ram_v4782.py')and
             guest['transportSourceSHA256']==sha(ROOT/'mk2ks_current_p1_campaign_ram_v4781.lua'),
             'Actual first-frame entire current guest bytes independently compared in RAM and exact corrected sources bound')
        # Read a fixed small initial window, not an unbounded growing file.
        with(folder/'run.log').open('rb')as stream:prefix=stream.read(65536)
        prefix=prefix[:prefix.rfind(b'\n')+1].decode('utf-8')
        initial=[l for l in prefix.splitlines()if l.startswith(tuple('MK2_NAT_CAMPAIGN_'+tag+' 'for tag in
          ('BOOT','SELECT','SELECT_ID','SELECT_EXIT','STAGE','LIVE')))]
        selects=[l for l in initial if l.startswith('MK2_NAT_CAMPAIGN_SELECT_ID ')]
        first=next(l for l in initial if l.startswith('MK2_NAT_CAMPAIGN_LIVE '))
        fields=dict(re.findall(r'(\w+)=([^\s]+)',first))
        need(len(selects)>=2 and all(f'roster={identity} state=3'in l and 'human_slot=1'in l for l in selects[:2])and
             fields['human_slot']=='1'and fields['fighter']==fighter and fields['human']==f'{identity}:{identity}'and
             fields['writes']=='0'and fields['assistance']=='none'and fields['stage']=='0',
             'Actual player-one native confirm and real owned true17/18 first match, not a proxy/pending selection')
        entry=dict(fighter=fighter,physicalSlot=1,identity=identity,execSession=session,nativePID=process['pid'],
          capture=str(folder),observation=str(observationpath),wholeCampaignProof=str(wholepath),
          actualWholeInitializedGuestComparedInRAM=True,actualInitialNativeSelectionAndMatchObserved=True,
          initialNativeRows=initial[:8],actualFullCampaignGrammarAccepted=False,actualNaturalTowerOwnEndingAttractAccepted=False,
          fullP1EndingPixelsAccepted=False,completeP1CampaignAudioAccepted=False)
        if observationpath.exists():
            observed=json.loads(observationpath.read_text());pin(observationpath)
            need(observed['passed']and observed['nativeExit']==0 and observed['physicalSlot']==1,
                 'Actual complete corrected player-one native terminal and observation, not elapsed time')
            for p,h in observed['inputHashes'].items():pin(p,h)
            entry.update(actualNativeTerminalExit=0,actualStages=observed['actualStages'],actualNativeRGBCallbacks=observed['actualNativeRGBFrameCallbacks'],
              observedEndingStarts=observed['endingStarts'],observedEndingCompletions=observed['endingCompletions'])
            if wholepath.exists():
                proof=json.loads(wholepath.read_text());pin(wholepath)
                entry['actualIndependentWholeProofPassed']=proof['passed']
                if proof['passed']:
                    need(proof['physicalSlot']==1 and proof['identity']==identity and proof['originalWholeCampaignGrammarRetained']and
                         proof['case']['passed']and proof['case']['human_slot']==1 and
                         len(proof['actualRowAndRAMGuestFaultsRejected'])>=17 and not proof['endingPixelsAccepted']and
                         not proof['completeCampaignAudioAccepted']and not proof['fullPortAcceptance'],
                         'Original complete native campaign, source/ownership/special/health/winner/continue/boss-input grammar and actual faults accepted')
                    for p,h in proof['inputHashes'].items():pin(p,h)
                    entry.update(actualFullCampaignGrammarAccepted=True,
                      actualNaturalTowerOwnEndingAttractAccepted=proof['actualNaturalP1TowerOwnEndingAttractAccepted'],
                      actualOwnNativeRoundWins=proof['case']['native_own_round_wins'],
                      actualPaidContinueLosses=proof['case']['paid_continue_losses'],
                      actualRowAndRAMGuestFaultsRejected=len(proof['actualRowAndRAMGuestFaultsRejected']))
                else:entry['actualIndependentWholeProofError']=proof['error'][:1000]
        else:
            native=any(r['ProcessId']==process['pid']and str(folder)in r['CommandLine']for r in live)
            collector=any(r['Name']=='python.exe'and '4782.py'in r['CommandLine']and f'--fighter {fighter}'in r['CommandLine']for r in live)
            need(native and collector,'Pending only after exact currently live native and collector commands confirmed')
            entry.update(nativeLiveNow=True,collectorLiveNow=True)
        cases.append(entry)
    bridge=ROOT/'tools/verify_current_p1_whole_campaign_v4787.py';body=bridge.read_text();ast.parse(body);pin(bridge)
    for token in('kano.make_native(expected)','sonya_make_native(expected)','physical.replay(text)','spacing.replay(text)',
                  "meta['human_slot']==1 and meta['cpu_slot']==2",'Actual natural ending-to-attract plus all300ordinary fields',
                  "positive['unassisted_clear_proven']",'Original-derived true-ID schedule','Actual RAM guest fault admitted'):
        need(token in body,'Complete prepared whole original P1 qualifier retains mandatory boundary '+token)
    report=dict(schema=1,baseFullScopeCheckpoint=str(BASE),parentAdditiveJournals=[str(p)for p in PARENTS],
      mergeRule='Read with4557 and all additive journals. Every original scope group, native finite acceptance, input pin, exclusion and public playable artifact persists. New actual P1 selection/combat and campaign evidence cannot stand in for complete ending pixels/audio, all contexts or finished release.',
      remaining=base['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
      previousGoalTurnClassification='progress: both actual current P2 full ending/attract videos and separate complete hardware ledgers accepted; all112Scorpion secondary native packet callers source-qualified with76actual caller faults, retaining whole previous audio and waveform evidence.',
      thisGoalTurnClassification='progress: inspected exact native physical-slot input/address/selection/continue/boss/ending routing; prepared slot-precondition-only P1 wrapper preserving original policies and RAM collector. Both first native boots actually failed before guest/gameplay on Lua return-value assignment; preserved complete failures, corrected only assignment into fresh sources and passed13retained/new source faults. Genuine true17/18 player-one selection and real matches now observed with every initialized current guest byte compared in RAM. Kano naturally reached all16stages, defeated both bosses and completed own ending+300attract with native terminal0; full independent grammar result recorded below. Sonya has activated native leg and ring moves with paid continues; no player-one clear is inferred from player-two evidence or a live prefix.',
      originalPrebootFailures=failures,exactCorrectedSourcePreflight=dict(report=str(preflightpath),passed=True,
        sourceFaultsRetained=13,noNativeGameplayOrPolicyChange=True,physicalSlot=1),
      actualP1CampaignCases=cases,liveJobsAuthoritativelyObservedNow=live,
      completeOriginalP1CampaignQualifier=str(bridge),candidateAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,
      newlyDeletedFiles=0,newlyReclaimedAllocatedBytes=0,
      nextAction='Poll exact9959Sonya4782 and its currently confirmed native118992/collector138964; never restart from an observation timeout or repeated paid losses. Consume actual4786S native terminal before invoking4787 --fighter sonya into unused4788S. If Kano4788 is pending, poll exact50669checker132132 and consume real result, preserving any checker counterexample. Full P1 ending pixels/audio remain separate from the currently complete P2 proofs. Sonya currently retries Kitana4 at stage2 with genuine owned native Ring activation, not a selection softlock. If her real5900host-deadline terminal remains incomplete, preserve complete native capture and investigate actual Kitana/owned-projectile/control chronology before designing a fresh physical-only guard/anti-air policy; never change native AI, health, RNG, identities or declare a P2 ending to be P1. All five original broader Pit/Tomb/art/grounding/shadows/CPU/repeated/KO/finisher/morph/secret/cinematic/selection/ladder/names/audio/cleanup/refreshed-release scope groups remain.',
      cleanupAccounting='Compressed source/text/digests only; new raw guest/VRAM/RGB/PCM never persisted. No new EXE/ROM/archive/playable build or deletion; previous32.49GiB reclaimed is not recounted.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Entire original scope and every additive immutable source/evidence byte retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),actualP1SelectionAndRealMatchContexts=2,
      actualP1NaturalClearAccepted=[r['fighter']for r in cases if r['actualNaturalTowerOwnEndingAttractAccepted']],
      pendingNativeCampaigns=[r['fighter']for r in cases if r.get('nativeLiveNow')],
      originalPrebootFailuresPreserved=2,newBuilds=0,rawMediaFilesWritten=0,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
