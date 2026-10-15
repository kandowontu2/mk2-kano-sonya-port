-- Read-only stock MKII disassembly for native individual-fatality integration.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local machine = manager.machine
    local debugger = machine.debugger
    debugger.visible_cpu = machine.devices[":maincpu"]
    debugger:command("dasm diagnostic_v78_stock_finish_gate.asm,FF876A00,C00")
    debugger:command("dasm diagnostic_v78_stock_liu_dragon_action.asm,FF8B7000,8000")
    debugger:command("dasm diagnostic_v78_stock_liu_dragon_core.asm,FF8BA000,6000")
    debugger:command("dasm diagnostic_v78_stock_finish_scheduler.asm,FF83B780,500")
    debugger:command("dasm diagnostic_v78_stock_liu_fatality.asm,FF8C6F40,1300")
    debugger:command("dasm diagnostic_v78_stock_finish_setup.asm,FF8CD700,900")
    debugger:command("dasm diagnostic_v78_stock_animation_scheduler.asm,FF83C000,A00")
    debugger:command("dasm diagnostic_v78_stock_finish_completion.asm,FFA14600,A00")
    debugger:command("dasm diagnostic_v78_stock_liu_input.asm,FF86AFB0,500")
    debugger.execution_state = "run"
    local program = machine.devices[":maincpu"].spaces.program
    for _, address in ipairs({0xff878de0,0xff876b40,0xff876f70,0xff8bdde0}) do
        local words = {}
        for index=0,11 do words[#words+1] = string.format("%04X",program:read_u16(address+index*0x10)) end
        print(string.format("MK2_FATALITY_WORDS at=%08X %s",address,table.concat(words,",")))
    end
end)
