-- Read-only original skeleton dispatch, distance gate and activation records.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_finish_gate.asm,FF998300,800")
d.execution_state="run"
