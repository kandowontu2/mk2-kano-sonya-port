-- Eight real-input blade swipes: seven to a KO, one after the native round reset.
-- Selection, identity, display teardown and HUD checks come from the base suite.
-- No game memory, health, position, identity or process-state writes are used.
local joined=...
assert(joined and joined.native_join or os.getenv("MK2KS_TWO_PLAYER")=="1", "Two live players are required")
for _,name in ipairs({"MK2KS_TEST_LEG","MK2KS_TEST_BALL","MK2KS_TEST_SQUARE"}) do
    assert((os.getenv(name) or "")=="", "Clear other special-move modes")
end
assert(os.getenv("MK2KS_TEST_PROJECTILES")~="1", "Clear projectile mode")
if not joined then dofile("mk2ks_selector_exit_test.lua") end

local side=joined and joined.side or tonumber(os.getenv("MK2KS_BLADE_SIDE") or "1")
local names=joined and joined.names or {os.getenv("MK2KS_TEST_FIGHTER"),os.getenv("MK2KS_P2_FIGHTER")}
local ids={kano=17,sonya=18,kitana=4,sub_zero=8}
assert(side==1 or side==2, "Invalid attacker side")
assert(names[side]=="kano", "The attacker must actually be Kano")
local victim_id=assert(ids[names[3-side]], "Unsupported lifecycle victim")
local actors={0x01060220,0x01060df0}
local processes={0x01060260,0x01060e30}
local health={0x010602f0,0x01060ec0}
local fields={2,2,2,2,2,4,4,12,4,4}
local frame,hud,round_start=0,nil,nil
local cpu,program,screen,buttons
local taps,cycles={},{}
local current,settled,ko_frame,next_round=nil,nil,nil,nil
local errors,native_huds,native_wins,palettes,next_palettes=0,0,0,0,0
local complete=false
local trace
local function check(value,label)
    if not value then
        errors=errors+1
        if errors<=40 then print("MK2KS_BLADE_LIFECYCLE_ERROR "..label) end
    end
end
local function signed(value) return value>=0x8000 and value-0x10000 or value end
local function actor(index) return program:read_u32(actors[index]) end
local function sample(index)
    local object=actor(index)
    local process=program:read_u32(processes[index])
    return {actor=object,process=process,id=program:read_u16(object+0x1f0),
        action=program:read_u16(process+0x1f0),health=program:read_u16(health[index]),
        x=signed(program:read_u16(object+0x90)),y=signed(program:read_u16(object+0xb0)),
        floor=signed(program:read_u16(process+0x200)),
        vx=program:read_u32(object+0x40),vy=program:read_u32(object+0x60),
        pose=program:read_u32(object+0x1d0),trail=program:read_u32(process+0x190)}
end
local function press(index,key) buttons[index][key]:set_value(1) end
local function body_palettes()
    local alternates=0
    for index,name in ipairs(names) do
        local donor=name=="kano" and {0xfec95de0,0xfec961f0} or
                    name=="sonya" and {0xfec96790,0xfec96ba0} or nil
        if donor then
            local object=actor(index)
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
            check(mismatches==0,"body palette side "..index.." mismatches="..mismatches)
            palettes=palettes+1
            if next_round then next_palettes=next_palettes+1 end
        end
    end
    check(alternates==(names[1]==names[2] and 1 or 0),"native mirror outfit choice")
