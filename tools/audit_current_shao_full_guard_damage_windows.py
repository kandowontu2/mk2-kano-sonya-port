"""Classify observed damage windows; no guest execution or writes."""
import json,re
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
log=root/'audit_current_kano_p2_shao_upper_full_recovery_guard_runtime/run.log'
out=root/'audit_current_shao_full_guard_damage_windows_checked'
assert not out.exists()
counts=Counter();hp=Counter();examples={};locked=False
for line in log.open():
    if not line.startswith('MK2_NAT_CAMPAIGN_'):continue
    tag=line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
    if tag=='FIGHT':locked=False
    if tag=='BOSS_ACTION' and r.get('stage')=='16' and r.get('id')=='17' and r.get('after')=='263':locked=True
    if tag=='SHAO_UPPER_RECOVERED_RELEASE':locked=False
    if tag!='SHAO_UPPER_DAMAGE' or r.get('victim_slot')!='2':continue
    key=('after_upper_before_recovered_release' if locked else 'outside_observed_upper_recovery')+':action'+r['human_action']
    counts[key]+=1;hp[key]+=int(r['before'])-int(r['after'])
    examples.setdefault(key,r)
assert sum(hp.values())==6601
report=dict(logSHA256=sync.sha(log),incomingEvents=dict(counts),incomingHP=dict(hp),firstExamples=examples,
    caveats=['Native action write precedes next controller sampling; windows do not prove exact button state at collision.',
    'Damage callback action is not necessarily pre-hit idle; CPU771 may be an active stock attack.',
    'This is one failed controller strategy, not proof of character defect or full campaign acceptance.'],fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(incomingEvents=dict(counts),incomingHP=dict(hp))))
