-- Read-only original Kano skeleton command record and distance validation.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_kano_distance_gate.asm,FF992CF0,400")
d:command("dasm audit_v265_original_kano_command.asm,FF986100,500")
d.execution_state="run"
