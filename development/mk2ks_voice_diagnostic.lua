-- Read-only audit of the extended winner sound table and hardware writes.
dofile("mk2ks_selector_exit_test.lua")
local frame, port, table_tap, table_reads = 0, nil, nil, 0
emu.register_frame(function()
    frame = frame + 1
    if frame ~= 1 then return end
    local cpu = manager.machine.devices[":maincpu"]
    local program = cpu.spaces.program
    local table_address = program:read_u32(0xff8209e0)
    print(string.format("MK2KS_VOICE_TABLE_ADDRESS %08X", table_address))
    for _, id in ipairs({0, 1, 11, 17, 18}) do
        print(string.format("MK2KS_VOICE_TABLE id=%d value=%04X",
            id, program:read_u16(table_address + id * 16)))
    end
    table_tap = program:install_read_tap(table_address + 17 * 16,
        table_address + 19 * 16 - 1, "added winner voice table reads",
        function(address, data, mask)
            if table_reads < 30 then
                table_reads = table_reads + 1
                print(string.format("MK2KS_VOICE_TABLE_READ frame=%d pc=%08X address=%08X data=%04X mask=%04X",
                    frame, cpu.state.PC.value, address, data & 0xffff, mask & 0xffff))
            end
        end)
    port = program:install_write_tap(0x01d01020, 0x01d0103f,
        "new native voice command audit", function(address, data, mask)
            if address == 0x01d01030 and (data & 0xff) >= 0xfb then
                print(string.format("MK2KS_VOICE_PORT frame=%d address=%08X data=%04X mask=%04X",
                    frame, address, data & 0xffff, mask & 0xffff))
            end
        end)
end)
