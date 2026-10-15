-- Diagnostic-only two-player selector override for hidden and boss opponents.
-- The regular input-only air-throw probe still drives the actual move. This
-- wrapper changes only the victim's roster choice before actor construction.
local hidden_id = assert(tonumber(os.getenv("MK2KS_DIAGNOSTIC_HIDDEN_ID")))
assert(hidden_id >= 12 and hidden_id <= 16)
local attacker_side = tonumber(os.getenv("MK2KS_AIRTHROW_SIDE") or "1")
assert(attacker_side == 1 or attacker_side == 2)
local choice_address = attacker_side == 1 and 0x01060e50 or 0x01060280
local actor_address = attacker_side == 1 and 0x01060df0 or 0x01060220
dofile("mk2ks_airthrow_probe.lua")

local frame, program, saw_pose, saw_recovery, min_health, ready_health =
    0, nil, false, false, 161, false
local expected_pose = hidden_id == 16 and 0xff94de20 or 0xff97ba70
emu.register_frame(function()
    frame = frame + 1
    if not program then program = manager.machine.devices[":maincpu"].spaces.program end
    if frame >= 1060 and frame <= 1216 then
        program:write_u16(choice_address, hidden_id)
    end
    if frame >= 1250 then
        local actor = program:read_u32(actor_address)
        local process = program:read_u32(attacker_side == 1 and 0x01060e30 or 0x01060260)
        if actor >= 0x01000000 and actor < 0x01100000 and
            process >= 0x01000000 and process < 0x01100000 and
            program:read_u16(actor + 0x1f0) == hidden_id then
            local pose = program:read_u32(actor + 0x1d0)
            local y, floor_y = program:read_u16(actor + 0xb0), program:read_u16(process + 0x200)
            local health = program:read_u16(attacker_side == 1 and 0x01060ec0 or 0x010602f0)
            if health == 161 then ready_health = true end
            if ready_health then
                if health < min_health then min_health = health end
                if pose == expected_pose and y + 10 < floor_y then saw_pose = true end
                if saw_pose and y >= floor_y and pose ~= expected_pose then saw_recovery = true end
            end
        end
    end
    if frame == 1059 or frame == 1070 or frame == 1200 or frame == 1217 or
        frame == 1250 or frame == 1500 then
        local actor = program:read_u32(actor_address)
        local id = actor >= 0x01000000 and actor < 0x01100000 and
            program:read_u16(actor + 0x1f0) or 0xffff
        print(string.format("MK2KS_HIDDEN_AIR_SETUP frame=%d choice=%d actor=%08X id=%d",
            frame, program:read_u16(choice_address), actor, id))
    end
end)
emu.register_stop(function()
    print(string.format("MK2KS_HIDDEN_AIR_RESULT id=%d pose=%s recovery=%s damage=%d",
        hidden_id, tostring(saw_pose), tostring(saw_recovery), 161 - min_health))
end)
