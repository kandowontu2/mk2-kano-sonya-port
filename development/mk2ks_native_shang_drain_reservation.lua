-- Passive cold-boot reservation observation on the exact existing candidate.
-- No controller inputs, guest writes, state loads, forced matches or outcome.
local main = assert(manager.machine.memory.regions[':maincpu'])
local gfx = assert(manager.machine.memory.regions[':gfxrom'])
local done = false
local function emit(kind, region, first, bytes)
    for offset = 0, bytes - 1, 512 do
        local count = math.min(512, bytes - offset)
        local hex = {}
        for i = 0, count - 1 do
            hex[#hex + 1] = string.format('%02x', region:read_u8(first + offset + i))
        end
        print(string.format('MK2_DRAIN_RESERVE kind=%s start=%X offset=%d bytes=%d writes=0 assistance=none hex=%s',
                            kind, first, offset, count, table.concat(hex)))
    end
end
emu.register_frame_done(function()
    if done then return end
    done = true
    emit('program', main, 0xb1000, 0x1000)
    emit('graphics', gfx, 0x1fb0000, 0x10000)
    emit('primary', main, (0xff9d7770 - 0xff800000) // 8, 68)
    emit('secondary', main, (0xff9d8d70 - 0xff800000) // 8, 68)
    emit('helper', main, (0xff8cb410 - 0xff800000) // 8, 18)
    emit('normal_kano', main, 0xfda00, 132)
    emit('normal_sonya', main, 0xfdb00, 132)
    emit('alternate_kano', main, 0xf1500, 132)
    emit('alternate_sonya', main, 0xf1600, 132)
    print('MK2_DRAIN_RESERVE_COMPLETE writes=0 assistance=none')
end)
