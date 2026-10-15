local frame=0
local pulses={}
local function pulse(field,first,duration) pulses[#pulses+1]={field=field,first=first,last=first+duration-1} end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports
        local p1=ports[":IN0"].fields; local sys=ports[":IN1"].fields
        pulse(p1["P1 High Punch"],300,4); pulse(sys["Coin 1"],600,4); pulse(sys["Coin 2"],615,4)
        pulse(sys["2 Players Start"],640,4); pulse(p1["P1 Left"],780,4)
        pulse(p1["P1 High Punch"],850,4); pulse(p1["P2 High Punch"],900,4)
        pulse(p1["P1 Right"],1600,3); pulse(p1["P1 Right"],1607,3); pulse(p1["P1 High Kick"],1614,3)
    end
    for _,item in ipairs(pulses) do
        if frame==item.first then item.field:set_value(1) end
        if frame==item.last+1 then item.field:clear_value() end
    end
    if frame>=1550 and frame<=1850 and frame%5==0 then manager.machine.video:snapshot() end
end)
