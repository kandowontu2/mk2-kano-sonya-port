"""Reuse whole acid gate with independently specified stock victim ID8."""
import inspect
import json
import qualify_current_native_deadpool_roles as acid
import verify_native_source_sync as sync

sync.verify()
source=inspect.getsource(acid.check)
old="victim=18 if own==17 else 17"
assert source.count(old)==1
source=source.replace(old,'victim=8')
namespace={}
exec(compile(source,'stock_victim_pure_gate','exec'),namespace)
gate=namespace['check']
out=sync.ROOT/'audit_current_native_deadpool_stock_victim_checked'
assert not out.exists()
cases=[]
for fighter,side in [('kano',1),('sonya',2)]:
 folder=sync.ROOT/f'audit_current_native_deadpool_stock_{fighter}_p{side}_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None
 records=acid.rows(folder/'run.log')
 result=gate(records,fighter,side)
 selected=[r for tag,r in records if tag=='SELECT_ID']
 assert len(selected)==2
 assert any(r['actual']=='8' and r['target']=='8' and int(r['slot'])==3-side for r in selected)
 result.update(victimID=8,physicalNativeSelection=True,logSHA256=sync.sha(folder/'run.log'))
 bad=[(tag,dict(r)) for tag,r in records]
 for tag,r in bad:
  if tag=='FIELD' and r['own']!='00000000':r['victim_id']='1'
 try:gate(bad,fighter,side)
 except AssertionError:pass
 else:raise AssertionError('Wrong victim accepted')
 cases.append(result)
out.mkdir()
(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
 'wrongVictimFaultRejected':True,'allVictimsCovered':False,'fullPortAccepted':False},indent=2))
print('PASS both added performers vs naturally selected stock Sub-Zero; full native gates/retirement')
