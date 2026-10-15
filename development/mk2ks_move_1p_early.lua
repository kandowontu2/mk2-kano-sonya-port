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
        pulse(system["Coin 1"], 600, 4)
        pulse(system["Coin 1"], 615, 4)
        pulse(system["1 Player Start"], 640, 4)
        pulse(high["P1 Left"], 780, 4)
        pulse(high["P1 High Punch"], 920, 4)

        if move == 1 then
            for at = 1490, 1530, 20 do
                pulse(high["P1 Block"], at, 6)
                pulse(high["P1 High Punch"], at + 1, 3)
            end
        elseif move == 2 then
            for at = 1490, 1530, 20 do
                pulse(high["P1 Block"], at, 6)
                pulse(low["P1 Low Punch"], at + 1, 3)
            end
        elseif move == 3 then
            for at = 1490, 1530, 20 do
                pulse(high["P1 Block"], at, 6)
                pulse(high["P1 High Kick"], at + 1, 3)
            end
        else
            pulse(low["P1 Low Kick"], 1400, 95)
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 1450 and frame <= 1700 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
