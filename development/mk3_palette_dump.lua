local frame = 0
local pulses = {}

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

    if frame == 3000 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        local values = {}
        for bank = 0, 0x7f do
            local count = 0
            for entry = 0, 0xff do
                if space:read_u16(0x01880000 + (bank * 0x100 + entry) * 0x10) ~= 0 then
                    count = count + 1
                end
            end
            if count ~= 0 then values[#values + 1] = string.format("%02X:%d", bank, count) end
        end
        print("MK3_PAL_BANKS " .. table.concat(values, " "))
        values = {}
        for index = 0x300, 0x33f do
            values[#values + 1] = string.format("%04X", space:read_u16(0x01880000 + index * 0x10))
        end
        print("MK3_KANO_PAL " .. table.concat(values, " "))
        for index = 0, 0x7ffc do
            if space:read_u16(0x01880000 + index * 0x10) == 0x77bd and
                space:read_u16(0x01880000 + (index + 1) * 0x10) == 0x739c then
                print(string.format("MK3_KANO_PAL_MATCH %04X", index))
            end
        end
        manager.machine.video:snapshot()
        for index = 0x100, 0x17f do
            local value = space:read_u16(0x01880000 + index * 0x10)
            if value ~= 0 and #values < 160 then
                values[#values + 1] = string.format("%04X=%04X", index, value)
            end
        end
    end
end)
