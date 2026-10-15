local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field=field, first=first, last=first+duration-1 }
end

emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports
        local p1=ports[":IN0"].fields; local sys=ports[":IN1"].fields
        pulse(p1["P1 High Punch"],300,4); pulse(sys["Coin 1"],600,4)
        pulse(sys["1 Player Start"],640,4); pulse(p1["P1 Block"],810,28)
        pulse(p1["P1 High Punch"],820,4)
    end
    for _,item in ipairs(pulses) do
        if frame==item.first then item.field:set_value(1) end
        if frame==item.last+1 then item.field:clear_value() end
    end
    if frame>=1200 and frame<=2000 and frame%30==0 then
        local space=manager.machine.devices[":maincpu"].spaces["program"]
        print(string.format("KNOWN_HEALTH frame=%d a=%04X b=%04X char=%04X",
            frame,
            space:read_u16(0x0105E500),
            space:read_u16(0x010602F0),
            space:read_u16(0x01060280)))
    end
end)
