-- Original MK3 reference: enter P1 first, then join P2 from the match.
-- A lone '2 Players Start' starts P2, not both human players.
local frame,pulses=0,{}
local function pulse(field,first)
    assert(field,"Missing original-game input")
    pulses[#pulses+1]={field,first,first+4}
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        local ports=manager.machine.ioport.ports
        local high,system=ports[":IN0"].fields,ports[":IN2"].fields
        for base=360,1320,480 do
            pulse(system["Coin 1"],base)
            pulse(system["1 Player Start"],base+20)
            for _,offset in ipairs({180,220,260}) do pulse(high["P1 Right"],base+offset) end
            pulse(high["P1 High Punch"],base+320)
        end
        for _,first in ipairs({2960,2980,3000}) do pulse(system["Coin 2"],first) end
        pulse(system["2 Players Start"],3020)
        for _,first in ipairs({3060,3090,3120}) do pulse(high["P1 Right"],first) end
        pulse(high["P1 High Punch"],3160)
        for _,first in ipairs({3100,3160,3220,3280}) do pulse(high["P2 Left"],first) end
        pulse(high["P2 Down"],3340)
        pulse(high["P2 High Punch"],3400)
    end
    for _,item in ipairs(pulses) do
        if frame==item[2] then item[1]:set_value(1) end
        if frame==item[3] then item[1]:clear_value() end
    end
end)
