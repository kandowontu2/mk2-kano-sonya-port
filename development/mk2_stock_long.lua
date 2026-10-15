local frame, pulses = 0, {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high, system = ports[":IN0"].fields, ports[":IN1"].fields
        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 High Punch"], 850, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 1200 and frame % 300 == 0 then
        local cpu = manager.machine.devices[":maincpu"].state
        print(string.format("MK2_LONG frame=%d pc=%08X A8=%08X", frame,
            cpu["PC"].value, cpu["A8"].value))
        manager.machine.video:snapshot()
    end
end)

emu.register_stop(function()
    local cpu = manager.machine.devices[":maincpu"].state
    local program = manager.machine.devices[":maincpu"].spaces["program"]
    print(string.format("MK2_LONG_STOP frame=%d pc=%08X A8=%08X", frame,
        cpu["PC"].value, cpu["A8"].value))
    local matches, nonzero = {}, 0
    for index = 0, 60 do
        local value = program:read_u32(0x0105bb30 + index * 0x40)
        if value ~= 0 then nonzero = nonzero + 1 end
        if value == 0xffafe5a0 then matches[#matches + 1] = index end
    end
    print(string.format("MK2_LONG_TABLE nonzero=%d target_indices=%s",
        nonzero, table.concat(matches, ",")))
end)
