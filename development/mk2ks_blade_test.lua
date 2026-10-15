-- Real selection and D,F+HP controls; emulated state is strictly read-only.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1", "Blade test needs two players")
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_BLADE_SIDE") or "1")
local mode=os.getenv("MK2KS_BLADE_MODE") or "near"
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert(names[side]=="kano")
assert(({near=true,block=true,duck_block=true,duck=true,far=true,air=true})[mode])
assert(mode~="air" or names[3-side]=="sonya", "Air acceptance currently has an original Sonya reference only")
local frame,hud,command,settle,baseline,last=0,nil,nil,nil,nil,nil
local cpu,program,screen,buttons
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local taps,entries,strikes,creates,steps,ready={},{},{},{},{},{}
local errors,pose_checks,palette_checks,alignment_checks=0,0,0,0
local palette_request,palette_upload
local observed,trail_objects={},{}
local fields={2,2,2,2,2,4,4,12,4,4}
local function require_result(condition,label)
    if not condition then errors=errors+1;if errors<=30 then print("MK2KS_BLADE_ERROR "..label) end end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {actor=actor,process=process,id=program:read_u16(actor+0x1f0),
        action=program:read_u16(process+0x1f0),x=signed(program:read_u16(actor+0x90)),
        y=signed(program:read_u16(actor+0xb0)),floor=signed(program:read_u16(process+0x200)),
        vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        pose=program:read_u32(actor+0x1d0),trail=program:read_u32(process+0x190),
        health=program:read_u16(health[index])}
