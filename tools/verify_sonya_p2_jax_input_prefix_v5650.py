"""Complete captured Jax inputs; unexecuted ground/jump branch stays unqualified."""
import inspect,json,traceback
from types import SimpleNamespace
import verify_current_sonya_p2_kitana_prefix_v5632 as previous
import verify_current_sonya_p2_campaign_v5630 as original
import run_verified_kitana_sonya_p2_campaign_v5642 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5651_sonya_p2_jax_input_prefix_checked'

def run():
 source=inspect.getsource(previous.run)
 for before,after in [('whole.original.supplemental.kitana','whole.original.supplemental.jax'),
  (' stage=2',' stage=4'),(' stage=3 ',' stage=5 '),('cpuIdentity=4','cpuIdentity=11')]:
  need(source.count(before)==1,'One whole original encounter context adaptation')
  source=source.replace(before,after,1)
 source=source.replace('KITANA_FIELD','JAX_FIELD').replace('KITANA_DECISION','JAX_DECISION')
 carrier=SimpleNamespace(capture=capture,original=original.original,p2_factory=original.p2_factory)
 scope=dict(vars(previous),__file__=__file__,OUT=OUT,whole=carrier)
 exec(compile(source,__file__+'::entire_completed_Jax_input_encounter','exec'),scope)
 report=scope['run']()
 report.update(actualFirstJaxGroundPoundCallbacksObserved=0,actualFirstJaxNativeJumpCallbacksObserved=0,
  nativeGroundPoundCarryGateAccepted=False,
  preservedStricterUnavailableBranchProof=str(ROOT/'audit_v5649_sonya_p2_jax_prefix_checked/report.json'),
  explanation='First completed encounter contains native throws507 but no CPU ground-pound137, no corresponding ground helper or owned jump callbacks. Whole physical-input/state replay passes; original native callback requirement remains unchanged and unproven here.')
 return report

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual input proof');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
