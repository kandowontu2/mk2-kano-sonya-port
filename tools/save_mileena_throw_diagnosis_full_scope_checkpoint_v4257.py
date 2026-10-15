"""Terminal P2 campaign diagnosis, preserving every original full-port group."""
import json,subprocess
from pathlib import Path
import verify_mileena_native_throw_interruptions_v4255 as evidence
ROOT,need,sha=evidence.ROOT,evidence.need,evidence.sha
PARENT=ROOT/'audit_v4240_arm_audio_terminal_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4258_mileena_throw_diagnosis_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'Every inherited logical byte unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);h=sha(p)
        need(key not in pins or pins[key]==h,'Inherited/shared evidence unchanged')
        need(wanted is None or h==wanted,'Exact executed source/evidence pin')
        pins[key]=h
    pin(PARENT);pin(__file__)
    names=('audit_v4248_mileena_duck_pressure_source_preflight',
           'audit_v4250_mileena_duck_pressure_actual_prefix_checked',
           'audit_v4252_mileena_duck_pressure_whole_campaign_checked',
           'audit_v4254_mileena_duck_pressure_activation_observed',
           'audit_v4256_mileena_native_throw_interruptions_checked')
    reports={}
    for name in names:
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed'],'Actual completed source/runtime proof')
        need(not r.get('fullPortAcceptance',False),'Bounded proof cannot imply full port');pin(p);reports[name]=r
        for path,h in r.get('inputHashes',r.get('case',{}).get('inputHashes',{})).items():pin(path,h)
    campaign=reports[names[2]];c=campaign['case'];activation=reports[names[3]];interrupt=reports[names[4]]
    need(c['passed'] and c['actualWholeCampaignGrammarRetained'] and c['actual3836P2WholeCampaignAlgorithmRetained'] and
         not c['unassisted_clear_proven'] and not campaign['actualNaturalSonyaP2TowerClearAccepted'],
         'Whole native grammar qualified; still no natural tower clear')
    need(c['stages_reached']==list(range(10)) and c['native_own_round_wins']==20 and c['paid_continue_losses']==19 and
         c['ending_starts']==c['ending_completions']==0 and c['actualFiniteHostDeadlineReached'],
         'Actual bounded terminal loss campaign, not boss/ending proof')
    need(c['actualWholeDuckInputReplay']['actualNativeHuman107Stores']==3 and
         c['actualWholeDuckInputReplay']['actualNativeHumanUppercutFetches']==4 and
         activation['actualHPButtonRisingEdges']==155 and activation['hpEdgesAfterObservedPreparationInjury']==104,
         'Actual physical command efficiency and original human activation independently distinguished')
    need(interrupt['actualOriginalOpponentCaptures']==4 and interrupt['nativeOpponentCaptureNotPortCleanup'] and
         interrupt['actualHuman107Starts']==3 and len(interrupt['actualFaultsRejected'])==11,
         'Actual original victim captures bound to source and real faults')
    failed=ROOT/'audit_v4244_mileena_duck_pressure_source_preflight/report.json';pin(failed)
    # The old preflight report is preserved as historical evidence only. Its
    # runner hash was superseded before execution; do not merge its stale pins.
    for name in ('mk2ks_mileena_duck_pressure_campaign_ram_v4241.lua',
                 'tools/run_mileena_duck_pressure_campaign_v4243.py',
                 'tools/qualify_mileena_duck_pressure_source_v4242.py',
                 'tools/qualify_mileena_duck_pressure_source_v4247.py',
                 'tools/verify_mileena_duck_pressure_prefix_v4249.py',
                 'tools/verify_mileena_duck_pressure_whole_campaign_v4251.py',
                 'tools/analyze_mileena_duck_pressure_activation_v4253.py',
                 'tools/verify_mileena_native_throw_interruptions_v4255.py'):pin(ROOT/name)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process -Filter "ProcessId=3528 OR ProcessId=135752 OR ProcessId=105096 OR ProcessId=106816 OR ProcessId=134624" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Actual campaign/prefix/whole/interruption processes terminal; handles consumed')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Every inherited full-scope requirement/exclusion and logical byte preserved.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: actual prior campaign30393 terminal0 consumed, no restart on missing process. New physical Down/HP Mileena branch yielded 3 original HUMAN107 starts/4 genuine routine fetches versus previous0. Full original campaign/selection/true ID/owner/morph/schedule/health/KO/continue/boss/ending grammar preserved and passed bounded state proof:20 own round wins,19paidlosses,stages0..9,0ending.155actualHPedges104preparationinjuries; all4native uppercut entries were interrupted by original opponent victim-capture Mainclear PCFF8428A0,3after107samefield and1before107. Entire original capture/throw-action tail matched exact RAM guest, native stock throw507 setter source-bound; do not claim every507field proves original entry. Actual 17duck+9originalcampaign+8guest+10mirror+11interruption counterexample executions rejected, positive restored after each. Prefix/whole/interruption jobs76979/41586/72453 terminal0 consumed. No game/source/public/ZIP edits, no new EXE/ROM/raw media copies. All five original groups remain incomplete.',
      currentDevelopmentCampaignObservation=str(ROOT/'audit_v4246_mileena_duck_pressure_campaign_observed/report.json'),
      currentDevelopmentCampaignReport=str(ROOT/'audit_v4252_mileena_duck_pressure_whole_campaign_checked/report.json'),
      currentNativeUppercutInterruptionReport=str(ROOT/'audit_v4256_mileena_native_throw_interruptions_checked/report.json'),
      currentTerminalMileenaDuckPressure=dict(capture=str(evidence.FOLDER),execHandle=30393,terminalExitCode=0,collectorPID=3528,nativePID=135752,
        nativeFields=c['actualWholeDuckInputReplay']['actualCompleteDuckFields'],trueHumanID=18,trueOpponentID=5,actualPhysicalHPRisingEdges=155,
        actualHuman107Starts=3,actualNativeUppercutRoutineFetches=4,actualOriginalOpponentCaptures=4,actualPreparationInjuryWindows=104,
        originalGroundThrow507SetterSourceBound=True,everyObserved507EntryProven=False,opponentCaptureNotPortCleanup=True,
        originalWholeCampaignGrammarRetained=True,stagesReached=c['stages_reached'],ownRoundWins=20,paidLosses=19,
        naturalTowerClearAccepted=False,endingAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False),
      supersededPreflight=dict(report=str(failed),reason='Historical flat mirror-only fields were too broad and runner pin predates execution edits; preserved, not merged as executed provenance. Actual4247/4248 preflight separately binds executed4243/4241.'),
      currentTurnReclaimedAllocatedBytes=0,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='No new cleanup this turn. Earlier completed4207 total3392749568B remains historical; do not count it again.',
      nextImplementationAction='Do not repeat the losing unguarded close-range uppercut policy. Actual native opponent throws—not port cleanup—interrupt this command. Next physical-input strategy should preserve throw spacing/use the genuine existing ranged or protected leg move, and observe native CPU507 setter/capture ownership if broader classification is needed; no health/AI/roster/RNG/difficulty/position override. SonyaP2 true natural full tower/ownending/attract remains open. Continue broader native Pit/Tomb victims/mirrors/branches/stage audio, complete move art/ground/floor shadows/cleanup inallarenas/CPU/repeat/KO/overlap, allotherfinishers/victims/morphs/secrets/cinematics, allfulltowers/ownendings/attract, and finalcombinedselection/ladder/names/audio/dependencycleanup/refreshedZIP. AlternateJaxarm old1063 forces victim flag40 and is only controlled branch evidence, not natural selection. Public1836 remains existing playtest, not final.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Every original goal group retained')
    for p,h in pins.items():need(sha(p)==h,'Every aggregated source/evidence logical byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress checkpoint before writing')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),actualNativeUppercutStarts=3,
      actualSourceBoundOpponentCaptures=4,wholeCampaignGrammarPassed=True,naturalTowerClearAccepted=False,
      allOriginalRemainingGroups=len(remaining),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
