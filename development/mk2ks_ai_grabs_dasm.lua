-- Inspect the new native CPU close-grab router without gameplay writes.
local debugger=assert(manager.machine.debugger)
debugger.visible_cpu=manager.machine.devices[":maincpu"]
debugger:command("dasm audit_v258_ai_close_router.asm,FFFBC400,400")
debugger:command("dasm audit_v258_ai_close_hook.asm,FF9B71A0,90")
print("MK2KS_AI_GRABS_DASM ready")
debugger.execution_state="run"
