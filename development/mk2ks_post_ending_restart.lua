-- Complete the actual P1/P2 tower, then buy a fresh P1/P2 game through inputs.
-- Existing tower health assistance ends before this entirely input-only new game.
assert(os.getenv("MK2KS_STOP_ON_CAMPAIGN_COMPLETE")~="1","Restart must not stop at attract")
local source_side=tonumber(os.getenv("MK2KS_RESTART_SOURCE_SIDE") or "1")
assert(source_side==1 or source_side==2)
if source_side==2 then
    assert(os.getenv("MK2_P2_POST_ENDING_RESTART")=="1","P2 tower must continue after actual ending")
    dofile("mk2ks_p2_tower_probe.lua")
else dofile("mk2ks_cpu_ladder_trace.lua") end
local source=assert(os.getenv(source_side==1 and "MK2KS_TEST_FIGHTER" or "MK2KS_P2_FIGHTER"))
local source_roster=source_side==1 and 0x01060280 or 0x01060e50
local source_state=source_side==1 and 0x010601f0 or 0x01060dc0
local target=assert(os.getenv("MK2KS_RESTART_TARGET"))
local new_side=tonumber(os.getenv("MK2KS_RESTART_NEW_SIDE") or "1")
assert(new_side==1 or new_side==2)
local players={
    {roster=0x01060280,state=0x010601f0,actor=0x01060220,health=0x010602f0},
    {roster=0x01060e50,state=0x01060dc0,actor=0x01060df0,health=0x01060ec0}}
local human,opponent=players[new_side],players[3-new_side]
local ids={kano=17,sonya=18}
local identity,desired=assert(ids[source]),assert(ids[target])
local frame,ended,css,match,live,errors=0,nil,nil,nil,0,0
local restart_complete=false
local pictures,texts={0,0},{0,0}
local taps,fields,route={},{},{}
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"]
local fresh_schedule,fresh_order,fresh_cpu=nil,nil,nil
local special_mode=os.getenv("MK2KS_RESTART_SPECIAL") or "none"
assert(special_mode=="none" or special_mode=="projectile" or special_mode=="mobility" or special_mode=="sequence" or special_mode=="pair" or special_mode=="airthrow" or special_mode=="lifecycle" or special_mode=="mobility_contact" or special_mode=="projectile_choreography")
assert(special_mode~="airthrow" or target=="kano","Only Kano has the intended standalone air throw")
local airthrow=special_mode=="airthrow" and dofile("mk2ks_restart_airthrow.lua")(new_side,os.getenv("MK2KS_AIR_JOIN_VICTIM")) or nil
local lifecycle=special_mode=="lifecycle" and dofile("mk2ks_restart_lifecycle.lua")(target,new_side) or nil
local mobility_contact=special_mode=="mobility_contact" and dofile("mk2ks_restart_lifecycle.lua")(target,new_side,{driver="mobility_contact"}) or nil
local projectile_choreography=special_mode=="projectile_choreography" and dofile("mk2ks_restart_lifecycle.lua")(target,new_side,{driver="projectile_contact"}) or nil
if projectile_choreography then
    assert(os.getenv("MK2KS_PROJECTILE_OBSERVER_ONLY")=="1")
    -- Autoboot runs in a sol sandbox, while dofile uses Lua's root globals.
    -- Use the explicit shared Lua table, never a guest-memory write.
    _G.MK2KS_PROJECTILE_OBSERVER_ARMED=false
    dofile("mk2ks_projectile_choreography_probe.lua")
end
local after_restart=airthrow or lifecycle or mobility_contact or projectile_choreography
local projectile=special_mode=="projectile" and dofile("mk2ks_restart_projectile.lua")(target,new_side) or nil
local mobility=special_mode=="mobility" and dofile("mk2ks_restart_mobility.lua")(target,new_side) or nil
local sequence=special_mode=="sequence" and dofile("mk2ks_restart_sequence.lua")(target,new_side) or nil
local pair=special_mode=="pair" and dofile("mk2ks_restart_pair.lua")(target,new_side) or nil
local coordinates={[17]={0,0},[1]={1,0},[0]={2,0},[2]={3,0},[9]={4,0},[18]={5,0},
    [8]={1,1},[6]={2,1},[4]={3,1},[11]={4,1},[5]={1,2},[3]={2,2},[10]={3,2},[7]={4,2}}
local function check(ok,label)
    if not ok then errors=errors+1;print("MK2_RESTART_ERROR frame="..frame.." "..label) end
end
local function pulse(name,age,first,duration)
    if age>=first and age<first+(duration or 5) then fields[name]:set_value(1) end
