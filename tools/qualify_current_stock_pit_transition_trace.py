"""Observe full-health rematch assumption without weakening admission gates."""
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_stock_pit_transition_trace_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_stock_pit_transition_trace_preparation/stage.lua')
rows=base.load(folder/'run.log')
old=base.load(sync.ROOT/'audit_current_stock_pit_direct_rematch_sonya_p1_kitana_runtime/run.log')
for tag in set(rows)|set(old):
    if tag in ('TRANSITION_SCALAR','TRANSITION_BOUND','RESULT'):continue
    assert [r for r in rows.get(tag,[]) if int(r['frame'])<19500]==[r for r in old.get(tag,[]) if int(r['frame'])<19500],tag
assert rows['TRANSITION_BOUND'][0]['frame']=='19500'
scalars=rows['TRANSITION_SCALAR'];assert scalars
report=dict(passedObserverNeutrality=True,unchangedControllerThrough=19499,
 nativeTransitionSamples=scalars,fullPortAccepted=False,sceneAccepted=False,
 logSHA256=sync.sha(folder/'run.log'))
out=sync.ROOT/'audit_current_stock_pit_transition_trace_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(scalars[-4:],indent=2))
