"""Actual first completed P2 Jax encounter, full input and native ground gates.

No tower acceptance from a loss or a growing log. Keep the exact current
campaign, controller, actor/Main, input/reset and native Carry/opcode proofs.
"""
import inspect,json,traceback
from types import SimpleNamespace
import verify_current_sonya_p2_kitana_prefix_v5632 as previous
import verify_current_sonya_p2_campaign_v5630 as original
import run_verified_kitana_sonya_p2_campaign_v5642 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5649_sonya_p2_jax_prefix_checked'

def run():
 source=inspect.getsource(previous.run)
 changes=[('whole.original.supplemental.kitana','whole.original.supplemental.jax'),
  ('KITANA_FIELD','JAX_FIELD'),('KITANA_DECISION','JAX_DECISION'),
  (' stage=2',' stage=4'),(' stage=3 ',' stage=5 '),
  ('cpuIdentity=4','cpuIdentity=11'),
  ('actualCompletePhysicalReplay=positive,','actualCompletePhysicalReplay=positive,actualNativeJaxCallbacks=callbacks,'),
  ('capture.source_boundary();f=fields[0];faults=[]',
   'callbacks=jax_callbacks(text,guest);capture.source_boundary();f=fields[0];faults=[]')]
 for before,after in changes:
  if before.startswith('KITANA_'):
   need(source.count(before)>=1,'Entire captured Jax observer context boundary')
   source=source.replace(before,after)
  else:
   need(source.count(before)==1,'Exactly one whole encounter context adaptation '+before)
   source=source.replace(before,after,1)
 carrier=SimpleNamespace(capture=capture,original=original.original,p2_factory=original.p2_factory)
 scope=dict(vars(previous),__file__=__file__,OUT=OUT,whole=carrier,jax_callbacks=original.jax_callbacks)
 exec(compile(source,__file__+'::entire_completed_Jax_encounter','exec'),scope)
 return scope['run']()

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual encounter proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
