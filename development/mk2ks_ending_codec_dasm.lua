local debugger = manager.machine.debugger
debugger.visible_cpu = manager.machine.devices[":maincpu"]
debugger:command("dasm diagnostic_v61_ending_codec.asm,FF903EE0,1000")
print("MK2KS_ENDING_CODEC_DASM wrote diagnostic_v61_ending_codec.asm")
debugger.execution_state = "run"
