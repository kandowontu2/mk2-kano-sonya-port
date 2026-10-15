"""Strict selection and native-health ledger for the current bounded attempt."""
import json
from collections import Counter
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kitana_confirmed_jump_runtime'
rows=chronology.load(folder/'run.log')
assert all(r['roster']=='17' for r in rows['SELECT_ID'])
assert all(r['human']=='17:17' for r in rows['LIVE'])
live=[r for r in rows['LIVE'] if r['stage']=='3' and r['cpu']=='4:4']
assert live
actions=Counter(r['actions'].split(',')[0] for r in live)
cpu=Counter(r['actions'].split(',')[1] for r in live)
damage=[r for r in rows['HEALTH'] if r.get('stage')=='3' and r.get('pc')=='FF836700' and int(r['after'])<int(r['before'])]
by_slot={s:dict(Counter(int(r['before'])-int(r['after']) for r in damage if r.get('slot')==s)) for s in ('1','2')}
report=dict(logSHA256=sync.sha(folder/'run.log'),strictIdentityChecksPassed=True,
 stage3SampleCount=len(live),humanActionCounts=dict(actions),cpuActionCounts=dict(cpu),
 damageRows=damage,nativeDamageAmountsBySlot=by_slot,
 jumpRequests=len(rows.get('KANO_KITANA_CONFIRMED_JUMP_ATTEMPT',[])),
 jumpStartupAcceptances=len(rows.get('KANO_KITANA_JUMP_ACCEPTED',[])),
 kitanaRoundWins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage']=='3'],
 exactDamageSourceAttributionProven=False,fullCampaignClear=False,fullPortAccepted=False)
out=sync.ROOT/'audit_current_kano_kitana_attempt_classified'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='damageRows'},indent=2))
