-- Read-only trace of DCS port writes during the normal selector/round harness.
dofile("mk2ks_selector_exit_test.lua")

local frame = 0
local taps = {}
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local program = manager.machine.devices[":maincpu"].spaces.program
        local cpu = manager.machine.devices[":maincpu"].state
        taps[#taps + 1] = program:install_write_tap(
            0x01d01020, 0x01d0103f, "voice sound port trace",
            function(offset, data, mask)
                print(string.format(
                    "MK2_VOICE_SOUND_PORT frame=%d address=%08X data=%04X mask=%04X pc=%08X",
                    frame, offset, data & 0xffff, mask & 0xffff, cpu.PC.value))
            end)
    end
end)
