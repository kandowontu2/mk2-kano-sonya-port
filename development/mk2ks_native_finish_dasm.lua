-- Diagnostic-only disassembly of emitted Kano/Sonya individual finish routes.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local debugger = manager.machine.debugger
    debugger.visible_cpu = manager.machine.devices[":maincpu"]
    debugger:command("dasm diagnostic_v79_kano_finish_route.asm,FFFAAE00,500")
    debugger:command("dasm diagnostic_v79_sonya_finish_route.asm,FFFAB200,500")
    debugger.execution_state = "run"
end)
