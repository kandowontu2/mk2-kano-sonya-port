-- Read-only follow-up to the normal input-driven finisher harness.
dofile("mk2ks_finish_state_trace.lua")

local frame = 0
emu.register_frame(function()
    frame = frame + 1
    if frame < 3480 or frame > 3750 then return end
    local image_at = { [3492]=true, [3496]=true, [3500]=true, [3516]=true,
        [3520]=true, [3524]=true, [3528]=true, [3532]=true, [3584]=true,
        [3600]=true }
    if not image_at[frame] and frame % 4 ~= 0 then return end
    local program = manager.machine.devices[":maincpu"].spaces.program
    local p1 = program:read_u32(0x01060220)
    if p1 < 0x01000000 or p1 >= 0x01400000 then return end
    if image_at[frame] then
        manager.machine.video:snapshot()
        print(string.format("MK2_SONYA_WIN_SNAPSHOT frame=%d",frame))
    end
    print(string.format("MK2_SONYA_WIN_TRACE frame=%d id=%04X pose=%08X mode=%d callback=%08X",
        frame, program:read_u16(p1 + 0x1f0), program:read_u32(p1 + 0x1d0),
        program:read_u16(0x01061b00), program:read_u32(0xffff3400 + 18 * 0x20)))
end)
