"""Entire6069 gate with its generated-function module/local-name collision fixed.

Keep the original16 catches, every native field and body/shadow parent proof.
Add actual landing-pose and deferred horizontal-publication negative controls.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_air_native_landing_v6069 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
OUT=ROOT/'audit_v6072_current_air_native_phase_scope_checked'

def check(b,guest,payload):
 source=inspect.getsource(earlier.check)
 before=" scope=dict(prior.check.__globals__,prior=prior,landing_pose=landing_pose,"
 after=" source=source.replace('prior.signed(', 'signed(').replace('prior.h(', 'h(')\n"+before
 need(source.count(before)==1,'Exact generated phase helper binding; local previous-row variable preserved')
 source=source.replace(before,after,1)
 scope=dict(earlier.check.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::whole_native_landing_and_separation_gate','exec'),scope)
 return scope['check'](b,guest,payload)

def run():
 failure=earlier.OUT/'report.json'
 need(not json.loads(failure.read_text())['passed']and 'UnboundLocalError'in json.loads(failure.read_text())['error'],
      'Executed generator scope failure preserved, not a gameplay diagnosis')
 scope=dict(earlier.run.__globals__,check=check,__file__=__file__)
 exec(compile(inspect.getsource(earlier.run),__file__+'::whole_recorded_matrix','exec'),scope)
 report=scope['run']()
 guest=earlier.prior.current.expected()
 payload=(ROOT/earlier.prior.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 for fighter,side,victim in earlier.prior.captured.MATRIX:
  b=earlier.prior.captured.load(fighter,side,victim)
  events=[r for r in b['rows']['MK2_BASIC_AIR_EVENT']if r['cycle']=='1'and r['driver']=='execute']
  landed=next(r for r in events if r['kind']=='victim_getup')
  flight=next(r for r in events if r['kind']in('own_flight','stock_flight'))
  post=b['rows']['MK2_HPHASE_POST_FIELD']
  tests=((int(landed['frame']),int(landed['slot']),'pose','wrong_actual_native_landing_pose'),
         (int(flight['frame'])+4,int(flight['slot']),'vx','wrong_actual_published_actor_speed'))
  for frame,slot,key,label in tests:
   index=next(i for i,r in enumerate(post)if(int(r['frame']),int(r['slot']))==(frame,slot))
   value=f'{earlier.prior.h(post[index],key)^1:08X}'
   changed=earlier.prior.mutated(b,'MK2_HPHASE_POST_FIELD',index,key,value)
   try:check(changed,guest,payload)
   except ValueError as error:report['actualSemanticFaultsRejected'].append(dict(fighter=fighter,side=side,victim=victim,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual source-native landing/publication fault accepted: '+label)
  print(f'{fighter} P{side}/{victim}: native landing and publication negative controls rejected',flush=True)
 for p in(failure,Path(earlier.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 need(len(report['actualSemanticFaultsRejected'])==48 and all(sha(p)==v for p,v in report['inputHashes'].items()),
      'All48 actual semantic trajectory/landing/publication faults and immutable inputs')
 report.update(retainedGeneratorScopeFailure=str(failure),scope=__doc__)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete airborne phase qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
