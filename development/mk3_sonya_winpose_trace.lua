-- Read-only continuation of the original MK3 Sonya fatality actor-pose trace.
dofile("mk3_fatality_asset_trace.lua")

local frame, program, last_pose = 0, nil, nil
emu.register_frame(function()
    frame = frame + 1
    if not program then program = manager.machine.devices[":maincpu"].spaces.program end
    if frame < 3380 or frame > 3600 then return end
    local actor = program:read_u32(0x010609b0)
    if actor < 0x01000000 or actor >= 0x01400000 then return end
    local pose = program:read_u32(actor + 0x1d0)
    if pose ~= last_pose or frame % 20 == 0 then
        print(string.format("MK3_SONYA_WINPOSE frame=%d age=%d pose=%08X x=%d y=%d",
            frame, frame - 3189, pose,
            program:read_u16(actor + 0x90), program:read_u16(actor + 0xb0)))
        last_pose = pose
    end
end)
