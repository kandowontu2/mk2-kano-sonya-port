-- Read-only disassembly of the custom stage-command parser and stock MKII gate.
local done=false
emu.register_frame(function()
    if done then return end
    done=true
    local debugger=assert(manager.machine.debugger)
    debugger.visible_cpu=manager.machine.devices[":maincpu"]
    debugger:command("dasm audit_v250_stage_finish_kano_parser.asm,FFFAA200,160")
    debugger:command("dasm audit_v250_stage_finish_sonya_parser.asm,FFFAA400,160")
    debugger:command("dasm audit_v250_stage_finish_stock_gate.asm,FF876D20,1200")
    debugger.execution_state="run"
end)
