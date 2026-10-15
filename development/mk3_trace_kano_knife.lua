local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function sequence(down, back, punch, spacing, duration)
    pulse(down, punch, duration)
    pulse(back, punch + spacing, duration)
    pulse(manager.machine.ioport.ports[":IN0"].fields["P1 High Punch"], punch + spacing * 2, duration)
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in2 = ports[":IN2"].fields
        pulse(in2["Coin 1"], 360, 4)
        pulse(in2["1 Player Start"], 380, 4)
        pulse(in0["P1 Right"], 540, 4)
        pulse(in0["P1 Right"], 580, 4)
        pulse(in0["P1 Right"], 620, 4)
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in0["P1 High Punch"], 1180, 4)

        pulse(in0["P1 Left"], 1705, 20)
        sequence(in0["P1 Down"], in0["P1 Left"], 1740, 3, 2)
        sequence(in0["P1 Down"], in0["P1 Left"], 1810, 4, 3)
        sequence(in0["P1 Down"], in0["P1 Left"], 1880, 2, 5)
        sequence(in0["P1 Down"], in0["P1 Left"], 1950, 1, 3)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 1735 or frame == 1746 or frame == 1760 or
       frame == 1805 or frame == 1818 or frame == 1835 or
       frame == 1875 or frame == 1884 or frame == 1900 or
       frame == 1945 or frame == 1955 or frame == 1970 then
        manager.machine.video:snapshot()
    end
end)
