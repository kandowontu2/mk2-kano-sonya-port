-- Real-input checks for every new edge, including native diagonal displacement.
-- No emulated memory writes or cursor relocation from the test.
local frame, css, checks, failures = 0, 0, 0, 0
local fields, screen, program
local path = {
    {"left",17}, {"left",17}, {"up",17}, {"down",8}, {"up",1},
    {"right",0}, {"right",2}, {"right",9}, {"right",18}, {"right",18},
    {"up",18}, {"down",11}, {"left",4}, {"up",2}, {"right",9},
    {"right",18}, {"left",9}, {"left",2}, {"left",0}, {"left",1},
    {"left",17}, {"right",1}, {"down",8}, {"left",8}, {"down",5},
    {"right",3}, {"right",10}, {"right",7}, {"up",11}, {"up",9}, {"right",18}
}
local positions = {
    [0]={139,20}, [1]={79,20}, [2]={199,20}, [3]={139,170},
    [4]={199,95}, [5]={79,170}, [6]={139,95}, [7]={259,170},
    [8]={79,95}, [9]={259,20}, [10]={199,170}, [11]={259,95},
    [17]={19,20}, [18]={319,20}
}
local function pulse(name, age, start)
    if age >= start and age < start + 4 then fields[name]:set_value(1) end
end
emu.register_frame(function()
    frame = frame + 1
    if not fields then
        local ports = manager.machine.ioport.ports
        local high, system = ports[":IN0"].fields, ports[":IN1"].fields
        fields = {left=high["P1 Left"],right=high["P1 Right"],up=high["P1 Up"],
            down=high["P1 Down"],hp=high["P1 High Punch"],coin=system["Coin 1"],start=system["1 Player Start"]}
        screen = manager.machine.screens[":screen"]
        program = manager.machine.devices[":maincpu"].spaces["program"]
    end
    for _, field in pairs(fields) do field:clear_value() end
    local pixels, width = screen:pixels()
    local function color(x,y) return string.unpack("<I4",pixels,(y*width+x)*4+1) end
    local function green(x,y)
        local c=color(x,y)
        local r,g,b=(c>>16)&255,(c>>8)&255,c&255
        return g>70 and g>r*2 and g>b*2
    end
    if css == 0 then
        if frame >= 600 then
            pulse("coin",(frame-600)%300,0)
            pulse("start",(frame-600)%300,20)
        end
        local yellow=0
        for y=0,24,2 do for x=40,360,2 do
            local c=color(x,y)
            if ((c>>16)&255)>175 and ((c>>8)&255)>140 and (c&255)<100 then yellow=yellow+1 end
        end end
        if frame>700 and yellow>=400 and yellow<=430 then css=frame end
        return
    end
    local age=frame-css
    for index, step in ipairs(path) do
        local first=12+(index-1)*18
        pulse(step[1],age,first)
        if age==first+10 then
            local actual=program:read_u16(0x01060280)
            local actor=program:read_u32(0x01060220)
            local live=actor~=0 and program:read_u16(actor+0x1f0) or -1
            local left,top=table.unpack(positions[step[2]])
            local border=0
            for y=top,top+77 do for x=left,left+62 do
                if (x<left+4 or x>left+58 or y<top+4 or y>top+73) and green(x,y) then border=border+1 end
            end end
            local pass=actual==step[2] and live==step[2] and border==1064
            checks=checks+1
            if not pass then failures=failures+1; manager.machine.video:snapshot() end
            print(string.format("MK2KS_GRID step=%d direction=%s expected=%d actual=%d live=%d border=%d pass=%s",
                index,step[1],step[2],actual,live,border,tostring(pass)))
        end
    end
    pulse("hp",age,600)
end)
emu.register_stop(function()
    print(string.format("MK2KS_GRID_RESULT pass=%s checks=%d failures=%d",tostring(checks==#path and failures==0),checks,failures))
end)
