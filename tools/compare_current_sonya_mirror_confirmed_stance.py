"""Compare actual state handoffs and contacts; retain productive prior controller."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_sonya_mirror_confirmed_stance_comparison'
assert not out.exists()
cases=[]
for name in ('standing_counter','confirmed_stance'):
    folder=sync.ROOT/('audit_current_sonya_mirror_'+name+'_runtime')
    rows=chronology.load(folder/'run.log')
    starts=[];previous=None
    for r in rows['MIRROR_STANDING_ACTION']:
        current=(r['p1_main'],r['actions'].split(',')[0])
        if current[1]=='259' and current!=previous:starts.append(r)
        previous=current
    damage=rows['MIRROR_STANDING_DAMAGE']
    contacts=[r for r in damage if r['victim_slot']=='2' and r['actions'].split(',')[0]=='259' and r['a8']==r['p1_actor'] and r['a13']==r['p1_main']]
    accepted=rows.get('MIRROR_STAND_ACCEPTED',[])
    assert all(r['action'] in ('0','771','772') and int(r['flags'],16)&0x1c==0 for r in accepted)
    cancellations=rows.get('MIRROR_STAND_CANCEL',[])
    cases.append(dict(case=name,nativeKickStarts=len(starts),nativeOwnKickContacts=len(contacts),outgoing=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),incoming=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),ownMirrorWins=[r for r in rows['WIN'] if r['stage']=='5' and r['slot']=='1'],standingPreparations=len(rows.get('MIRROR_STAND_PREPARE',[])),confirmedStandingAcceptances=accepted,standingCancellations=cancellations,logSHA256=sync.sha(folder/'run.log')))
assert len(cases[0]['ownMirrorWins'])==1 and not cases[1]['ownMirrorWins']
out.mkdir();(out/'report.json').write_text(json.dumps(dict(comparisonCompleted=True,cases=cases,successorImprovementAccepted=False,priorProductiveControllerRetained=True,exactParserRejectReasonProven=False,fullPortAccepted=False),indent=2))
print(json.dumps([{k:r[k] for k in ('case','nativeKickStarts','nativeOwnKickContacts','outgoing','incoming','standingPreparations')}|dict(accepted=len(r['confirmedStandingAcceptances']),cancelled=len(r['standingCancellations']),ownRounds=len(r['ownMirrorWins'])) for r in cases]))
