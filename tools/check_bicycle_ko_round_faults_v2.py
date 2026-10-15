"""Bind the inherited input gate and retain all actual fault checks."""
import json,types
from pathlib import Path
import check_bicycle_ko_round_faults as original
current=original.current
model=types.SimpleNamespace(**dict(vars(original.model),prior=current.original.square.prior))
scope=dict(original.scope,__file__=__file__,model=model,original=original)
exec(compile(original.source,__file__+'::whole_actual_KO_fault_suite_inherited_input_binding','exec'),scope)
check=scope['check']

def additional_projectile_faults(c):
 out=model.ROOT/f"audit_bicycle_ko_projectile_faults_p{c['side']}";model.need(not out.exists(),'Fresh actual projectile counterexamples')
 original_gate=current.projectile_gate(c);faults=[]
 records=model.rows(c['text'],'MK2_FIREBALL_COUNTER_EVENT')
 selected=next(r for r in records if r['kind']=='contact'and r['id']=='1')
 for kind,key,value in (('collision','a0','FF8F3890'),('collision','pc','FF835460'),
                        ('contact','parentActor','01000000'),('contact','victimMain','01000000'),
                        ('contact','a7','FF8DE760'),('contact','a10','00000017'),
                        ('rectangles','a2','7FFF7FFF')):
  changed=original.original.faults.change(c['text'],'MK2_FIREBALL_COUNTER_EVENT',lambda r:r['kind']==kind and r['frame']==selected['frame']and r['a8']==selected['a8'],key,value)
  try:current.projectile_gate(dict(c,text=changed))
  except(ValueError,AssertionError,KeyError)as error:faults.append(dict(kind=kind,key=key,rejectedBy=str(error)))
  else:raise ValueError('Changed actual projectile branch admitted: '+key)
 model.need(current.projectile_gate(c)==original_gate,'Whole actual native projectile positive restored')
 proof=model.ROOT/f"audit_bicycle_launch_ko_round_checked_p{c['side']}/report.json"
 report=dict(passed=True,nativeTerminal=c['terminal'],actualFaultsRejected=faults,fullPortAcceptance=False,newNativeBoots=0,
  inputHashes={str(p):model.sha(p)for p in (Path(__file__),Path(original.__file__),Path(current.__file__),proof)})
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(side=c['side'],projectileFaults=len(faults))),flush=True)
 return report

def preserve_binding_failure(c):
 out=model.ROOT/'audit_bicycle_ko_fault_binding_rejection';model.need(not out.exists(),'Fresh preserved fault namespace rejection')
 report=dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error="AttributeError: 'types.SimpleNamespace' object has no attribute 'prior'",
  inputHashes={str(Path(original.__file__)):model.sha(original.__file__)},newNativeBoots=0,fullPortAcceptance=False)
 out.mkdir();(out/'failure.json').write_text(json.dumps(report,indent=2)+'\n')
