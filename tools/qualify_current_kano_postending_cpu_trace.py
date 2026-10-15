"""Observer-only credits/attract trace; failed early one-coin start retained."""
import json,re
from collections import Counter
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_postending_cpu_trace_runtime'
out=root/'audit_current_kano_postending_cpu_trace_checked';assert not out.exists()
def load(path):
    lines=path.read_text().splitlines();assert not any('LUA ERROR' in s for s in lines)
    return [(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in lines if s.startswith('MK2_NAT_CAMPAIGN_')]
rows=load(case/'run.log');prior=load(root/'audit_current_kano_earned_postending_join_runtime/run.log')
assert [(t,r) for t,r in rows if t!='POST_ENDING_CPU_TRACE']==prior
states=[r for t,r in rows if t=='STATE' and int(r['frame'])>75116]
attract=next(r for r in states if r['mode']=='1');assert attract['frame']=='80232'
traces=[r for t,r in rows if t=='POST_ENDING_CPU_TRACE'];assert len(traces)==50
assert len({r['pc'] for r in traces})>5 and any(r['mode']=='1' for r in traces)
assert not any(t=='POST_ENDING_FIGHT' for t,r in rows)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(nativeHistoryExactlyPreservedThrough=81116,postEndingAttractModeEntered=80232,
    registerTraceSamples=50,observedPCs=dict(Counter(r['pc'] for r in traces)),
    cinematicModeDidNotPersistEntireBound=True,freshStartPassed=False,
    earlyStartAttemptCoinPulses=1,knownEstablishedPaymentPatternCoinPulses=2,
    terminal=terminal,logSHA256=sync.sha(case/'run.log'),fullPortAccepted=False,
    caveat='This excludes a persistent mode11 hang on this route. It does not prove the exact rejection cause; retry with normal two-coin payment after actual mode1 admission.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
