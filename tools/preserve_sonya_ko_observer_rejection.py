"""Preserve two normally terminal attempts with a missing passive observer."""
import json
from pathlib import Path
import qualify_launch_ko_round as base
ROOT,need,sha=base.ROOT,base.need,base.sha

def record(c):
 out=ROOT/f"audit_sonya_ko_missing_observer_p{c['side']}";need(not out.exists(),'Fresh missing-observer diagnosis')
 need(c['report']['passed']and c['terminal']['nativeExit']==0 and not c['decodeErrors']and
      not base.rows(c['text'],'MK2_KO_FIELD'),'Exactly actual terminal transport, no full boundary fields')
 source=ROOT/'mk2ks_sonya_launch_ko_round.lua'
 need('template:sub(assert(template:find('in source.read_text(),'Actual executed multi-return slicing defect')
 report=dict(passed=False,nativeTerminal=c['terminal'],actualBoundaryFields=0,controllerTerminal=base.one(c['text'],'MK2_HSPECIAL_RESULT'),
             actualKO=base.one(c['text'],'MK2_HSPECIAL_KO'),actualReset=base.one(c['text'],'MK2_HSPECIAL_ROUND_RESET'),
             fullPhysicalKOResetAcceptance=False,sourceWaveformAcceptance=False,fullPortAcceptance=False,
             cause='Lua assert propagates both find offsets into sub(start,end), retaining only the declaration instead of the whole observer.',
             nativeGameFailure=False,originalExecutedSourcePreserved=True,RAMReleasedAfterThisDiagnosis=True,
             newBuilds=0,newROMCopies=0,newRawMedia=0,inputHashes={str(source):sha(source),str(Path(__file__)):sha(__file__),str(c['folder']/'report.json'):sha(c['folder']/'report.json')})
 out.mkdir();(out/'failure.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(side=c['side'],missingBoundaryFields=True,nativeExit=0)),flush=True)
