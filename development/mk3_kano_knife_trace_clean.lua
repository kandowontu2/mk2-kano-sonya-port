local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN2"].fields

        for base = 360, 1320, 480 do
            pulse(system["Coin 1"], base, 4)
            pulse(system["1 Player Start"], base + 20, 4)
            pulse(high["P1 Right"], base + 180, 4)
            pulse(high["P1 Right"], base + 220, 4)
            pulse(high["P1 Right"], base + 260, 4)
            pulse(high["P1 High Punch"], base + 320, 4)
        end

        local use_left = false
        for first = 3120, 4320, 80 do
            pulse(high["P1 Block"], first - 50, 35)
            pulse(high["P1 Down"], first, 4)
            local back = use_left and high["P1 Left"] or high["P1 Right"]
            pulse(back, first + 5, 8)
            pulse(high["P1 High Punch"], first + 7, 4)
            use_left = not use_left
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 2500 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        space:write_u8(0x01060A40, 0xA6)
        space:write_u8(0x010615F0, 0xA6)
    end

    if frame >= 3060 and frame <= 4400 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
