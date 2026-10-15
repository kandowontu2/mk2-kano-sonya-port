"""Carry every unfinished original gate and actual new standing-jump campaign evidence."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2585_current_guard_walk_dependency_descriptor_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2606_current_standing_jump_full_scope_checkpoint'

def need(ok,label):
 if not ok:raise ValueError(label)

def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active'and prior['objective']=='Once again, the goal is clear: THey need to appear as a natural part of the game in all aspects.'and not prior['fullPortAcceptance']and not prior['finishedRelease'],'Complete original unfinished objective')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual accepted bounded proof '+str(path))
  for file,wanted in r['inputHashes'].items():
   need(file not in pins or pins[file]==wanted,'Consistent preserved/current dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r
 contexts=dict(prior['currentSourceBoundBossCampaigns']);need(len(contexts)==62,'Exact previous accepted physical-context inventory')
 fresh={}
 for policy,capture_version,proof_version,ledger_version,negative_version,progress_version,boundary in (
  ('standing_retreat',2580,2581,2588,2589,2591,'audit_v2584_standing_retreat_source_boundary_checked'),
  ('standing_cross',2596,2597,2602,2603,2599,'audit_v2598_standing_cross_source_boundary_checked')):
  source_path=ROOT/boundary/'report.json';source=accept(source_path)
  need(source['fullSourceInverse']and source['wholeLauncherInverse']and source['wholeGuestAndPayloadReconstructed']and len(source['rejectedSpecificSourceCounterexamples'])==7,'Full physical-only controller/launcher/unchanged game boundary')
  for fighter in ('kano','sonya'):
   case=f'{fighter}_shao_{policy}';capture=ROOT/f'audit_v{capture_version}_current_{fighter}_p1_shao_{policy}_campaign'
   proof_path=ROOT/f'audit_v{proof_version}_current_{fighter}_p1_shao_{policy}_checked/report.json';proof=accept(proof_path)
   book_path=ROOT/f'audit_v{ledger_version}_current_{fighter}_shao_{policy}_boss_ledger_checked/report.json';book=accept(book_path)
   negative_path=ROOT/f'audit_v{negative_version}_current_{fighter}_shao_{policy}_input_counterexamples/report.json';negative=accept(negative_path)
   progress_path=ROOT/f'audit_v{progress_version}_current_{fighter}_shao_{policy}_progress/report.json';progress=accept(progress_path)
   need(proof['bounded_campaign_evidence_proven']and proof['bossPolicy']==f'shao_{policy}'and proof['human_slot']==1,'Actual matching physical campaign, true character and player slot')
   need(book['rejectedSpecificCounterexamples']==8 and book['finalUnmodifiedControlPassed']and negative['rejectedSpecificCounterexamples']==26 and negative['finalUnmodifiedFullCampaignControlPassed'],'Eight ordered and twenty-six full physical-input corruptions with final untouched controls')
   need(progress['exactPreShaoNativeRecords']==(92646 if fighter=='kano'else 136135)and len(progress['rejectedSpecificPrefixCounterexamples'])==3 and progress['actualKintaroMatchClear'],'Every ordinary/Kintaro chronological record unchanged; actual owned Kintaro clear')
   need(progress['actualFullNativeCampaignAndReturnPath']==proof['unassisted_clear_proven'],'Actual earned full Shao/ending/attract gate, never round-only acceptance')
   need(case not in contexts,'No replay counted as duplicate physical strategy coverage')
   entry={k:v for k,v in progress.items()if k not in('inputHashes','scope')}
   entry.update(campaignReport=str(proof_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),progressReport=str(progress_path),
    sourceBoundaryReport=str(source_path),capture=str(capture),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
    ownBossUppercutDamage=book['ownBossUppercutDamage'],ownBossRoundWins=book['ownBossRoundWins'],fullCampaignClear=proof['unassisted_clear_proven'],
    endingAccepted=False,fullEndingArtAudioAcceptance=False,repeatedKintaroControlNotIndependentStrategyCoverage=True)
   fresh[case]=entry;contexts[case]=entry
 for p in(Path(__file__).resolve(),ROOT/'tools/verify_current_boss_shao_standing_retreat_v2578.py',ROOT/'tools/verify_current_boss_shao_standing_cross_v2594.py'):
  pins[str(p)]=launch.sha(p)
 launch.module_pins(pins)
 print('Revalidating complete preserved/current graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed authoritative dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status only',
  thisGoalTurnClassification='progress: archive dependency check completed with exact equivalent target/source/protection checks and original slow checker explicitly superseded. Both native standing-retreat campaigns completed and every actual input/action/health/win/progression record verified. Observed native walking action0 showed missed jump opportunities and retreating flight stayed outside kick range; only physical walking eligibility and forward flight were changed in successor campaigns. Game bytes, identities, AI, difficulty, health, RNG, positions and stages unchanged. All unfinished original fidelity gates retained.',
  currentSourceBoundBossCampaigns=contexts,currentFreshStandingJumpCampaigns=fresh,
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in contexts.values()),
  currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in contexts.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+sum(c['actualKintaroRoundWins']for c in fresh.values()),
  currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+len(fresh),
  currentRealShaoKahnRoundWins=sum(c.get('actualShaoRoundWins',0)for c in contexts.values()),
  currentRealShaoKahnMatchClears=prior['currentRealShaoKahnMatchClears']+sum(c['actualShaoMatchClear']is not None for c in fresh.values()),
  currentFreshActualShaoRoundWins=sum(c['actualShaoRoundWins']for c in fresh.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in contexts.values()),
  currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in contexts.values()),
  actualFullLadderClearAccepted=any(c['fullCampaignClear']for c in fresh.values())or prior['actualFullLadderClearAccepted'],
  actualEndingsAccepted=False,fullEndingArtAudioAcceptance=False,gameSourceAndPlayableBytesChangedThisTurn=False,testAutomationSourceChangedThisTurn=True,
  nativeDifficultyHealthAIPositionStageRNGModified=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='The retreat approach earned Kano one and Sonya two separate Shao round wins; forward flight with walk0 eligibility earned none, so do not promote it as an improvement. Incoming retreat damage was concentrated in native walking action0 (Kano4835/Sonya3062), while every161/120 Shao Up plan actually reached native308. Test walking-eligible backward jumps without the unsuccessful forward-flight change; observe actual incoming damage, original motion and owned match outcomes. Complete natural full clears, own ending art/audio/return for both characters/both slots; retain all-arena move art, grounding, floor shadows, cleanup, audio, CPU/repeated/KO/overlap, all finishers/victims/morphs/secrets/cinematics, integrated UI/ladder/names regression and finished release ZIP. Required restored native dependency files remain protected. Actual single-round wins never substitute for match/ending acceptance.',
  inputHashes=pins)
 need(len(contexts)==66 and len(prior['remaining'])>=5,'Every original scope item and all accepted context provenance retained')
 return prior

if __name__=='__main__':
 need(not OUT.exists(),'Immutable full-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],acceptedPhysicalContexts=len(r['currentSourceBoundBossCampaigns']),actualFreshShaoRoundWins=r['currentFreshActualShaoRoundWins'],
  actualShaoMatchClears=r['currentRealShaoKahnMatchClears'],actualFullLadderClearAccepted=r['actualFullLadderClearAccepted'],gameChanged=False,fullPortAcceptance=False,finishedRelease=False),indent=2),flush=True)
