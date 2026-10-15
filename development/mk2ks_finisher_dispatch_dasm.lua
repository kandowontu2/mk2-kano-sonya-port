-- Diagnostic only: inspect MKII's stock input dispatch and per-fighter rows.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local machine = manager.machine
    local debugger = machine.debugger
    debugger.visible_cpu = machine.devices[":maincpu"]
    debugger:command("dasm diagnostic_v73_stock_input_dispatch.asm,FF85F000,6800")
    debugger:command("dasm diagnostic_v73_stock_finisher_candidates.asm,FF86B000,11000")
    debugger:command("dasm diagnostic_v73_liu_hk_candidate.asm,FF86AE00,400")
    debugger:command("dasm diagnostic_v73_stock_finish_actions.asm,FF8BD800,1000")
    debugger.execution_state = "run"
    local program = machine.devices[":maincpu"].spaces.program
    for _, entry in ipairs({
        {"hp", 0xff8628a0}, {"lp", 0xff862a20},
        {"block", 0xff862ba0}, {"hk", 0xff862d20},
        {"lk", 0xff862ea0}, {"forward", 0xff8620d0}
    }) do
        local values = {}
        for id = 0, 16 do
            values[#values + 1] = string.format("%d:%08X", id, program:read_u32(entry[2] + id * 0x20))
        end
        print("MK2_FINISH_DISPATCH " .. entry[1] .. " " .. table.concat(values, " "))
    end
    for _, entry in ipairs({{"liu_dragon", 0xff878de0}, {"kung_lao_stage", 0xff87b340}}) do
        local values = {}
        for word = 0, 12 do values[#values + 1] = string.format("%04X", program:read_u16(entry[2] + word * 0x10)) end
        print("MK2_FINISH_RECORD " .. entry[1] .. " " .. table.concat(values, " "))
    end
end)
