local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local program = manager.machine.devices[":maincpu"].spaces.program
    local bases = {program:read_u32(0xff8f51c0), program:read_u32(0xff8f53e0)}
    for page = 1, 2 do
        for _, id in ipairs({8, 17, 18}) do
            for segment = 0, 2 do
                local pointer = program:read_u32(bases[page] + (id * 3 + segment) * 32)
                if pointer ~= 0 then
                    local header, chars = {}, {}
                    for n = 0, 23 do header[#header + 1] = string.format("%02X", program:read_u8(pointer + n * 8)) end
                    for n = 0, 150 do
                        local byte = program:read_u8(pointer + (24 + n) * 8)
                        if byte == 0 then break end
                        chars[#chars + 1] = byte >= 32 and byte <= 126 and string.char(byte) or string.format("<%02X>", byte)
                    end
                    print(string.format("MK2KS_STORY page=%d id=%d segment=%d header=%s text=%s",
                        page, id, segment, table.concat(header, " "), table.concat(chars)))
                end
            end
        end
    end
end)
