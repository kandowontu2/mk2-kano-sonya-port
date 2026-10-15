-- Read-only follow-up for the input-driven one-player Kano finish.
-- Observe whether the attached skeleton survives the winner screen and is
-- retired by the game's own transition before the next ladder/fight.
dofile("mk2ks_finish_state_trace.lua")

local frame, program, previous = 0, nil, nil
local saw_win_skeleton, saw_next_fight_cleared = false, false
local function valid(pointer)
    return pointer >= 0x01000000 and pointer < 0x01100000
end
emu.register_frame(function()
    frame = frame + 1
    if not program then program = manager.machine.devices[":maincpu"].spaces.program end
    if frame < 2500 then return end
    local owner = program:read_u32(0x01060260)
    local attached = valid(owner) and program:read_u32(owner + 0x190) or 0
    local stage = program:read_u16(0x01061b30)
    local arena = program:read_u16(0x01061ac0)
    local mode = program:read_u16(0x01061b00)
    local pose = valid(attached) and program:read_u32(attached + 0x1d0) or 0
    if stage == 0 and arena == 0 and mode == 1 and pose == 0xfe9b2490 then
        saw_win_skeleton = true
    end
    if saw_win_skeleton and stage >= 1 and mode == 0 and attached == 0 then
        saw_next_fight_cleared = true
    end
    local state = string.format("%d:%08X:%08X", stage, attached, pose)
    if (state ~= previous or frame % 300 == 0) and frame < 8000 then
        print(string.format("MK2_SKELETON_LIFECYCLE frame=%d stage=%d arena=%d mode=%d owner=%08X attached=%08X pose=%08X",
            frame, stage, arena, mode, owner, attached, pose))
        previous = state
    end
end)
emu.register_stop(function()
    print(string.format("MK2_SKELETON_LIFECYCLE_RESULT pass=%s win_skeleton=%s next_fight_cleared=%s",
        tostring(saw_win_skeleton and saw_next_fight_cleared),
        tostring(saw_win_skeleton), tostring(saw_next_fight_cleared)))
end)
