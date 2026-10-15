"""Preserve full original goal and exact terminal/live native evidence."""
import hashlib,json,subprocess
from pathlib import Path
import run_jax_arms_native_audio_routes_v4212 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4209_mirror_terminal_storage_live_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4222_storage_campaign_arm_audio_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'All inherited logical bytes preserved')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);h=sha(p)
        need(key not in pins or pins[key]==h,'Inherited/current evidence unchanged')
        need(wanted is None or h==wanted,'Actual terminal report provenance');pins[key]=h
    pin(PARENT);pin(__file__)
    campaign_path=ROOT/'audit_v4197_mirror_guard_zoning_whole_campaign_checked/report.json'
    campaign=json.loads(campaign_path.read_text());case=campaign['case'];guard=case['actualWholeGuardInputReplay']
    need(campaign['passed']and not campaign['actualNaturalSonyaP2TowerClearAccepted']and not campaign['fullPortAcceptance']and case['actualWholeCampaignGrammarRetained'],'Complete original native campaign grammar, not a natural clear')
    need(case['paid_continue_losses']==99 and case['native_own_round_wins']==33 and case['stages_reached']==list(range(10))and case['ending_starts']==case['ending_completions']==0,'Actual failed tower remained atMileena9, no boss/ending claim')
    need(guard['actualCompleteGuardFields']==10041 and guard['actualNativeLegActivations']==8 and guard['actualNativeHumanUppercut107Stores']==0,'Actual complete mirror-only guard supplement, not other-roster zoning-field replay')
    pin(campaign_path)
    for p,h in case['inputHashes'].items():pin(p,h)
    for p,h in campaign.get('inputHashes',{}).items():pin(p,h)
    compaction=ROOT/'audit_v4207_frozen_friendship_set_compaction';report=json.loads((compaction/'report.json').read_text())
    plan=json.loads((compaction/'plan.json').read_text());ledger=[json.loads(s)for s in(compaction/'files.jsonl').read_text().splitlines()]
    need(report['passed']and report['exactFilesSelected']==report['exactFilesVerified']==len(ledger)==33517 and report['errors']==[],'Actual complete terminal compaction, all33517rows verified')
    need(len({r['path']for r in ledger})==33517 and {r['path']for r in ledger}=={r['path']for r in plan['targets']},'Exactly planned original files, no duplicates or extra targets')
    need(all(r['allocatedAfter']<=r['allocatedBefore']and len(r['sha256'])==64 and r['reclaimed']==r['allocatedBefore']-r['allocatedAfter']for r in ledger),'Every before/after logical SHA and actual allocation result present')
    need(sum(r['reclaimed']for r in ledger)==report['reclaimedAllocatedBytes']==3392749568 and report['deletedFiles']==0 and report['previousSampleReclamationNotCountedAgain'],'Actual completed savings only, not partials or prior4205sample')
    for p,h in report['inputHashes'].items():pin(p,h)
    for name in('report.json','plan.json','files.jsonl'):pin(compaction/name)
    for name in('tools/run_jax_arms_native_audio_routes_v4212.py','tools/verify_jax_arms_audio_routes_state_v4211.py','mk2ks_jax_arms_audio_routes_ram_v4210.lua','tools/verify_jax_arms_native_audio_routes_v4215.py','tools/run_remaining_jax_arms_audio_v4216.py','tools/verify_jax_arms_native_audio_routes_v4218.py','tools/run_remaining_jax_arms_audio_v4219.py'):
        pin(ROOT/name)
    failures=[]
    for name,expected in(('audit_v4214_jax_arms_native_audio_routes_observed','through749 sound fields'),('audit_v4217_jax_arms_native_audio_routes_checked','One complete native dispatch per selector')):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(not r['passed']and expected in r['error'],'Original false checker assumption remains immutable');pin(p);failures.append(dict(report=str(p),error=r['error'],accepted=False))
    completed_captures=[]
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        for enabled in (True,False):
            folder=ROOT/f"audit_v4213_jax_arms_{fighter}_p{side}_audio_queue_{'samples'if enabled else'nosamples'}"
            if not(folder/'result.json').exists():continue
            meta=json.loads((folder/'result.json').read_text())
            need(meta['exit_code']==0 and meta['fighter']==fighter and meta['side']==side and meta['samples_enabled']==enabled and not meta['stockReferenceOnly']and meta['rawAudioRasterVRAMROMCopiesWritten']==0 and meta['guestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821','Actual terminal true-ID native arm capture and entire RAM guest')
            for p,h in meta['input_hashes'].items():pin(p,h)
            for p in folder.rglob('*'):
                if p.is_file():pin(p)
            completed_captures.append(dict(fighter=fighter,side=side,samplesEnabled=enabled,path=str(folder),exitCode=0,mixedPCMBytes=meta['mixedPCMBytesVerifiedInRAM']))
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=118888 OR ProcessId=126724 OR ProcessId=11348" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0,'Actual current PID check');processes=json.loads(q.stdout)if q.stdout.strip()else[]
    if isinstance(processes,dict):processes=[processes]
    by={p['ProcessId']:p for p in processes}
    need(118888 not in by and 126724 not in by,'Compactor7745 and campaign qualifier2326 actually terminal, handles consumed')
    audio_report=ROOT/'audit_v4220_jax_arms_native_audio_routes_checked/report.json'
    if audio_report.exists():
        r=json.loads(audio_report.read_text());pin(audio_report)
        audio=dict(execSession=31306,report=str(audio_report),reportPresent=True,passed=r['passed'],process=by.get(11348),fullPortAcceptance=False)
        if r['passed']:
            need(r['actualContexts']==4 and r['actualPairedCaptures']==8 and not r['additionalDirectPacketCallerOriginsAccepted'],'Bounded full matrix, extra direct packet origins remain open')
            for p,h in r['inputHashes'].items():pin(p,h)
    else:
        need(11348 in by and 'run_remaining_jax_arms_audio_v4219.py'in by[11348]['CommandLine'],'Exact continuing audio proof31306/PID11348 confirmed live; no restart')
        audio=dict(execSession=31306,pythonPID=11348,process=by[11348],report=str(audio_report),reportPresent=False,complete=False,fullPortAcceptance=False)
    state.update(inputHashes=pins,previousCheckpoint=str(PARENT),inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='All inherited full-scope requirements/exclusions and logical bytes retained.'),
      previousGoalTurnClassification='verified wait: same live7745 compactor and2326 campaign qualifier polled, actual output showed continued work.',
      thisGoalTurnClassification='progress: consumed7745 terminal0, exact33517frozenfiles verified SHA/size/timestamp preserved,3392749568B lossless savings,0deletions. Consumed2326 terminal0, complete original native campaign grammar and10041mirror guard fields,8Leg tasks;33roundwins/99paidlosses/Mileena9/noending, no clear. New true-ID earned Jax arm-rip audio captures use originalBBBBLPgap96, native147-field wrap, whole guest/PCM RAM-only. Preserved false4214video/audio tick assumption and4217overwide selector dispatch window failures; independent4218 binds every50Hz update, original1074earned state/palette/tables and3952generic PCM/channels/packets/ADSP grammar. Exact continuation4219 uses original captures rather than rerunning KanoP1; observed first55source selectors/26actual state/audio/palette faults rejected. Four extra direct native packet caller origins remain unclassified. No public/game edits, newbuilds or rawmedia copies. All five original remaining groups intact.',
      completedMirrorZoningWholeCampaign=dict(execSession=2326,terminalExitCode=0,report=str(campaign_path),actualOwnRoundWins=33,actualPaidLosses=99,actualMirrorGuardFields=10041,actualLegActivations=8,actualHuman107Stores=0,originalWholeCampaignGrammarRetained=True,otherRosterZoningFieldReplayAccepted=False,naturalTowerClearAccepted=False,endingAccepted=False),
      pendingSonyaP2MirrorZoningCampaign=dict(execSession=49138,terminalExitCode=0,wholeQualifierExecSession=2326,wholeQualifierTerminalExitCode=0,wholeQualifierReport=str(campaign_path),boundedWholeCampaignAccepted=True,naturalTowerClearAccepted=False,ownEndingReached=False),
      pendingFrozenFriendshipCompaction=dict(execSession=7745,terminalExitCode=0,complete=True,report=str(compaction/'report.json'),exactFilesSelected=33517,exactFilesVerified=33517,reclaimedAllocatedBytes=3392749568,deletedFiles=0),
      currentTurnReclaimedAllocatedBytes=3392749568,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='Only completed4207report total3392749568B counted this turn; no prior partial row total or earlier4205sample41115648B added again. All historical reclamation/deletion accounting remains prior.',
      armAudioState=dict(completedNativeCaptures=completed_captures,immutableFalseAssumptionReports=failures,wholeAudioProof=audio,originalPhysicalBBBBLPGap96=True,trueOwnVictims17And18=True,originalNative147FieldWrap=True,fullInitializedGuestAndPCMOnlyInRAM=True,additionalDirectPacketCallerOriginsAccepted=False,allArenasAccepted=False,alternateCostumesAccepted=False,allFinisherAudioAccepted=False),
      nextImplementationAction='Poll exact audio31306/PID11348 while confirmed live; never restart on timeout. Completed native inputs/captures4213 are immutable. Require4220 terminal full4context/8capture state/voice/table/packet/PCM/fault proof before bounded acceptance; even then four additional direct packet caller origins need actual return-PC trace, not inferred labels. Both old7745storage and2326campaign handles consumed terminal0, no stale running claims. SonyaP2 policy again failedMileena9 after99losses; do not repeat identical losing policy or treat bounded verification as towerclear. All five original groups remain: broader Pit/Tomb branches/mirrors/victim/stage audio; all move art/ground/shadows/cleanup/CPU/repeat/KO/overlap arenas; other finishers/victims/morphs/secrets/cinematics; full natural towers/own endings/attract; combined UI/ladder/names/audio, dependency-aware cleanup and refreshed finalZIP. Public1836/ZIP installed binary and dirty12file source unchanged; no retired dependency resurrection.',
      gameSourceAndPlayableBytesChangedThisTurn=False,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Full original goal preserved')
    for p,h in pins.items():need(sha(p)==h,'All checkpoint logical inputs unchanged after aggregation')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writing')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),actualCompletedReclaimedBytes=3392749568,terminalNativeArmCaptures=len(completed_captures),audio=audio,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
