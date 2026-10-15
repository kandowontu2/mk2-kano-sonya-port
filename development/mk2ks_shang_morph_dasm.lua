-- Read only: the two observed original CPU actor-ID stores.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v274_native_shang_morph.asm,FF86E510,300")
d:command("dasm audit_v274_native_shang_restore.asm,FFA165C0,300")
d.execution_state="run"