end
local function snap(label) manager.machine.screens[":screen"]:snapshot("restart_"..label..".png") end
local function fresh_cpu_state(capture)
    local table,schedule=p:read_u32(0xff8a11f0),p:read_u32(0x01061b10)
    local order=-1
    if table==0xfffa2c00 then
        for n=0,5 do if p:read_u32(table+n*32)==schedule then order=n end end
    end
    local expected=order>=0 and p:read_u16(schedule) or 0xffff
    local actor=p:read_u32(opponent.actor)
    local valid=actor>=0x01000000 and actor<0x01100000
    local roster,state=p:read_u16(opponent.roster),p:read_u16(opponent.state)
    local live_id=valid and p:read_u16(actor+0x1f0) or 0xffff
    check(order>=0 and valid and state==0 and roster==expected and live_id==expected and
        p:read_u16(0x01061b30)==0 and p:read_u16(0x01061b00)==0 and p:read_u16(opponent.health)>0,
        "new-game native CPU ownership and cleared opposite participation")
    if not fresh_schedule then fresh_schedule,fresh_order,fresh_cpu=schedule,order,expected end
    check(schedule==fresh_schedule and order==fresh_order and expected==fresh_cpu,"new-game CPU schedule stable")
    if capture then
        print(string.format("MK2_RESTART_CPU frame=%d state=%d roster=%d id=%d actor=%08X order=%d schedule=%08X expected=%d cpu_side=%d",frame,state,roster,live_id,actor,order,schedule,expected,3-new_side))
    end
end
local function visible_css()
    local pixels,width=manager.machine.screens[":screen"]:pixels()
    if width~=400 then return false end
    local yellow,early=0,0
    for y=0,24,2 do for x=40,360,2 do
        local color=string.unpack("<I4",pixels,(y*width+x)*4+1)
        local r,g,b=(color>>16)&255,(color>>8)&255,color&255
        if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
    end end
    return yellow>=400 and yellow<=430 and early>=10
end
local function own_name_shadow()
    local ui=manager.machine.memory.regions[":ksui"]
    local colors=ui:read_u8(6)|(ui:read_u8(7)<<8)
    local names=8+2*(colors*2+ui:read_u8(4)*ui:read_u8(5))
    local w,h=ui:read_u8(names),ui:read_u8(names+1)
    local base=names+2+(target=="kano" and 0 or w*h)
    local first,last,face=w,-1,{}
    for y=0,9 do for x=0,w-1 do
        if ui:read_u8(base+y*w+x)>48 then first,last=math.min(first,x),math.max(last,x);face[y*w+x]=true end
    end end
    local count,matched=0,0
    local left=new_side==1 and 29 or 367-(last-first+2)
    local pixels,width=manager.machine.screens[":screen"]:pixels()
    for y=0,9 do for x=first+1,last+1 do
        if not face[y*w+x] and (face[y*w+x-1] or (y>0 and face[(y-1)*w+x-1])) then
            count=count+1
            local px=left+x-first
            if (string.unpack("<I4",pixels,((30+y)*width+px)*4+1)&0xffffff)==0x420000 then matched=matched+1 end
        end
    end end
    check(count>20 and matched==count,"fresh target name and native shadow")
    print(string.format("MK2_RESTART_SHADOW target=%s matched=%d expected=%d pass=%s",target,matched,count,tostring(count>20 and matched==count)))
end
for page=0,1 do
    local entry=0xfffa4800+(50+(identity-17)*2+page)*32
    taps[#taps+1]=p:install_read_tap(entry,entry+31,"actual own ending picture before restart",function(at,data)
        if at==entry and not ended and p:read_u16(0x01061b30)==16 and p:read_u16(source_roster)==identity then
            pictures[page+1]=pictures[page+1]+1
            print(string.format("MK2_RESTART_PICTURE frame=%d page=%d id=%d pc=%08X value=%04X",frame,page+1,identity,cpu.state.PC.value,data&0xffff))
        end
    end)
    local base=page==0 and 0xfffa5000 or 0xfffa5800
    taps[#taps+1]=p:install_read_tap(base+identity*96,base+(identity+1)*96-1,"actual own ending text before restart",function(at,data)
        if (at-base)%32==0 and not ended and p:read_u16(0x01061b30)==16 and p:read_u16(source_roster)==identity then
            texts[page+1]=texts[page+1]+1
            print(string.format("MK2_RESTART_TEXT frame=%d page=%d id=%d pc=%08X value=%04X",frame,page+1,identity,cpu.state.PC.value,data&0xffff))
        end
    end)
