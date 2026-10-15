-- Original-ROM input validator; read-only evidence, no actor/state edits.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_finish_distance_validation.asm,FF993160,A00")
d:command("dasm audit_v265_original_input_validation.asm,FF982880,C00")
d:command("dasm audit_v265_original_button_elapsed.asm,FF9615D0,180")
d.execution_state="run"
