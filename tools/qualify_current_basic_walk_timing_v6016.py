"""Whole6014 native gate with actual two-field controller-consumption latency.

Do not weaken walking to a broad distance range: require all24 actual fixed-point
velocity/position fields exactly, including both facing signs and clean stop.
Retain the original mistaken controller-age distance expectation.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_basic_ground_v6014 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6017_current_ordinary_walk_timing_checked'

def state_gate():
 source=inspect.getsource(prior.state_gate)
 for before,after in(("pre(56)['x']","pre(58)['x']"),("pre(32)['x']","pre(34)['x']"),
                      ("pre(100)['x']","pre(102)['x']"),("pre(76)['x']","pre(78)['x']")):
  need(source.count(before)==1,'One observed native walking boundary correction');source=source.replace(before,after,1)
 before=' jumps=[]'
 after=""" for start,speed in((34,sign*0x28000),(78,-sign*0x20000)):
  origin=int(pre(start)['x'])<<16
  for age in range(start,start+24):
   r=pre(age)
   need(int(r['vx'],16)==speed&0xffffffff and int(r['x'])==(origin+speed*(age-start))>>16 and
        int(r['y'])==int(r['floor'])and r['vy']=='00000000'and r['gravity']=='00000000',
        'Every original24field signed16.16 walking velocity/position and owned floor exact')
  need(pre(start+24)['vx']=='00000000'and int(pre(start+24)['x'])==(origin+speed*24)>>16,
       'Exact24native movement updates and immediate clean stop')
 jumps=[]"""
 need(source.count(before)==1,'Add every actual walking-cycle state, never discard fields');source=source.replace(before,after,1)
 scope=dict(prior.state_gate.__globals__)
 exec(compile(source,__file__+'::entire_physical_gate_exact_native_walk_cycles','exec'),scope)
 return scope['state_gate']

def bindings():
 scope=dict(prior.bindings.__globals__,state_gate=state_gate())
 exec(compile(inspect.getsource(prior.bindings),__file__+'::whole_original_body_shadow_bindings','exec'),scope)
 return scope['bindings']()

def run():
 failed=prior.OUT/'report.json';report=json.loads(failed.read_text())
 need(not report['passed']and 'Native24field forward2.5/backward2pixel walking distance'in report['error'],
      'Actual failed controller-age walk boundary preserved')
 scope=dict(prior.run.__globals__,OUT=OUT,bindings=bindings,__file__=__file__)
 exec(compile(inspect.getsource(prior.run),__file__+'::whole_ordinary_matrix_all_original_faults','exec'),scope)
 report=scope['run']()
 for p in(failed,Path(prior.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(retainedFailedControllerAgeWalkingExpectation=str(failed),
               all24SourceDefinedWalkVelocityPositionUpdatesExact=True,originalWholeBodyShadowAndFaultGatesRetained=True)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable native-walk/body/shadow matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
