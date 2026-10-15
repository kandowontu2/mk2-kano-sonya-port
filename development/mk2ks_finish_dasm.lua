-- Read-only map of MKII's native finish prompt and nearby dispatch paths.
local debugger = manager.machine.debugger
debugger.visible_cpu = manager.machine.devices[":maincpu"]
debugger:command("dasm diagnostic_v69_finish_prompt.asm,FF829200,1800")
debugger:command("dasm diagnostic_v69_finish_input.asm,FF82A800,1800")
print("MK2KS_FINISH_DASM wrote prompt and input disassembly")
debugger.execution_state = "run"
