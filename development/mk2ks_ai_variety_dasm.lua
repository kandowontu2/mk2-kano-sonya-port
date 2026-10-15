-- Read-only inspection of MKII CPU special selection and invocation.
local debugger = assert(manager.machine.debugger)
debugger.visible_cpu = manager.machine.devices[":maincpu"]
debugger:command("dasm audit_v254_ai_choice.asm,FF9B9000,520")
debugger:command("dasm audit_v254_ai_action.asm,FF8A58C0,480")
debugger:command("dasm audit_v254_ai_callback.asm,FF9B7600,420")
debugger:command("dasm audit_v254_ai_random.asm,FF80EBE0,230")
debugger:command("dasm audit_v254_ai_router.asm,FFFBC000,800")
debugger:command("dasm audit_v254_ai_decision.asm,FF9B1C80,A00")
print("MK2KS_AI_DASM ready")
debugger.execution_state = "run"
