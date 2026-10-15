"""Retain all original gates and actual current Friendship restriction evidence."""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_current_interrupt_v1870 as launch
ROOT=launch.ROOT
PREVIOUS=ROOT/'audit_v2662_current_cooldown_friendship_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v2666_current_friendship_restrictions_full_scope_checkpoint'

def need(ok,label):
 if not ok:raise ValueError(label)

def save():
 prior=json.loads(PREVIOUS.read_text())
 need(prior['goalStatus']=='active'and not prior['fullPortAcceptance']and not prior['finishedRelease']and len(prior['currentSourceBoundBossCampaigns'])==70 and len(prior['remaining'])>=5,'Full original unfinished goal and current evidence retained')
 pins=dict(prior['inputHashes']);pins[str(PREVIOUS)]=launch.sha(PREVIOUS);restrictions={}
 for fighter in ('kano','sonya'):
  for side in (1,2):
   for command_case in ('wrong_command','punch_used'):
    path=ROOT/f'audit_v2664_current_{fighter}_friendship_{command_case}_p{side}_checked/report.json'
    r=json.loads(path.read_text())
    need(r['passed']and r['commandCase']==command_case and r['actualPhysicalFriendshipRestrictionAccepted']and not r['actualUnwantedActivation']and r['action']==-1 and
     r['currentWholeGuestAndPayloadReconstructed']and r['originalFriendshipRowsPreserved']==17 and r['observedOriginalOwnWinnerDispatches']==2 and
     r['rejectedSpecificCounterexamples']==8 and r['finalUnmodifiedControlPassed']and not r['fullFinisherAcceptance']and not r['fullPortAcceptance'],'Exact current physical invalid-command/no-punch restriction and normal native next-screen return')
    for file,wanted in r['inputHashes'].items():
     need(file not in pins or pins[file]==wanted,'Consistent actual dependency '+file);pins[file]=wanted
    pins[str(path)]=launch.sha(path)
    key=f'{fighter}_{command_case}_p{side}'
    restrictions[key]={k:v for k,v in r.items()if k not in ('inputHashes','scope','outcomes')};restrictions[key]['report']=str(path)
 need(len(restrictions)==8,'Every fighter/slot/restriction combination actually accepted')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 print('Revalidating complete preserved/current graph:',len(pins),'actual files',flush=True)
 with ThreadPoolExecutor(max_workers=4)as pool:
  for index,((file,wanted),actual)in enumerate(zip(pins.items(),pool.map(launch.sha,pins)),1):
   need(actual==wanted,'Changed authoritative dependency '+file)
   if index%5000==0:print('Verified',index,'actual dependencies',flush=True)
 prior.update(previousCheckpoint=str(PREVIOUS),
  thisGoalTurnClassification='progress: both cooldown-retreat campaigns fully accepted, six fresh separate natural Shao rounds but no match/ending; two verifier-only defects retained and corrected full controls repeated. Four current-build earned Friendships and eight real wrong-command/no-punch restriction cases cover both fighters/both slots.112 specific Friendship counterexamples and14 bubble reference phase matches accepted. Every original unfinished art, shadow, audio, arena, finisher, victim, morph, secret, cinematic, ending, integrated UI and finished-release gate remains open as appropriate. Game bytes/settings unchanged.',
  currentPhysicalFriendshipRestrictionCases=restrictions,currentPhysicalFriendshipRestrictionCounterexamples=64,
  currentFriendshipPositiveAndRestrictionCases=12,currentFriendshipSpecificCounterexamples=112,
  currentFriendshipCompleteSceneRasterShadowAudioAccepted=False,gameSourceAndPlayableBytesChangedThisTurn=False,
  nativeDifficultyHealthAIPositionStageRNGModified=False,actualEndingsAccepted=False,fullPortAcceptance=False,finishedRelease=False,goalStatus='active',
  nextAction='Extend the current12 Friendship cases to complete native scene pixels, floor shadows/cleanup and audio, retaining original references and actual ownership. Cooldown-retreat earned Kano4/Sonya2 separate Shao rounds, not full matches; full natural boss clears and own ending art/audio/return remain required for both fighters/both slots without game assistance. Continue all original move-phase, arena, CPU/repeated/KO/overlap, finisher/victim/morph/secret/cinematic, integrated UI/ladder/names/audio and finished release gates. Required historical native dependencies remain protected.',inputHashes=pins)
 return prior

if __name__=='__main__':
 need(not OUT.exists(),'Immutable full original-scope checkpoint')
 r=save();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(goalStatus=r['goalStatus'],acceptedPhysicalContexts=len(r['currentSourceBoundBossCampaigns']),currentFriendshipCases=r['currentFriendshipPositiveAndRestrictionCases'],
  friendshipSpecificCounterexamples=r['currentFriendshipSpecificCounterexamples'],actualShaoMatchClears=r['currentRealShaoKahnMatchClears'],actualEndingsAccepted=False,
  fullPortAcceptance=False,finishedRelease=False,gameChanged=False),indent=2),flush=True)
