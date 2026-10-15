local frame = 0
local pulses = {}
local capture = os.getenv("MK3_CAPTURE") ~= "0"

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

        -- Join during round two, then select Kano from the top-left cursor.
        pulse(system["Coin 2"], 3000, 4)
        pulse(system["2 Players Start"], 3020, 4)
        pulse(high["P1 Right"], 3060, 4)
        pulse(high["P1 Right"], 3090, 4)
        pulse(high["P1 Right"], 3120, 4)
        pulse(high["P1 High Punch"], 3160, 4)
        pulse(high["P2 High Punch"], 3180, 4)

        -- Native MK3 knife throw: Down, Back, High Punch.
        for first = 3900, 4260, 120 do
            pulse(high["P1 Down"], first, 4)
            pulse(high["P1 Left"], first + 5, 4)
            pulse(high["P1 High Punch"], first + 10, 4)
        end
    end

    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end

    if frame >= 3500 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        space:write_u8(0x01060A40, 0xA6)
        space:write_u8(0x010615F0, 0xA6)
    end

    if capture and frame >= 3700 and frame <= 4400 and frame % 2 == 0 then
        manager.machine.video:snapshot()
    end
end)
