local frame = 0
local pulses = {}

local function pulse(field, first, duration)
    pulses[#pulses + 1] = { field=field, first=first, last=first+duration-1 }
end

local function sequence(first, fields)
    for index, field in ipairs(fields) do pulse(field, first+(index-1)*7, 3) end
end

emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports
        local p1=ports[":IN0"].fields; local sys=ports[":IN1"].fields; local low=ports[":IN2"].fields
        pulse(p1["P1 High Punch"],300,4)
        pulse(sys["Coin 1"],600,4); pulse(sys["Coin 1"],615,4)
        pulse(sys["1 Player Start"],640,4)
        pulse(p1["P1 Block"],810,28); pulse(p1["P1 High Punch"],820,4)
        sequence(1480,{p1["P1 Right"],p1["P1 Right"],p1["P1 High Punch"]})
        sequence(1680,{p1["P1 Right"],p1["P1 Right"],low["P1 Low Punch"]})
        sequence(1880,{p1["P1 Right"],p1["P1 Right"],p1["P1 High Kick"]})
        pulse(low["P1 Low Kick"],2080,190)
        pulse(p1["P1 Left"],2360,90)
        sequence(2480,{p1["P1 Right"],p1["P1 Right"],p1["P1 High Kick"]})
    end
    for _,item in ipairs(pulses) do
        if frame==item.first then item.field:set_value(1) end
        if frame==item.last+1 then item.field:clear_value() end
    end
    if frame>=1280 then
        local space=manager.machine.devices[":maincpu"].spaces["program"]
        -- MKII stores P1's live and displayed energy separately.
        space:write_u16(0x0105E500,0x00A1)
        space:write_u16(0x010602F0,0x00A1)
    end
    if frame>=1160 and frame<=2700 and frame%10==0 then manager.machine.video:snapshot() end
end)
