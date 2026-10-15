"""Only failed source-loader anchor corrected; actual bounded native comparison."""
import inspect,json,traceback
import run_sonya_p2_jax_ring_probe_v5653 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5659_sonya_p2_jax_ring_bound_probe'
LUA='mk2ks_sonya_p2_jax_ring_bound_probe_v5657.lua'
CONTROLLERS=[LUA,*previous.CONTROLLERS]

def capture():
 scope=dict(vars(previous),__file__=__file__,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS)
 exec(compile(inspect.getsource(previous.capture),__file__+'::entire_bounded_Jax_capture','exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 try:capture()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2),flush=True);raise
