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

        pulse(in2["Coin 1"], 360, 4)
        pulse(in2["1 Player Start"], 380, 4)
        pulse(in0["P1 Right"], 540, 4)
        pulse(in0["P1 Right"], 580, 4)
        pulse(in0["P1 Right"], 620, 4)
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in0["P1 High Punch"], 1180, 4)

        -- Knife throw: Down, Back, High Punch.
        pulse(in0["P1 Down"], 1660, 5)
        pulse(in0["P1 Left"], 1675, 5)
        pulse(in0["P1 High Punch"], 1690, 5)

        -- Cannonball: hold Low Kick for about three seconds, then release.
        pulse(in1["P1 Low Kick"], 1810, 185)

        -- Choke: Down, Forward, Low Punch.
        pulse(in0["P1 Down"], 2150, 5)
        pulse(in0["P1 Right"], 2165, 5)
        pulse(in1["P1 Low Punch"], 2180, 5)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 600 or frame == 900 or frame == 1200 or frame == 1550 or
       frame == 1690 or frame == 1720 or frame == 1995 or frame == 2025 or
       frame == 2180 or frame == 2210 then
        manager.machine.video:snapshot()
    end
end)
