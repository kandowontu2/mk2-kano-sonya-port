-- Diagnostic-only original MK3 Kano/Jax selection with physical controls.
local frame = 0
local pulses = {}
local victim = os.getenv("MK3_FATALITY_VICTIM") or "jax"
assert(victim=="jax" or victim=="sonya" or victim=="sub_zero")
local join_frame = tonumber(os.getenv("MK3_P2_JOIN_FRAME") or "1720")
assert(join_frame==630 or join_frame==1720)
local function pulse(field, first, duration)
    pulses[#pulses + 1] = {field = field, first = first, last = first + duration - 1}
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0, in2 = ports[":IN0"].fields, ports[":IN2"].fields
        pulse(in2["Coin 1"], 360, 4)
        pulse(in2["Coin 2"], 360, 4)
        pulse(in2["1 Player Start"], 380, 4)
        for _, at in ipairs({540, 580, 620}) do pulse(in0["P1 Right"], at, 4) end
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in2["Coin 1"], join_frame-20, 4)
        pulse(in2["Coin 2"], join_frame-20, 4)
        pulse(in2["2 Players Start"], join_frame, 4)
        if join_frame>1000 then
            -- Joining from an active match opens a new selector for both sides.
            for _, at in ipairs({join_frame+70,join_frame+100,join_frame+130}) do
                pulse(in0["P1 Right"], at, 4)
            end
            pulse(in0["P1 High Punch"], join_frame+190, 4)
        end
        -- P2 starts on Liu Kang (top right). Keep Kano, stage timing and
        -- the automatic finish unchanged while selecting the victim.
        if victim=="sonya" or victim=="sub_zero" then
            pulse(in0["P2 Down"], join_frame+100, 4)
        end
        pulse(in0["P2 Left"], join_frame+130, 4)
        if victim~="sub_zero" then pulse(in0["P2 Left"], join_frame+160, 4) end
        if victim=="sonya" then pulse(in0["P2 Left"], join_frame+190, 4) end
        pulse(in0["P2 High Punch"], join_frame+220, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame == 500 or frame == 540 or frame == 580 or frame == 620 or
        frame == 680 or frame == 720 or frame == join_frame+30 or
        frame == join_frame+130 or frame == join_frame+160 or
        frame == join_frame+200 or frame == join_frame+240 or
        frame == join_frame+480 then
        manager.machine.video:snapshot()
    end
end)
