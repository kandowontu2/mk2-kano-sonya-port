-- Original MK3 palette selection; read-only, not loaded by the port.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v272_original_palette_selection.asm,FFA60D00,6000")
d:command("dasm audit_v272_original_freeze_victim.asm,FF9E7700,600")
d.execution_state="run"
