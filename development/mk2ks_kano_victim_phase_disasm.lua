local debugger=assert(manager.machine.debugger)
debugger.visible_cpu=manager.machine.devices[":maincpu"]
debugger:command("dasm audit_v261_victim_phase_draw.asm,FFFBE400,400")
debugger:command("dasm audit_v261_skeleton_action.asm,FFFB8000,3000")
debugger.execution_state="run"
