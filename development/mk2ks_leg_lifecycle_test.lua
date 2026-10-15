-- Repeated real-input leg grabs, including a KO and the next native round.
-- The base harness owns selection, display/identity checks and input clearing.
-- No health, position, identity, process-state or input-history writes are used.
assert((os.getenv("MK2KS_TEST_LEG") or "")=="", "Clear single-grab mode")
assert((os.getenv("MK2KS_TEST_BALL") or "")=="", "Clear cannonball mode")
assert((os.getenv("MK2KS_TEST_SQUARE") or "")=="", "Clear square-wave mode")
assert(os.getenv("MK2KS_TEST_PROJECTILES")~="1", "Clear projectile mode")
assert(os.getenv("MK2KS_TWO_PLAYER")=="1", "Two live players are required")
dofile("mk2ks_selector_exit_test.lua")

local side=tonumber(os.getenv("MK2KS_LEG_SIDE") or "1")
assert(side==1 or side==2, "Invalid Sonya side")
local names={os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
assert(names[side]=="sonya", "The grabber must be Sonya")
local ids={kano=17,sonya=18,kitana=4,sub_zero=8}
local victim_id=assert(ids[names[3-side]], "Unsupported lifecycle victim")
local actor_ptrs={0x01060220,0x01060df0}
local process_ptrs={0x01060260,0x01060e30}
local health_ptrs={0x010602f0,0x01060ec0}
local frame,hud_frame,round_start=0,nil,nil
local cpu,program,screen,controls
local taps,cycles={},{}
local current,settled,ko_frame,next_round=nil,nil,nil,nil
local native_huds,native_wins,errors=0,0,0
local palette_checks,next_round_palette_checks=0,0
local completed=false
local mash=os.getenv("MK2KS_LEG_LIFECYCLE_MASH")=="1"
local function require_state(condition,label)
    if not condition then
        errors=errors+1
        if errors<=20 then print("MK2KS_LEG_LIFECYCLE_ERROR "..label) end
    end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function read(side_index)
    local actor=program:read_u32(actor_ptrs[side_index])
    local process=program:read_u32(process_ptrs[side_index])
    return {actor=actor,process=process,id=program:read_u16(actor+0x1f0),
        action=program:read_u16(process+0x1f0),health=program:read_u16(health_ptrs[side_index]),
        x=signed(program:read_u16(actor+0x90)),y=signed(program:read_u16(actor+0xb0)),
        floor=signed(program:read_u16(process+0x200)),
        vx=program:read_u32(actor+0x40),vy=program:read_u32(actor+0x60)}
end
local function press(which,key) controls[which][key]:set_value(1) end
local function chord(which) press(which,"down");press(which,"lp");press(which,"block") end
local function check_palettes()
    local alternate_count=0
    for index,name in ipairs(names) do
        local donor=name=="kano" and {0xfec95de0,0xfec961f0} or
            name=="sonya" and {0xfec96790,0xfec96ba0} or nil
        if donor then
            local actor=program:read_u32(actor_ptrs[index])
            local alternate=(program:read_u16(actor+0x160)&0x40)~=0
            if alternate then alternate_count=alternate_count+1 end
            local bank=program:read_u16(actor+0x140)&0x7f00
            local mismatches=0
            for color=1,63 do
                local expected=program:read_u16(donor[alternate and 2 or 1]+16+color*16)&0x7fff
                local actual=program:read_u16(0x01800000+(bank+color)*16)&0x7fff
                if actual~=expected then mismatches=mismatches+1 end
            end
            require_state(mismatches==0,"native palette side "..index.." mismatches "..mismatches)
            palette_checks=palette_checks+1
            if next_round then next_round_palette_checks=next_round_palette_checks+1 end
        end
    end
    require_state(alternate_count==(names[1]==names[2] and 1 or 0),"native mirror outfit selection")
end

emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"]
        program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        local high=manager.machine.ioport.ports[":IN0"].fields
        local low=manager.machine.ioport.ports[":IN2"].fields
        controls={}
        for index=1,2 do
            local prefix="P"..index.." "
            controls[index]={left=high[prefix.."Left"],right=high[prefix.."Right"],
                down=high[prefix.."Down"],up=high[prefix.."Up"],
                lp=low[prefix.."Low Punch"],block=high[prefix.."Block"]}
        end
        for _,entry in ipairs({{0xfff80800,"entry"},{0xfff83800,"collision"},{0xff861350,"ready"}}) do
                taps[#taps+1]=program:install_read_tap(entry[1],entry[1]+15,"leg lifecycle "..entry[2],
                    function(offset,data,mask)
                        if not current then return end
                        local actor=cpu.state.A8.value
                        if entry[2]=="ready" then
                            for index,pointer in ipairs(actor_ptrs) do
                                if actor==program:read_u32(pointer) then current.ready[index]=frame end
                            end
                        elseif actor==program:read_u32(actor_ptrs[side]) then
                            current[entry[2]]=current[entry[2]]+1
                            current[entry[2].."_frame"]=current[entry[2].."_frame"] or frame
                        end
                    end)
        end
        local hud_entry=0xff800000+((side==1 and 0xfdc00 or 0xfdd00)+18*8)*8
        taps[#taps+1]=program:install_read_tap(hud_entry,hud_entry+15,"leg native round HUD",
            function(offset,data,mask) native_huds=native_huds+1 end)
        local win_entry=0xff800000+(0xfdf00+18*4)*8
        taps[#taps+1]=program:install_read_tap(win_entry,win_entry+15,"leg native winner",
            function(offset,data,mask)
                native_wins=native_wins+1
                print(string.format("MK2KS_LEG_LIFECYCLE_WIN frame=%d wins=%d",frame,native_wins))
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
        if green>250 then hud_frame=frame;round_start=frame end
        return
    end
    if completed then return end
    local own,victim=read(side),read(3-side)
    if ko_frame and not next_round then
        if own.health==161 and victim.health==161 and frame>ko_frame+60 and
            own.id==18 and victim.id==victim_id then
            next_round=frame;round_start=frame;settled=nil
            print(string.format("MK2KS_LEG_LIFECYCLE_NEXT_ROUND frame=%d hud_entries=%d",frame,native_huds))
        else return end
    end
    if frame<round_start+180 then return end
    if not current then
        if math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");settled=nil
        else
            settled=settled or frame
            if frame-settled>=30 then
                current={number=#cycles+1,command=frame,entry=0,collision=0,paired=0,
                    ready={},own=own,victim=victim,damage_events=0,damage=0}
                print(string.format("MK2KS_LEG_LIFECYCLE_COMMAND cycle=%d frame=%d health=%d,%d x=%d,%d mash=%s",
                    current.number,frame,own.health,victim.health,own.x,victim.x,tostring(mash)))
                check_palettes()
                chord(side)
            end
        end
        return
    end
    local age=frame-current.command
    if age<4 or (mash and ((age>=22 and age<26) or (age>=40 and age<44))) then chord(side) end
    if mash and age>=30 and age<34 then chord(3-side) end
    if victim.action==0x111 then current.paired=current.paired+1 end
    local damage=current.victim.health-victim.health
    if damage~=current.damage then
        current.damage_events=current.damage_events+1
        current.damage=damage;current.release=frame
        print(string.format("MK2KS_LEG_LIFECYCLE_DAMAGE cycle=%d frame=%d damage=%d action=%04X",
            current.number,frame,damage,victim.action))
        require_state(victim.action==0x506,"damage occurs in native knockdown state")
    end
    if age==45 or age==65 then
        if victim.health>0 then check_palettes() end
        manager.machine.video:snapshot()
    end
    if age==150 then
        require_state(current.entry==1 and current.collision==1,"one entry/collision per command")
        require_state(current.entry_frame and current.collision_frame and
            current.collision_frame-current.entry_frame==10,"native startup duration")
        require_state(current.paired>=46 and current.paired<=48,"complete paired interval")
        require_state(current.damage_events==1 and current.damage==math.min(35,current.victim.health),"one release damage event")
        require_state(current.release and current.collision_frame and
            current.release-current.collision_frame==(side==1 and 48 or 47),"native release scheduling")
        require_state(own.id==18 and victim.id==victim_id,"own identities retained")
        require_state(own.health==current.own.health,"no spurious grabber damage")
        require_state(own.action~=0x110 and victim.action~=0x111,"paired states cleared")
        require_state(own.y==current.own.floor and own.vx==0 and own.vy==0,"grabber grounded recovery")
        if victim.health>0 then
            check_palettes()
            require_state(victim.y==current.victim.floor and victim.vx==0 and victim.vy==0,"victim grounded recovery")
            require_state(current.release and current.ready[side] and current.ready[3-side] and
                current.ready[side]>=current.release and current.ready[3-side]>=current.release,"both native ready continuations")
        else
            require_state(not ko_frame,"only one tested KO")
            ko_frame=frame
        end
        print(string.format("MK2KS_LEG_LIFECYCLE_CYCLE cycle=%d entry=%d collision=%d paired=%d damage=%d health=%d,%d errors=%d",
            current.number,current.entry,current.collision,current.paired,current.damage,own.health,victim.health,errors))
        cycles[#cycles+1]=current;current=nil;settled=nil
        if next_round then completed=true;manager.machine.video:snapshot() end
    end
end)

emu.register_stop(function()
    require_state(completed and #cycles==6,"five grabs to KO, then a sixth in the next round")
    require_state(ko_frame and next_round and next_round>ko_frame,"actual native round transition")
    require_state(native_huds>=2 and native_wins>=1,"native HUD rebuild and Sonya win entry")
    require_state(palette_checks>=20 and next_round_palette_checks>=4,"paired/recovered/next-round palette coverage")
    print(string.format("MK2KS_LEG_LIFECYCLE_RESULT pass=%s side=%d victim=%s mash=%s cycles=%d native_huds=%d native_wins=%d next_round=%d palettes=%d next_round_palettes=%d errors=%d",
        tostring(errors==0),side,names[3-side],tostring(mash),#cycles,native_huds,native_wins,next_round or -1,
        palette_checks,next_round_palette_checks,errors))
    for _,tap in ipairs(taps) do tap:remove() end
end)
