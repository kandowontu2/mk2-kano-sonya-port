-- Interrupt Sonya's startup with a real opponent uppercut, then retry the grab.
-- All writes are ordinary input-field presses; emulated state is read-only.
assert((os.getenv("MK2KS_TEST_LEG") or "")=="", "Clear the single-grab driver")
assert(os.getenv("MK2KS_TWO_PLAYER")=="1", "Two live players are required")
dofile("mk2ks_selector_exit_test.lua")

local side=tonumber(os.getenv("MK2KS_LEG_SIDE") or "1")
-- Native P1/P2 task order shifts this deliberately timed counter by one field.
local delay=tonumber(os.getenv("MK2KS_LEG_INTERRUPT_DELAY") or tostring(3-side))
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert(names[side]=="sonya" and (names[3-side]=="kano" or names[3-side]=="sonya"))
local frame,hud_frame=0,nil
local program,cpu,screen,buttons
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local taps,entries,collisions,ready={},{},{},{{},{}}
local command,settle,second,retry_settle=nil,nil,nil,nil
local baseline,interrupted,last=nil,nil,nil
local errors=0
local function require_result(condition,label)
    if not condition then errors=errors+1;print("MK2KS_LEG_INTERRUPT_ERROR "..label) end
end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {id=program:read_u16(actor+0x1f0),action=program:read_u16(process+0x1f0),
        x=program:read_u16(actor+0x90),y=program:read_u16(actor+0xb0),
        floor=program:read_u16(process+0x200),vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        health=program:read_u16(health[index])}
end
local function press(index,key) buttons[index][key]:set_value(1) end
local function chord() press(side,"down");press(side,"lp");press(side,"block") end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        local low=manager.machine.ioport.ports[":IN2"].fields
        buttons={}
        for index=1,2 do
            local prefix="P"..index.." "
            buttons[index]={left=high[prefix.."Left"],right=high[prefix.."Right"],
                down=high[prefix.."Down"],hp=high[prefix.."High Punch"],
                lp=low[prefix.."Low Punch"],block=high[prefix.."Block"]}
        end
        for _,entry in ipairs({{0xfff80800,entries},{0xfff83800,collisions}}) do
            taps[#taps+1]=program:install_read_tap(entry[1],entry[1]+15,"interrupted leg event",
                function(offset,data,mask)
                    if command and cpu.state.A8.value==program:read_u32(pointers[side]) then
                        entry[2][#entry[2]+1]=frame
                        print(string.format("MK2KS_LEG_INTERRUPT_EVENT pc=%08X frame=%d",entry[1],frame))
                    end
                end)
        end
        taps[#taps+1]=program:install_read_tap(0xff861350,0xff86135f,"interrupted leg ready",
            function(offset,data,mask)
                if not command then return end
                for index,pointer in ipairs(pointers) do
                    if cpu.state.A8.value==program:read_u32(pointer) then ready[index][#ready[index]+1]=frame end
                end
            end)
    end
    if not hud_frame then
        local pixels,width=screen:pixels()
        if width~=400 or frame<900 then return end
        local green=0
        for x=20,380 do
            local c=string.unpack("<I4",pixels,(30*width+x)*4+1)
            local r,g,b=(c>>16)&255,(c>>8)&255,c&255
            if g>100 and g>r*3//2 and g>b*3//2 then green=green+1 end
        end
        if green>250 then hud_frame=frame end
        return
    end
    if frame<hud_frame+180 or last then return end
    local own,victim=sample(side),sample(3-side)
    if not command then
        if math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                command=frame+12;baseline={own,victim}
                print(string.format("MK2KS_LEG_INTERRUPT_COMMAND frame=%d delay=%d x=%d,%d",command,delay,own.x,victim.x))
            end
        end
        return
    end
    if frame>=command and frame<command+4 then chord() end
    -- Enter the native crouch first; pressing Down and HP together can consume
    -- HP in the stance transition without starting an uppercut at all.
    if frame>=command+delay-8 and frame<command+delay+4 then press(3-side,"down") end
    if frame>=command+delay and frame<command+delay+4 then press(3-side,"hp") end
    if frame>=command-10 and frame<=command+100 and frame%3==0 then
        print(string.format("MK2KS_LEG_INTERRUPT_STATE age=%d health=%d,%d action=%04X,%04X x=%d,%d y=%d,%d",
            frame-command,own.health,victim.health,own.action,victim.action,own.x,victim.x,own.y,victim.y))
    end
    if frame==command+14 or frame==command+40 then manager.machine.video:snapshot() end
    if frame==command+180 then
        interrupted={own,victim,entries=#entries,collisions=#collisions}
        print(string.format("MK2KS_LEG_INTERRUPT_RECOVERED entries=%d collisions=%d health=%d,%d",#entries,#collisions,own.health,victim.health))
    end
    if interrupted and not second then
        if math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");retry_settle=nil
        else
            retry_settle=retry_settle or frame
            if frame-retry_settle>=30 then second=frame;chord() end
        end
    elseif second then
        if frame<second+4 then chord() end
        if frame==second+150 then last={own,victim};manager.machine.video:snapshot() end
    end
end)
emu.register_stop(function()
    require_result(baseline and interrupted and last,"both attempts completed")
    if baseline and interrupted and last then
        require_result(interrupted.entries==1 and interrupted.collisions==0,"startup entered, then interrupted before catch")
        require_result(interrupted[1].health==baseline[1].health-40 and interrupted[2].health==baseline[2].health,"native uppercut actually interrupted Sonya")
        require_result(interrupted[1].action~=0x110 and interrupted[2].action~=0x111,"interrupted states cleared")
        require_result(#entries==2 and #collisions==1,"retry enters and catches once")
        require_result(last[1].health==interrupted[1].health and last[2].health==interrupted[2].health-35,"retry damages only victim")
        for index,s in ipairs(last) do
            local expected=index==1 and 18 or names[3-side]=="kano" and 17 or 18
            require_result(s.id==expected and s.action~=0x110 and s.action~=0x111,"recovered own identities/states")
            require_result(s.y==s.floor and s.vx==0 and s.vy==0,"grounded retry recovery")
        end
        require_result(#ready[side]>0 and #ready[3-side]>0,"native ready continuations")
    end
    print(string.format("MK2KS_LEG_INTERRUPT_RESULT pass=%s side=%d victim=%s delay=%d entries=%d collisions=%d errors=%d",
        tostring(errors==0),side,names[3-side],delay,#entries,#collisions,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
