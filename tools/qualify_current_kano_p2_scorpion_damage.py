"""Observer-neutral native damage evidence, not campaign acceptance."""
import json
from collections import defaultdict
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_scorpion_damage_runtime'
out=sync.ROOT/'audit_current_kano_p2_scorpion_damage_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_p2_scorpion_damage_preparation/campaign.lua')
assert not (case/'stderr.log').read_text().strip()
rows=chronology.load(case/'run.log')
old=chronology.load(sync.ROOT/'audit_current_kano_p2_campaign_32000_runtime/run.log')
extra='KANO_P2_SCORPION_DAMAGE'
for tag in set(rows)|set(old):
    if tag!=extra: assert rows.get(tag,[])==old.get(tag,[]),tag
assert rows['RESULT'][0]['frame']=='32000'
assert all(r['human']=='17:17' for r in rows['LIVE']+rows['FIGHT'])
assert all(r['writes']=='0' and r['assistance']=='none' for group in rows.values() for r in group)
stages=chronology.check(rows,2,17,list(range(13))+[14,15,16])
damage=rows[extra]; assert damage
totals=defaultdict(int);counts=defaultdict(int)
for r in damage:
    assert r['ids']=='3,17' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main']
    amount=int(r['before'])-int(r['after']);assert 0<amount<=161
    key='victim'+r['victim_slot']+'_actions'+r['actions']
    totals[key]+=amount;counts[key]+=1
out.mkdir()
report=dict(passiveObserverNeutral=True,earnedStages=stages,terminal=terminal,
    damageBySimultaneousActions=dict(totals),contactCounts=dict(counts),
    interpretation='Actions are sampled at native HP write; projectile creator ownership not established by these fields alone.',
    fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