end
local function press(index,key) buttons[index][key]:set_value(1) end
local function palette_matches(actor,source,count,skip)
    local palette=program:read_u16(actor+0x140)&0x7f00
    for color=1,count do
        if (program:read_u16(0x01800000+(palette+color)*16)&0x7fff)~=
            (program:read_u16(source+skip+color*16)&0x7fff) then return false end
    end
    return true
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        buttons={}
        for index=1,2 do
            local prefix="P"..index.." "
            buttons[index]={left=high[prefix.."Left"],right=high[prefix.."Right"],
                down=high[prefix.."Down"],up=high[prefix.."Up"],
                hp=high[prefix.."High Punch"],block=high[prefix.."Block"]}
        end
        for _,entry in ipairs({{0xfff8cc00,entries},{0xfff8e400,strikes},
                               {0xfff8d800,creates},{0xfff8e000,steps},{0xff861350,ready}}) do
            taps[#taps+1]=program:install_read_tap(entry[1],entry[1]+15,"native blade event",
                function(offset,data,mask)
                    if command and cpu.state.A8.value==program:read_u32(pointers[side]) and
                        entry[2][#entry[2]]~=frame then
                        entry[2][#entry[2]+1]=frame
                        print(string.format("MK2KS_BLADE_EVENT pc=%08X frame=%d",entry[1],frame))
                    end
                end)
        end
        taps[#taps+1]=program:install_read_tap(0xff80c6b0,0xff80c6bf,"blade palette queue",
            function()
                if command and cpu.state.A0.value==0xff680810 then
                    palette_request=frame
                    require_result(cpu.state.A2.value==64,"native palette queues exactly 64 colors")
                    print("MK2KS_BLADE_PALETTE_QUEUED frame="..frame)
                end
            end)
        taps[#taps+1]=program:install_read_tap(0xff80ca00,0xff80ca0f,"blade palette upload complete",
            function()
                if command and cpu.state.A2.value==0xff680c10 then
                    palette_upload=frame
                    local own=sample(side)
                    require_result(own.trail~=0 and palette_matches(own.trail,0xff680800,23,16),
                        "first palette fully uploaded by native VBLANK queue")
                    palette_checks=palette_checks+1
                    print("MK2KS_BLADE_PALETTE_UPLOADED frame="..frame)
                end
            end)
        taps[#taps+1]=program:install_read_tap(0xff83ebc0,0xff83ebcf,"blade aligned effect",
            function()
                if not command or cpu.state.A8.value~=program:read_u32(pointers[side]) then return end
                local object=cpu.state.A0.value
                local descriptor=program:read_u32(object+0x1a0)
                if descriptor<0xfff8f800 or descriptor>0xfff8fda0 then return end
                local own=sample(side)
                local xo=signed(program:read_u16(descriptor+32))
                local yo=signed(program:read_u16(descriptor+48))
                local flip=(program:read_u16(own.actor+0xf0)&16)~=0
                local expected=flip and own.x+xo-program:read_u16(descriptor) or own.x-xo
                require_result(signed(program:read_u16(object+0x90))==expected and
                    signed(program:read_u16(object+0xb0))==own.y-yo,"exact attached origin and facing")
                alignment_checks=alignment_checks+1
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
    local own,victim=sample(side),sample(3-side)
    if not command then
        if mode~="far" and math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                command=frame+20;baseline={own,victim}
                print(string.format("MK2KS_BLADE_COMMAND mode=%s side=%d frame=%d x=%d,%d",mode,side,command,own.x,victim.x))
                manager.machine.video:snapshot()
            end
        end
        return
    end
    local age=frame-command
    if age>=0 and age<3 then press(side,"down") end
    if age>=5 and age<8 then press(side,baseline[1].x<baseline[2].x and "right" or "left") end
    if age>=6 and age<9 then press(side,"hp") end
    if age>=-15 and age<100 then
        if mode=="block" or mode=="duck_block" then press(3-side,"block") end
        if mode=="duck" or mode=="duck_block" then press(3-side,"down") end
    end
    if mode=="air" and age>=-5 and age<-2 then press(3-side,"up") end
    if age>=-2 and age<=85 then
        observed[frame]={own,victim}
        local trail_frame=own.trail~=0 and program:read_u32(own.trail+0x1a0) or 0
        print(string.format("MK2KS_BLADE_STATE age=%d frame=%d action=%04X,%04X x=%d,%d y=%d,%d health=%d,%d pose=%08X trail=%08X trail_frame=%08X",
            age,frame,own.action,victim.action,own.x,victim.x,own.y,victim.y,own.health,victim.health,own.pose,own.trail,trail_frame))
        local elapsed=entries[1] and frame-entries[1] or -1
        if elapsed>=1 and elapsed<=38 then
            local pose,total=1,fields[1]
            while elapsed>total do pose=pose+1;total=total+fields[pose] end
            pose_checks=pose_checks+1
            require_result(own.pose==0xfe82fc40+(pose-1)*0x60,"body pose field "..elapsed)
            require_result(own.trail~=0,"attached trail field "..elapsed)
            if own.trail~=0 then
                trail_objects[own.trail]=true
                require_result(trail_frame==0xfff8f800+(pose-1)*160,"trail frame field "..elapsed)
                -- This notifier precedes VBLANK palette upload on the first
                -- allocation field. Check that field at the actual upload,
                -- not against the stale RAM from before MKII drains its queue.
                if elapsed==1 then
                    require_result(palette_request==entries[1],"first-field native palette request")
                else
                    require_result(palette_matches(own.trail,0xff680800,23,16),"independent trail palette")
                    palette_checks=palette_checks+1
                end
            end
            local alternate=(program:read_u16(own.actor+0x160)&0x40)~=0
            require_result(palette_matches(own.actor,alternate and 0xfec961f0 or 0xfec95de0,63,16),"unchanged Kano body palette")
            require_result(own.id==17,"Kano body identity")
            require_result(own.y==own.floor,"blade remains grounded")
        end
    end
    if age>=6 and age<=48 and age%3==0 then manager.machine.video:snapshot() end
    if age==180 then
        last={own,victim};manager.machine.video:snapshot()
        -- Parent-slot clearing alone is not proof that the effect was removed.
        local cursor=program:read_u32(0x0105d480)
        local count=0
        while cursor~=0 and count<1024 do
            require_result(not trail_objects[cursor],"trail object leaked into recovered display list")
            cursor=program:read_u32(cursor);count=count+1
        end
        require_result(count<1024,"native object list terminates")
    end
end)
emu.register_stop(function()
    require_result(baseline and last,"command and recovery completed")
    require_result(#entries==1 and #strikes==1,"one action entry and one collision check")
    require_result(#creates==1 and #steps==9,"one allocated trail, nine native updates")
    require_result(pose_checks==38 and palette_checks==38,"all 38 body/effect fields checked")
    require_result(alignment_checks==10,"all ten trail origins and facings checked")
    require_result(palette_request and palette_upload and palette_upload-palette_request<=1,
        "queued palette uploaded within the native next field")
    if entries[1] and strikes[1] then require_result(strikes[1]-entries[1]==10,"collision after ten fields") end
    if baseline and last then
        -- Original real-input Sonya reference hits for 26 near her jump apex.
        -- The earlier Liu reference misses: its different tucked-leg pose is
        -- not evidence that this move universally misses airborne targets.
        local damage=(mode=="near" or mode=="duck" or mode=="air") and 26 or
            (mode=="block" or mode=="duck_block") and 3 or 0
        require_result(last[1].health==baseline[1].health,"attacker health unchanged")
        require_result(last[2].health==baseline[2].health-damage,"correct victim damage "..damage)
        require_result(last[1].trail==0 and last[1].action~=0x117 and last[1].action~=0x618,"native attack and trail cleared")
        require_result(last[1].y==last[1].floor and last[1].vx==0 and last[1].vy==0,"grounded ready recovery")
        if mode=="air" and strikes[1] then
            local contact=observed[strikes[1]]
            require_result(contact and contact[2].floor-contact[2].y>=80,
                "actual high airborne Sonya contact, not a grounded hit")
            require_result(last[2].y==last[2].floor and last[2].vx==0 and last[2].vy==0,
                "native airborne victim recovery")
        end
        if mode=="far" and entries[1] then
            local first,final=observed[entries[1]+1],observed[entries[1]+38]
            require_result(first and final and math.abs(final[1].x-first[1].x)==57,"authored 57-pixel unobstructed advance")
        end
    end
    require_result(#ready>0,"native ready continuation observed")
    print(string.format("MK2KS_BLADE_RESULT pass=%s mode=%s side=%d entries=%d strikes=%d creates=%d steps=%d pose_checks=%d palette_checks=%d alignment_checks=%d errors=%d",
        tostring(errors==0),mode,side,#entries,#strikes,#creates,#steps,pose_checks,palette_checks,alignment_checks,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
