-- Read-only disassembly of the native winner announcement lookup and call.
local output = assert(os.getenv("MK2KS_VOICE_DASM_PATH"), "Set MK2KS_VOICE_DASM_PATH")
local debugger = manager.machine.debugger
debugger.visible_cpu = manager.machine.devices[":maincpu"]
debugger:command(string.format("dasm %s,FF820940,300", output))
debugger:command(string.format("dasm %s.router,FFFB7000,100", output))
debugger:command(string.format("dasm %s.sound,FFA12400,300", output))
debugger:command(string.format("dasm %s.port,FFA13C00,300", output))
debugger:command(string.format("dasm %s.winner_followup,FF829EC0,300", output))
debugger:command(string.format("dasm %s.ending_loader,FF844800,200", output))
debugger:command(string.format("dasm %s.ending_draw,FFA2EA40,260", output))
debugger:command(string.format("dasm %s.ending_coop,FFA2E9C0,180", output))
debugger:command(string.format("dasm %s.ending_path,FF844600,800", output))
print("MK2KS_VOICE_DASM wrote " .. output)
debugger.execution_state = "run"
