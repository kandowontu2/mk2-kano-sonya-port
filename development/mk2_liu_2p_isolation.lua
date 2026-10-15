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
        pulse(system["2 Players Start"], 640, 4)
        pulse(high["P1 High Punch"], 850, 4)
        pulse(high["P2 High Punch"], 900, 4)
        pulse(high["P2 Block"], 1250, 1000)

        pulse(high["P1 Right"], 1500, 3)
        pulse(high["P1 Right"], 1505, 3)
        pulse(high["P1 High Punch"], 1506, 3)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 700 and frame <= 1700 and frame % 5 == 0 then
        manager.machine.video:snapshot()
    end
end)
