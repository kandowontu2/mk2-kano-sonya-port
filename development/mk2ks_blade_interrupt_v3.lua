-- Interrupt an actually active swipe, prove native trail teardown, then retry.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1")
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_BLADE_SIDE") or "1")
-- As with the leg-grab counter, native P1/P2 task ordering gives simultaneous
-- collisions different priority. Start P1 Sonya's counter one field earlier
-- when she must interrupt P2 Kano, without altering either game scheduler.
local counter_delay=11-side
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert(names[side]=="kano" and names[3-side]=="sonya")
local frame,hud,command,retry,settle,baseline,interrupted,last=0,nil,nil,nil,nil,nil,nil,nil
local cpu,program,screen,buttons
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local taps,entries,strikes,creates,trail_objects={},{},{},{},{}
local interrupt_trace
local errors,cleared_at=0,nil
local hit_frame,cleanup_frame
local function require_result(condition,label)
    if not condition then errors=errors+1;print("MK2KS_BLADE_INTERRUPT_ERROR "..label) end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {id=program:read_u16(actor+0x1f0),action=program:read_u16(process+0x1f0),
        x=signed(program:read_u16(actor+0x90)),y=signed(program:read_u16(actor+0xb0)),
        floor=signed(program:read_u16(process+0x200)),vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        trail=program:read_u32(process+0x190),health=program:read_u16(health[index])}
end
local function press(index,key)
    buttons[index][key]:set_value(1)
    print(string.format("MK2_INTERRUPT_INPUT frame=%d slot=%d button=%s writes=0",frame,index,key))
end
local function input(at,own,victim)
    local age=frame-at
    if age>=0 and age<3 then press(side,"down") end
    if age>=5 and age<8 then press(side,own.x<victim.x and "right" or "left") end
    if age>=6 and age<9 then press(side,"hp") end
