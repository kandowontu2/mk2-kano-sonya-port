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
        local in2 = ports[":IN2"].fields
        for base = 360, 1320, 480 do
            pulse(in2["Coin 1"], base, 4)
            pulse(in2["1 Player Start"], base + 20, 4)
            pulse(in0["P1 Right"], base + 180, 4)
            pulse(in0["P1 Right"], base + 220, 4)
            pulse(in0["P1 Right"], base + 260, 4)
            pulse(in0["P1 High Punch"], base + 320, 4)
        end

        pulse(in0["P1 Down"], 1780, 3)
        pulse(in0["P1 Left"], 1785, 3)
        pulse(in0["P1 High Punch"], 1790, 3)
        pulse(in0["P1 Down"], 1880, 3)
        pulse(in0["P1 Left"], 1884, 3)
        pulse(in0["P1 High Punch"], 1888, 3)
        pulse(in0["P1 Down"], 1980, 5)
        pulse(in0["P1 Left"], 1983, 5)
        pulse(in0["P1 High Punch"], 1986, 5)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 1500 or frame == 1750 or frame == 1790 or frame == 1810 or
       frame == 1888 or frame == 1910 or frame == 1986 or frame == 2010 then
        manager.machine.video:snapshot()
    end
end)
