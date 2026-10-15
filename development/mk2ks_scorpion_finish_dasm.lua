-- Read-only stock MKII Scorpion HP dispatch and fatality-command inspection.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local machine = manager.machine
    local debugger = machine.debugger
    debugger.visible_cpu = machine.devices[":maincpu"]
    local program = machine.devices[":maincpu"].spaces.program
    local table_address = 0xff800000 + (0xff180 + 10 * 4) * 8
    local handler = program:read_u32(table_address)
    print(string.format("MK2_SCORPION_HP table=%08X handler=%08X", table_address, handler))
    assert(handler >= 0xff800000 and handler < 0xffe00000)
    for _, address in ipairs({0xff878eb0, 0xff878f80, 0xff879bb0}) do
        local words = {}
        for index = 0, 15 do
            words[#words + 1] = string.format("%04X", program:read_u16(address + index * 0x10))
        end
        print(string.format("MK2_SCORPION_RECORD address=%08X words=%s",
            address, table.concat(words, ",")))
    end
    debugger:command(string.format("dasm diagnostic_v103_scorpion_hp.asm,%08X,1400", handler))
    for _, segment in ipairs({
        {"actor_fire", 0xff8c6600, 0x900},
        {"victim_fire", 0xff9e1400, 0x1000},
    }) do
        debugger:command(string.format("dasm diagnostic_v103_scorpion_%s.asm,%08X,%X",
            segment[1], segment[2], segment[3]))
    end
    debugger.execution_state = "run"
end)
