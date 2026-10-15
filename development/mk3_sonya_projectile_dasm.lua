-- Read-only original fatality projectile program, never loaded by the port.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v266_original_sonya_projectile.asm,FF9AF500,1800")
d:command("dasm audit_v266_original_sonya_finish_entry.asm,FF9AF200,300")
d:command("dasm audit_v266_original_sonya_command.asm,FF98A400,800")
d:command("dasm audit_v266_original_run_fatality.asm,FF97B500,300")
d.execution_state="run"
