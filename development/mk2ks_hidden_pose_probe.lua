-- Diagnostic-only wrapper: observe hidden opponents' native pose groups.
-- The regular ladder harness selects and fights them; this callback never
-- writes game memory or inputs.
dofile("mk2ks_cpu_ladder_trace.lua")

local frame, program, last_pose, last_id, changes = 0, nil, nil, nil, 0
emu.register_frame(function()
    frame = frame + 1
    if not program then program = manager.machine.devices[":maincpu"].spaces.program end
    local actor = program:read_u32(0x01060df0)
    if actor < 0x01000000 or actor >= 0x01100000 then return end
    local id = program:read_u16(actor + 0x1f0)
    if id < 14 or id > 16 then return end
    local pose = program:read_u32(actor + 0x1d0)
    if id == last_id and pose == last_pose then return end
    local process = program:read_u32(0x01060e30)
    local action = process >= 0x01000000 and process < 0x01100000 and
        program:read_u16(process + 0x1f0) or 0xffff
    local x, y = program:read_u16(actor + 0x90), program:read_u16(actor + 0xb0)
    local health = program:read_u16(0x01060ec0)
    if changes < 160 then
        print(string.format("MK2KS_HIDDEN_POSE frame=%d id=%d action=%04X pose=%08X xy=%d,%d health=%d",
            frame, id, action, pose, x, y, health))
        changes = changes + 1
    end
    last_id, last_pose = id, pose
end)
