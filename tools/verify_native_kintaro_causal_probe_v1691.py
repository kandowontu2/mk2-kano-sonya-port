"""Source-bound actual native boss flight causality; no pixel acceptance."""
import json,traceback
from pathlib import Path
import verify_native_kintaro_launch_cull_v1690 as boss
ROOT=boss.ROOT;OUT=ROOT/'audit_v1691_native_kintaro_causal_probe_checked'
if __name__=='__main__':
 assert not OUT.exists()
 try:
  guest,_,payload=boss.arena.corrected_source.expected()
  c=boss.build_context(ROOT/'audit_v1664_current_kano_p1_native_counter',guest,payload)
  flights=[boss.flight(c,h)for h in c['hits']if h['frame']in (42379,45155)]
  assert len(flights)==2
  report=dict(passed=True,flights=flights,descriptor=c['descriptor'],originalInstructionSlices=c['originalSlices'],
   actualNativeFields=len(c['fields']),guestEvidence='Exact same-candidate actual initialized guest, not a campaign-time dump',
   allInputWritesPhysicalOnly=True,fullPortAcceptance=False,inputHashes=c['pins'])
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
