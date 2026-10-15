local frame, pulses, taps = 0, {}, {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function sequence(first, fields)
    for index, field in ipairs(fields) do
        pulse(field, first + (index - 1) * 7, 3)
    end
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local low = ports[":IN2"].fields
        local space = manager.machine.devices[":maincpu"].spaces["program"]

        taps[#taps + 1] = space:install_read_tap(0xFF91FC60, 0xFF91FD7F, "liu main root",
            function(offset)
                if frame >= 1800 then
                    print(string.format("MK2ROOT frame=%d table=main offset=%08X id=%02X",
                        frame, offset, (offset - 0xFF91FC60) // 0x20))
                end
            end)
        taps[#taps + 1] = space:install_read_tap(0xFF9204A0, 0xFF9205BF, "liu special root",
            function(offset)
                if frame >= 1800 then
                    print(string.format("MK2ROOT frame=%d table=special offset=%08X id=%02X",
                        frame, offset, (offset - 0xFF9204A0) // 0x20))
                end
            end)

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 2"], 615, 4)
        pulse(system["2 Players Start"], 640, 4)
        pulse(high["P1 High Punch"], 920, 4)
        pulse(high["P2 High Punch"], 980, 4)
        pulse(high["P2 Block"], 1200, 2200)

        sequence(1850, { high["P1 Right"], high["P1 Right"], high["P1 High Punch"] })
        sequence(2100, { high["P1 Right"], high["P1 Right"], low["P1 Low Punch"] })
        sequence(2350, { high["P1 Right"], high["P1 Right"], high["P1 High Kick"] })
        pulse(low["P1 Low Kick"], 2600, 190)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
end)
