-- Native Sonya bicycle: ordinary selection and controls; memory is read-only.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1")
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_BICYCLE_SIDE") or "1")
local mode=os.getenv("MK2KS_BICYCLE_MODE") or "near"
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert((side==1 or side==2) and names[side]=="sonya")
assert(({near=true,far=true,block=true,duck=true,duck_block=true,air=true,held=true,
    reversed=true,expired=true,wrong_button=true,airborne=true,with_block=true})[mode])
local rejected=mode=="reversed" or mode=="expired" or mode=="wrong_button" or mode=="airborne" or mode=="with_block"
local hit=mode=="near" or mode=="air" or mode=="held"
local ids={kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,shang_tsung=6,
    raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11,kano=17,sonya=18}
local frame,hud,command,settle,baseline,final=0,nil,nil,nil,nil,nil
local cpu,program,screen,buttons
local taps,entries,releases,ticks,errors,palette_checks={},0,0,0,0,0
local pairs_checked,checks,poses=0,{},{}
local tick_frames,release_frame,flings={},nil,0
local actorptr={0x01060220,0x01060df0}
local processptr={0x01060260,0x01060e30}
local healthptr={0x010602f0,0x01060ec0}
local function check(value,label)
    if not value then errors=errors+1;if errors<=40 then print("MK2KS_BICYCLE_ERROR "..label) end end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function state(index)
    local actor=program:read_u32(actorptr[index])
    local process=program:read_u32(processptr[index])
    return {actor=actor,process=process,id=program:read_u16(actor+0x1f0),
        x=signed(program:read_u16(actor+0x90)),y=signed(program:read_u16(actor+0xb0)),
        floor=signed(program:read_u16(process+0x200)),pose=program:read_u32(actor+0x1d0),
        vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
        gravity=program:read_u32(actor+0x20),action=program:read_u16(process+0x1f0),
        trail=program:read_u32(process+0x190),health=program:read_u16(healthptr[index])}
end
local function palettes()
    local alternate_count=0
    for index,name in ipairs(names) do
        local source=name=="kano" and {0xfec95de0,0xfec961f0} or name=="sonya" and {0xfec96790,0xfec96ba0} or nil
        if source then
            local actor=program:read_u32(actorptr[index])
            local alternate=(program:read_u16(actor+0x160)&0x40)~=0
            if alternate then alternate_count=alternate_count+1 end
            local bank=program:read_u16(actor+0x140)&0x7f00
            for color=1,63 do
                check((program:read_u16(0x01800000+(bank+color)*16)&0x7fff)==
                    (program:read_u16(source[alternate and 2 or 1]+16+color*16)&0x7fff),"native body palette")
            end
            palette_checks=palette_checks+1
        end
    end
    check(alternate_count==(names[1]==names[2] and 1 or 0),"native mirror outfit")
