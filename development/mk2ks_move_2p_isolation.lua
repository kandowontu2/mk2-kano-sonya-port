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

        -- Clear the first-run warning and start a human-vs-human match so the
        -- second fighter cannot interrupt the move under test.
        pulse(high["P1 High Punch"], 300, 4)
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 2"], 615, 4)
        pulse(system["2 Players Start"], 640, 4)

        -- MKII starts P1 on Sub-Zero in two-player mode.  Move the native
        -- cursor up to Liu Kang before entering either virtual cell so the
        -- gameplay proxy matches the hybrid animation scripts.
        pulse(high["P1 Up"], 740, 4)

        if fighter == "kano" then
            pulse(high["P1 Left"], 780, 4)
        else
            for at = 750, 870, 30 do
                pulse(high["P1 Right"], at, 4)
            end
        end
        pulse(high["P1 High Punch"], 920, 4)
        pulse(high["P2 High Punch"], 980, 4)
        pulse(high["P2 Block"], 1200, 1200)

        if move == 1 then
            pulse(high["P1 Block"], 1850, 6)
            pulse(high["P1 High Punch"], 1851, 3)
        elseif move == 2 then
            pulse(high["P1 Block"], 1850, 6)
            pulse(low["P1 Low Punch"], 1851, 3)
        elseif move == 3 then
            pulse(high["P1 Block"], 1850, 6)
            pulse(high["P1 High Kick"], 1851, 3)
        else
            pulse(low["P1 Low Kick"], 1700, 95)
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 1650 and frame <= 2200 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
