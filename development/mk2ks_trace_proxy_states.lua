local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function sequence(first, fields)
    for index, field in ipairs(fields) do pulse(field, first + (index - 1) * 7, 3) end
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in1 = ports[":IN1"].fields
        local in2 = ports[":IN2"].fields

        pulse(in0["P1 High Punch"], 300, 4)
        pulse(in1["Coin 1"], 600, 4)
        pulse(in1["Coin 1"], 615, 4)
        pulse(in1["1 Player Start"], 640, 4)
        pulse(in0["P1 Left"], 780, 4)
        pulse(in0["P1 High Punch"], 850, 4)

        -- The three native Liu states used as safe MKII gameplay proxies.
        sequence(1480, { in0["P1 Right"], in0["P1 Right"], in0["P1 High Punch"] })
        sequence(1680, { in0["P1 Right"], in0["P1 Right"], in2["P1 Low Punch"] })
        sequence(1880, { in0["P1 Right"], in0["P1 Right"], in0["P1 High Kick"] })
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
end)
