local frame, pulses, input_tap, root_tap, last_input = 0, {}, nil, nil, -1

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high, system = ports[":IN0"].fields, ports[":IN1"].fields
        local program = manager.machine.devices[":maincpu"].spaces["program"]
        input_tap = program:install_read_tap(0x01600000, 0x0160000f,
            "MK2 stock 2P input probe", function(offset, data, mask)
                if frame >= 1550 and frame < 1660 and data ~= last_input then
                    print(string.format("MK2_2P_INPUT frame=%d data=%04X", frame, data & 0xffff))
                    last_input = data
                end
            end)
        root_tap = program:install_read_tap(0xff91fc60, 0xff920d1f,
            "MK2 stock 2P root probe", function(offset, data, mask)
                if frame >= 1500 and frame < 1750 then
                    local state = manager.machine.devices[":maincpu"].state
                    if state["PC"].value == 0xff906140 and state["A8"].value == 0x01034e90 then
                        print(string.format("MK2_2P_ROOT frame=%d addr=%08X data=%04X", frame, offset, data & 0xffff))
                    end
                end
            end)

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 2"], 608, 4)
        pulse(system["2 Players Start"], 620, 4)
        pulse(high["P1 Up"], 706, 4)
        pulse(high["P1 High Punch"], 730, 4)
        pulse(high["P2 High Punch"], 780, 6)
        pulse(high["P1 Right"], 1600, 3)
        pulse(high["P1 Right"], 1605, 3)
        pulse(high["P1 High Punch"], 1606, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 1500 and frame <= 1750 and frame % 4 == 0 then
        manager.machine.video:snapshot()
    end
end)
