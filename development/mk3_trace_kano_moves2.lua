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

        -- Create room before testing the projectile.
        pulse(in0["P1 Left"], 1710, 24)

        -- Knife throw: Down, Back, High Punch with arcade-speed taps.
        pulse(in0["P1 Down"], 1750, 3)
        pulse(in0["P1 Left"], 1755, 3)
        pulse(in0["P1 High Punch"], 1760, 3)

        -- Blade swipe: Down, Forward, High Punch.
        pulse(in0["P1 Down"], 1840, 3)
        pulse(in0["P1 Right"], 1845, 3)
        pulse(in0["P1 High Punch"], 1850, 3)

        -- Cannonball: hold Low Kick for about three seconds, then release.
        pulse(in1["P1 Low Kick"], 1910, 190)

        -- Grab and shake: Down, Forward, Low Punch.
        pulse(in0["P1 Down"], 2200, 3)
        pulse(in0["P1 Right"], 2205, 3)
        pulse(in1["P1 Low Punch"], 2210, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 1690 or frame == 1760 or frame == 1775 or frame == 1850 or
       frame == 1865 or frame == 2100 or frame == 2120 or frame == 2210 or
       frame == 2230 then
        manager.machine.video:snapshot()
    end
end)
