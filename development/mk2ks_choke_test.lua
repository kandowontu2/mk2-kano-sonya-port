-- Real selection and D,F+LP only. All emulated memory access is read-only.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1")
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_CHOKE_SIDE") or "1")
local mode=os.getenv("MK2KS_CHOKE_MODE") or "near"
local approach_gap=tonumber(os.getenv("MK2KS_CHOKE_APPROACH_GAP") or "68")
assert(approach_gap>=50 and approach_gap<=140)
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert(side==1 or side==2);assert(names[side]=="kano")
assert(({near=true,block=true,duck=true,duck_block=true,air=true,far=true,
    held=true,reversed=true,expired=true,wrong_button=true,airborne=true,with_block=true})[mode])
local positive=mode=="near" or mode=="held"
local negative=mode=="reversed" or mode=="expired" or mode=="wrong_button" or mode=="airborne" or mode=="with_block"
local ids={kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,shang_tsung=6,
    raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11,kano=17,sonya=18}
local expected_victim=assert(ids[names[3-side]])
local frame,hud,command,settle,baseline,final=0,nil,nil,nil,nil,nil
local cpu,program,screen,buttons
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local errors,taps,entries,collisions,paired_frames,pulses,releases=0,{},{},{},{},{},{}
local checks,observed={},{}
local pair_checks=0
local palette_checks,airborne_checks,block_checks=0,0,0
local flings,clamps,velocity_requests=0,{},0
local own_groups={0xfe8304e0,0xfe830540,0xfe8305a0,0xfe830600,0xfe830660,0xfe8306c0,0xfe830660}
local original_xy={
    [17]={{79,-8},{56,-31},{27,-28},{29,-26},{51,-43},{68,-45},{51,-43}},
    [18]={{77,-19},{52,-43},{26,-36},{29,-36},{54,-50},{64,-50},{54,-50}}
}
local stock_groups={0xff917430,0xff924db0,0xff930c00,0xff93e430,0xff94f340,0xff94f340,
    0xff95c500,0xff96aaf0,0xff97bcb0,0xff97bcb0,0xff97bcb0,0xff991030}
local stock_grip={{-9,50},{-7,44},{-11,48},{-14,47},{-12,47},{-12,47},
    {-19,48},{-7,43},{-9,41},{-9,41},{-9,41},{-6,44}}
local function check(value,label)
    if not value then errors=errors+1;if errors<=40 then print("MK2KS_CHOKE_ERROR "..label) end end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {actor=actor,process=process,id=program:read_u16(actor+0x1f0),
        x=signed(program:read_u16(actor+0x90)),y=signed(program:read_u16(actor+0xb0)),
        floor=signed(program:read_u16(process+0x200)),pose=program:read_u32(actor+0x1d0),
        vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        flags=program:read_u16(actor+0xf0),action=program:read_u16(process+0x1f0),
        trail=program:read_u32(process+0x190),health=program:read_u16(health[index])}
end
local function press(index,key) buttons[index][key]:set_value(1) end
local function body_palettes()
    local alternates=0
    for index,name in ipairs(names) do
        local donor=name=="kano" and {0xfec95de0,0xfec961f0} or
                    name=="sonya" and {0xfec96790,0xfec96ba0} or nil
        if donor then
            local object=program:read_u32(pointers[index])
            local alternate=(program:read_u16(object+0x160)&0x40)~=0
            if alternate then alternates=alternates+1 end
            local bank=program:read_u16(object+0x140)&0x7f00
            local mismatches=0
            for color=1,63 do
                if (program:read_u16(0x01800000+(bank+color)*16)&0x7fff)~=
                   (program:read_u16(donor[alternate and 2 or 1]+16+color*16)&0x7fff) then
                    mismatches=mismatches+1
                end
            end
            check(mismatches==0,"original body palette side "..index)
            palette_checks=palette_checks+1
        end
    end
    check(alternates==(names[1]==names[2] and 1 or 0),"native alternate outfit selection")