end
emu.register_frame(function()
    frame=frame+1
    if restart_complete then after_restart.drive(frame);return end
    if frame==1 then
        local system=manager.machine.ioport.ports[":IN1"].fields
        local high=manager.machine.ioport.ports[":IN0"].fields
        local low=manager.machine.ioport.ports[":IN2"].fields
        local label="P"..new_side.." "
        fields={coin=system["Coin "..new_side],start=system[new_side==1 and "1 Player Start" or "2 Players Start"],up=high[label.."Up"],
            left=high[label.."Left"],right=high[label.."Right"],hp=high[label.."High Punch"],block=high[label.."Block"],
            down=high[label.."Down"],lp=low[label.."Low Punch"],lk=low[label.."Low Kick"],hk=high[label.."High Kick"]}
        print("MK2_RESTART_BOOT source="..source.." target="..target.." restart_writes=0 source_side="..source_side.." new_side="..new_side)
    end
    if not ended and frame>10000 and pictures[1]>0 and pictures[2]>0 and texts[1]>0 and texts[2]>0 and
        p:read_u16(0x01061b30)==16 and p:read_u16(0x010601d0)==11 and
        p:read_u16(source_roster)~=identity and p:read_u16(source_state)==0 then
        ended=frame
        print(string.format("MK2_RESTART_ATTRACT frame=%d source=%s mode=11 roster=%d pictures=%d,%d texts=%d,%d",
            frame,source,p:read_u16(source_roster),pictures[1],pictures[2],texts[1],texts[2]))
        snap("attract")
    end
    if not ended then return end
    local age=frame-ended
    pulse("coin",age,150);pulse("coin",age,180);pulse("start",age,240)
    if not css and p:read_u16(0x010601d0)==4 and p:read_u16(human.state)==3 and visible_css() then
        css=frame
        local initial=p:read_u16(human.roster)
        local coordinate=assert(coordinates[initial],"Unknown actual new-game initial cursor")
        for n=1,coordinate[2] do route[#route+1]="up" end
        local delta=coordinates[desired][1]-coordinate[1]
        for n=1,math.abs(delta) do route[#route+1]=delta<0 and "left" or "right" end
        print(string.format("MK2_RESTART_CSS frame=%d initial=%d target=%d route=%s",frame,initial,desired,table.concat(route,",")))
        snap("css")
    end
    if css then
        local selected_age=frame-css
        for index,direction in ipairs(route) do pulse(direction,selected_age,56+(index-1)*12) end
        if selected_age==140 or selected_age==156 then
            check(p:read_u16(human.roster)==desired,"selected own canonical identity")
            print(string.format("MK2_RESTART_HIGHLIGHT frame=%d age=%d target=%d roster=%d",frame,selected_age,desired,p:read_u16(human.roster)))
            snap("highlight_"..selected_age)
        end
        pulse("hp",selected_age,176,8)
        local actor=p:read_u32(human.actor)
        local valid=actor>=0x01000000 and actor<0x01100000
        if not match and p:read_u16(0x010601d0)==2 and p:read_u16(human.state)==1 and valid and
            p:read_u16(human.roster)==desired and p:read_u16(actor+0x1f0)==desired and p:read_u16(human.health)==161 then
            match=frame
            check(p:read_u16(0x01061b30)==0,"new game resets ladder index")
            print(string.format("MK2_RESTART_MATCH frame=%d target=%s id=%d actor=%08X stage=%d",frame,target,desired,actor,p:read_u16(0x01061b30)))
            snap("match")
        end
        if match then
            fresh_cpu_state(frame==match or frame-match==600)
            check(valid and p:read_u16(actor+0x1f0)==desired and p:read_u16(human.roster)==desired and
                p:read_u16(human.state)==1 and p:read_u16(human.health)>0,"new-game live identity/state")
            live=live+1
            -- Ordinary guarding protects the bounded restart observation, not health writes.
            if frame-match>=100 then fields.block:set_value(1) end
            if projectile then projectile.drive(frame,match,fields) end
            if mobility then mobility.drive(frame,match,fields) end
            if sequence then sequence.drive(frame,match,fields) end
            if pair then pair.drive(frame,match,fields) end
            if frame-match==120 then own_name_shadow() end
            if frame-match==120 or frame-match==600 then snap("combat_"..(frame-match)) end
            if live>=601 then
                if projectile then check(projectile.finish(),"owned projectile after restart") end
                if mobility then check(mobility.finish(),"owned mobility move after restart") end
                if sequence then check(sequence.finish(),"owned blade/bicycle sequence after restart") end
                if pair then check(pair.finish(),"complete native close pair after restart") end
                print(string.format("MK2_RESTART_COMPLETE frame=%d source=%s target=%s live=%d errors=%d restart_writes=0",frame,source,target,live,errors))
                if after_restart then
                    if projectile_choreography then _G.MK2KS_PROJECTILE_OBSERVER_ARMED=true end
                    restart_complete=true;after_restart.begin(frame)
                else manager.machine:exit() end
            end
        end
    end
end)
emu.register_stop(function()
    print(string.format("MK2_RESTART_RESULT pass=%s source=%s target=%s ended=%s css=%s match=%s live=%d errors=%d pictures=%d,%d texts=%d,%d restart_writes=0",
        tostring(ended~=nil and css~=nil and match~=nil and live>=601 and errors==0),source,target,
        tostring(ended),tostring(css),tostring(match),live,errors,pictures[1],pictures[2],texts[1],texts[2]))
    for _,tap in ipairs(taps) do tap:remove() end
end)
