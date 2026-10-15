local frame = 0
local pulses = {}

local function pulse(field, start_frame, duration)
    pulses[#pulses + 1] = { field = field, first = start_frame, last = start_frame + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in1 = ports[":IN1"].fields
        local in2 = ports[":IN2"].fields
        pulse(in1["Coin 1"], 360, 4)
        pulse(in1["Coin 1"], 375, 4)
        pulse(in1["1 Player Start"], 390, 4)
        pulse(in0["P1 High Punch"], 540, 4)
        pulse(in0["P1 High Punch"], 620, 4)
        pulse(in0["P1 High Punch"], 700, 4)
        pulse(in0["P1 Right"], 1450, 90)
        pulse(in0["P1 High Punch"], 1580, 4)
        pulse(in2["P1 Low Punch"], 1650, 4)
        pulse(in0["P1 High Kick"], 1720, 4)
        pulse(in2["P1 Low Kick"], 1790, 4)
        pulse(in0["P1 Down"], 1860, 50)
        pulse(in0["P1 High Punch"], 1870, 4)
        pulse(in0["P1 Up"], 1970, 4)
        pulse(in0["P1 Right"], 1970, 4)
        pulse(in0["P1 High Kick"], 2010, 4)
        pulse(in0["P1 Block"], 2140, 60)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 1250 or frame == 1450 or frame == 1650 or frame == 1850 or
       frame == 2050 or frame == 2250 then
        manager.machine.video:snapshot()
    end
end)
