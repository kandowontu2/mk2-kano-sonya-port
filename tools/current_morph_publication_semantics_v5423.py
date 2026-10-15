"""Correct only native hexadecimal pointer transport; preserve failed attempt."""
import json,traceback
from pathlib import Path
import current_morph_publication_semantics_v5421 as original

OUT=original.ROOT/'audit_v5424_current_morph_publication_progress'
FAILED=original.OUT/'progress.json'

def run():
 failure=json.loads(FAILED.read_text())
 original.need(not failure['passed']and failure['error']=="ValueError('Native post-task state binds independent next physical callback')",
  'Preserve exact first semantic-parser failure, not an actual game mutation')
 original.need(not {'p1','p2','main1','main2'}&original.HEX,'Exact four native pointers omitted from initial hexadecimal transport')
 original.HEX.update({'p1','p2','main1','main2'})
 report=original.run()
 report.update(preservedActualCheckerFailure=str(FAILED),
  checkerTransportCorrection='Only FLOOR_STATE p1/p2/main1/main2 decode as hexadecimal addresses, exactly as native observer emits; no semantic/source/ownership gate relaxed.')
 for p in(FAILED,Path(__file__).resolve()):report['newInputHashes'][str(p)]=original.sha(p)
 return report

if __name__=='__main__':
 original.need(not OUT.exists(),'Fresh corrected immutable native publication checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','actualRecordFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
