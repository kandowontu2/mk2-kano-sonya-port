"""Preserve full goal; verified natural Scorpion/Shang clears, Kintaro still open."""
import json,subprocess
from pathlib import Path
import verify_shang_jump_retry_whole_campaign_v4308 as campaign
ROOT,need,sha=campaign.ROOT,campaign.need,campaign.sha
PARENT=ROOT/'audit_v4295_mileena_clear_jump_retry_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4313_scorpion_clear_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);actual=sha(path)
        need(key not in pins or pins[key]==actual,'Inherited logical bytes unchanged')
        need(wanted is None or actual==wanted,'Actual executed/report input unchanged')
        pins[key]=actual
    for path,h in pins.items():need(sha(path)==h,'Every inherited source/native/public byte preserved')
    pin(PARENT);pin(__file__)
    names=('audit_v4302_shang_jump_retry_source_preflight','audit_v4305_shang_jump_retry_campaign_observed',
           'audit_v4307_shang_jump_retry_actual_prefix_checked','audit_v4309_shang_jump_retry_whole_campaign_checked')
    reports={}
    for name in names:
        path=ROOT/name/'report.json';r=json.loads(path.read_text())
        need(r['passed'] and not r.get('fullPortAcceptance',False),'Actual completed bounded proof, not full port')
        pin(path);reports[name]=r
        for p,h in r.get('inputHashes',r.get('case',{}).get('inputHashes',{})).items():pin(p,h)
    full=reports[names[3]];c=full['case'];folder=campaign.FOLDER
    need(c['passed'] and c['actualWholeCampaignGrammarRetained'] and c['actual3836P2WholeCampaignAlgorithmRetained'],
         'Full original native selection/identity/schedule/morph/health/KO/boss/ending grammar retained')
    need(not full['actualNaturalSonyaP2TowerClearAccepted'] and not c['unassisted_clear_proven'] and
         c['ending_starts']==c['ending_completions']==0,'Kintaro/whole tower and own ending still unproven')
    need(c['stages_reached']==list(range(13))+[14,15] and c['paid_continue_losses']==8,
         'Actual original schedule progression to Kintaro15 with eight paid losses')
    r=c['actualWholeRingSpacingInputReplay']
    need(r['actualCompleteRangeFields']==4722 and r['actualNativeOwnRingTasks']==49 and
         r['actualNativeHuman308JumpStores']==r['actualNativeHuman200AirKickStores']==9,
         'Actual native fields, own Ring tasks, original jump/air-kick stores required')
    rows=campaign.spacing.parse((folder/'run.log').read_text())
    earned={stage:[v for v in rows if v['tag']=='WIN' and v['slot']=='2' and v['stage']==str(stage)]
            for stage in (12,14,15)}
    need([[v['health'] for v in earned[s]] for s in (12,14,15)]==[['0,161','0,37'],['0,129','0,139'],['0,81','0,41']],
         'Actual two Scorpion rounds, two Shang rounds, two separate Kintaro rounds; no Kintaro match clear')
    need(all(v['id']=='18' and v['entry']=='FFFEFA40' and v['pc']=='FF8296B0' for vs in earned.values() for v in vs),
         'Own true Sonya native winner-table dispatch, never a proxy')
    failed=ROOT/'audit_v4311_range_jump_retry_observer_runtime_checked/report.json'
    f=json.loads(failed.read_text())
    need(not f['passed'] and 'both roles after Main address opposite-side reuse' in f['error'],
         'Strict observer role-reuse scope remains unexercised/failed, not weakened')
    pin(failed)
    for name in ('mk2ks_shang_jump_retry_campaign_ram_v4300.lua','tools/qualify_shang_jump_retry_source_v4301.py',
                 'tools/run_shang_jump_retry_campaign_v4303.py','tools/verify_shang_jump_retry_prefix_v4306.py',
                 'tools/verify_shang_jump_retry_whole_campaign_v4308.py','tools/verify_range_jump_retry_observer_runtime_v4310.py',
                 'mk2ks_stock_scorpion_secondary_inputs_v1210.lua','tools/verify_stock_scorpion_secondary_v1222.py',
                 'tools/verify_human_shang.py'):pin(ROOT/name)
    process=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process -Filter "ProcessId=139012 OR ProcessId=132476 OR ProcessId=135276 OR ProcessId=93728" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(process.returncode==0 and not process.stdout.strip(),'Actual native/collector/prefix/whole jobs terminal; handles consumed')
    next_action=('Sonya P2 now naturally clears Mileena5, Scorpion10 at12 and actual Shang6 at14, reaching Kintaro12 at15. '
      'Kintaro has two earned single-round wins across paid-loss attempts, not a match clear. Inspect actual boss control/damage '
      'timing before the next physical-only test; preserve native AI/difficulty/health/roster/RNG/position and all original '
      'campaign/boss/ending grammar. Stage12 was mislabeled Shang in4294 and4300/4301/4303 filenames: native10 is Scorpion, '
      'native6 is Shang; historical executed files remain immutable. Repaired slot/Main observer runtime still needs a natural '
      'opposite-role reuse and throw/capture case;4311 correctly remains failed, no recreated events or weakened gate. '
      'Continue all five original groups: broader Pit/Tomb victims/branches/stage audio; all move art/ground/floor shadows/erase '
      'across arenas/CPU/repeats/KO/overlap; other finishers/victims/morphs/secrets/cinematics; actual full towers/own endings/attract; '
      'final combined selection/ladder/names/audio, dependency-aware cleanup and refreshed release ZIP. Public1836 is unchanged playtest, not final.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='All full-goal requirements, exclusions and inherited logical bytes retained.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      previousUserAcknowledgementClassification='no progress; no implementation authorized by thanks alone. Current goal continuation revalidated actual state and took available safe action.',
      thisGoalTurnClassification='progress: exact controller-only numeric10 dispatch added to proven Mileena Ring/jump retry; fresh actual3836 cold SonyaP2 campaign reached Kintaro15, naturally cleared Scorpion10 and Shang6. Complete native campaign/physical replay verified. No gameplay/public build changes.',
      currentDevelopmentCampaignObservation=str(ROOT/names[1]/'report.json'),
      currentDevelopmentCampaignReport=str(ROOT/names[3]/'report.json'),
      currentTerminalScorpionJumpRetry=dict(capture=str(folder),execHandle=97882,collectorPID=139012,nativePID=132476,
        terminalExitCode=0,prefixExecHandle=33068,wholeExecHandle=31599,
        trueHumanID=18,trueScorpionID=10,trueShangID=6,stagesReached=c['stages_reached'],
        actualOwnRoundWins=c['native_own_round_wins'],paidLosses=8,actualOwnRangeRingTasks=49,
        actualNativeRangeJumpStores=9,actualNativeRangeAirKickStores=9,actualEarnedScorpionRounds=earned[12],
        actualEarnedShangRounds=earned[14],actualEarnedKintaroRounds=earned[15],
        naturalKintaroMatchClearAccepted=False,naturalTowerClearAccepted=False,endingAccepted=False,
        completeCampaignAudioAccepted=False,fullPortAcceptance=False),
      nativeOpponentNameCorrection=dict(nativeScorpionID=10,nativeShangID=6,
        previousCheckpointStage12ShangLabelIncorrect=True,executedMisnamedSourcesPreserved=True,
        numericDispatchUnchanged=True,fullOriginalNativeIDChecksRetained=True),
      currentNativeObserverSlotReuseRuntimeGate=dict(report=str(failed),passed=False,
        reason='New winning ranged branches still did not exercise both-role Main reuse or logged CPU throw/victim capture.',
        nativeBothRoleReuseProven=False,strictGateNotWeakened=True,oldMissingEventsNotRecreated=True),
      nextAction=next_action,nextImplementationAction=next_action,
      currentTurnReclaimedAllocatedBytes=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,
      currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='Compressed-before-write native text/proofs only; no deletion or raw guest/raster/audio/EXE/ROM copies. Historical savings not counted again.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All five original goal groups retained exactly')
    for p,h in pins.items():need(sha(p)==h,'All actual inherited/new evidence remains exact')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress checkpoint before writing')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),stages=c['stages_reached'],
      nativeOwnRoundWins=c['native_own_round_wins'],scorpionRounds=2,shangRounds=2,kintaroSingleRounds=2,
      naturalTowerClearAccepted=False,allOriginalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
