"""Classify actual unaccepted challenger input and preserve scalar-equivalent control."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_native_challenger_join_delay_runtime'
out=sync.ROOT/'audit_current_native_challenger_delay_checked';assert not out.exists()
rows=chronology.load(folder/'run.log')
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert [(r['button'],int(r['age'])) for r in rows['JOIN_INPUT']]==[('Coin_1',n) for n in range(1,5)]+[('Start_1',n) for n in range(24,28)]
assert rows['JOIN_SELECTION'][0]['frame']=='4518' and rows['LOSS'][0]['frame']=='4206'
assert not any(r['p1']=='3' for r in rows['JOIN_PLAYER_STATE'])
prior=chronology.load(sync.ROOT/'audit_current_native_battle_audio_join_selection_runtime/run.log')
for tag in set(rows)|set(prior):
 if tag in ('JOIN_INPUT','JOIN_PLAYER_STATE'):continue
 assert rows.get(tag,[])==prior.get(tag,[])
report={'passedObservationChecks':True,'normalRunCompleted':True,'challengerJoinAccepted':False,
 'P2ContinueStillObserved':True,'otherScalarTraceExact':True,'logSHA256':sync.sha(folder/'run.log'),
 'fieldLabelCorrection':"JOIN_PLAYER_STATE credits field is a raw IN1 port read, not a stored credit count; do not use it as credit evidence.",
 'nextAction':'Compare physical join after round-introduction completion against a naturally selected stock CPU control; do not infer an added-character defect from this early-input probe.',
 'fullPortAccepted':False}
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
