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

        -- Clear a first-run CMOS warning, then enter the select screen.
        pulse(in0["P1 High Punch"], 300, 4)
        pulse(in1["Coin 1"], 600, 4)
        pulse(in1["Coin 1"], 615, 4)
        pulse(in1["1 Player Start"], 640, 4)

        -- Liu Kang is the upper-left portrait.  Block+HP selects Kano.
        pulse(in0["P1 Block"], 810, 28)
        pulse(in0["P1 High Punch"], 820, 4)

        -- Exercise several ordinary MKII attacks once the match begins.
        pulse(in0["P1 Right"], 1350, 90)
        pulse(in0["P1 High Punch"], 1470, 4)
        pulse(in2["P1 Low Punch"], 1540, 4)
        pulse(in0["P1 High Kick"], 1610, 4)
        pulse(in2["P1 Low Kick"], 1680, 4)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 720 or frame == 810 or frame == 950 or frame == 1250 or
       frame == 1500 or frame == 1750 then
        manager.machine.video:snapshot()
    end
end)
