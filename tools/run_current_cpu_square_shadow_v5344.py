"""Complete original Square RAM collector with explicit inner source inventory binding."""
import inspect,json,traceback
import run_current_cpu_square_shadow_v5341 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5346_current_cpu_sonya_square_observed'
def run():
 source=inspect.getsource(previous.run)
 source=source.replace('audit_v5342_current_cpu_sonya_square_human_','audit_v5345_current_cpu_sonya_square_human_')
 before=" namespace=dict(original.collector.__globals__,LUA=LUA,__file__=__file__,CHAIN=CHAIN)"
 after=""" inner="namespace=dict(original.capture.__globals__,native=current,LUA=LUA,__file__=__file__,original=original)"
 need(source.count(inner)==1,'Exact inner collector globals inventory binding')
 source=source.replace(inner,inner[:-1]+',CHAIN=CHAIN)',1)
 namespace=dict(original.collector.__globals__,LUA=LUA,__file__=__file__,CHAIN=CHAIN)"""
 need(source.count(before)==1,'Only collector source inventory scope correction')
 source=source.replace(before,after,1)
 namespace=dict(previous.run.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::complete_original_Square_transport_with_inventory_binding','exec'),namespace)
 report=namespace['run']()
 failed=previous.OUT/'report.json'
 need(not json.loads(failed.read_text())['passed'],'Preserve pre-launch host collector binding failure')
 for p in(failed,previous.__file__):report['inputHashes'][str(p)]=sha(p)
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current capture')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
