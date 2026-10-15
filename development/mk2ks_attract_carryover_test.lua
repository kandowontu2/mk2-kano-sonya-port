-- Observe the first stock attract fight after a native fighter's campaign ends.
-- This adds no gameplay writes to the existing input-driven selector harness.
dofile("mk2ks_selector_exit_test.lua")

local frame, first, count = 0, nil, 0
emu.register_frame(function()
    frame = frame + 1
    if frame < 9000 then return end
    local program = manager.machine.devices[":maincpu"].spaces.program
    local p1, p2 = program:read_u32(0x01060220), program:read_u32(0x01060df0)
    local valid = p1 >= 0x01000000 and p1 < 0x01100000 and
        p2 >= 0x01000000 and p2 < 0x01100000
    if valid then
        local id1, id2 = program:read_u16(p1 + 0x1f0), program:read_u16(p2 + 0x1f0)
        if id1 <= 11 and id2 <= 11 then
            if not first and program:read_u16(0x010602f0) == 161 and
                program:read_u16(0x01060ec0) == 161 then first = frame end
            if first and (frame == first or frame == first + 45 or frame == first + 90) then
                count = count + 1
                print(string.format(
                    "MK2KS_ATTRACT_CARRYOVER frame=%d age=%d stock_ids=%d,%d roster_ids=%d,%d hp=%d,%d snapshot=%d",
                    frame, frame - first, id1, id2,
                    program:read_u16(0x01060280), program:read_u16(0x01060e50),
                    program:read_u16(0x010602f0), program:read_u16(0x01060ec0), count))
                manager.machine.video:snapshot()
            end
        end
    end
    if frame == 13600 then
        print(string.format("MK2KS_ATTRACT_CARRYOVER_RESULT stock_combat=%s captures=%d",
            tostring(first ~= nil), count))
    end
end)
