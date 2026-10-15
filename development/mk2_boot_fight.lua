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
        pulse(in0["P1 High Punch"], 540, 4)
        pulse(in0["P1 High Punch"], 620, 4)
        pulse(in0["P1 High Punch"], 700, 4)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 450 or frame == 560 or frame == 900 or frame == 1250 then
        print("MKII trace snapshot frame " .. frame)
        manager.machine.video:snapshot()
    end
end)
