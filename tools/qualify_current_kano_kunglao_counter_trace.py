"""Observer neutrality and counter-action windows, no semantic guesswork."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_kano_kunglao_counter_trace_runtime'
out=sync.ROOT/'audit_current_kano_kunglao_counter_trace_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (folder/'stderr.log').read_text().strip()
new=chronology.load(folder/'run.log')
old=chronology.load(sync.ROOT/'audit_current_kano_kunglao_stance_counter_runtime/run.log')
for tag in set(new)|set(old):
    if tag in ('KUNGLAO_DAMAGE_DETAIL','KUNGLAO_ACTION_CHANGE','RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):continue
    assert [r for r in new.get(tag,[]) if int(r['frame'])<19500]==[r for r in old.get(tag,[]) if int(r['frame'])<19500],tag
assert new['RESULT'][0]['frame']=='19500'
assert all(r['ids']=='17,0' for r in new['KUNGLAO_ACTION_CHANGE']+new['KUNGLAO_DAMAGE_DETAIL'])
windows=[]
for r in new.get('KANO_KUNGLAO_COUNTER',[]):
    actions=[a for a in new['KUNGLAO_ACTION_CHANGE'] if int(r['frame'])<=int(a['frame'])<int(r['frame'])+40]
    windows.append(dict(request=r,actionChangesWithin40=actions))
report=dict(passedObserverNeutrality=True,entirePriorInputAndOrdinaryPrefixExact=True,requestWindows=windows,nativeDamageDetails=new['KUNGLAO_DAMAGE_DETAIL'],actionChanges=len(new['KUNGLAO_ACTION_CHANGE']),terminal=terminal,logSHA256=sync.sha(folder/'run.log'),fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(dict(passed=True,requests=len(windows),actionChanges=len(new['KUNGLAO_ACTION_CHANGE']))))
