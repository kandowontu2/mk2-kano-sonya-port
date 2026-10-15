local frame, pulses = 0, {}
local fighter = os.getenv("MK2KS_TEST_FIGHTER") or "kano"
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
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 Block"], 810, 28)
        pulse(high[fighter == "kano" and "P1 High Punch" or "P1 High Kick"], 820, 4)

        -- Battle-plan timing varies with NVRAM.  Retry the same move often
        -- enough that several attempts land after player control is enabled.
        for at = 1800, 6500, 120 do
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
            for at = 1750, 6450, 220 do pulse(low["P1 Low Kick"], at, 100) end
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 1600 and frame <= 7000 and frame % 5 == 0 then
        manager.machine.video:snapshot()
    end
end)