end
local function press(index,key) buttons[index][key]:set_value(1) end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        buttons={{},{}}
        for index=1,2 do
            for key,label in pairs({left="Left",right="Right",up="Up",down="Down",block="Block",hk="High Kick",hp="High Punch"}) do
                buttons[index][key]=assert(high["P"..index.." "..label])
            end
        end
        for _,address in ipairs({0xfff9a400,0xfff9d000,0xfff9e000,0xff876650}) do
            taps[#taps+1]=program:install_read_tap(address,address+15,"native bicycle",function()
                if not command or frame<command or frame>command+260 then return end
                local own,victim=state(side),state(3-side)
                if address==0xfff9a400 and cpu.state.A8.value==own.actor then
                    entries=entries+1;print("MK2KS_BICYCLE_ENTRY frame="..frame)
                elseif address==0xfff9d000 and cpu.state.A8.value==own.actor then
                    ticks=ticks+1;checks[frame+1]=true;tick_frames[#tick_frames+1]=frame
                elseif address==0xfff9e000 and cpu.state.A8.value==victim.actor then
                    releases=releases+1;release_frame=frame;print("MK2KS_BICYCLE_RELEASE frame="..frame)
                    check(victim.y<victim.floor,"victim release from actual lifted height")
                elseif address==0xff876650 and release_frame and cpu.state.A8.value==victim.actor then
                    flings=flings+1
                    check(cpu.state.A0.value==0x40000 and cpu.state.A1.value==0xfffa0000 and
                        cpu.state.A2.value==0xa000 and cpu.state.A3.value==5,"original victim fling parameters")
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
    local own,victim=state(side),state(3-side)
    if not command then
        if mode~="far" and math.abs(own.x-victim.x)>68 then
            press(side,own.x<victim.x and "right" or "left");settle=nil
        else
            settle=settle or frame
            if frame-settle>=30 then
                command=frame+20;baseline={own,victim};palettes()
                print(string.format("MK2KS_BICYCLE_COMMAND frame=%d side=%d mode=%s x=%d,%d",command,side,mode,own.x,victim.x))
            end
        end
        return
    end
    local age=frame-command
    local forward=baseline[1].x<baseline[2].x and "right" or "left"
    local back=forward=="right" and "left" or "right"
    local down=mode=="expired" and 72 or 12
    if (age>=0 and age<3) or (age>=6 and age<9) then press(side,mode=="reversed" and forward or back) end
    if age>=down and age<down+3 then press(side,"down") end
    if age>=down+1 and age<(mode=="held" and 110 or down+4) then press(side,mode=="wrong_button" and "hp" or "hk") end
    if mode=="airborne" and age>=-5 and age<-2 then press(side,"up") end
    if mode=="with_block" and age>=-15 and age<200 then press(side,"block") end
    if (mode=="block" or mode=="duck_block") and age>=-15 and age<200 then press(3-side,"block") end
    if (mode=="duck" or mode=="duck_block") and age>=-15 and age<200 then press(3-side,"down") end
    if mode=="air" and age>=0 and age<3 then press(3-side,"up") end
    if age>=0 and age<=230 then
        check(own.id==18 and victim.id==ids[names[3-side]],"actual identities persist")
        for index,s in ipairs({own,victim}) do
            print(string.format("MK2KS_BICYCLE_STATE age=%d which=%d action=%04X x=%d y=%d floor=%d vx=%08X vy=%08X gravity=%08X pose=%08X health=%d",age,index,s.action,s.x,s.y,s.floor,s.vx,s.vy,s.gravity,s.pose,s.health))
        end
        if own.pose>=0xfe83ea40 and own.pose<=0xfe83ec80 then poses[own.pose]=true end
        if checks[frame] and victim.action==0x215 then
            check(victim.x-own.x==(forward=="right" and 48 or -48) and victim.y-own.y==-32,"original paired contact offset")
            local magnitude=own.vy==0xfffd0000 and 0x30000 or 0x10000
            local velocity=forward=="right" and magnitude or 0x100000000-magnitude
            check(own.vx==velocity and victim.vx==velocity,"original rising/float horizontal velocity")
            pairs_checked=pairs_checked+1;palettes()
        end
        if age%10==0 and age<=130 then manager.machine.video:snapshot() end
    end
    if age==250 then final={own,victim};palettes();manager.machine.video:snapshot() end
end)
emu.register_stop(function()
    check(final~=nil,"complete input and recovery observation")
    check(entries==(rejected and 0 or 1),"exact native action activation count")
    check(releases==(hit and 1 or 0),"paired release count")
    if hit then
        check(ticks>=16 and ticks<=48 and pairs_checked>=ticks-1,"complete bounded paired flight")
        check(flings==1,"one native victim fling")
        for i=2,#tick_frames do check(tick_frames[i]-tick_frames[i-1]==1,"one paired update per game field") end
        for _,group in ipairs({0xfe83ea40,0xfe83ea80,0xfe83eae0,0xfe83eb40,0xfe83eb80,0xfe83ebc0,0xfe83ec00,0xfe83ec40,0xfe83ec80}) do
            check(poses[group],"original own pose "..string.format("%08X",group))
        end
    else check(ticks==0,"no paired flight after miss/block/rejected input") end
    if final then
        check(final[1].health==baseline[1].health,"attacker health unchanged")
        if not rejected then check(final[2].health==baseline[2].health-(hit and 22 or mode=="block" and 3 or 0),"exact native damage/chip/miss") end
        for _,s in ipairs(final) do
            check(s.y==s.floor and s.vx==0 and s.vy==0 and s.gravity==0,"grounded recovery with stopped physics")
            check(s.trail==0,"no attached object leak")
            check(s.action~=0x214 and s.action~=0x215,"both native paired states released")
        end
    end
    print(string.format("MK2KS_BICYCLE_RESULT pass=%s side=%d mode=%s entries=%d ticks=%d pair_checks=%d releases=%d palettes=%d errors=%d",tostring(errors==0),side,mode,entries,ticks,pairs_checked,releases,palette_checks,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
