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
        local in2 = ports[":IN2"].fields

        -- Repeated start/select sequence is intentionally redundant: it makes
        -- this trace deterministic from a completely fresh MK3 NVRAM folder.
        for base = 360, 1320, 480 do
            pulse(in2["Coin 1"], base, 4)
            pulse(in2["1 Player Start"], base + 20, 4)
            pulse(in0["P1 Right"], base + 180, 4)
            pulse(in0["P1 Right"], base + 220, 4)
            pulse(in0["P1 Right"], base + 260, 4)
            pulse(in0["P1 High Punch"], base + 320, 4)
        end

        -- The fresh-boot path reaches round one just before frame 2,000.
        -- Leave room, then exercise one native move at a time.
        pulse(in0["P1 Left"], 2020, 18)

        -- Knife throw: Down, Back, High Punch.
        pulse(in0["P1 Down"], 2070, 3)
        pulse(in0["P1 Left"], 2075, 3)
        pulse(in0["P1 High Punch"], 2080, 3)

        -- Blade swipe: Down, Forward, High Punch.
        pulse(in0["P1 Down"], 2200, 3)
        pulse(in0["P1 Right"], 2205, 3)
        pulse(in0["P1 High Punch"], 2210, 3)

        -- Grab and shake: Down, Forward, Low Punch.
        pulse(in0["P1 Down"], 2340, 3)
        pulse(in0["P1 Right"], 2345, 3)
        pulse(in1["P1 Low Punch"], 2350, 3)

        -- Cannonball: hold Low Kick for about three seconds, then release.
        pulse(in1["P1 Low Kick"], 2460, 190)

        -- A second pass runs late enough to cover the slower fresh-NVRAM boot
        -- path used by some hosts.
        pulse(in0["P1 Left"], 2760, 18)
        pulse(in0["P1 Down"], 2820, 3)
        pulse(in0["P1 Left"], 2825, 3)
        pulse(in0["P1 High Punch"], 2830, 3)
        pulse(in0["P1 Down"], 2970, 3)
        pulse(in0["P1 Right"], 2975, 3)
        pulse(in0["P1 High Punch"], 2980, 3)
        pulse(in0["P1 Down"], 3120, 3)
        pulse(in0["P1 Right"], 3125, 3)
        pulse(in1["P1 Low Punch"], 3130, 3)
        pulse(in1["P1 Low Kick"], 3250, 190)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    local shots = {
        [2000] = true, [2080] = true, [2095] = true, [2120] = true,
        [2210] = true, [2225] = true, [2250] = true,
        [2350] = true, [2365] = true, [2400] = true,
        [2645] = true, [2660] = true, [2700] = true,
        [2830] = true, [2845] = true, [2880] = true,
        [2980] = true, [2995] = true, [3030] = true,
        [3130] = true, [3145] = true, [3190] = true,
        [3435] = true, [3450] = true, [3490] = true,
    }
    if shots[frame] then manager.machine.video:snapshot() end
end)
