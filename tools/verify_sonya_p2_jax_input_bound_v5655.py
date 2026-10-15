"""Bind actual module provenance omitted by5650; whole physical gate unchanged."""
import inspect,json,traceback
import verify_sonya_p2_jax_input_prefix_v5650 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5656_sonya_p2_jax_input_bound_checked'

def run():
 source=inspect.getsource(previous.run)
 before='carrier=SimpleNamespace(capture=capture,'
 need(source.count(before)==1,'One missing host module provenance binding only')
 source=source.replace(before,'carrier=SimpleNamespace(__file__=original.__file__,capture=capture,',1)
 scope=dict(vars(previous),__file__=__file__,OUT=OUT)
 exec(compile(source,__file__+'::whole_Jax_input_gate_with_provenance','exec'),scope)
 return scope['run']()

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable source-bound input proof');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
