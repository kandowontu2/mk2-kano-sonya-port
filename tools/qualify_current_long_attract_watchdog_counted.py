"""Bounded attract evidence; do not equate watchdog polling with reset."""
import json,re
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_long_attract_watchdog_counted_runtime'
out=root/'audit_current_long_attract_watchdog_counted_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
rows=[]
for line in (case/'run.log').open():
    assert 'LUA ERROR' not in line
    if line.startswith('MK2_LIGHT_ATTRACT_'):
        rows.append((line.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
assert rows and all(r['writes']=='0' and r['assistance']=='none' for _,r in rows)
counts=[r for t,r in rows if t=='WATCHDOG_COUNT']
assert counts and all(int(a['executions'])<=int(b['executions']) for a,b in zip(counts,counts[1:]))
bound=any(t=='BOUND' and r.get('maximum_fields')=='135000' for t,r in rows)
normal=terminal['exitCode']==0 and terminal['limitReason'] is None and bound
report=dict(terminal=terminal,lastObservedFrame=max(int(r['frame']) for _,r in rows),
    observedModes=dict(Counter(r['mode'] for t,r in rows if t=='FIELD')),
    biographyCounterValues=sorted({int(r['counter']) for t,r in rows if t=='FIELD'}),
    observedPictureRows=sorted({int(r['row']) for t,r in rows if t=='PICTURE'}),
    watchdogInstructionExecutions=int(counts[-1]['executions']),bounded135000FrameRunCompleted=normal,
    resetAbsenceProved=False,earnedEndingExecution=False,heardAudioAccepted=False,fullPortAccepted=False,
    logSHA256=sync.sha(case/'run.log'),
    caveat='Watchdog instruction is executed repeatedly during normal attract; its count is not reset detection. Mode samples are sparse and do not prove reset absence.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
