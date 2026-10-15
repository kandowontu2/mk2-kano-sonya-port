"""Actual action259 starts and native own damage, not requested-button counts."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kunglao_early_counter_runtime'
out=sync.ROOT/'audit_current_kano_kunglao_early_counter_classified'
assert not out.exists()
rows=chronology.load(folder/'run.log')
assert all(r['ids']=='17,0' for r in rows['KUNGLAO_ACTION_CHANGE']+rows['KUNGLAO_DAMAGE_DETAIL'])
starts=[];previous=None
for r in rows['KUNGLAO_ACTION_CHANGE']:
    current=(r['p1_main'],r['actions'].split(',')[0])
    if current[1]=='259' and current!=previous:starts.append(r)
    previous=current
contacts=[r for r in rows['KUNGLAO_DAMAGE_DETAIL'] if r['victim_slot']=='2' and r['actions'].split(',')[0]=='259' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
assert starts and contacts
wins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage']=='4']
outgoing=sum(int(r['before'])-int(r['after']) for r in rows['KUNGLAO_DAMAGE_DETAIL'] if r['victim_slot']=='2')
incoming=sum(int(r['before'])-int(r['after']) for r in rows['KUNGLAO_DAMAGE_DETAIL'] if r['victim_slot']=='1')
report=dict(passedNativeActivationAndContact=True,standingHighKickStarts=starts,nativeOwnHighKickDamageCallbacks=contacts,totalOutgoingNativeDamage=outgoing,totalIncomingNativeDamage=incoming,ownKungLaoRoundWins=wins,observedStages=[int(r['stage']) for r in rows['STAGE']],logSHA256=sync.sha(folder/'run.log'),fullCampaignClear=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(nativeStandingKickStarts=len(starts),nativeOwnKickContacts=len(contacts),outgoing=outgoing,incoming=incoming,ownKungLaoRounds=len(wins))))
