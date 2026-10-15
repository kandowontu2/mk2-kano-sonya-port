"""Native same-ID mirror normal-contact ownership and finite actual win."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_standing_counter_runtime'
out=sync.ROOT/'audit_current_sonya_mirror_standing_counter_classified'
assert not out.exists()
rows=chronology.load(folder/'run.log')
assert all(r['ids']=='18,18' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main'] for r in rows['MIRROR_STANDING_ACTION']+rows['MIRROR_STANDING_DAMAGE'])
starts=[];previous=None
for r in rows['MIRROR_STANDING_ACTION']:
    current=(r['p1_main'],r['actions'].split(',')[0])
    if current[1]=='259' and current!=previous:starts.append(r)
    previous=current
damage=rows['MIRROR_STANDING_DAMAGE']
contacts=[r for r in damage if r['victim_slot']=='2' and r['actions'].split(',')[0]=='259' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
assert starts and contacts
wins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage']=='5']
assert len(wins)==1 and wins[0]['frame']=='19008' and wins[0]['health']=='28,0' and wins[0]['id']=='18' and wins[0]['entry']=='FFFEFA40'
incoming={}
for r in damage:
    if r['victim_slot']=='1':
        action=r['actions'].split(',')[1]
        item=incoming.setdefault(action,dict(callbacks=0,damage=0))
        item['callbacks']+=1;item['damage']+=int(r['before'])-int(r['after'])
report=dict(passedNativeMirrorContactAndRoundWin=True,actualStandingKickStarts=len(starts),nativeOwnKickDamageCallbacks=contacts,totalOutgoingNativeDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),incomingByCpuActionAtCallback=incoming,ownMirrorRoundWins=wins,logSHA256=sync.sha(folder/'run.log'),mirrorMatchCleared=False,fullCampaignClear=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(nativeKickStarts=len(starts),nativeOwnKickContacts=len(contacts),outgoing=report['totalOutgoingNativeDamage'],incoming=incoming,ownMirrorRoundWin=wins[0])))
