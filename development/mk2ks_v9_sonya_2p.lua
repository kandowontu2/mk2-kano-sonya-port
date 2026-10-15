local frame, pulses = 0, {}
local function pulse(field, first, duration) pulses[#pulses + 1] = { field=field, first=first, last=first+duration-1 } end
local function seq(first, fields) for i, field in ipairs(fields) do pulse(field, first+(i-1)*7, 3) end end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports; local hi,sys,lo=ports[":IN0"].fields,ports[":IN1"].fields,ports[":IN2"].fields
        pulse(hi["P1 High Punch"],300,4); pulse(sys["Coin 1"],600,4); pulse(sys["Coin 2"],615,4)
        pulse(sys["2 Players Start"],640,4)
        pulse(hi["P1 Right"],750,4); pulse(hi["P1 Right"],780,4); pulse(hi["P1 Right"],810,4); pulse(hi["P1 Right"],850,4)
        pulse(hi["P1 High Punch"],920,4); pulse(hi["P2 High Punch"],950,4)
        pulse(hi["P2 Block"],1500,1000)
        seq(1600,{hi["P1 Down"],hi["P1 Right"],lo["P1 Low Punch"]})
        pulse(hi["P1 Down"],1820,4); pulse(lo["P1 Low Punch"],1820,4); pulse(hi["P1 Block"],1820,4)
        seq(2040,{hi["P1 Right"],hi["P1 Left"],hi["P1 High Punch"]})
        seq(2260,{hi["P1 Left"],hi["P1 Left"],hi["P1 Down"],hi["P1 High Kick"]})
    end
    for _,item in ipairs(pulses) do if frame==item.first then item.field:set_value(1) end; if frame==item.last+1 then item.field:clear_value() end end
    if frame>=1480 and frame<=2440 and frame%10==0 then manager.machine.video:snapshot() end
end)
