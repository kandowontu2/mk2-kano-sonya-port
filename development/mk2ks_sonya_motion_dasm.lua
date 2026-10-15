-- Read-only native effect coordinates, drawing, sleep and retirement helpers.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v267_native_effect_coordinates.asm,FF83E8F0,780")
d:command("dasm audit_v267_native_effect_create.asm,FF83ADA0,400")
d:command("dasm audit_v267_native_effect_draw.asm,FF840B60,300")
d:command("dasm audit_v267_native_effect_cleanup.asm,FF83EFD0,400")
d:command("dasm audit_v267_native_sleep.asm,FF80DCC0,600")
d.execution_state="run"
