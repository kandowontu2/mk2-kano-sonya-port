"""Exact report-path repair; all original current/native checks unchanged.

Retain failed6166/6167. Consume the same four actual terminal matches without
restarting or altering guest state. Save this successor's failure if present.
"""
import json,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
prior=Path(__file__).with_name('qualify_current_subzero_shatter_v6166.py')
source=prior.read_text()
before="replace('audit_v5003_subzero_','audit_v6165_current_subzero_')"
after="replace(\"observed=ROOT/f'audit_v5003_subzero_{fighter}_p{side}_lifecycle_observed/report.json'\",\"observed=ROOT/f'audit_v6165_current_subzero_{fighter}_p{side}_observed/report.json'\")"
need(source.count(before)==1,'Exact actual current terminal report path repair')
source=source.replace(before,after,1)
source=source.replace('audit_v6167_current_subzero_shatter_checked','audit_v6171_current_subzero_shatter_checked')
before='Path(__file__),Path(original.__file__),Path(refill_source.__file__)'
need(source.count(before)==1,'Retain all executed precursor source pins')
source=source.replace(before,'prior,Path(__file__),Path(original.__file__),Path(refill_source.__file__)',1)
scope=dict(globals(),__name__='exact_current_shatter_successor')
exec(compile(source,__file__+'::whole_complete_current_matrix','exec'),scope)
if __name__=='__main__':
 out=ROOT/'audit_v6171_current_subzero_shatter_checked';need(not out.exists(),'Fresh exact successor terminal report')
 try:scope['run']()
 except Exception as error:
  need(not out.exists(),'Never overwrite an executed matrix report')
  out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),inputHashes={str(prior.resolve()):sha(prior),str(Path(__file__).resolve()):sha(__file__)},fullPortAcceptance=False),indent=2)+'\n')
  raise
