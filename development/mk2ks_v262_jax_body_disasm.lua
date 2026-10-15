-- Read-only loaded candidate evidence; never overwrite prior build captures.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v262_skeleton_action_loaded.asm,FFFB8000,3000")
d.execution_state="run"
