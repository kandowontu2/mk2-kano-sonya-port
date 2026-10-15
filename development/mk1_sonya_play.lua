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
        pulse(in1["Coin 1"], 360, 4)
        pulse(in1["Coin 1"], 375, 4)
        pulse(in1["1 Player Start"], 390, 4)
        pulse(in0["P1 Right"], 470, 4)
        pulse(in0["P1 Right"], 490, 4)
        pulse(in0["P1 High Punch"], 540, 4)

        -- Exercise a representative set of Sonya movement and attack animations.
        pulse(in0["P1 Right"], 1500, 90)
        pulse(in0["P1 High Punch"], 1610, 4)
        pulse(in1["P1 Low Punch"], 1660, 4)
        pulse(in0["P1 High Kick"], 1710, 4)
        pulse(in1["P1 Low Kick"], 1760, 4)
        pulse(in0["P1 Down"], 1810, 50)
        pulse(in0["P1 High Punch"], 1820, 4)
        pulse(in0["P1 Up"], 1900, 4)
        pulse(in0["P1 Right"], 1900, 4)
        pulse(in0["P1 High Kick"], 1930, 4)
        pulse(in0["P1 Left"], 2020, 20)
        pulse(in0["P1 High Punch"], 2040, 4)
        pulse(in0["P1 Block"], 2110, 60)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 510 or frame == 560 or frame == 900 or frame == 1100 or
       frame == 1300 or frame == 1500 or frame == 1800 or frame == 2100 then
        print("snapshot frame " .. frame)
        manager.machine.video:snapshot()
    end
end)
