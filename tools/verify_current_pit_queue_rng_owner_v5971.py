"""Whole5950 direct ownership and all104 actual faults on5964 captures."""
import inspect,json,traceback
from pathlib import Path
import qualify_current_subzero_pit_owner_v5950 as original_owner
import verify_current_pit_queue_rng_mix_v5965 as actual_audio
ROOT,need,sha=actual_audio.ROOT,actual_audio.need,actual_audio.sha
OUT=ROOT/'audit_v5972_current_pit_queue_rng_owner_checked'
source=inspect.getsource(original_owner.run)
before='audit_v5947_current_subzero_pit_mix_';after='audit_v5964_current_pit_queue_rng_'
need(source.count(before)==1,'One actual current capture path substitution')
source=source.replace(before,after,1)
scope=dict(original_owner.run.__globals__,__file__=__file__,__doc__=__doc__,whole=actual_audio)
exec(compile(source,__file__+'::whole5950_direct_owner_and_all104faults','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete direct owner/fault matrix')
 try:
  report=run();report['inputHashes'][str(Path(original_owner.__file__).resolve())]=sha(original_owner.__file__)
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Whole executed/prior/direct-owner evidence unchanged')
  report.update(whole5950DirectOwnerAndActualFaultSuiteRetained=True,fullPortAcceptance=False)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
