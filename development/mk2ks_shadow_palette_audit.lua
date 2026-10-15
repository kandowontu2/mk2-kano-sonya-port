dofile("mk2ks_ground_alignment_test.lua")
local frame=0
emu.register_frame(function()
    frame=frame+1
    if frame~=1450 then return end
    local palette=manager.machine.palettes[":palette"]
    for _,bank in ipairs({0x0000,0x0100,0x0200,0x0300,0x1b00,0x1c00}) do
        for pen=0,31 do
            print(string.format("MK2_SHADOW_PEN index=%04X rgb=%08X",bank+pen,palette:pen_color(bank+pen)))
        end
    end
end)
