"""Finite true Sub-Zero Ring-controller comparison, not a full-run restart."""
import inspect,json,re,traceback
import run_sonya_p2_kitana_ring_probe_v5637 as host
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as context
import run_sonya_p2_jax_ring_bound_probe_v5658 as previous
ROOT,need,sha=context.ROOT,context.need,context.sha
OUT=ROOT/'audit_v5673_sonya_p2_subzero_ring_probe'
LUA='mk2ks_sonya_p2_subzero_ring_probe_v5671.lua'
CONTROLLERS=[LUA,*previous.CONTROLLERS]
native=context.native
qualify_payload_metadata_warning=context.qualify_payload_metadata_warning


def capture():
 context.source_boundary()
 source=inspect.getsource(host.capture)
 scope=dict(vars(host),__file__=__file__,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS)
 exec(compile(source,__file__+'::entire_bounded_current_native_host','exec'),scope)
 return scope['capture']()


if __name__=='__main__':
 try:capture()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2),flush=True);raise
