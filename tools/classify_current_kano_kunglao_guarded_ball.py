"""Owned ball launches/contact and finite opponent outcome; source controller caveat."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kunglao_guarded_ball_runtime'
out=sync.ROOT/'audit_current_kano_kunglao_guarded_ball_classified'
assert not out.exists()
rows=chronology.load(folder/'run.log')
entries=rows.get('KANO_KUNGLAO_NATIVE_BALL',[])
assert entries and all(r['id']=='17' and r['owner']==r['actor'] and r['pc']=='FFFFDE10' for r in entries)
damage=rows['KUNGLAO_DAMAGE_DETAIL']
contacts=[r for r in damage if r['victim_slot']=='2' and r['actions'].split(',')[0]=='523' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
assert contacts
incoming={}
for r in damage:
    if r['victim_slot']=='1':
        action=r['actions'].split(',')[1]
        item=incoming.setdefault(action,dict(callbacks=0,damage=0))
        item['callbacks']+=1;item['damage']+=int(r['before'])-int(r['after'])
wins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage']=='4']
source=(sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
assert 'ball_movi(1, 0x020b);' in source
controller=(sync.ROOT/'audit_current_kano_kunglao_guarded_ball_preparation/campaign.lua').read_text()
assert 'human.action~=531 and frame-kb_release>=12' in controller
report=dict(passedOwnedBallObservation=True,nativeEntries=len(entries),nativeOwnBallContacts=contacts,totalOutgoingNativeDamage=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),incomingByCpuActionAtCallback=incoming,ownKungLaoRoundWins=wins,logSHA256=sync.sha(folder/'run.log'),testControllerCaveat='Post-release branch excludes531, but current ball action is0x20b=523. Down/Block are therefore requested during some native ball fields. Executed case preserved; correct this in successor, not game code.',fullCampaignClear=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(entries=len(entries),nativeOwnBallContacts=len(contacts),outgoing=report['totalOutgoingNativeDamage'],incoming=incoming,ownRounds=len(wins))))
