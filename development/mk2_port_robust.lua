local frame = 0
local pulses = {}

local function pulse(field, start_frame, duration)
    pulses[#pulses + 1] = { field = field, first = start_frame, last = start_frame + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in1 = ports[":IN1"].fields
        local in2 = ports[":IN2"].fields

        -- A clean NVRAM boot can spend much longer in diagnostics/attract than
        -- an established run.  Repeated credit/start pairs make this harness
        -- insensitive to that timing without touching emulated memory.
        for first = 600, 2400, 300 do
            pulse(in1["Coin 1"], first, 4)
            pulse(in1["1 Player Start"], first + 20, 4)
        end
        for first = 1000, 3000, 120 do
            pulse(in0["P1 High Punch"], first, 4)
        end

        pulse(in0["P1 Right"], 2800, 80)
        pulse(in0["P1 High Punch"], 2920, 4)
        pulse(in2["P1 Low Punch"], 3040, 4)
        pulse(in0["P1 High Kick"], 3160, 4)
        pulse(in2["P1 Low Kick"], 3280, 4)
        pulse(in0["P1 Down"], 3400, 50)
        pulse(in0["P1 High Punch"], 3410, 4)
        pulse(in0["P1 Up"], 3540, 4)
        pulse(in0["P1 Right"], 3540, 4)
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame == 900 or frame == 1500 or frame == 2100 or frame == 2600 or
       frame == 2900 or frame == 3200 or frame == 3500 or frame == 3800 then
        print("MKII robust snapshot frame " .. frame)
        manager.machine.video:snapshot()
    end
end)
