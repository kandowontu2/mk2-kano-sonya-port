-- Diagnostic-only MK3 input/health assistance to locate original winner audio.
-- This never runs against the MKII Kano/Sonya candidate.
dofile("mk3_sound_command_trace.lua")

local frame, program, fields = 0, nil, nil
local health_writes, last_health_write = 0, -1000
local function signed(value)
    return value >= 0x8000 and value - 0x10000 or value
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        program = manager.machine.devices[":maincpu"].spaces["program"]
        fields = manager.machine.ioport.ports[":IN0"].fields
    end
    if frame < 2250 then return end
    local p1, p2 = program:read_u32(0x010609b0), program:read_u32(0x01061560)
    local live = p1 >= 0x01000000 and p1 < 0x01400000 and
        p2 >= 0x01000000 and p2 < 0x01400000
    fields["P1 Right"]:clear_value()
    fields["P1 Left"]:clear_value()
    fields["P1 Down"]:clear_value()
    fields["P1 High Punch"]:clear_value()
    if not live then return end
    local hp1, hp2 = program:read_u16(0x01060a40), program:read_u16(0x010615f0)
    if hp1 > 0 and hp2 > 0 and hp2 <= 0xa6 then
        if hp2 > 1 then
            program:write_u16(0x010615f0, 1)
            health_writes = health_writes + 1
            last_health_write = frame
            print(string.format("MK3_WIN_HEALTH_WRITE frame=%d p1=%d cpu=%d count=%d",
                frame, hp1, hp2, health_writes))
        end
        if hp1 < 0xa6 then program:write_u16(0x01060a40, 0xa6) end
        local x1, x2 = signed(program:read_u16(p1 + 0x90)), signed(program:read_u16(p2 + 0x90))
        if math.abs(x1 - x2) > 75 then
            fields[x1 < x2 and "P1 Right" or "P1 Left"]:set_value(1)
        else
            fields["P1 Down"]:set_value(1)
            if frame % 32 <= 3 then fields["P1 High Punch"]:set_value(1) end
        end
    end
    if frame % 300 == 0 then
        print(string.format("MK3_WIN_STATE frame=%d p1=%d p2=%d hp=%d,%d writes=%d last=%d",
            frame, program:read_u16(p1 + 0x1f0), program:read_u16(p2 + 0x1f0), hp1, hp2,
            health_writes, last_health_write))
        manager.machine.video:snapshot()
    end
end)
