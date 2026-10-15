-- Read-only diagnostic of the stock ending picture records and graphics mapping.
local done = false
emu.register_frame(function()
    if done then return end
    done = true
    local program = manager.machine.devices[":maincpu"].spaces.program
    local table_base = program:read_u32(0xff8447b0)
    for _, index in ipairs({16, 17, 32, 33, 38, 39, 50, 51, 52, 53}) do
        local pointer = program:read_u32(table_base + index * 0x20)
        print(string.format("MK2KS_PICTURE index=%d ptr=%08X", index, pointer))
        local words = {}
        for at = 0, 95 do
            words[#words + 1] = string.format("%04X", program:read_u16(pointer + at * 16))
        end
        print("MK2KS_PICTURE_WORDS " .. table.concat(words, " "))
        local colors = program:read_u16(pointer + 48)
        local stream = pointer + (4 + colors) * 16
        local head = {}
        for at = 0, 95 do
            head[#head + 1] = string.format("%04X", program:read_u16(stream + at * 16))
        end
        print(string.format("MK2KS_PICTURE_STREAM index=%d address=%08X %s",
            index, stream, table.concat(head, " ")))
    end
end)
