-- Two humans, Sonya P1 and Kano P2. No character, actor or position writes.
local frame,pulses=0,{}
local function pulse(field,first)
    assert(field,"Missing original-game input")
    pulses[#pulses+1]={field,first,first+4}
end
local function sonya(high,prefix,base)
    for _,offset in ipairs({180,220,260,300}) do pulse(high[prefix.."Left"],base+offset) end
    pulse(high[prefix.."Down"],base+340)
    pulse(high[prefix.."High Punch"],base+380)
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports
        local high,system=ports[":IN0"].fields,ports[":IN2"].fields
        for base=360,1320,480 do
            pulse(system["Coin 1"],base)
            pulse(system["1 Player Start"],base+20)
            sonya(high,"P1 ",base)
        end
        for _,first in ipairs({2960,2980,3000}) do pulse(system["Coin 2"],first) end
        pulse(system["2 Players Start"],3020)
        sonya(high,"P1 ",2880)
        -- P2 starts at Liu Kang, the rightmost top slot. Kano is one left;
        -- Right does not wrap the native MK3 grid.
        pulse(high["P2 Left"],3100)
        pulse(high["P2 High Punch"],3400)
    end
    for _,item in ipairs(pulses) do
        if frame==item[2] then item[1]:set_value(1) end
        if frame==item[3] then item[1]:clear_value() end
    end
    if frame==3080 or frame==3140 or frame==3200 or frame==3260 or frame==3420 then
        manager.machine.video:snapshot()
    end
end)
