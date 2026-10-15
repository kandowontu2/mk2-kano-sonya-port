local frame, pulses = 0, {}
local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high, system, low = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4); pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 Left"], 780, 4); pulse(high["P1 High Punch"], 850, 4)
        pulse(high["P1 Right"], 1480, 3); pulse(high["P1 Right"], 1487, 3)
        pulse(low["P1 Low Punch"], 1494, 3)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
end)
