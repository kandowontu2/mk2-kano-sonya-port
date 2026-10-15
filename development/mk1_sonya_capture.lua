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
        pulse(in1["Coin 1"], 2200, 4)
        pulse(in1["Coin 1"], 2220, 4)
        pulse(in1["Coin 1"], 2240, 4)
        pulse(in1["1 Player Start"], 2280, 4)
        pulse(in0["P1 Right"], 2410, 4)
        pulse(in0["P1 Right"], 2440, 4)
        pulse(in0["P1 High Punch"], 2500, 4)
        pulse(in0["P1 Right"], 3100, 90)
        pulse(in0["P1 High Punch"], 3210, 4)
        pulse(in1["P1 Low Punch"], 3270, 4)
        pulse(in0["P1 High Kick"], 3330, 4)
        pulse(in1["P1 Low Kick"], 3390, 4)
        pulse(in0["P1 Down"], 3450, 50)
        pulse(in0["P1 High Punch"], 3460, 4)
        pulse(in0["P1 Up"], 3550, 4)
        pulse(in0["P1 Right"], 3550, 4)
        pulse(in0["P1 High Kick"], 3580, 4)
        pulse(in0["P1 Block"], 3700, 60)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 2350 or frame == 2550 or frame == 2900 or frame == 3300 or frame == 3700 then
        manager.machine.video:snapshot()
    end
end)