end
local function tap(address,label,callback)
    taps[#taps+1]=program:install_read_tap(address,address+15,label,callback)
end
emu.register_frame(function()
    frame=joined and joined.now() or frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        screen=manager.machine.screens[":screen"]
        if os.getenv("MK2KS_LIFECYCLE_TRACE")=="1" then
            trace=dofile("mk2ks_lifecycle_trace.lua")("blade",side,names,function()
                return frame,current and current.number,current and frame-current.command or -1
            end)
        end
        local controls=manager.machine.ioport.ports[":IN0"].fields
        buttons={}
        for index=1,2 do
            local prefix="P"..index.." "
            buttons[index]={left=controls[prefix.."Left"],right=controls[prefix.."Right"],
                down=controls[prefix.."Down"],hp=controls[prefix.."High Punch"]}
        end
        for _,event in ipairs({{0xfff8cc00,"entry"},{0xfff8e400,"strike"},
                                {0xfff8d800,"create"},{0xfff8e000,"step"},{0xff861350,"ready"}}) do
            tap(event[1],"blade lifecycle "..event[2],function()
                if not current or frame<current.command then return end
                local object=cpu.state.A8.value
                if event[2]=="ready" then
                    for index=1,2 do if object==actor(index) then current.ready[index]=frame end end
                elseif object==actor(side) and current[event[2].."_last"]~=frame then
                    current[event[2]]=current[event[2]]+1
                    current[event[2].."_last"]=frame
                    current[event[2].."_frame"]=current[event[2].."_frame"] or frame
                end
            end)
        end
        tap(0xfff90000,"blade lifecycle own victim reaction",function()
            if not current or not current.entry_frame then return end
            current.hurts=current.hurts+1;current.hurt_frame=frame
            check(cpu.state.A8.value==actor(3-side),"own blade reaction uses actual victim")
        end)
        tap(0xff9a5b00,"blade lifecycle blood request",function()
            if not current or current.hurt_frame~=frame then return end
            current.requests=current.requests+1
            check(cpu.state.A0.value==1 and cpu.state.A8.value==actor(3-side),"original native victim blood recipe")
        end)
        tap(0xff9a7f70,"blade lifecycle blood task",function()
            if current and current.hurt_frame and frame<=current.hurt_frame+25 then current.starts=current.starts+1 end
        end)
        tap(0xff9aff00,"blade lifecycle blood allocated",function()
            if not current or not current.hurt_frame or frame>current.hurt_frame+25 then return end
            local object=cpu.state.A8.value
            check(not current.objects[object],"separate blood allocation within this generation")
            check(cpu.state.A11.value==actor(3-side),"blood belongs to current victim")
            current.objects[object]={};current.allocations=current.allocations+1
        end)
        tap(0xff83f610,"blade lifecycle blood inserted",function()
            local object=current and current.objects[cpu.state.A8.value]
            if object and not object.inserted then object.inserted=frame;current.insertions=current.insertions+1 end
        end)
        tap(0xff9b0e50,"blade lifecycle blood cleanup",function()
            local object=current and current.objects[cpu.state.A8.value]
            if object and not object.cleaned then object.cleaned=frame;current.cleanups=current.cleanups+1 end
        end)
        local hud_entry=0xff800000+((side==1 and 0xfdc00 or 0xfdd00)+17*8)*8
        tap(hud_entry,"blade lifecycle native HUD",function() native_huds=native_huds+1 end)
        local win_entry=0xff800000+(0xfdf00+17*4)*8
        tap(win_entry,"blade lifecycle native winner",function()
            native_wins=native_wins+1
            print(string.format("MK2KS_BLADE_LIFECYCLE_WIN frame=%d wins=%d",frame,native_wins))
        end)
    end
    if joined then
        if not joined.active() then return end
        joined.clear_controls()
    end
    if not hud then
        local pixels,width=screen:pixels()
        if width~=400 or frame<900 then return end
        local green=0
        for x=20,380 do
            local color=string.unpack("<I4",pixels,(30*width+x)*4+1)
            local r,g,b=(color>>16)&255,(color>>8)&255,color&255
            if g>100 and g>r*3//2 and g>b*3//2 then green=green+1 end
        end
        if green>250 then hud=frame;round_start=frame end
        return
    end
    if complete then return end
    local own,victim=sample(side),sample(3-side)
    if ko_frame and not next_round then
        if own.health==161 and victim.health==161 and frame>ko_frame+60 and own.id==17 and victim.id==victim_id then
            next_round=frame;round_start=frame;settled=nil
            print(string.format("MK2KS_BLADE_LIFECYCLE_NEXT_ROUND frame=%d hud_entries=%d",frame,native_huds))
        else return end
    end
    if frame<round_start+180 then return end
    if not current then
        if math.abs(own.x-victim.x)>85 then
            press(side,own.x<victim.x and "right" or "left");settled=nil
        else
            settled=settled or frame
            if frame-settled>=30 then
                current={number=#cycles+1,command=frame+20,entry=0,strike=0,create=0,step=0,
                    hurts=0,requests=0,starts=0,allocations=0,insertions=0,cleanups=0,
                    objects={},trails={},ready={},own=own,victim=victim,damage=0,damage_events=0,poses=0}
                body_palettes()
                print(string.format("MK2KS_BLADE_LIFECYCLE_COMMAND cycle=%d frame=%d health=%d,%d x=%d,%d",current.number,current.command,own.health,victim.health,own.x,victim.x))
            end
        end
        return
    end
    local age=frame-current.command
    if trace and age>=0 then trace.field(frame,current.number,age) end
    if age>=0 and age<3 then press(side,"down") end
    if age>=5 and age<8 then press(side,current.own.x<current.victim.x and "right" or "left") end
    if age>=6 and age<9 then press(side,"hp") end
    local damage=current.victim.health-victim.health
    if damage~=current.damage then
        current.damage_events=current.damage_events+1;current.damage=damage;current.contact=frame
        print(string.format("MK2KS_BLADE_LIFECYCLE_DAMAGE cycle=%d frame=%d damage=%d action=%04X health=%d",current.number,frame,damage,victim.action,victim.health))
    end
    local elapsed=current.entry_frame and frame-current.entry_frame or -1
    if elapsed>=1 and elapsed<=38 then
        local pose,total=1,fields[1]
        while elapsed>total do pose=pose+1;total=total+fields[pose] end
        check(own.pose==0xfe82fc40+(pose-1)*0x60,"complete original body pose field "..elapsed)
        check(own.trail~=0,"attached blade exists during action")
        if own.trail~=0 then
            current.trails[own.trail]=true
            check(program:read_u32(own.trail+0x1a0)==0xfff8f800+(pose-1)*160,"matching native blade trail phase")
        end
        current.poses=current.poses+1
    end
    if age==35 then body_palettes() end
    if age==35 and (current.number==1 or current.number==7 or next_round) then manager.machine.video:snapshot() end
    if age==150 then
        check(current.entry==1 and current.strike==1,"one blade entry and strike per complete command")
        check(current.create==1 and current.step==9 and current.poses==38,"one complete ten-pose, 38-field body/trail action")
        check(current.entry_frame and current.strike_frame and current.strike_frame-current.entry_frame==10,"original ten-field startup")
        check(current.damage_events==1 and current.damage==math.min(26,current.victim.health),"one correctly clipped hit damage event")
        check(current.hurts==1 and current.requests==1 and current.starts==1,"one own reaction and native blood recipe")
        check(current.allocations==8 and current.insertions==8 and current.cleanups==8,"all eight blood allocations inserted and cleaned")
        check(own.id==17 and victim.id==victim_id,"actual identities survive repeated hits")
        check(own.health==current.own.health,"no spurious attacker damage")
        check(own.trail==0 and own.action~=0x117 and own.action~=0x618,"native action and attached trail cleared")
        check(own.y==own.floor and own.vx==0 and own.vy==0,"grounded attacker recovery")
        local cursor,count=program:read_u32(0x0105d480),0
        while cursor~=0 and count<1024 do
            local descriptor=program:read_u32(cursor+0x1a0)
            check(not (current.trails[cursor] and descriptor>=0xfff8f800 and descriptor<=0xfff8fda0),"no stale trail frame in native display list")
            check(not current.objects[cursor] or current.objects[cursor].cleaned,"no uncleaned blood generation remains displayed")
            cursor=program:read_u32(cursor);count=count+1
        end
        check(count<1024,"native display list terminates")
        if victim.health>0 then
            body_palettes()
            check(victim.y==victim.floor and victim.vx==0 and victim.vy==0,"grounded victim recovery")
            check(current.contact and current.ready[side] and current.ready[3-side] and
                current.ready[side]>=current.contact and current.ready[3-side]>=current.contact,"both native ready continuations")
        else
            check(not ko_frame,"one tested knockout")
            ko_frame=frame
        end
        print(string.format("MK2KS_BLADE_LIFECYCLE_CYCLE cycle=%d entries=%d strikes=%d creates=%d steps=%d poses=%d damage=%d health=%d,%d blood=%d/%d/%d errors=%d",current.number,current.entry,current.strike,current.create,current.step,current.poses,current.damage,own.health,victim.health,current.allocations,current.insertions,current.cleanups,errors))
        cycles[#cycles+1]=current;current=nil;settled=nil
        if next_round then
            complete=true;manager.machine.video:snapshot()
            if joined then joined.complete(frame,errors==0);manager.machine:exit() end
        end
    end
end)
emu.register_stop(function()
    check(#taps==13,"all lifecycle observers initialized")
    check(complete and #cycles==8,"seven swipes to a KO, then an eighth in the next round")
    check(ko_frame and next_round and next_round>ko_frame,"actual native round transition")
    check(native_huds>=2 and native_wins>=1,"native HUD rebuild and Kano win entry")
    check(palettes>=20 and next_palettes>=3,"native body palettes checked across repeated hits and the next round")
    print(string.format("MK2KS_BLADE_LIFECYCLE_RESULT pass=%s side=%d victim=%s cycles=%d hud_entries=%d wins=%d next_round=%d palettes=%d next_palettes=%d errors=%d",tostring(errors==0),side,names[3-side],#cycles,native_huds,native_wins,next_round or -1,palettes,next_palettes,errors))
    for _,handle in ipairs(taps) do handle:remove() end
end)
