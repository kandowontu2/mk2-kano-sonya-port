-- Read-only original finisher helper ABI and activation records.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_kano_helpers.asm,FF9BA6F0,1300")
d:command("dasm audit_v265_original_finish_setup.asm,FF9B9ED0,400")
d.execution_state="run"
