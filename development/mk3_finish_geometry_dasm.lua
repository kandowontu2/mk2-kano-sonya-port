-- Read-only original group-coordinate handling; no actor/state writes.
local d=assert(manager.machine.debugger)
d.visible_cpu=manager.machine.devices[":maincpu"]
d:command("dasm audit_v265_original_pose_anchor.asm,FF965650,800")
d.execution_state="run"
