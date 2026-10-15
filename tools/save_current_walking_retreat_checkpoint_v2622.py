"""Carry the full original objective and accepted walking-retreat evidence."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2606_current_standing_jump_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2623_current_walking_retreat_full_scope_checkpoint'

def need(ok,label):
 if not ok:raise ValueError(label)

def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active' and not prior['fullPortAcceptance'] and not prior['finishedRelease'] and len(prior['remaining'])>=5,'Full original unfinished objective')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS)
 def accept(path):
  r=json.loads(path.read_text());need(r['passed'] and not r['fullPortAcceptance'],'Accepted bounded actual proof '+str(path))
  for file,wanted in r['inputHashes'].items():
   need(file not in pins or pins[file]==wanted,'Consistent actual dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r
 contexts=dict(prior['currentSourceBoundBossCampaigns']);need(len(contexts)==66,'Exact previous accepted context inventory')
 source_path=ROOT/'audit_v2613_walking_retreat_source_boundary_checked/report.json';source=accept(source_path)
 need(source['fullSourceInverse'] and source['wholeLauncherInverse'] and source['wholeGuestAndPayloadReconstructed'] and len(source['rejectedSpecificSourceCounterexamples'])==8,'Exact physical-only predecessor boundary')
 fresh={}
 for fighter in ('kano','sonya'):
  case=f'{fighter}_shao_walking_retreat'
  proof_path=ROOT/f'audit_v2612_current_{fighter}_p1_shao_walking_retreat_checked/report.json'
  book_path=ROOT/f'audit_v2616_current_{fighter}_shao_walking_retreat_boss_ledger_checked/report.json'
  negative_path=ROOT/f'audit_v2617_current_{fighter}_shao_walking_retreat_input_counterexamples/report.json'
  progress_path=ROOT/f'audit_v2621_current_{fighter}_shao_walking_retreat_progress/report.json'
  proof,book,negative,progress=[accept(p)for p in (proof_path,book_path,negative_path,progress_path)]
  need(proof['bounded_campaign_evidence_proven'] and proof['human_slot']==1 and proof['bossPolicy']=='shao_walking_retreat','Matching true own physical campaign')
  need(book['rejectedSpecificCounterexamples']==8 and book['finalUnmodifiedControlPassed'] and negative['rejectedSpecificCounterexamples']==28 and negative['finalUnmodifiedFullCampaignControlPassed'],'Full actual ordered/input controls and specific negatives')
  need(progress['exactPreShaoNativeRecords']==(92646 if fighter=='kano' else 136135) and len(progress['rejectedSpecificPrefixCounterexamples'])==3 and progress['actualKintaroMatchClear'],'Every pre-Shao record unchanged and actual earned Kintaro match')
  need(progress['actualFullNativeCampaignAndReturnPath']==proof['unassisted_clear_proven'],'Actual full Shao/own-ending gate, never an individual round')
  need(case not in contexts,'Distinct physical successor context')
  entry={k:v for k,v in progress.items()if k not in ('inputHashes','scope')}
  entry.update(campaignReport=str(proof_path),ledgerReport=str(book_path),inputCounterexampleReport=str(negative_path),progressReport=str(progress_path),sourceBoundaryReport=str(source_path),
   capture=str(ROOT/f'audit_v2611_current_{fighter}_p1_shao_walking_retreat_campaign'),stagesReached=proof['stages_reached'],actualNativeHuman107Assignments=book['originalHuman107Assignments'],
   fullCampaignClear=proof['unassisted_clear_proven'],endingAccepted=False,fullEndingArtAudioAcceptance=False,repeatedKintaroControlNotIndependentStrategyCoverage=True)
  fresh[case]=entry;contexts[case]=entry
 individual={}
 for fighter in ('kano','sonya'):
  for policy in ('standing_retreat','standing_cross','walking_retreat'):
   path=ROOT/f'audit_v2625_current_{fighter}_{policy}_jump_correspondence_checked/report.json';r=accept(path)
   need(r['rejectedSpecificCounterexamples']==7 and r['finalUnmodifiedControlPassed'] and r['individuallyMatchedAssignments']==r['actualOriginal308Assignments'] and
    r['physicalJumpAttempts']==r['actualOriginal308Assignments']+r['attemptsWithoutNative308'] and r['actualOriginal308Assignments']==r['actualRisingFlightAttempts']+r['assignedWithoutObservedRisingFlight'],
    'Individual original jump assignment/motion correspondence; ignored and interrupted attempts separated')
   individual[f'{fighter}_{policy}']={k:v for k,v in r.items()if k not in ('inputHashes','scope','outcomes','matchedAttempts','unactivatedAttempts')}
   individual[f'{fighter}_{policy}']['report']=str(path)
 diagnostic_path=ROOT/'audit_v2627_current_shao_retreat_cooldown_diagnostic/report.json';diagnostic=accept(diagnostic_path)
 successor_path=ROOT/'audit_v2632_cooldown_retreat_source_boundary_checked/report.json';successor=accept(successor_path)
 need(successor['fullSourceInverse'] and successor['wholeLauncherInverse'] and successor['wholeGuestAndPayloadReconstructed'] and len(successor['rejectedSpecificSourceCounterexamples'])==9,'Exact physical-only 60-to48 successor; game unchanged')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating complete preserved/current graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed authoritative dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification='no progress: user-requested status only',
  thisGoalTurnClassification='progress: both whole walking-retreat campaigns, eight ordered and twenty-eight full input negatives per fighter and exact ordinary/Kintaro prefixes accepted. Six campaigns have per-plan original jump assignments and real rising-flight correspondence, including ignored/interrupted attempts. Actual grounded48-to59 cooldown damage identified a physical-controller wait; a sole stage16 60-to48 successor boundary passed. Playable game bytes, AI, difficulty, health, IDs, positions, RNG and all original unfinished gates unchanged.',
  currentSourceBoundBossCampaigns=contexts,currentFreshWalkingRetreatCampaigns=fresh,currentActualIndividualJumpCorrespondence=individual,oldAggregateJumpActivationClaimNowIndividuallyVerified=True,
  currentMeasuredRetreatCooldownDiagnostic=diagnostic['cases'],currentMeasuredRetreatCooldownReport=str(diagnostic_path),currentCooldownRetreatSuccessorSourceBoundary=str(successor_path),
  currentActualBossHuman107Assignments=sum(c['actualNativeHuman107Assignments']for c in contexts.values()),currentActualBossUppercutDamage=sum(c['ownBossUppercutDamage']for c in contexts.values()),
  currentRealKintaroRoundWins=prior['currentRealKintaroRoundWins']+sum(c['actualKintaroRoundWins']for c in fresh.values()),currentRealKintaroMatchClears=prior['currentRealKintaroMatchClears']+len(fresh),
  repeatedKintaroMatchReplaysNotNewIndependentOrdinaryOrKintaroStrategyCoverage=True,currentRealShaoKahnRoundWins=sum(c.get('actualShaoRoundWins',0)for c in contexts.values()),
  currentRealShaoKahnMatchClears=prior['currentRealShaoKahnMatchClears']+sum(c['actualShaoMatchClear']is not None for c in fresh.values()),currentFreshActualShaoRoundWins=sum(c['actualShaoRoundWins']for c in fresh.values()),
  currentBossLedgerCounterexamples=sum(c['rejectedSpecificLedgerCounterexamples']for c in contexts.values()),currentBossPhysicalInputCounterexamples=sum(c.get('rejectedSpecificInputCounterexamples',0)for c in contexts.values()),
  actualFullLadderClearAccepted=prior['actualFullLadderClearAccepted']or any(c['fullCampaignClear']for c in fresh.values()),actualEndingsAccepted=False,fullEndingArtAudioAcceptance=False,
  gameSourceAndPlayableBytesChangedThisTurn=False,testAutomationSourceChangedThisTurn=True,nativeDifficultyHealthAIPositionStageRNGModified=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Collect and independently verify the exact cooldown-retreat campaigns already running; shortening physical cooldown is not an assumed improvement. A native jump store, actual flight and an earned full match are distinct gates. Complete natural full clears, own ending art/audio/return for both characters/both slots. Retain all-arena move art, grounding, floor shadows, cleanup, audio, CPU/repeated/KO/overlap, all finishers/victims/morphs/secrets/cinematics, integrated UI/ladder/names regression and a finished release ZIP. Required restored native history remains protected.',inputHashes=pins)
 need(len(contexts)==68 and len(prior['remaining'])>=5,'All original gates and accepted provenance retained')
 return prior

if __name__=='__main__':
 need(not OUT.exists(),'Immutable full-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],acceptedPhysicalContexts=len(r['currentSourceBoundBossCampaigns']),actualFreshShaoRoundWins=r['currentFreshActualShaoRoundWins'],
  actualShaoMatchClears=r['currentRealShaoKahnMatchClears'],actualFullLadderClearAccepted=r['actualFullLadderClearAccepted'],gameChanged=False,fullPortAcceptance=False,finishedRelease=False),indent=2),flush=True)
