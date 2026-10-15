"""Actual bicycle contacts and throw-damage timing, not throw catch geometry."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_sonya_p2_kunglao_midrange_bicycle_runtime'
out=sync.ROOT/'audit_current_sonya_p2_bicycle_recovery_exposure_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_sonya_p2_kunglao_midrange_bicycle_checked/report.json').read_text())
assert prior['finiteEvidenceVerified'] and prior['logSHA256']==sync.sha(case/'run.log')
rows=chronology.load(case/'run.log')
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='3' and r['entry']=='FFF9A400']
damage=rows['SONYA_KUNGLAO_DAMAGE']
contacts=[r for r in damage if r['victim_slot']=='1' and r['human_action']=='516' and r['a8']==r['human_actor'] and r['a13']==r['human_main']]
ages=[]
for r in damage:
    if r['victim_slot']!='2' or r['cpu_action']!='1287':continue
    preceding=[e for e in entries if int(e['frame'])<int(r['frame']) and e['actor']==r['human_actor'] and e['main']==r['human_main']]
    if preceding:ages.append(int(r['frame'])-max(int(e['frame']) for e in preceding))
report=dict(passed=True,ownedNativeBicycleEntries=len(entries),ownedBicycleAction516Contacts=len(contacts),ownedBicycleDamage=sum(int(r['before'])-int(r['after']) for r in contacts),
    throwDamageAgesAfterLatestSameOwnerBicycle=ages,throwInitiationAgeDirectlyObserved=False,fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
