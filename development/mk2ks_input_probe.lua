local frame, pulses = 0, {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

local function two_step(first, direction, button, tap, gap, overlap)
    pulse(direction, first, tap)
    pulse(direction, first + tap + gap, tap)
    pulse(button, first + tap + gap + tap - overlap, tap)
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields

        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 2"], 615, 4)
        pulse(system["2 Players Start"], 640, 4)
        pulse(high["P1 Left"], 780, 4)
        pulse(high["P1 High Punch"], 850, 4)
        pulse(high["P2 High Punch"], 880, 4)
        pulse(high["P2 Block"], 1450, 1800)

        -- Probe increasingly generous timings, with the attack overlapping
        -- the second direction so the game's recorder cannot miss the chord.
        two_step(1600, high["P1 Right"], high["P1 High Punch"], 3, 2, 2)
        two_step(1850, high["P1 Right"], high["P1 High Punch"], 5, 3, 3)
        two_step(2100, high["P1 Right"], high["P1 High Punch"], 8, 4, 5)
        two_step(2350, high["P1 Left"], high["P1 High Punch"], 5, 3, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
end)