end
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
            buttons[index]={}
            for key,label in pairs({left="Left",right="Right",up="Up",down="Down",block="Block",hp="High Punch"}) do
                buttons[index][key]=assert(high[prefix..label])
            end
            buttons[index].lp=assert(low[prefix.."Low Punch"])
        end
        for _,address in ipairs({0xfff91400,0xfff94800,0xfff89400,0xfff93400,0xfff93800,
                                0xff876650,0xff805560,0xff8055f0,0xff831bd0}) do
            taps[#taps+1]=program:install_read_tap(address,address+15,"native choke",function()
                if not command or frame<command or frame>command+220 then return end
                local own,victim=sample(side),sample(3-side)
                if address==0xfff91400 and cpu.state.A8.value==own.actor then entries[#entries+1]=frame
                elseif address==0xfff94800 and cpu.state.A8.value==own.actor then collisions[#collisions+1]=frame
                elseif address==0xfff93400 and cpu.state.A8.value==victim.actor then
                    pulses[#pulses+1]=frame;print("MK2KS_CHOKE_DAMAGE frame="..frame.." before="..victim.health)
                elseif address==0xfff93800 and cpu.state.A8.value==victim.actor then
                    releases[#releases+1]=frame
                    check(victim.y<victim.floor,"release from actual lifted height")
                elseif address==0xff876650 and releases[1] and cpu.state.A8.value==victim.actor then
                    flings=flings+1
                    check(cpu.state.A0.value==0x40000 and cpu.state.A1.value==0xfffc0000 and
                        cpu.state.A2.value==0x8000 and cpu.state.A3.value==5,"original native fling parameters")
                elseif address==0xff831bd0 and releases[1] and frame<=releases[1]+1 and cpu.state.A8.value==victim.actor then
                    local velocity=baseline[1].x<baseline[2].x and 0x40000 or 0xfffc0000
                    local destination=side==1 and 0x01060ea0 or 0x010602d0
                    check(cpu.state.A0.value==velocity and cpu.state.A1.value==destination,
                        "native signed horizontal-velocity request for actual victim")
                    velocity_requests=velocity_requests+1
                    print(string.format("MK2KS_CHOKE_VELOCITY_REQUEST frame=%d velocity=%08X destination=%08X",frame,cpu.state.A0.value,cpu.state.A1.value))
                elseif (address==0xff805560 or address==0xff8055f0) and releases[1] and
                    cpu.state.A2.value==victim.actor and victim.action==0x506 then
                    local bound=signed((address==0xff805560 and cpu.state.A0.value or cpu.state.A1.value)&0xffff)
                    check(cpu.state.A4.value==0 and
                        (address==0xff805560 and victim.x<=bound or address==0xff8055f0 and victim.x>=bound),
                        "native boundary alone cancels outward release velocity")
                    clamps[frame]=true
                    if frame<=releases[1]+1 then print(string.format("MK2KS_CHOKE_CLAMP frame=%d x=%d bound=%d",frame,victim.x,bound)) end
                elseif address==0xfff89400 and cpu.state.A8.value==own.actor and own.action==0x111 then
                    local group=program:read_u32(cpu.state.A9.value)
                    if group~=0 then
                        local count=#paired_frames+1
                        local phase=count<=3 and count or (count-4)%4+4
                        paired_frames[count]=frame;checks[frame+1]=phase
                        check(group==own_groups[phase],"paired own phase "..count)
                        print(string.format("MK2KS_CHOKE_PAIR frame=%d count=%d phase=%d",frame,count,phase))
                    end
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
        if mode~="far" and math.abs(own.x-victim.x)>approach_gap then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                command=frame+20;baseline={own,victim}
                body_palettes()
                print(string.format("MK2KS_CHOKE_COMMAND frame=%d side=%d mode=%s x=%d,%d",command,side,mode,own.x,victim.x))
                manager.machine.video:snapshot()
            end
        end
        return
    end
    local age=frame-command
    local forward=baseline[1].x<baseline[2].x and "right" or "left"
    local last_direction=mode=="expired" and 64 or 5
    if age>=0 and age<3 then press(side,mode=="reversed" and forward or "down") end
    if age>=last_direction and age<last_direction+3 then press(side,mode=="reversed" and "down" or forward) end
    if age>=last_direction+1 and age<(mode=="held" and 100 or last_direction+4) then
        press(side,mode=="wrong_button" and "hp" or "lp")
    end
    if mode=="airborne" and age>=-5 and age<-2 then press(side,"up") end
    if mode=="with_block" and age>=-15 and age<160 then press(side,"block") end
    if age==last_direction+1 then
        if mode=="airborne" then
            check(own.y<own.floor and own.vy~=0,"actual airborne command precondition");airborne_checks=airborne_checks+1
        elseif mode=="with_block" then
            check((own.action==0x301 or own.action==0x302) and
                (program:read_u16(0x01600000)&(side==1 and 0x20 or 0x2000))==0,
                "actual held block before command");block_checks=block_checks+1
        end
    end
    if age>=-15 and age<160 then
        if mode=="block" or mode=="duck_block" then press(3-side,"block") end
        if mode=="duck" or mode=="duck_block" then press(3-side,"down") end
    end
    if mode=="air" and age>=-5 and age<-2 then press(3-side,"up") end
    if age>=-2 and age<=220 then
        observed[frame]={own,victim}
        print(string.format("MK2KS_CHOKE_STATE age=%d frame=%d action=%04X,%04X x=%d,%d y=%d,%d health=%d,%d pose=%08X,%08X",
            age,frame,own.action,victim.action,own.x,victim.x,own.y,victim.y,own.health,victim.health,own.pose,victim.pose))
        check(own.id==17 and victim.id==expected_victim,"true live identities")
    end
    local phase=checks[frame]
    if phase then
        local reference=original_xy[expected_victim] or original_xy[18]
        local dx,dy=reference[phase][1],reference[phase][2]
        local group
        if expected_victim==17 then group=phase==7 and 0xfe8294a0 or 0xfe829500
        elseif expected_victim==18 then group=0xfe836860
        else
            group=stock_groups[expected_victim+1]
            dx=dx+8+stock_grip[expected_victim+1][1]
            dy=dy+54-stock_grip[expected_victim+1][2]
        end
        local facing=baseline[1].x<baseline[2].x and 1 or -1
        check(own.pose==own_groups[phase] and victim.pose==group,"actual paired composites phase "..phase)
        check(victim.x==own.x+facing*dx and victim.y==own.y+dy,
            string.format("paired alignment phase=%d actual=%d,%d expected=%d,%d",phase,victim.x,victim.y,own.x+facing*dx,own.y+dy))
        -- Depending on scheduler order the release process can already have
        -- initialized velocity on the last held field. The held pose and XY
        -- must still be visible, as in the original game's mirror captures.
        local releasing=pair_checks==21 and releases[1]==frame-1
        check(victim.action==(releasing and 0x506 or 0x112),"paired state or actual last-field release")
        if releasing then
            local normal_vx=facing==1 and 0x40000 or 0xfffc0000
            -- FF831AC0 writes the requested velocity; MKII's ordinary motion
            -- process publishes/eases actor+40 later (FF8285D0). Checking the
            -- actor word immediately mistakes that scheduling delay for a
            -- missing launch on some stock bodies.
            check(program:read_u32(side==1 and 0x01060ea0 or 0x010602d0)==normal_vx and
                victim.vy==0xfffc0000,"native requested release velocity without early pose advancement")
        end
        check(own.y==own.floor and own.vx==0 and own.vy==0,"stationary grounded grabber")
        pair_checks=pair_checks+1
        body_palettes()
        if pair_checks==1 or pair_checks==6 or pair_checks==22 then manager.machine.video:snapshot() end
    end
    if age==220 then final={own,victim};body_palettes();manager.machine.video:snapshot() end
end)
emu.register_stop(function()
    check(#taps==9,"all native observers initialized")
    check(baseline and final,"command and recovery completed")
    check(#entries==(negative and 0 or 1),"exactly one valid activation, no invalid activation")
    check(negative and #collisions==0 or not negative and #collisions>=1 and #collisions<=6,"bounded native contact checks")
    check(#paired_frames==(positive and 22 or 0) and pair_checks==#paired_frames,"all paired phases, no blocked/missed capture")
    check(#pulses==(positive and 4 or 0) and #releases==(positive and 1 or 0),"four damage pulses and one native release")
    check(flings==(positive and 1 or 0),"one original-parameter native fling")
    check(velocity_requests==(positive and 1 or 0),"one actual native velocity request")
    if positive and releases[1] then
        -- Wide/leaning stock bodies can still overlap on release. MKII's
        -- FF828620 separation phase uses three-pixel opposing velocities
        -- before publishing the requested four-pixel fling. Original native
        -- processing, not the command callback, owns that short transition.
        local landed_request=observed[releases[1]+8]
        local was_clamped=false
        for at=releases[1],releases[1]+8 do was_clamped=was_clamped or clamps[at] end
        local expected=baseline[1].x<baseline[2].x and 0x40000 or 0xfffc0000
        check(landed_request and (landed_request[2].vx==expected or landed_request[2].vx==0 and was_clamped),
            "requested velocity reaches actual actor after bounded native separation")
    end
    if positive and #paired_frames==22 then
        for i=2,22 do
            check(paired_frames[i]-paired_frames[i-1]==(i<=4 and 5 or 3),"native paired phase timing "..i)
        end
        for i=2,#pulses do check(pulses[i]-pulses[i-1]==12,"four-pose squeeze damage cadence") end
    end
    if final and baseline then
        check(final[1].health==baseline[1].health,"attacker health unchanged")
        if not negative then
            check(final[2].health==baseline[2].health-(positive and 32 or 0),"exact native total damage or miss")
        end
        for index=1,2 do
            check(final[index].y==final[index].floor and final[index].vx==0 and final[index].vy==0,"both actors recovered on ground")
            check(final[index].trail==0,"no attached objects after recovery")
        end
    end
    if mode=="airborne" then check(airborne_checks==1,"observed airborne precondition") end
    if mode=="with_block" then check(block_checks==1,"observed held-block precondition") end
    check(palette_checks==(pair_checks+2)*(expected_victim>=17 and 2 or 1),"all body palette checks completed")
    print(string.format("MK2KS_CHOKE_RESULT pass=%s side=%d mode=%s victim=%s entries=%d collisions=%d pairs=%d pair_checks=%d pulses=%d releases=%d palettes=%d errors=%d",
        tostring(errors==0),side,mode,names[3-side],#entries,#collisions,#paired_frames,pair_checks,#pulses,#releases,palette_checks,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
