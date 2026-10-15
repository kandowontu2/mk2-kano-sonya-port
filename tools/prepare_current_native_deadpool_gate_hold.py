"""Keep physical low buttons held after uppercut entry through native acid gate."""
import verify_native_source_sync as sync

sync.verify()
base = sync.ROOT / 'audit_current_native_deadpool_gate_trace_preparation'
out = sync.ROOT / 'audit_current_native_deadpool_gate_hold_preparation'
assert not out.exists()
source = (base / 'stage.lua').read_text()
needle = ' -- A normal paid challenger after an expired finish window. Never touch state.'
assert source.count(needle) == 1
source = source.replace(needle, ''' -- Continue the requested physical hold even after uppercut-entry observation.
 if action and command and frame-command>=51 and frame-command<90 then
  press(side,'Low Punch');press(side,'Low Kick')
 end
''' + needle)
out.mkdir()
lua = out / 'stage.lua'
lua.write_text(source)
runner = (base / 'run.ps1').read_text()
runner = runner.replace(base.name+'/stage.lua', out.name+'/stage.lua')
runner = runner.replace(sync.sha(base/'stage.lua'), sync.sha(lua))
runner = runner.replace('audit_current_native_deadpool_gate_trace_kano_p1_runtime',
                        'audit_current_native_deadpool_gate_hold_kano_p1_runtime')
(out / 'run.ps1').write_text(runner)
print('Prepared continuous physical LP/LK hold through native eligibility; no game edits/media')
