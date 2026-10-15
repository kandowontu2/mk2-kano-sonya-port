"""Distinguish observed paid continue from attempted but unproven challenger join."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_native_battle_audio_join_selection_runtime'
out=sync.ROOT/'audit_current_audio_selection_transition_classification'
assert not out.exists()
rows=chronology.load(folder/'run.log')
loss=next(r for r in rows['LOSS'] if r['frame']=='4206')
selection=rows['JOIN_SELECTION'][0]
assert selection['frame']=='4518'
state=next(r for r in rows['STATE'] if r['frame']=='4519')
assert state['mode']=='4' and state['states']=='0,3'
continued=next(r for r in rows['SELECT'] if r['frame']=='4519')
assert continued['continue']==loss['frame'] and continued['number']=='2'
ids=[r for r in rows['SELECT_ID'] if int(r['frame'])>4519]
assert ids and all(r['roster']=='9' and r['state']=='3' for r in ids)
proof=sync.ROOT/'audit_current_native_battle_audio_join_cold_channel_checked/report.json'
prior=json.loads(proof.read_text())
assert prior['passed'] and prior['logSHA256']==sync.sha(folder/'run.log')
report={'passedClassificationChecks':True,'transition':'P2 paid continue after native loss',
 'newP1ChallengerJoinProven':False,'bothAudioOwnersClearedInSelection':True,
 'battleFinishAudioChannelsStoppedInSelection':True,'selectorAudioFields':161,
 'continuedSonyaIdentityReselected':False,'controllerComputedRouteBeforeRosterInitialization':
 {'initialRoster':continued['initial'],'target':continued['target'],'route':continued['path'],
  'subsequentObservedRoster':9},
 'nextAction':'Compute continue navigation only after native selector initialization, then require actual target identity before confirmation. Challenger-join test needs separate accepted P1 state evidence.',
 'logSHA256':sync.sha(folder/'run.log'),'previousProofSHA256':sync.sha(proof),'fullPortAccepted':False}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
