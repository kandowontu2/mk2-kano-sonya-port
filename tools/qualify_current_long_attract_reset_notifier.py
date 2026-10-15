"""Finite completed attract observation through historical frontier."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_long_attract_reset_notifier_runtime'
out=root/'audit_current_long_attract_reset_notifier_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
text=(case/'run.log').read_text();assert 'LUA ERROR' not in text
assert not (case/'stderr.log').read_text().strip()
rows=[(line.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',line))) for line in text.splitlines() if line.startswith('MK2_LIGHT_ATTRACT_')]
lua=root/'mame-mkp/src/frontend/mame/luaengine.cpp'
code=lua.read_text()
assert 'machine().add_notifier(MACHINE_NOTIFY_RESET, machine_notify_delegate(&lua_engine::on_machine_start, this));' in code
assert 'execute_function("LUA_ON_START");' in code
assert 'register_function(func, "LUA_ON_START")' in code
def gate(records):
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert all(r['writes']=='0' and r['assistance']=='none' for _,r in records)
    assert any(t=='BOUND' and r['frame']=='135000' and r['maximum_fields']=='135000' for t,r in records)
    assert any(t=='RESULT' and r['normal_callback']=='true' for t,r in records)
    assert not any(t=='ACTUAL_RESET_NOTIFY' for t,r in records)
gate(rows)
bad=copy.deepcopy(rows);bad.append(('ACTUAL_RESET_NOTIFY',dict(frame='125670',writes='0',assistance='none',count='1')))
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Reset event incorrectly accepted')
report=dict(completed135000FieldAttractRun=True,observedResetNotifications=[],resetFaultRejected=True,
    observedBiographyCounters=sorted({int(r['counter']) for t,r in rows if t=='FIELD'}),
    terminal=terminal,logSHA256=sync.sha(case/'run.log'),localResetCallbackSourceSHA256=sync.sha(lua),
    scope='This ordinary cold attract route only; historical secret-route reset is not reproduced or repaired by this check.',
    heardAudioAccepted=False,earnedEndingExecution=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
