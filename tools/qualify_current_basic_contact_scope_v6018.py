"""Whole6016 kernels/faults; explicitly bind the two real ordinary contacts.

The knockback moves Kitana outside later attack range. Do not claim three hits
or a blocked-contact branch merely from its phase label. Retain all real fields
and exact two-store43damage ledger, with missing branch coverage explicit.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_basic_walk_timing_v6016 as walking
ROOT,need,sha=walking.ROOT,walking.need,walking.sha
OUT=ROOT/'audit_v6019_current_ordinary_contact_scope_checked'

def state_gate():
 source=inspect.getsource(walking.state_gate)
 before=" scope=dict(prior.state_gate.__globals__)"
 after=""" before='count==len(stores)>=3 and totals[side]==0 and totals[3-side]>0'
 need(source.count(before)==1,'Original mistaken minimum-contact expectation is unique')
 source=source.replace(before,"count==len(stores)==2 and totals[side]==0 and totals[3-side]==43 and [(int(r['frame'])-ready,int(r['slot']),int(r['before']),int(r['after']))for r in stores]==[(1171,3-side,161,150),(1228,3-side,150,118)]",1)
 before='allThreePreviouslyUnactivatedCrouchAttacksNowActivated=True,fullPortAcceptance=False'
 need(source.count(before)==1,'One explicit ordinary branch-scope receipt')
 source=source.replace(before,'allThreePreviouslyUnactivatedCrouchAttacksNowActivated=True,actualOrdinaryContacts=2,actualBlockedStrikeContactAccepted=False,allOrdinaryStrikeHitMissBlockBranchesAccepted=False,fullPortAcceptance=False',1)
 scope=dict(prior.state_gate.__globals__)"""
 need(source.count(before)==1,'One complete physical-generator binding insertion');source=source.replace(before,after,1)
 scope=dict(walking.state_gate.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::entire6016_physical_generator_with_exact_actual_contacts','exec'),scope)
 return scope['state_gate']()

def bindings():
 scope=dict(walking.bindings.__globals__,state_gate=state_gate)
 exec(compile(inspect.getsource(walking.bindings),__file__+'::whole_native_body_shadow_binding','exec'),scope)
 return scope['bindings']()

def run():
 failed=walking.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Actual ordinary contacts, no synthetic damage or omitted stores'in failure['error'],
      'Actual two-contact vs three-assumed contact admission failure retained')
 scope=dict(walking.run.__globals__,OUT=OUT,bindings=bindings,__file__=__file__)
 exec(compile(inspect.getsource(walking.run),__file__+'::whole6016_four_case_full_kernel_fault_matrix','exec'),scope)
 report=scope['run']()
 for p in(failed,Path(walking.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(retainedFailedMinimumContactsExpectation=str(failed),exactTwoActualOrdinaryContactsAndFullHealthLedgerAccepted=True,
               allOrdinaryStrikeHitMissBlockBranchesAccepted=False,actualBlockedStrikeContactAccepted=False)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual-contact native body/shadow matrix')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
