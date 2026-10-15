-- Diagnostic only: observe MKII Sub-Zero's own knockdown/final prone groups.
dofile("mk2ks_selector_exit_test.lua")

local frame = 0
local last_pose
emu.register_frame(function()
    frame = frame + 1
    if frame < 1750 or frame > 2300 then return end
    local program = manager.machine.devices[":maincpu"].spaces.program
    local actor = program:read_u32(0x01060df0)
    if actor < 0x01000000 or actor >= 0x01100000 then return end
    if program:read_u16(actor + 0x1f0) ~= 8 then return end
    local health = program:read_u16(0x01060ec0)
    local pose = program:read_u32(actor + 0x1d0)
    if pose ~= last_pose or frame % 16 == 0 and health == 0 then
        print(string.format("MK2_STOCK_SUBZERO_PRONE frame=%d health=%d pose=%08X x=%d y=%d",
            frame, health, pose, program:read_u16(actor + 0x90),
            program:read_u16(actor + 0xb0)))
        if health == 0 and pose ~= last_pose then
            manager.machine.video:snapshot()
        end
        last_pose = pose
    end
end)
