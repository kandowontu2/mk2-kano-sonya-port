-- Read-only disassembly of the native palette queue and its observed caller.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v271_native_palette_copy.asm,FF80C600,1000")
d:command("dasm audit_v271_native_palette_caller.asm,FF816500,1000")
d:command("dasm audit_v271_native_shock_palette.asm,FF910000,1400")
d.execution_state="run"
