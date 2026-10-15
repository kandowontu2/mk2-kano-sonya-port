-- Seven real-input chokes: six to KO, one in the actual following round.
assert(os.getenv("MK2KS_TWO_PLAYER")=="1")
dofile("mk2ks_selector_exit_test.lua")
local side=tonumber(os.getenv("MK2KS_CHOKE_SIDE") or "1")
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert(names[side]=="kano")
local ids={kano=17,sonya=18,kitana=4,sub_zero=8}
local victim_id=assert(ids[names[3-side]])
local frame,hud,round_start,settled,ko,next_round=0,nil,nil,nil,nil,nil
local current,done=nil,false
local cpu,program,screen,buttons
local pointers={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local errors,taps,cycles,huds,wins,palettes=0,{},{},0,0,0
local function check(value,label)
    if not value then errors=errors+1;if errors<=30 then print("MK2KS_CHOKE_LIFECYCLE_ERROR "..label) end end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function sample(index)
    local actor=program:read_u32(pointers[index])
    local process=program:read_u32(processes[index])
    return {actor=actor,process=process,id=program:read_u16(actor+0x1f0),
        action=program:read_u16(process+0x1f0),x=signed(program:read_u16(actor+0x90)),
        y=signed(program:read_u16(actor+0xb0)),floor=signed(program:read_u16(process+0x200)),
        vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60),
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
                   (program:read_u16(donor[alternate and 2 or 1]+16+color*16)&0x7fff) then mismatches=mismatches+1 end
            end
            check(mismatches==0,"native body palette side "..index);palettes=palettes+1
        end
    end
    check(alternates==(names[1]==names[2] and 1 or 0),"native mirror outfit count")
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
            buttons[index]={left=high[prefix.."Left"],right=high[prefix.."Right"],down=high[prefix.."Down"],lp=low[prefix.."Low Punch"]}
        end
        for _,event in ipairs({{0xfff91400,"entries",side},{0xfff93400,"pulses",3-side},{0xfff93800,"releases",3-side}}) do
            taps[#taps+1]=program:install_read_tap(event[1],event[1]+15,"choke lifecycle",function()
                if current and frame>=current.command and cpu.state.A8.value==sample(event[3]).actor then
                    current[event[2]]=current[event[2]]+1
                end
            end)
        end
        local hud_entry=0xff800000+((side==1 and 0xfdc00 or 0xfdd00)+17*8)*8
        taps[#taps+1]=program:install_read_tap(hud_entry,hud_entry+15,"choke next HUD",function() huds=huds+1 end)
        local win_entry=0xff800000+(0xfdf00+17*4)*8
        taps[#taps+1]=program:install_read_tap(win_entry,win_entry+15,"choke native win",function() wins=wins+1 end)
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
        if green>250 then hud=frame;round_start=frame end
        return
    end
    if done then return end
    local own,victim=sample(side),sample(3-side)
    if ko and not next_round and not current then
        if frame>ko+60 and own.id==17 and victim.id==victim_id and own.health==161 and victim.health==161 then
            next_round=frame;round_start=frame;settled=nil
            print(string.format("MK2KS_CHOKE_LIFECYCLE_NEXT frame=%d huds=%d",frame,huds))
        else return end
    end
    if frame<round_start+180 then return end
    if not current then
        if math.abs(own.x-victim.x)>68 then
            press(side,own.x<victim.x and "right" or "left");settled=nil
        else
            settled=settled or frame
            if frame-settled>=30 then
                current={number=#cycles+1,command=frame+20,health=victim.health,entries=0,pulses=0,releases=0,
                    direction=own.x<victim.x and "right" or "left"}
                body_palettes()
                print(string.format("MK2KS_CHOKE_LIFECYCLE_START cycle=%d frame=%d health=%d",current.number,current.command,victim.health))
            end
        end
        return
    end
    local age=frame-current.command
    if age>=0 and age<3 then press(side,"down") end
    if age>=5 and age<8 then press(side,current.direction) end
    if age>=6 and age<9 then press(side,"lp") end
    if age>=0 then
        check(own.id==17 and victim.id==victim_id,"true IDs through repeated choke")
        if victim.health==0 and not ko then ko=frame;print("MK2KS_CHOKE_LIFECYCLE_KO frame="..frame) end
    end
    if age==45 then
        body_palettes()
        if current.number==1 or current.number==6 or next_round then manager.machine.video:snapshot() end
    end
    if age==180 then
        check(current.entries==1 and current.pulses==4 and current.releases==1,"one complete action with four pulses, cycle "..current.number)
        check(victim.health==math.max(0,current.health-32),"exact clipped damage cycle "..current.number)
        check(own.health==161,"attacker undamaged")
        for _,actor in ipairs({own,victim}) do
            check(actor.y==actor.floor and actor.vx==0 and actor.vy==0,"grounded recovery cycle "..current.number)
            check(actor.trail==0,"no retained attached objects")
        end
        body_palettes()
        print(string.format("MK2KS_CHOKE_LIFECYCLE_CYCLE number=%d before=%d after=%d entries=%d pulses=%d releases=%d",
            current.number,current.health,victim.health,current.entries,current.pulses,current.releases))
        cycles[#cycles+1]=current;current=nil;settled=nil
        if next_round then done=true;manager.machine.video:snapshot() end
    end
end)
emu.register_stop(function()
    check(#taps==5,"all lifecycle observers installed")
    check(done and #cycles==7,"six chokes to KO and a seventh in the following round")
    check(ko and next_round and next_round>ko,"actual KO and native following round")
    check(huds>=2 and wins>=1,"native HUD rebuild and true Kano win")
    print(string.format("MK2KS_CHOKE_LIFECYCLE_RESULT pass=%s side=%d victim=%s cycles=%d huds=%d wins=%d next_round=%d palettes=%d errors=%d",
        tostring(errors==0),side,names[3-side],#cycles,huds,wins,next_round or -1,palettes,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
