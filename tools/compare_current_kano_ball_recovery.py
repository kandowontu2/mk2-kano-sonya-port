"""Read actual native state/contact ledgers; input differences aren't gameplay wins."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_kano_ball_recovery_comparison'
assert not out.exists()
folders=[sync.ROOT/('audit_current_kano_kunglao_'+name+'_runtime') for name in ('guarded_ball','ball_recovery_fixed')]
old,new=[chronology.load(f/'run.log') for f in folders]
for tag in set(old)|set(new):
    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in old.get(tag,[]) if int(r['frame'])<18097]==[r for r in new.get(tag,[]) if int(r['frame'])<18097],tag
cases=[]
for folder,rows in zip(folders,(old,new)):
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    entries=rows.get('KANO_KUNGLAO_NATIVE_BALL',[])
    assert entries and all(r['id']=='17' and r['actor']==r['owner'] for r in entries)
    damage=rows['KUNGLAO_DAMAGE_DETAIL']
    ownwins=[r for r in rows['WIN'] if r['stage']=='4' and r['slot']=='1']
    cases.append(dict(case=folder.name,nativeBallEntries=len(entries),ownKungLaoWins=ownwins,outgoing=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),incoming=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),stages=[int(r['stage']) for r in rows['STAGE']],terminal=terminal,logSHA256=sync.sha(folder/'run.log')))
tags=('STATE','LIVE','STAGE','WIN','LOSS','HEALTH','KUNGLAO_ACTION_CHANGE','KUNGLAO_DAMAGE_DETAIL','KANO_KUNGLAO_NATIVE_BALL')
equal={tag:old.get(tag,[])==new.get(tag,[]) for tag in tags}
report=dict(comparisonCompleted=True,priorProductiveRouteExact=True,cases=cases,nativeLedgerEquality=equal,allComparedNativeLedgersIdentical=all(equal.values()),physicalInputDigestChanged=old['INPUT_DIGEST_FINAL']!=new['INPUT_DIGEST_FINAL'],gameSourcesChanged=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(comparisonCompleted=True,nativeLedgersIdentical=all(equal.values()),cases=[{k:r[k] for k in ('nativeBallEntries','outgoing','incoming','ownKungLaoWins','stages')} for r in cases])))
