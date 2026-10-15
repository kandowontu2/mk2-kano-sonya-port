local frame = 0
local pulses = {}
local candidates = {}
local checkpoints = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local high = ports[":IN0"].fields
        local system = ports[":IN2"].fields
        for base = 360, 1320, 480 do
            pulse(system["Coin 1"], base, 4)
            pulse(system["1 Player Start"], base + 20, 4)
            pulse(high["P1 Right"], base + 180, 4)
            pulse(high["P1 Right"], base + 220, 4)
            pulse(high["P1 Right"], base + 260, 4)
            pulse(high["P1 High Punch"], base + 320, 4)
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    local space = manager.machine.devices[":maincpu"].spaces["program"]
    if frame == 3000 then
        for address = 0x01000000, 0x013FFFF0, 0x10 do
            local value = space:read_u16(address)
            candidates[#candidates + 1] = { address = address, original = value }
        end
        print(string.format("MK3HEALTH candidates=%d", #candidates))
    elseif frame == 3200 or frame == 3400 or frame == 3600 then
        checkpoints[frame] = {}
        for index, item in ipairs(candidates) do
            checkpoints[frame][index] = space:read_u16(item.address)
        end
        if frame == 3600 then
            for index, item in ipairs(candidates) do
                local a, b, c = checkpoints[3200][index], checkpoints[3400][index], checkpoints[3600][index]
                if item.original >= a and a >= b and b >= c and item.original > c then
                    print(string.format("MK3HEALTH direction=down address=%08X values=%04X,%04X,%04X,%04X", item.address, item.original, a, b, c))
                elseif item.original <= a and a <= b and b <= c and item.original < c then
                    print(string.format("MK3HEALTH direction=up address=%08X values=%04X,%04X,%04X,%04X", item.address, item.original, a, b, c))
                end
            end
        end
    end
    if frame == 3000 or frame == 3200 or frame == 3400 or frame == 3600 then
        manager.machine.video:snapshot()
    end
end)
