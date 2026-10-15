local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local low = ports[":IN1"].fields
        local system = ports[":IN2"].fields

        pulse(system["Coin 1"], 360, 4)
        pulse(system["1 Player Start"], 380, 4)
        pulse(high["P1 Right"], 540, 4)
        pulse(high["P1 Right"], 580, 4)
        pulse(high["P1 Right"], 620, 4)
        pulse(high["P1 High Punch"], 680, 4)
        pulse(high["P1 High Punch"], 1180, 4)

        -- Repeat Kano's native knife command after the round is fully active.
        -- Blocking between attempts reduces CPU interruptions without changing
        -- the command itself: Down, Back, High Punch from the left side.
        for first = 2200, 3520, 120 do
            pulse(high["P1 Block"], first - 75, 55)
            pulse(high["P1 Down"], first, 4)
            pulse(high["P1 Left"], first + 5, 4)
            pulse(high["P1 High Punch"], first + 10, 4)
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 2160 and frame <= 3600 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
