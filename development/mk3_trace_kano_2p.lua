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
        pulse(in2["Coin 2"], 360, 4)
        pulse(in2["2 Players Start"], 380, 4)
        pulse(in0["P1 Right"], 540, 4)
        pulse(in0["P1 Right"], 580, 4)
        pulse(in0["P1 Right"], 620, 4)
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in0["P2 High Punch"], 700, 4)

        -- Kano knife throw.
        pulse(in0["P1 Down"], 1250, 5)
        pulse(in0["P1 Left"], 1265, 5)
        pulse(in0["P1 High Punch"], 1280, 5)

        -- Kano cannonball.
        pulse(in1["P1 Low Kick"], 1430, 185)

        -- Kano choke.
        pulse(in0["P1 Down"], 1760, 5)
        pulse(in0["P1 Right"], 1775, 5)
        pulse(in1["P1 Low Punch"], 1790, 5)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 600 or frame == 720 or frame == 900 or frame == 1100 or
       frame == 1280 or frame == 1300 or frame == 1615 or frame == 1640 or
       frame == 1790 or frame == 1820 then
        manager.machine.video:snapshot()
    end
end)
