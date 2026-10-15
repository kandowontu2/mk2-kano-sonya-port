"""Strict accepted-route prefix plus bounded released-input followthrough."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_sonya_smoke_long_idle_runtime'
out=root/'audit_current_sonya_smoke_long_idle_checked'
assert not out.exists()
def load(path):
    rows=[]
    for line in path.open():
        assert 'LUA ERROR' not in line
        if line.startswith('MK2_STAGE_'):
            rows.append((line.split()[0].removeprefix('MK2_STAGE_'),dict(re.findall(r'(\w+)=([^\s]+)',line))))
    return rows
prior=load(root/'audit_current_sonya_smoke_transition_batched_runtime/run.log')
rows=load(case/'run.log');terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
prefix=[(t,r) for t,r in prior if t!='RESULT']
assert [(t,r) for t,r in rows if int(r['frame'])<=25691]==prefix
def gate(records):
    assert (terminal['exitCode']==0 and terminal['limitReason'] is None) or terminal['limitReason']=='wall_limit'
    assert not any(t=='SECRET_NATIVE_RESET' for t,r in records)
    assert any(t=='SECRET_RETURN_COMPLETE' and r['frame']=='25691' for t,r in records)
    assert all(r['writes']=='0' and r['assistance']=='none' for _,r in records)
    idle=[r for t,r in records if t=='LONG_IDLE']
    assert idle and int(idle[-1]['frame'])>=110000
gate(rows)
bad=copy.deepcopy(rows);bad.append(('SECRET_NATIVE_RESET',dict(frame='125670',writes='0',assistance='none')))
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Reset wrongly accepted')
assert not (case/'stderr.log').read_text().strip()
report=dict(acceptedSecretRoutePrefixExactlyPreservedThrough=25691,physicalButtonsReleasedAfter=25691,
    completed135000FieldBound=any(t=='HOST_BOUND' and r['frame']=='135000' for t,r in rows),
    lastObservedFrame=max(int(r['frame']) for _,r in rows),resetNotifications=[],syntheticResetFaultRejected=True,
    longIdleModeValues=sorted({int(r['mode']) for t,r in rows if t=='LONG_IDLE'}),
    terminal=terminal,logSHA256=sync.sha(case/'run.log'),
    scope='Current Sonya P1 earned Smoke/return followed by released-input idle; not identical to historical Sonya P2 failing route.',
    heardAudioAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
