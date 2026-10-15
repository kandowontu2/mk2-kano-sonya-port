-- Read-only disassembly of the MKII boss-victory / ending transition.
local debugger = manager.machine.debugger
print("MK2KS_END_DASM load debugger=" .. tostring(debugger))
debugger.visible_cpu = manager.machine.devices[":maincpu"]
debugger:command("dasm diagnostic_v59_shao_end.asm,FF903800,600")
debugger:command("dasm diagnostic_v59_shao_end2.asm,FF903E00,800")
debugger:command("dasm diagnostic_v59_ending_dispatch.asm,FF8F4F00,1000")
debugger:command("dasm diagnostic_v59_ending_intro.asm,FF8F4B00,600")
debugger:command("dasm diagnostic_v59_ending_draw.asm,FF8446E0,600")
debugger:command("dasm diagnostic_v59_ending_picture.asm,FF903640,900")
debugger:command("dasm diagnostic_v59_ending_unpack.asm,FF9043D0,1400")
print("MK2KS_END_DASM wrote disassembly")
debugger.execution_state = "run"
