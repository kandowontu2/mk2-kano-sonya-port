-- Read-only disassembly around the actual native health writer.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v273_native_health_writer.asm,FF836400,600")
d.execution_state="run"
