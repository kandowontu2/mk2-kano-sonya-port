-- Original MK3 reference: real controls and read-only state observation.
-- No health, position, actor, ROM or input-history memory writes.
local frame, pulses, taps = 0, {}, {}
local program, cpu
-- MAME 0.289 notifier subscriptions must stay reachable after script return.
mk3_square_subscriptions = {}
local function pulse(field, first, duration)
    pulses[#pulses + 1] = {field, first, first + (duration or 4)}
end
local function signed(value)
    return value >= 0x8000 and value - 0x10000 or value
end
mk3_square_subscriptions.frame = (emu.add_machine_frame_notifier or emu.register_frame)(function()
    frame = frame + 1
    if frame == 1 then
        cpu = manager.machine.devices[":maincpu"]
        program = cpu.spaces.program
        local ports = manager.machine.ioport.ports
        local high, system = ports[":IN0"].fields, ports[":IN2"].fields
        for base = 360, 1320, 480 do
            pulse(system["Coin 1"], base)
            pulse(system["1 Player Start"], base + 20)
            pulse(high["P1 Down"], base + 240)
            pulse(high["P1 High Punch"], base + 320)
        end
        pulse(system["Coin 2"], 2960)
        pulse(system["Coin 2"], 2980)
        pulse(system["Coin 2"], 3000)
        pulse(system["2 Players Start"], 3020)
        pulse(high["P1 Down"], 3090)
        pulse(high["P1 High Punch"], 3160)
        pulse(high["P2 High Punch"], 3180)
        for first = 3900, 4300, 200 do
            pulse(high["P1 Right"], first, 3)
            pulse(high["P1 Left"], first + 5, 3)
            pulse(high["P1 High Punch"], first + 6, 3)
        end
        if os.getenv("MK3_SQUARE_TARGET") == "air" then pulse(high["P2 Up"], 3913, 3) end
        taps[#taps + 1] = program:install_read_tap(0xffa5a930, 0xffa5a99f,
            "original square hitbox", function(offset, data, mask)
                if offset == 0xffa5a930 then
                    local actor = cpu.state.A8.value
                    print(string.format("MK3_SQUARE_ATTACK frame=%d actor=%08X x=%d y=%d ground=%d action=%04X",
                        frame, actor, signed(program:read_u16(actor+0x90)), signed(program:read_u16(actor+0xb0)),
                        signed(program:read_u16(cpu.state.A13.value+0x200)), program:read_u16(cpu.state.A13.value+0x1f0)))
                end
            end)
    end
    for _, p in ipairs(pulses) do
        if frame == p[2] then p[1]:set_value(1) end
        if frame == p[3] then p[1]:clear_value() end
    end
    if frame % 120 == 0 or (frame >= 3890 and frame <= 4000) then
        local actors = {program:read_u32(0x010609b0), program:read_u32(0x01061560)}
        for side, actor in ipairs(actors) do
            if actor >= 0x01000000 and actor < 0x01400000 then
                print(string.format("MK3_SQUARE_STATE frame=%d side=%d actor=%08X id=%d x=%d y=%d vx=%08X vy=%08X health=%d,%d",
                    frame, side, actor, program:read_u16(actor+0x1f0), signed(program:read_u16(actor+0x90)),
                    signed(program:read_u16(actor+0xb0)), program:read_u32(actor+0x40), program:read_u32(actor+0x60),
                    program:read_u16(0x01060a40),program:read_u16(0x010615f0)))
            end
        end
    end
    if frame == 3050 or frame == 3140 or frame == 3400 or frame == 3800 or (frame >= 3900 and frame <= 3980 and frame % 4 == 0) then
        manager.machine.video:snapshot()
    end
end)
mk3_square_subscriptions.stop = (emu.add_machine_stop_notifier or emu.register_stop)(function()
    for _, tap in ipairs(taps) do tap:remove() end
end)
