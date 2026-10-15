local frame, pulses = 0, {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 Left"], 780, 4)
        pulse(high["P1 High Punch"], 850, 4)

        pulse(high["P1 Block"], 1700, 180)
        pulse(high["P1 Block"], 2000, 6)
        pulse(high["P1 High Punch"], 2001, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 1940 and frame <= 2140 and frame % 4 == 0 then
        manager.machine.video:snapshot()
    end
end)
