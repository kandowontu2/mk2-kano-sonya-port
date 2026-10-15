-- Read-only current native program-ROM free-space inventory.
local rom = assert(manager.machine.memory.regions[":maincpu"])
local start, finish, run = 0xf8400, 0xf9000, nil
for at = start, finish do
    local free = at < finish and rom:read_u8(at) == 0xff
    if free and not run then run = at end
    if not free and run then
        if at - run >= 0x50 then
            print(string.format("MK2KS_ROM_FREE start=%05X finish=%05X bytes=%X", run, at, at - run))
        end
        run = nil
    end
end
