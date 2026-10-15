"""Finite3actual-loss Ring comparison; preserve the running full campaign."""
import inspect,json,traceback
import run_sonya_p2_subzero_ring_probe_v5672 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5684_sonya_p2_subzero_ring_retries'
LUA='mk2ks_sonya_p2_subzero_ring_retries_v5682.lua'
CONTROLLERS=[LUA,*previous.CONTROLLERS]
native=previous.native
qualify_payload_metadata_warning=previous.qualify_payload_metadata_warning


def capture():
 scope=dict(vars(previous),__file__=__file__,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS)
 exec(compile(inspect.getsource(previous.capture),__file__+'::whole_bounded_three_encounter_host','exec'),scope)
 return scope['capture']()


if __name__=='__main__':
 try:capture()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2),flush=True);raise
