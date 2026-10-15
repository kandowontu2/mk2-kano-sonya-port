-- Read-only original-MK3 Kano air-throw probe using real player inputs.
local frame, pulses, program, cpu = 0, {}, nil, nil
local taps = {}
local approach = tonumber(os.getenv("MK3_AIRTHROW_APPROACH") or "80")
local jump = tonumber(os.getenv("MK3_AIRTHROW_JUMP") or "3900")
local block = tonumber(os.getenv("MK3_AIRTHROW_BLOCK") or "3920")
assert(approach >= 0 and approach <= 80 and block > jump)
local function pulse(field, first, duration)
    assert(field)
    pulses[#pulses + 1] = {field, first, first + (duration or 4)}
end
local function signed(value) return value >= 0x8000 and value - 0x10000 or value end
local function state(side)
    local actor = program:read_u32(side == 1 and 0x010609b0 or 0x01061560)
    local process = program:read_u32(side == 1 and 0x010609f0 or 0x010615a0)
    return {
        actor = actor, process = process,
        id = program:read_u16(actor + 0x1f0),
        x = signed(program:read_u16(actor + 0x90)),
        y = signed(program:read_u16(actor + 0xb0)),
        pose = program:read_u32(actor + 0x1d0),
        action = program:read_u16(process + 0x1f0),
        health = program:read_u16(side == 1 and 0x01060a40 or 0x010615f0),
    }
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        cpu = manager.machine.devices[":maincpu"]
        program = cpu.spaces.program
        local ports = manager.machine.ioport.ports
        local high, low, system = ports[":IN0"].fields, ports[":IN1"].fields, ports[":IN2"].fields
        for base = 360, 1320, 480 do
            pulse(system["Coin 1"], base)
            pulse(system["1 Player Start"], base + 20)
            for _, offset in ipairs({180, 220, 260}) do pulse(high["P1 Right"], base + offset) end
            pulse(high["P1 High Punch"], base + 320)
        end
        for _, first in ipairs({2960, 2980, 3000}) do pulse(system["Coin 2"], first) end
        pulse(system["2 Players Start"], 3020)
        for _, first in ipairs({3060, 3090, 3120}) do pulse(high["P1 Right"], first) end
        pulse(high["P1 High Punch"], 3160)
        for _, first in ipairs({3100, 3160, 3220, 3280}) do pulse(high["P2 Left"], first) end
        pulse(high["P2 Down"], 3340)
        pulse(high["P2 High Punch"], 3400)
        if approach > 0 then pulse(high["P1 Right"], 3800, approach) end
        pulse(high["P1 Up"], jump, 3)
        pulse(high["P2 Up"], jump, 3)
        pulse(high["P1 Block"], block, 6)
        for _, range in ipairs({{0xff823ca0, 0xff8244bf, "main"},
                                 {0xff8244c0, 0xff824cdf, "special"}}) do
            taps[#taps + 1] = program:install_read_tap(range[1], range[2],
                "Kano donor air-throw animation", function(offset, data, mask)
                    if frame >= block - 3 and frame <= block + 65 and offset % 32 == 0 then
                        print(string.format("MK3_AIRTHROW_ROOT frame=%d kind=%s index=%d actor=%08X pc=%08X",
                            frame, range[3], (offset - range[1]) // 32,
                            cpu.state.A8.value, cpu.state.PC.value))
                    end
                end)
        end
    end
    for _, input in ipairs(pulses) do
        if frame == input[2] then input[1]:set_value(1) end
        if frame == input[3] then input[1]:clear_value() end
    end
    if frame == 3800 then
        assert(state(1).id == 0 and state(2).id == 1, "Original Kano/Sonya selection failed")
    end
    if frame == 3890 and os.getenv("MK3_AIRTHROW_TRACE") == "1" then
        local attacker, victim = state(1), state(2)
        for _, item in ipairs({{attacker.process + 0x1f0, "attacker_action"},
                                {victim.actor + 0x90, "victim_x"},
                                {victim.actor + 0xb0, "victim_y"},
                                {0x010615f0, "victim_health"}}) do
            taps[#taps + 1] = program:install_write_tap(item[1], item[1] + 15,
                "MK3 donor air throw " .. item[2], function(offset, data, mask)
                    if frame >= block - 2 and frame <= block + 60 then
                        print(string.format("MK3_AIRTHROW_WRITE frame=%d field=%s at=%08X data=%08X pc=%08X A8=%08X A13=%08X",
                            frame, item[2], offset, data, cpu.state.PC.value,
                            cpu.state.A8.value, cpu.state.A13.value))
                    end
                end)
        end
    end
    if frame >= 3890 and frame <= 4010 and frame % 4 == 0 then
        local a, b = state(1), state(2)
        print(string.format("MK3_AIRTHROW_STATE frame=%d distance=%d p1=%d,%d action=%04X pose=%08X health=%d p2=%d,%d action=%04X pose=%08X health=%d",
            frame, math.abs(a.x - b.x), a.x, a.y, a.action, a.pose, a.health,
            b.x, b.y, b.action, b.pose, b.health))
    end
    if frame == block + 10 or frame == block + 20 or frame == block + 35 then
        manager.machine.video:snapshot()
    end
end)
emu.register_stop(function()
    print("MK3_AIRTHROW_REFERENCE_END frame=" .. frame)
    for _, tap in ipairs(taps) do tap:remove() end
end)
