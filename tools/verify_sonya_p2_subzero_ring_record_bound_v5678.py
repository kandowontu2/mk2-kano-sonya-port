"""Match the complete actual native row, including a final stage=7 field.

5676's trailing-space lookup failed; its immutable failure is retained. No
gate, controller, native record, fault or real encounter outcome is changed.
"""
import inspect,json,traceback
from pathlib import Path
import verify_sonya_p2_subzero_ring_bound_v5676 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5679_sonya_p2_subzero_ring_record_bound_checked'


def run():
 source=inspect.getsource(previous.run)
 old="line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_SPECIAL frame='+str(ring['frame'])+' ')\n  and ' stage=7 'in s and ' move=ring 'in s)"
 new="line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_SPECIAL ')\n  and dict(re.findall(r'(\\w+)=([^\\s]+)',s))=={k:str(v)for k,v in ring.items()if k!='tag'})"
 need(source.count(old)==1,'One failed end-of-record Ring lookup, every guard retained')
 source=source.replace(old,new,1)
 old="line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION frame='+str(action['frame'])+' ')\n  and ' stage=7 'in s and ' actor='+action['actor']+' 'in s and ' after='+action['after']+' 'in s)"
 new="line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION ')\n  and dict(re.findall(r'(\\w+)=([^\\s]+)',s))=={k:str(v)for k,v in action.items()if k!='tag'})"
 need(source.count(old)==1,'One same actual native action row lookup')
 source=source.replace(old,new,1)
 scope=dict(vars(previous),__file__=__file__,OUT=OUT)
 exec(compile(source,__file__+'::whole_native_gate_exact_actual_row_lookup','exec'),scope)
 report=scope['run']()
 failure=previous.OUT/'report.json'
 need(json.loads(failure.read_text())['passed']is False,'Original lookup failure preserved, not relabeled')
 for p in [Path(previous.__file__),Path(__file__),failure]:
  report['inputHashes'][str(p.resolve())]=sha(p)
 report['preservedRecordLookupFailure']=str(failure)
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual input/proof/failure/source byte intact')
 return report


if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Immutable actual record-bound proof');OUT.mkdir()
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
