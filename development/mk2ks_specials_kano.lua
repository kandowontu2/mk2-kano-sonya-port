local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in1 = ports[":IN1"].fields
        local in2 = ports[":IN2"].fields
        pulse(in0["P1 High Punch"], 300, 4)
        pulse(in1["Coin 1"], 600, 4)
        pulse(in1["Coin 1"], 615, 4)
        pulse(in1["1 Player Start"], 640, 4)
        pulse(in0["P1 Block"], 810, 28)
        pulse(in0["P1 High Punch"], 820, 4)

        -- Liu Kang inputs drive the donor special-animation table.
        pulse(in0["P1 Right"], 1440, 3)
        pulse(in0["P1 Right"], 1450, 3)
        pulse(in0["P1 High Punch"], 1460, 4)
        pulse(in0["P1 Right"], 1580, 3)
        pulse(in0["P1 Right"], 1590, 3)
        pulse(in0["P1 High Kick"], 1600, 4)
        pulse(in2["P1 Low Kick"], 1740, 190)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 1420 or frame == 1462 or frame == 1470 or frame == 1480 or
       frame == 1500 or frame == 1602 or frame == 1610 or frame == 1620 or
       frame == 1640 or frame == 1928 or frame == 1940 or frame == 1960 then
        manager.machine.video:snapshot()
    end
end)
