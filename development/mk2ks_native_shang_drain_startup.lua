-- Passive startup identity of BOTH initialized ROM windows and new GFX.
-- No input, game/register/state writes, cheats, savestates, or forced outcome.
local main = assert(manager.machine.memory.regions[':maincpu'])
local owned = assert(manager.machine.memory.regions[':mk3data'])
local gfx = assert(manager.machine.memory.regions[':gfxrom'])
local done = false
local function emit(kind, region, first, bytes)
    for offset = 0, bytes - 1, 4096 do
        local count = math.min(4096, bytes - offset)
        local hex = {}
        for i = 0, count - 1 do
            hex[#hex + 1] = string.format('%02x', region:read_u8(first + offset + i))
        end
        print(string.format('MK2_DRAIN_STARTUP kind=%s start=%X offset=%d bytes=%d writes=0 assistance=none hex=%s',
                            kind, first, offset, count, table.concat(hex)))
    end
end
emu.register_frame_done(function()
    if done then return end
    done = true
    emit('high', main, 0, 0x100000)
    emit('owned', owned, 0, 0x200000)
    emit('graphics', gfx, 0x1fb0000, 0x10000)
    print('MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none')
end)
