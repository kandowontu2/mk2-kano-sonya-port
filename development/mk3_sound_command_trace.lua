-- Read-only MK3 sound-port trace for identifying character-owned commands.
dofile(os.getenv("MK3_TRACE_SELECTION_SCRIPT") or "mk3_kano_native.lua")

local frame, tap = 0, nil
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local cpu = manager.machine.devices[":maincpu"]
        local program = cpu.spaces["program"]
        tap = program:install_write_tap(0x01680000, 0x0168001f,
            "mk3 sound bytes", function(offset, data, mask)
                if offset == 0x01680000 and (mask & 0xff) ~= 0 then
                    print(string.format("MK3_SOUND_BYTE frame=%d pc=%08X data=%02X mask=%04X",
                        frame, cpu.state["PC"].value, data & 0xff, mask & 0xffff))
                end
            end)
    end
end)
