-- Input-only ground harness plus an airborne snapshot for floor-shadow QA.
dofile("mk2ks_ground_alignment_test.lua")
local frame=0
emu.register_frame(function()
    frame=frame+1
    if frame==1510 or frame==1710 then
        manager.machine.screens[":screen"]:snapshot()
        local program=manager.machine.devices[":maincpu"].spaces.program
        for side,pointers in ipairs({{0x01060220,0x01060260},{0x01060df0,0x01060e30}}) do
            local actor=program:read_u32(pointers[1])
            local task=program:read_u32(pointers[2])
            print(string.format("MK2_FLOOR_SHADOW_AIR frame=%d side=%d y=%d floor=%d",
                frame,side,program:read_u16(actor+0xb0),program:read_u16(task+0x200)))
        end
    end
end)
