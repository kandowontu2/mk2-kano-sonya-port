"""Whole native acid gate for stock performer and independently bound added victims."""
import inspect
import json
import qualify_current_native_deadpool_roles as acid
import verify_native_source_sync as sync
sync.verify()
source=inspect.getsource(acid.check)
old="own=17 if fighter=='kano' else 18\n    victim=18 if own==17 else 17"
assert source.count(old)==1
out=sync.ROOT/'audit_current_native_deadpool_added_victims_checked'
assert not out.exists()
cases=[]
for victim,side in [(17,1),(18,2)]:
 namespace={}
 exec(compile(source.replace(old,f'own=8\n    victim={victim}'),'added_victim_gate','exec'),namespace)
 folder=sync.ROOT/f'audit_current_native_deadpool_victim_{victim}_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None
 records=acid.rows(folder/'run.log')
 result=namespace['check'](records,'subzero',side)
 selected=[r for tag,r in records if tag=='SELECT_ID']
 assert len(selected)==2 and all(r['actual']==r['target'] for r in selected)
 assert {int(r['actual']) for r in selected}=={8,victim}
 result.update(performerID=8,victimID=victim,physicalNativeSelection=True,
               logSHA256=sync.sha(folder/'run.log'))
 cases.append(result)
out.mkdir()
(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
 'allStockPerformersCovered':False,'continuousVictimVisualAudioAccepted':False,'fullPortAccepted':False},indent=2))
print('PASS stock Sub-Zero acid performer against real Kano and Sonya victims, normal retirement')
