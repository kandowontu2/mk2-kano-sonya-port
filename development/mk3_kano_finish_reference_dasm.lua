-- Read-only original program: fatality entry, spacing helpers and pose lists.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_kano_finish.asm,FF9B1000,1000")
d:command("dasm audit_v265_original_kano_finish_prefix.asm,FF9B0000,1000")
d.execution_state="run"
