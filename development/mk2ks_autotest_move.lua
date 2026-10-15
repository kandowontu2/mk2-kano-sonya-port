local frame, pulses = 0, {}
local move = tonumber(os.getenv("MK2KS_TEST_MOVE") or "1")

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN1"].fields
        local low = ports[":IN2"].fields
        pulse(high["P1 High Punch"], 300, 4)
        for at = 600, 2400, 300 do
            pulse(system["Coin 1"], at, 4)
            pulse(system["1 Player Start"], at + 20, 4)
        end
        for at = 900, 4000, 180 do pulse(high["P1 High Punch"], at, 4) end

        for at = 4200, 7000, 120 do
            if move == 1 then
                pulse(high["P1 Block"], at, 6)
                pulse(high["P1 High Punch"], at + 1, 3)
            elseif move == 2 then
                pulse(high["P1 Block"], at, 6)
                pulse(low["P1 Low Punch"], at + 1, 3)
            elseif move == 3 then
                pulse(high["P1 Block"], at, 6)
                pulse(high["P1 High Kick"], at + 1, 3)
            end
        end
        if move == 4 then
            for at = 4150, 6950, 220 do pulse(low["P1 Low Kick"], at, 100) end
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 3200 and frame <= 7300 and frame % 10 == 0 then
        manager.machine.video:snapshot()
    end
end)
