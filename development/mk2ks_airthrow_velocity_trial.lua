-- Diagnostic only: override the post-impact Kano air-throw horizontal
-- velocity in the loaded ROM image, then run the normal real-input probe.
-- This never writes a ROM file or changes the playable candidate.
local speed = tonumber(assert(os.getenv("MK2KS_AIRTHROW_TRIAL_SPEED_HEX")), 16)
assert(speed >= 0x00008000 and speed <= 0x00020000)
local rom = assert(manager.machine.memory.regions[":maincpu"])
local at = 0xf8280
assert(rom:read_u16(at) == 0x09e0 and
    rom:read_u16(at + 2) == 0xfc00 and rom:read_u16(at + 4) == 0x0001,
    "unexpected Kano rebound velocity layout")
rom:write_u16(at + 2, speed & 0xffff)
rom:write_u16(at + 4, speed >> 16)
assert(rom:read_u16(at + 2) == (speed & 0xffff) and
    rom:read_u16(at + 4) == (speed >> 16))
print(string.format("MK2KS_AIRTHROW_TRIAL speed=%08X", speed))
dofile("mk2ks_airthrow_probe.lua")
