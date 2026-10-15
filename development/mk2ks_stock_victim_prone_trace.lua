-- Diagnostic only: observe a stock P2 fighter's own held end-of-round pose.
dofile("mk2ks_selector_exit_test.lua")

local ids = {kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,
    shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11}
local victim = assert(os.getenv("MK2KS_P2_FIGHTER"))
local expected = assert(ids[victim], "stock victim required")
local frame, held_pose, held_health, held_id = 0, nil, nil, nil
local last_pose

emu.register_frame(function()
    frame = frame + 1
    if frame < 1800 or frame > 2300 then return end
    local program = manager.machine.devices[":maincpu"].spaces.program
    local actor = program:read_u32(0x01060df0)
    if actor < 0x01000000 or actor >= 0x01100000 then return end
    local id = program:read_u16(actor + 0x1f0)
    if id ~= expected then return end
    local health = program:read_u16(0x01060ec0)
    local pose = program:read_u32(actor + 0x1d0)
    if health == 0 and pose ~= last_pose then
        print(string.format("MK2_STOCK_VICTIM_FALL frame=%d victim=%s id=%d pose=%08X",
            frame, victim, id, pose))
        last_pose = pose
    end
    if frame == 2200 then
        held_pose, held_health, held_id = pose, health, id
        manager.machine.video:snapshot()
        print(string.format("MK2_STOCK_VICTIM_HELD frame=%d victim=%s id=%d health=%d pose=%08X",
            frame, victim, id, health, pose))
    end
end)

emu.register_stop(function()
    print(string.format("MK2_STOCK_VICTIM_PRONE_RESULT pass=%s victim=%s id=%s health=%s pose=%s",
        tostring(held_id == expected and held_health == 0 and held_pose ~= nil),
        victim, tostring(held_id), tostring(held_health),
        held_pose and string.format("%08X", held_pose) or "missing"))
end)
