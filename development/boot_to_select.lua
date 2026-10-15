local frame = 0
local pulses = {}

local function pulse(field, start_frame, duration)
    pulses[#pulses + 1] = { field = field, first = start_frame, last = start_frame + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        pulse(ports[":IN1"].fields["Coin 1"], 360, 4)
        pulse(ports[":IN1"].fields["Coin 1"], 375, 4)
        pulse(ports[":IN1"].fields["1 Player Start"], 390, 4)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 300 or frame == 365 or frame == 400 or frame == 450 or
       frame == 520 or frame == 620 or frame == 760 then
        print("snapshot frame " .. frame)
        manager.machine.video:snapshot()
    end
end)
