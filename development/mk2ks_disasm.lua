emu.register_start(function()
    local debugger = manager.machine.debugger
    debugger.visible_cpu = manager.machine.devices[":maincpu"]
    debugger:command("dasm mk2ks_pc.asm,FF80C000,2000")
    debugger.execution_state = "run"
end)
