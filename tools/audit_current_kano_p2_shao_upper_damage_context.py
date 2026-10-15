"""Direct owned upper damage and incoming state context; no strategy-success claim."""
import json
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;out=root/'audit_current_kano_p2_shao_upper_damage_context_checked'
assert not out.exists()
path=root/'audit_current_kano_p2_shao_upper_contact_bounded180_checked/upper-contact.json'
data=json.loads(path.read_text());assert data['shaoObserved']
outgoing=[r for r in data['actualNativeDamage'] if r['victim_slot']=='1']
incoming=[r for r in data['actualNativeDamage'] if r['victim_slot']=='2']
assert outgoing and all(r['human_action']=='263' and r['a8']==r['human_actor'] and r['a13']==r['human_main'] and r['pc']=='FF836700' for r in outgoing)
def sums(records,key):
    c=Counter()
    for r in records:c[key(r)]+=int(r['before'])-int(r['after'])
    return dict(c)
report=dict(passedFiniteDamageChecks=True,actualOwnedUpperStateEntries=len(data['actualOwnedUpperStateEntries']),actualDirectUpperHitRecords=len(outgoing),upperDamageValues=dict(Counter(int(r['before'])-int(r['after']) for r in outgoing)),outgoingHP=data['outgoingHP'],incomingHP=data['incomingHP'],incomingHumanActionContext=sums(incoming,lambda r:r['human_action']),incomingCpuHumanContext=sums(incoming,lambda r:r['cpu_action']+':'+r['human_action']),incomingZeroActionDoesNotProvePreHitIdle=True,campaignStrategyAdopted=False,fullPortAccepted=False,inputReportSHA256=sync.sha(path))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
