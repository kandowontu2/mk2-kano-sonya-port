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

        for base = 360, 1320, 480 do
            pulse(in2["Coin 1"], base, 4)
            pulse(in2["1 Player Start"], base + 20, 4)
            pulse(in0["P1 Down"], base + 240, 4)
            pulse(in0["P1 High Punch"], base + 320, 4)
        end

        -- Late pass: the slowest fresh-NVRAM route is in round one here.
        pulse(in0["P1 Left"], 2760, 18)

        -- Energy rings: Down, Forward, Low Punch.
        pulse(in0["P1 Down"], 2820, 3)
        pulse(in0["P1 Right"], 2825, 3)
        pulse(in1["P1 Low Punch"], 2830, 3)

        -- Leg grab: Down + Low Punch + Block.
        pulse(in0["P1 Down"], 2980, 4)
        pulse(in1["P1 Low Punch"], 2980, 4)
        pulse(in0["P1 Block"], 2980, 4)

        -- Square-wave punch: Forward, Back, High Punch.
        pulse(in0["P1 Right"], 3140, 3)
        pulse(in0["P1 Left"], 3145, 3)
        pulse(in0["P1 High Punch"], 3150, 3)

        -- Bicycle kick: Back, Back, Down, High Kick.
        pulse(in0["P1 Left"], 3300, 3)
        pulse(in0["P1 Left"], 3307, 3)
        pulse(in0["P1 Down"], 3314, 3)
        pulse(in0["P1 High Kick"], 3321, 3)

        -- Round-two pass tries both facing directions.  This removes opponent
        -- side-switching as a variable in the animation trace.
        pulse(in0["P1 Down"], 3450, 3); pulse(in0["P1 Right"], 3455, 3); pulse(in1["P1 Low Punch"], 3460, 3)
        pulse(in0["P1 Down"], 3550, 3); pulse(in0["P1 Left"], 3555, 3); pulse(in1["P1 Low Punch"], 3560, 3)
        pulse(in0["P1 Right"], 3660, 3); pulse(in0["P1 Left"], 3665, 3); pulse(in0["P1 High Punch"], 3670, 3)
        pulse(in0["P1 Left"], 3760, 3); pulse(in0["P1 Right"], 3765, 3); pulse(in0["P1 High Punch"], 3770, 3)
        pulse(in0["P1 Left"], 3860, 3); pulse(in0["P1 Left"], 3867, 3); pulse(in0["P1 Down"], 3874, 3); pulse(in0["P1 High Kick"], 3881, 3)
        pulse(in0["P1 Right"], 3980, 3); pulse(in0["P1 Right"], 3987, 3); pulse(in0["P1 Down"], 3994, 3); pulse(in0["P1 High Kick"], 4001, 3)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    local shots = {
        [2700] = true,
        [2830] = true, [2845] = true, [2880] = true,
        [2980] = true, [2995] = true, [3040] = true,
        [3150] = true, [3165] = true, [3210] = true,
        [3321] = true, [3336] = true, [3380] = true,
        [3460] = true, [3475] = true, [3510] = true,
        [3560] = true, [3575] = true, [3610] = true,
        [3670] = true, [3685] = true, [3720] = true,
        [3770] = true, [3785] = true, [3820] = true,
        [3881] = true, [3896] = true, [3940] = true,
        [4001] = true, [4016] = true, [4060] = true,
    }
    if shots[frame] then manager.machine.video:snapshot() end
end)
