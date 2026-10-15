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
        local system = ports[":IN2"].fields

        -- A completely clean run reaches the title around frame 6,700 after
        -- the first uninterrupted attract/audit path.  Start there so the
        -- selection and move trace no longer depend on cached NVRAM timing.
        pulse(system["Coin 1"], 6720, 4)
        pulse(system["1 Player Start"], 6740, 4)
        pulse(high["P1 Right"], 6900, 4)
        pulse(high["P1 Right"], 6940, 4)
        pulse(high["P1 Right"], 6980, 4)
        pulse(high["P1 High Punch"], 7040, 4)
        pulse(high["P1 High Punch"], 7540, 4)

        for first = 8250, 9090, 120 do
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

    if frame >= 6520 and frame <= 9200 and frame % 10 == 0 then
        manager.machine.video:snapshot()
    end
end)
