-- Ordinary selection and button history only; no emulated memory writes.
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_BLADE_SIDE") or "1")
local mode=os.getenv("MK2KS_BLADE_MODE")
assert(({native=true,held=true,reversed=true,expired=true,wrong_button=true,airborne=true,with_block=true})[mode])
local positive=mode=="native" or mode=="held"
local frame,hud,command,settle=0,nil,nil,nil
local program,cpu,screen,buttons,taps=nil,nil,nil,{},{}
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local baseline,final,forward,backward
local entries,strikes,creates,blood,errors=0,0,0,0,0
local airborne_checks,blocked_checks,last_hurt=0,0,nil
local function check(value,label)
    if not value then errors=errors+1;print("MK2KS_BLADE_COMMAND_ERROR "..label) end
end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {actor=actor,process=process,id=program:read_u16(actor+0x1f0),
        x=program:read_u16(actor+0x90),y=program:read_u16(actor+0xb0),
        floor=program:read_u16(process+0x200),vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        action=program:read_u16(process+0x1f0),trail=program:read_u32(process+0x190),
        health=program:read_u16(health[index])}
end
local function press(name) buttons[name]:set_value(1) end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        local low=manager.machine.ioport.ports[":IN2"].fields
        local prefix="P"..side.." "
        for key,label in pairs({left="Left",right="Right",down="Down",up="Up",hp="High Punch",block="Block"}) do buttons[key]=high[prefix..label] end
        buttons.lp=assert(low[prefix.."Low Punch"])
        for _,address in ipairs({0xfff8cc00,0xfff8e400,0xfff8d800,0xfff90000,0xff9a5b00}) do
            taps[#taps+1]=program:install_read_tap(address,address+15,"blade command event",function()
                if not command or frame<command or frame>command+140 then return end
                local own=sample(side)
                if address==0xfff90000 then
                    if cpu.state.A8.value==sample(3-side).actor then last_hurt=frame end
                elseif address==0xff9a5b00 then
                    if last_hurt==frame and cpu.state.A8.value==sample(3-side).actor and cpu.state.A0.value==1 then blood=blood+1 end
                elseif cpu.state.A8.value==own.actor then
                    if address==0xfff8cc00 then entries=entries+1
                    elseif address==0xfff8e400 then strikes=strikes+1
                    else creates=creates+1 end
                end
            end)
        end
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
    if frame<hud+180 or final then return end
    local own,victim=sample(side),sample(3-side)
    if not command then
        if math.abs(own.x-victim.x)>85 then press(own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                command=frame+20;baseline={own,victim}
                forward=own.x<victim.x and "right" or "left";backward=forward=="right" and "left" or "right"
                print(string.format("MK2KS_BLADE_COMMAND_START side=%d mode=%s frame=%d",side,mode,command))
            end
        end
        return
    end
    local age=frame-command
    if mode=="airborne" and age>=-5 and age<-2 then press("up") end
    if mode=="with_block" and age>=-15 and age<110 then press("block") end
    local last_direction=mode=="expired" and 64 or 5
    if age>=0 and age<3 then press(mode=="reversed" and forward or "down") end
    if age>=last_direction and age<last_direction+3 then press(mode=="reversed" and "down" or forward) end
    if age>=last_direction+1 and age<(mode=="held" and 100 or last_direction+4) then press(mode=="wrong_button" and "lp" or "hp") end
    if age==last_direction+1 then
        if mode=="airborne" then check(own.y<own.floor and own.vy~=0,"actual airborne command");airborne_checks=airborne_checks+1 end
        if mode=="with_block" then
            print(string.format("MK2KS_BLADE_COMMAND_BLOCK action=%04X pose=%08X input=%04X",own.action,
                program:read_u32(own.actor+0x1d0),program:read_u16(0x01600000)))
            check((own.action==0x301 or own.action==0x302) and
                (program:read_u16(0x01600000)&(side==1 and 0x20 or 0x2000))==0,
                "actual standing/crouching block and held button before command");blocked_checks=blocked_checks+1
        end
    end
    if age==220 then final={own,victim};manager.machine.video:snapshot() end
end)
emu.register_stop(function()
    check(#taps==5,"all command observers initialized")
    check(baseline and final,"completed command and post-command recovery")
    check(entries==(positive and 1 or 0),"one valid activation, no invalid activation")
    check(strikes==(positive and 1 or 0) and creates==strikes,"no duplicate or rejected strike/effect")
    if mode=="airborne" then check(airborne_checks==1,"airborne precondition observed") end
    if mode=="with_block" then check(blocked_checks==1,"blocking precondition observed") end
    if final then
        check(final[1].id==17 and final[1].trail==0,"Kano identity and attachment recovery")
        check(final[1].y==final[1].floor and final[1].vx==0 and final[1].vy==0,"native grounded recovery")
        if positive then
            check(final[1].health==baseline[1].health and final[2].health==baseline[2].health-26,"one original-damage hit")
            check(blood==1,"exactly one blade blood reaction")
        end
    end
    print(string.format("MK2KS_BLADE_COMMAND_RESULT pass=%s mode=%s side=%d entries=%d strikes=%d creates=%d blood=%d errors=%d",
        tostring(errors==0),mode,side,entries,strikes,creates,blood,errors))
    for _,handle in ipairs(taps) do handle:remove() end
end)
