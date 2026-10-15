"""Native health ledger, scoped by observed stage4 arrival; no attack attribution."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kunglao_stance_counter_runtime'
out=sync.ROOT/'audit_current_kano_kunglao_stance_counter_classified'
assert not out.exists()
rows=chronology.load(folder/'run.log')
cut=int(next(r['frame'] for r in rows['STAGE'] if r['stage']=='4'))
assert not any(int(r['stage'])>4 for r in rows['STAGE'])
health=[r for r in rows.get('HEALTH',[]) if int(r['frame'])>=cut and r['pc']=='FF836700' and int(r['before'])>int(r['after'])]
requests=rows.get('KANO_KUNGLAO_COUNTER',[])
windows=[]
for r in requests:
    hits=[h for h in health if int(r['frame'])<=int(h['frame'])<int(r['frame'])+32]
    windows.append(dict(request=r,nativeHealthWritesWithin32Fields=hits))
ownwins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage']=='4']
outgoing=sum(int(h['before'])-int(h['after']) for h in health if h['slot']=='2')
incoming=sum(int(h['before'])-int(h['after']) for h in health if h['slot']=='1')
assert len(requests)==10 and outgoing==0 and not ownwins
report=dict(passedObservation=True,requests=len(requests),requestWindows=windows,allNativeOutgoingDamage=outgoing,allNativeIncomingDamage=incoming,ownKungLaoRoundWins=ownwins,logSHA256=sync.sha(folder/'run.log'),strategyImprovementAccepted=False,attackSourceAttribution=False,gameDefectEstablished=False,nextAction='Observe exact owned action changes and victim health callback context around counter requests; do not rerun this guard/HK timing unchanged.',fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(requests=len(requests),outgoing=outgoing,incoming=incoming,strategyImprovementAccepted=False)))
