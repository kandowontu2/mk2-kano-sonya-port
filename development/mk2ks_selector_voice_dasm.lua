-- Read-only disassembly of the native selection-announcement entry and trampoline.
local output = assert(os.getenv("MK2KS_SELECTOR_DASM_PATH"), "Set MK2KS_SELECTOR_DASM_PATH")
local debugger = manager.machine.debugger
debugger.visible_cpu = manager.machine.devices[":maincpu"]
debugger:command(string.format("dasm %s,FF8979C0,300", output))
debugger:command(string.format("dasm %s.trampoline,FFFF3C00,200", output))
debugger.execution_state = "run"
