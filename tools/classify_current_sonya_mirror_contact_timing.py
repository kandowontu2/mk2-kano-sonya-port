"""Compare actual native HK starts/contact timing in the best finite melee run."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_mirror_neutral_recovery_runtime'
out=sync.ROOT/'audit_current_sonya_mirror_contact_timing'
assert not out.exists()
rows=chronology.load(folder/'run.log')
starts=[];previous=None
for r in rows['MIRROR_STANDING_ACTION']:
    current=(r['p1_main'],r['actions'].split(',')[0])
    if current[1]=='259' and current!=previous:starts.append(r)
    previous=current
requests=rows['MIRROR_STANDING_COUNTER']
groups={};windows=[]
for request in requests:
    begin=int(request['frame']);end=begin+32
    changes=[r for r in starts if begin<=int(r['frame'])<end]
    damage=[r for r in rows['MIRROR_STANDING_DAMAGE'] if begin<=int(r['frame'])<end]
    own=[r for r in damage if r['victim_slot']=='2' and r['actions'].split(',')[0]=='259' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
    incoming=[r for r in damage if r['victim_slot']=='1']
    group=groups.setdefault(request['action'],dict(requests=0,activated=0,contacts=0,outgoing=0,incoming=0,startAges=[],contactAges=[]))
    group['requests']+=1;group['activated']+=bool(changes);group['contacts']+=len(own)
    group['outgoing']+=sum(int(r['before'])-int(r['after']) for r in own)
    group['incoming']+=sum(int(r['before'])-int(r['after']) for r in incoming)
    group['startAges'] += [int(r['frame'])-begin for r in changes]
    group['contactAges'] += [int(r['frame'])-begin for r in own]
    windows.append(dict(request=request,starts=changes,ownContacts=own,incoming=incoming))
assert len(starts)==29
out.mkdir();report=dict(groups=groups,windows=windows,requestWindowFields=32,
    exactAttackSourceForAllIncomingProven=False,fullPortAccepted=False,logSHA256=sync.sha(folder/'run.log'))
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(groups))
