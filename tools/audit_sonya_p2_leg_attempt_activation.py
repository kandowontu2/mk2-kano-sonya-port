"""Bounded retained-log analysis; plans are not move activations or hits."""
import json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT
case=root/'audit_current_sonya_p2_kunglao_leg_attack_guard_runtime'
out=root/'audit_current_sonya_p2_leg_attempt_activation_checked'
assert not out.exists()
rows=[]
for line in (case/'run.log').read_text().splitlines():
    match=re.match(r'MK2_NAT_CAMPAIGN_(\S+) (.*)',line)
    if match:
        row=dict(re.findall(r'(\w+)=([^ ]+)',match[2]));row['kind']=match[1]
        if row.get('stage')=='3':rows.append(row)
plans=[r for r in rows if r['kind']=='KUNGLAO_GUARD_ATTEMPT']
entries=[r for r in rows if r['kind']=='SPECIAL' and r.get('move')=='leg']
damage=[r for r in rows if r['kind']=='SONYA_KUNGLAO_DAMAGE' and r.get('victim_slot')=='2']
assert plans and entries and damage
assert all(r['id']=='18' and r['roster']=='18' and r['a8']==r['actor'] and r['a13']==r['main'] for r in entries)
results=[]
for plan in plans:
    frame=int(plan['frame'])
    moves=[r for r in entries if 0<=int(r['frame'])-frame<12]
    hits=[r for r in damage if 0<=int(r['frame'])-frame<12]
    results.append(dict(planFrame=frame,gap=int(plan['gap']),nativeEntries=[int(r['frame']) for r in moves],incomingWithinCommand=[dict(frame=int(r['frame']),cpuAction=int(r['cpu_action']),humanAction=int(r['human_action']),damage=int(r['before'])-int(r['after'])) for r in hits]))
assert len({f for r in results for f in r['nativeEntries']})==len(entries)
report=dict(passedFiniteLogChecks=True,logSHA256=sync.sha(case/'run.log'),plannedCommands=len(plans),nativeOwnedEntries=len(entries),plansWithoutObservedEntry=sum(not r['nativeEntries'] for r in results),plansDamagedBeforeObservedEntry=sum(bool(r['incomingWithinCommand']) and (not r['nativeEntries'] or min(d['frame'] for d in r['incomingWithinCommand'])<min(r['nativeEntries'])) for r in results),results=results,parserRejectionCauseDirectlyObserved=False,moveContactsNotInferred=True,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'}))
