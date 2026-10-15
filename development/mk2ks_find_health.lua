local frame = 0
local pulses = {}
local baseline = {}

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

    local space=manager.machine.devices[":maincpu"].spaces["program"]
    if frame==1360 then
        for address=0x01000000,0x013FFFF0,0x10 do
            local value=space:read_u16(address)
            if value==0x00A1 or value==0xA100 or value==0x0064 or value==0x6400 then
                baseline[address]=value
            end
        end
        print(string.format("HEALTH_SCAN baseline=%d", #baseline))
    elseif frame==1800 then
        local count=0
        for address,old in pairs(baseline) do
            local value=space:read_u16(address)
            if value~=old then
                print(string.format("HEALTH_CANDIDATE address=%08X old=%04X new=%04X delta=%d",address,old,value,old-value))
                count=count+1
            end
        end
        print(string.format("HEALTH_SCAN candidates=%d",count))
    end
end)
