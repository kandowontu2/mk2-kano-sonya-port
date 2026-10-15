-- Original MK3 two-player Kano/Sonya selection by physical inputs only.
local frame = 0
local pulses = {}
local function pulse(field, first, duration)
    pulses[#pulses + 1] = {field = field, first = first, last = first + duration - 1}
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0, in2 = ports[":IN0"].fields, ports[":IN2"].fields
        -- The first start clears fresh CMOS/boot prompts; selection happens later.
        pulse(in2["Coin 1"], 360, 4)
        pulse(in2["Coin 2"], 360, 4)
        pulse(in2["2 Players Start"], 380, 4)
        pulse(in0["P1 Right"], 540, 4)
        pulse(in0["P1 Right"], 580, 4)
        pulse(in0["P1 Right"], 620, 4)
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in2["Coin 1"], 840, 4)
        pulse(in2["Coin 2"], 840, 4)
        pulse(in2["2 Players Start"], 860, 4)
        for _, at in ipairs({1000, 1030, 1060}) do
            pulse(in0["P1 Right"], at, 4)
        end
        pulse(in0["P1 High Punch"], 1090, 4)
        pulse(in0["P2 Down"], 1120, 4)
        for _, at in ipairs({1150, 1180, 1210}) do
            pulse(in0["P2 Left"], at, 4)
        end
        pulse(in0["P2 High Punch"], 1240, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 850 or frame == 900 or frame == 950 or frame == 1000 or
        frame == 1050 or frame == 1075 or frame == 1100 or frame == 1125 or
        frame == 1160 or frame == 1190 or frame == 1220 or frame == 1260 or
        frame == 1500 or frame == 1800 or
        frame == 2000 or frame == 2200 or frame == 2400 then
        manager.machine.video:snapshot()
    end
end)