end
local function check_no_trail()
    local cursor=program:read_u32(0x0105d480)
    local count=0
    while cursor~=0 and count<1024 do
        local descriptor=program:read_u32(cursor+0x1a0)
        require_result(descriptor<0xfff8f800 or descriptor>0xfff8fda0,"no blade frame remains in native display list")
        cursor=program:read_u32(cursor);count=count+1
    end
    require_result(count<1024,"display list terminates")
    for entry=0x0105bb30,0x0105ca30,64 do
        if program:read_u32(entry)==0xff680800 then
            require_result(program:read_u16(entry+32)==0,"native blade palette reference released")
        end
    end
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        interrupt_trace=dofile("mk2ks_interrupt_trace_v2.lua")("blade",side,names,function()
            return frame,(retry and frame>=retry)and 2 or 1,(retry and frame>=retry)and retry or command
        end)
        local high=manager.machine.ioport.ports[":IN0"].fields
        buttons={}
        for index=1,2 do
            local prefix="P"..index.." "
            buttons[index]={left=high[prefix.."Left"],right=high[prefix.."Right"],
                down=high[prefix.."Down"],hp=high[prefix.."High Punch"]}
        end
        for _,entry in ipairs({{0xfff8cc00,entries},{0xfff8e400,strikes},{0xfff8d800,creates}}) do
            taps[#taps+1]=program:install_read_tap(entry[1],entry[1]+15,"interrupted blade event",
                function()
                    if command and cpu.state.A8.value==program:read_u32(pointers[side]) and entry[2][#entry[2]]~=frame then
                        entry[2][#entry[2]+1]=frame
                        print(string.format("MK2KS_BLADE_INTERRUPT_EVENT pc=%08X frame=%d",entry[1],frame))
                    end
                end)
        end
        taps[#taps+1]=program:install_write_tap(health[side],health[side]+15,"blade interruption damage",
            function(offset,data,mask)
                if baseline and not interrupted and (data&0xffff)<baseline[1].health then
                    hit_frame=frame;print("MK2KS_BLADE_INTERRUPT_HIT frame="..frame)
                end
            end)
        taps[#taps+1]=program:install_read_tap(0xff83efd0,0xff83efdf,"blade native hit cleanup",
            function()
                if command and not interrupted and cpu.state.A13.value==program:read_u32(processes[side]) and
                    program:read_u32(cpu.state.A13.value+0x190)~=0 then
                    cleanup_frame=frame;print("MK2KS_BLADE_INTERRUPT_CLEANUP frame="..frame)
                end
            end)
    end
    if not hud then
        local pixels,width=screen:pixels()
        if width~=400 or frame<900 then return end
        local green=0
        for x=20,380 do
            local c=string.unpack("<I4",pixels,(30*width+x)*4+1)
            local r,g,b=(c>>16)&255,(c>>8)&255,c&255
            if g>100 and g>r*3//2 and g>b*3//2 then green=green+1 end
        end
        if green>250 then hud=frame end
        return
    end
    if frame<hud+180 or last then return end
    interrupt_trace.field()
    local own,victim=sample(side),sample(3-side)
    if not command then
        if math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then command=frame+20;baseline={own,victim};settle=nil end
        end
        return
    end
    input(command,own,victim)
    local age=frame-command
    if age>=2 and age<16 then press(3-side,"down") end
    if age>=counter_delay and age<counter_delay+4 then press(3-side,"hp") end
    if own.trail~=0 then trail_objects[own.trail]=true end
    if not cleared_at and #creates>0 and own.trail==0 and own.health<baseline[1].health then cleared_at=frame end
    if age>=6 and age<=60 then
        print(string.format("MK2KS_BLADE_INTERRUPT_STATE age=%d health=%d,%d action=%04X,%04X trail=%08X",
            age,own.health,victim.health,own.action,victim.action,own.trail))
        if age%6==0 then manager.machine.video:snapshot() end
    end
    if age==180 then
        interrupted={own,victim,entries=#entries,strikes=#strikes,creates=#creates}
        check_no_trail()
    end
    if interrupted and not retry then
        if math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then retry=frame+10 end
        end
    elseif retry then
        input(retry,own,victim)
        if frame==retry+180 then last={own,victim};check_no_trail();manager.machine.video:snapshot() end
    end
end)
emu.register_stop(function()
    require_result(baseline and interrupted and last,"interrupt and retry completed")
    if baseline and interrupted and last then
        require_result(interrupted.entries==1 and interrupted.creates==1 and interrupted.strikes==0,"trail was active before interruption prevented strike")
        -- Frame samples precede native task execution. An uppercut can win
        -- priority on the very field where the cancelled blade would strike;
        -- measure teardown against actual damage/cleanup, not an earlier
        -- guessed field relative to the attacker's entry.
        require_result(hit_frame and cleanup_frame and cleared_at and
            cleanup_frame>=hit_frame and cleanup_frame-hit_frame<=1 and
            cleared_at>=cleanup_frame and cleared_at-cleanup_frame<=1,
            "native hit handoff immediately cleared trail")
        require_result(interrupted[1].health==baseline[1].health-40 and interrupted[2].health==baseline[2].health,"actual uppercut damage")
        require_result(#entries==2 and #creates==2 and #strikes==1,"one clean retry with one strike")
        require_result(last[1].health==interrupted[1].health and last[2].health==interrupted[2].health-26,"retry damage")
        require_result(last[1].id==17 and last[2].id==18,"native identities preserved")
        require_result(last[1].trail==0 and last[1].action~=0x117 and last[1].action~=0x618,"retry state and trail cleared")
        require_result(last[1].y==last[1].floor and last[1].vx==0 and last[1].vy==0,"grounded retry recovery")
    end
    print(string.format("MK2KS_BLADE_INTERRUPT_RESULT pass=%s side=%d entries=%d strikes=%d creates=%d errors=%d",
        tostring(errors==0),side,#entries,#strikes,#creates,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)




