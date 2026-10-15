"""Read-only expanded error context for preserved failed escape input replays.
The verifier gate stays unchanged; only its diagnostic text is expanded.
No capture edits, no acceptance override, no gameplay writes.
"""
import inspect,json
from pathlib import Path
import verify_current_boss_stomp_window_campaign_v2285 as native
source=inspect.getsource(native.verify)
old="'Every actual stomp-window crouch/HP/jumpkick/guard input equals independently replayed native state and height policy'"
new="f'Every actual stomp-window crouch/HP/jumpkick/guard input: frame={frame} expected={sorted(expected)} actual={sorted(input_at.get(frame,set()))} command={command} jump={jump} direction={direction}'"
assert source.count(old)==1
space=dict(native.__dict__);exec(compile(source.replace(old,new),str(Path(__file__).resolve()),'exec'),space)
out={}
for fighter in('kano','sonya'):
 folder=native.ROOT/f'audit_v2286_current_{fighter}_p1_window_escape_campaign'
 result=space['verify'](folder)
 assert not result['passed'],'Expected original failed diagnostic control'
 out[fighter]=dict(passed=result['passed'],errorCount=len(result['errors']),errors=result['errors'][:12])
print(json.dumps(out,indent=2),flush=True)
