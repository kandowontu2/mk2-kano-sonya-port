local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field = field, first = first, last = first + duration - 1 }
end

emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        local ports = manager.machine.ioport.ports
        local in0 = ports[":IN0"].fields
        local in2 = ports[":IN2"].fields
        pulse(in2["Coin 1"], 360, 4)
        pulse(in2["1 Player Start"], 380, 4)
        pulse(in0["P1 Right"], 540, 4)
        pulse(in0["P1 Right"], 580, 4)
        pulse(in0["P1 Right"], 620, 4)
        pulse(in0["P1 High Punch"], 680, 4)
        pulse(in0["P1 High Punch"], 1180, 4)
    end
    for _, item in ipairs(pulses) do
        if frame == item.first then item.field:set_value(1) end
        if frame == item.last + 1 then item.field:clear_value() end
    end
    if frame >= 1600 and frame <= 1900 and frame % 20 == 0 then
        local space = manager.machine.devices[":maincpu"].spaces["program"]
        print(string.format(
            "MK3POS frame=%d p1_100=%04X p1_120=%04X p1_130=%04X p1_140=%04X p2_100=%04X p2_120=%04X p2_130=%04X p2_140=%04X",
            frame,
            space:read_u16(0x010334c0), space:read_u16(0x010334e0),
            space:read_u16(0x010334f0), space:read_u16(0x01033500),
            space:read_u16(0x010336d0), space:read_u16(0x010336f0),
            space:read_u16(0x01033700), space:read_u16(0x01033710)))
    end
end)
