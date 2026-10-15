-- Read-only disassembly around near-only stock CPU decision addresses.
local debugger=assert(manager.machine.debugger)
debugger.visible_cpu=manager.machine.devices[":maincpu"]
debugger:command("dasm audit_v257_ai_close_router.asm,FFFBC400,180")
debugger:command("dasm audit_v257_ai_close_hook.asm,FF9B71A0,90")
debugger:command("dasm audit_v255_ai_close_00.asm,FF9B0000,220")
debugger:command("dasm audit_v255_ai_close_09.asm,FF9B0980,3B0")
debugger:command("dasm audit_v255_ai_close_10.asm,FF9B10D0,220")
debugger:command("dasm audit_v255_ai_close_19.asm,FF9B19C0,1A0")
debugger:command("dasm audit_v255_ai_close_55.asm,FF9B55C0,260")
debugger:command("dasm audit_v255_ai_close_6f.asm,FF9B6F60,360")
debugger:command("dasm audit_v255_ai_close_87.asm,FF9B8680,3A0")
debugger:command("dasm audit_v255_ai_close_7e.asm,FF9B7DE0,280")
debugger:command("dasm audit_v255_ai_close_89.asm,FF9B8920,220")
debugger:command("dasm audit_v255_ai_close_8e.asm,FF9B8E40,180")
print("MK2KS_AI_CLOSE_DASM ready")
debugger.execution_state="run"
