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
        pulse(in1["Coin 1"], 360, 4)
        pulse(in1["Coin 1"], 375, 4)
        pulse(in1["1 Player Start"], 390, 4)
        pulse(in0["P1 Down"], 445, 4)
        pulse(in0["P1 Down"], 470, 4)
        pulse(in0["P1 Right"], 495, 4)
        pulse(in0["P1 Right"], 520, 4)
        pulse(in0["P1 High Punch"], 565, 4)
        pulse(in0["P1 High Punch"], 640, 4)
        pulse(in0["P1 High Punch"], 720, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 440 or frame == 530 or frame == 920 or frame == 1080 or frame == 1280 then
        manager.machine.video:snapshot()
    end
end)
