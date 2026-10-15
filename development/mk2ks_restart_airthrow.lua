-- Native challenger join and Kano air throw. Inputs only; taps never replace data.
return function(side,victim)
    assert(side==1 or side==2)
    victim=victim or "sonya"
    local vid=assert(({sonya=18,sub_zero=8})[victim])
    local followup=os.getenv("MK2KS_AIR_JOIN_FOLLOWUP")=="1"
    -- Sub-Zero lands farther away than the donor victim. Close that distance
    -- with ordinary walking input so the recovery probe really tests contact.
    local follow_walk=vid==8 and 24 or 8
    local p=manager.machine.devices[":maincpu"].spaces.program
    local cpu=manager.machine.devices[":maincpu"].state
    local screen=manager.machine.screens[":screen"]
    local slots={
        {actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
        {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
    local coords={[17]={0,0},[1]={1,0},[0]={2,0},[2]={3,0},[9]={4,0},[18]={5,0},
        [8]={1,1},[6]={2,1},[4]={3,1},[11]={4,1},[5]={1,2},[3]={2,2},[10]={3,2},[7]={4,2}}
    local fields,taps,routes={},{},{}
    local frame,begin,css,match,ready,jump,command=0,nil,nil,nil,nil,nil,nil
    local errors,damage,stores=0,0,0
    local caught,own_recovered,victim_recovered,complete=nil,nil,nil,false
    local follow_epoch,follow_done=nil,false
    local counts={}
    local follow_physics={}
    local function valid(x) return x>=0x01000000 and x<0x01100000 end
    local function signed(x) return x>=0x8000 and x-0x10000 or x end
    local function check(ok,why)
        if not ok then errors=errors+1;if errors<=20 then print("MK2_AIR_JOIN_ERROR frame="..frame.." "..why) end end
    end
    local function sample(n)
        local slot=slots[n]
        local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
        if not valid(actor) or not valid(main) then return end
        return {actor=actor,main=main,id=p:read_u16(actor+0x1f0),roster=p:read_u16(slot.id),state=p:read_u16(slot.state),
            x=signed(p:read_u16(actor+0x90)),y=signed(p:read_u16(actor+0xb0)),floor=signed(p:read_u16(main+0x200)),
            yraw=p:read_u32(actor+0xa0),
            action=p:read_u16(main+0x1f0),pose=p:read_u32(actor+0x1d0),vx=p:read_u32(actor+0x40),vy=p:read_u32(actor+0x60),
            flags=p:read_u16(main+0x210),body=p:read_u16(actor+0x160),trail=p:read_u32(main+0x190),hp=p:read_u16(slot.hp)}
    end
    local function owned(s,v) return s and v and s.id==17 and s.roster==17 and s.state==1 and v.id==vid and v.roster==vid and v.state==1 end
    local function clean(s) return (s.action==0 or s.action==0x303) and s.y==s.floor and s.vx==0 and s.vy==0 and s.flags&0x1c==0 and s.body&0x0c==0 and s.trail==0 end
    local function state(tag,s,v)
        print(string.format("MK2_AIR_JOIN_%s frame=%d age=%d side=%d actor=%08X main=%08X id=%d roster=%d state=%d action=%04X x=%d y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X trail=%08X pose=%08X hp=%d victim=%08X vmain=%08X vid=%d vroster=%d vstate=%d vaction=%04X vxpos=%d vypos=%d vfloor=%d vvx=%08X vvy=%08X vflags=%04X vbody=%04X vtrail=%08X vpose=%08X vhp=%d suppression=%d callback=%08X vcallback=%08X yraw=%08X vyraw=%08X writes=0",
            tag,frame,frame-match,side,s.actor,s.main,s.id,s.roster,s.state,s.action,s.x,s.y,s.floor,s.vx,s.vy,s.flags,s.body,s.trail,s.pose,s.hp,
            v.actor,v.main,v.id,v.roster,v.state,v.action,v.x,v.y,v.floor,v.vx,v.vy,v.flags,v.body,v.trail,v.pose,v.hp,p:read_u16(0x010619d0),p:read_u32(s.main+0x290),p:read_u32(v.main+0x290),s.yraw,v.yraw))
    end
    local function event(kind,entry,s,v)
        counts[kind]=(counts[kind] or 0)+1
        print(string.format("MK2_AIR_JOIN_EVENT frame=%d age=%d kind=%s entry=%08X pc=%08X a8=%08X a13=%08X actor=%08X main=%08X victim=%08X vmain=%08X a0=%08X a1=%08X a2=%08X a3=%08X a6=%08X a7=%08X a9=%08X a10=%08X count=%d",
            frame,frame-match,kind,entry,cpu.PC.value,cpu.A8.value,cpu.A13.value,s.actor,s.main,v.actor,v.main,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A6.value,cpu.A7.value,cpu.A9.value,cpu.A10.value,counts[kind]))
    end
    local entries={gate=0xff8643e0,action=0xff8b6ff0,align=0xfffc0680,release=0xfffff980,
        flight=0xfffff580,callback=0xfffff800,bounce=0xfffc2000,damage=0xff83a7a0,
        own_landing=0xfffc1c00,victim_getup=0xff8ea320,recovery=0xff861410}
    for entry_kind,address in pairs(entries) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"native joined air throw "..entry_kind,function(at)
            if at~=address or not match or not command or frame-command>180 then return end
            local s,v=sample(side),sample(3-side)
            if not owned(s,v) then return end
            local kind=entry_kind
            local actor=cpu.A8.value
            if kind=="gate" or kind=="action" then
                if actor~=s.actor then return end
                if kind=="action" then caught=frame;check(cpu.A13.value==s.main,"main air-throw ownership") end
            elseif not caught then return
            elseif kind=="recovery" then
                if actor==s.actor and cpu.A13.value==s.main and not own_recovered then own_recovered=frame;kind="own_recovery"
                elseif actor==v.actor and cpu.A13.value==v.main and not victim_recovered then victim_recovered=frame;kind="victim_recovery"
                else return end
            elseif kind=="flight" or kind=="callback" or kind=="bounce" or kind=="victim_getup" then
                if actor~=v.actor then return end
            elseif actor~=s.actor then return end
            event(kind,address,s,v)
        end)
    end
    local health=slots[3-side].hp
    taps[#taps+1]=p:install_write_tap(health,health+15,"native air-throw health store",function(at,data)
        if at~=health or not caught or complete or frame-caught>180 then return end
        local s,v=sample(side),sample(3-side)
        if not owned(s,v) then return end
        local after=data&0xffff
        if after==v.hp then return end
        stores=stores+1;damage=damage+v.hp-after
        print(string.format("MK2_AIR_JOIN_HEALTH frame=%d age=%d pc=%08X a8=%08X a13=%08X actor=%08X victim=%08X before=%d after=%d delta=%d stores=%d writes=0",
            frame,frame-match,cpu.PC.value,cpu.A8.value,cpu.A13.value,s.actor,v.actor,v.hp,after,v.hp-after,stores))
    end)
    for n,slot in ipairs(slots) do
        taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,"native follow-up punch health",function(at,data)
            if at~=slot.hp or not follow_epoch or frame<follow_epoch+112 then return end
            local s=sample(n);if not s then return end
            local after=data&0xffff
            if after==s.hp then return end
            print(string.format("MK2_AIR_JOIN_FOLLOW_HEALTH frame=%d age=%d slot=%d actor=%08X main=%08X pc=%08X a8=%08X a13=%08X before=%d after=%d delta=%d writes=0",frame,frame-follow_epoch,n,s.actor,s.main,cpu.PC.value,cpu.A8.value,cpu.A13.value,s.hp,after,s.hp-after))
        end)
    end
    taps[#taps+1]=p:install_read_tap(0xff876660,0xff87666f,"native follow-up jump physics",function(at)
        if at~=0xff876660 or not follow_epoch or frame<follow_epoch+40 or frame>follow_epoch+52 then return end
        for n=1,2 do
            local s=sample(n)
            if s and cpu.A8.value==s.actor and cpu.A13.value==s.main and not follow_physics[n] then
                follow_physics[n]=frame
                print(string.format("MK2_AIR_JOIN_FOLLOW_EVENT frame=%d age=%d slot=%d kind=jump_physics entry=FF876660 pc=%08X a8=%08X a13=%08X actor=%08X main=%08X a0=%08X a1=%08X a2=%08X a6=%08X writes=0",frame,frame-follow_epoch,n,cpu.PC.value,cpu.A8.value,cpu.A13.value,s.actor,s.main,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A6.value))
            end
        end
    end)
    local function pulse(n,name,age,first,duration)
        if age>=first and age<first+(duration or 5) then
            fields[n][name]:set_value(1)
            if match then print(string.format("MK2_AIR_JOIN_CONTROL frame=%d slot=%d button=%s value=1 writes=0",frame,n,name)) end
        end
    end
    local function visible_css()
        local pixels,width=screen:pixels()
        if width~=400 then return false end
        local yellow=0
        for y=0,24,2 do for x=40,360,2 do
            local c=string.unpack("<I4",pixels,(y*width+x)*4+1)
            if (c>>16)&255>175 and (c>>8)&255>140 and c&255<100 then yellow=yellow+1 end
        end end
        return yellow>=400 and yellow<=430
    end
    local function finish()
        local pass=complete and errors==0 and damage==16 and stores==1 and caught and own_recovered and victim_recovered and (not followup or follow_done)
        print(string.format("MK2_AIR_JOIN_RESULT pass=%s side=%d victim=%s begin=%s css=%s match=%s jump=%s command=%s caught=%s own_recovery=%s victim_recovery=%s damage=%d stores=%d errors=%d writes=0",
            tostring(not not pass),side,victim,tostring(begin),tostring(css),tostring(match),tostring(jump),tostring(command),tostring(caught),tostring(own_recovered),tostring(victim_recovered),damage,stores,errors))
        return not not pass
    end
    emu.register_stop(function() for _,tap in ipairs(taps) do tap:remove() end end)
    local root=p:read_u32(0xff0008e0)
    local poses={};for i=0,9 do poses[#poses+1]=string.format("%08X",p:read_u32(root+i*32)) end
    local align=p:read_u32(0xfffc0400+vid*32)
    local flightpose=p:read_u32(0xfffc0b00+vid*32)
    check(root==0xff014900 and p:read_u32(0xffff9320)==0xff8643e0 and align==0xfffd0029,"native air root/block table/alignment guards")
    print(string.format("MK2_AIR_JOIN_ROM side=%d vid=%d block_gate=%08X root=%08X poses=%s alignment=%08X flight_pose=%08X writes=0",side,vid,p:read_u32(0xffff9320),root,table.concat(poses,","),align,flightpose))
    return {
        begin=function(now)
            begin=now
            local high=manager.machine.ioport.ports[":IN0"].fields
            local low=manager.machine.ioport.ports[":IN2"].fields
            local system=manager.machine.ioport.ports[":IN1"].fields
            for n=1,2 do
                local label="P"..n.." "
                fields[n]={up=high[label.."Up"],down=high[label.."Down"],left=high[label.."Left"],right=high[label.."Right"],hp=high[label.."High Punch"],
                    hk=high[label.."High Kick"],block=high[label.."Block"],lp=low[label.."Low Punch"],lk=low[label.."Low Kick"],coin=system["Coin "..n],start=system[n==1 and "1 Player Start" or "2 Players Start"]}
            end
            print(string.format("MK2_AIR_JOIN_BEGIN frame=%d side=%d joining=%d victim=%s mode=%d p1=%d,%d p2=%d,%d writes=0",now,side,3-side,victim,p:read_u16(0x010601d0),p:read_u16(slots[1].state),p:read_u16(slots[1].id),p:read_u16(slots[2].state),p:read_u16(slots[2].id)))
        end,
        drive=function(now)
            assert(begin);frame=now
            for _,slot in ipairs(fields) do for _,field in pairs(slot) do field:set_value(0) end end
            local age=frame-begin
            for _,a in ipairs({10,30}) do pulse(3-side,"coin",age,a) end
            pulse(3-side,"start",age,60)
            if age==10 or age==30 or age==60 then print(string.format("MK2_AIR_JOIN_INPUT frame=%d age=%d slot=%d button=%s hold=5 writes=0",frame,age,3-side,age==60 and "start" or "coin")) end
            if age%60==0 and not match then print(string.format("MK2_AIR_JOIN_WAIT frame=%d age=%d mode=%d p1=%d,%d p2=%d,%d",frame,age,p:read_u16(0x010601d0),p:read_u16(slots[1].state),p:read_u16(slots[1].id),p:read_u16(slots[2].state),p:read_u16(slots[2].id))) end
            if not css and p:read_u16(0x010601d0)==4 and visible_css() then
                css=frame
                for n=1,2 do
                    local initial=p:read_u16(slots[n].id)
                    local desired=n==side and 17 or vid
                    local from,to=assert(coords[initial]),coords[desired]
                    local route={}
                    for _=1,from[2] do route[#route+1]="up" end
                    local delta=to[1]-from[1]
                    for _=1,math.abs(delta) do route[#route+1]=delta<0 and "left" or "right" end
                    for _=1,to[2] do route[#route+1]="down" end
                    routes[n]=route
                    print(string.format("MK2_AIR_JOIN_CSS frame=%d slot=%d initial=%d target=%d state=%d route=%s writes=0",frame,n,initial,desired,p:read_u16(slots[n].state),table.concat(route,",")))
                end
                screen:snapshot("air_join_css.png")
            end
            if css and not match then
                local age_css=frame-css
                for n=1,2 do
                    for index,direction in ipairs(routes[n]) do pulse(n,direction,age_css,56+(index-1)*12) end
                    if age_css==156 then
                        local desired=n==side and 17 or vid
                        check(p:read_u16(slots[n].id)==desired,"joined selection identity slot "..n)
                        print(string.format("MK2_AIR_JOIN_HIGHLIGHT frame=%d age=%d slot=%d target=%d roster=%d state=%d",frame,age_css,n,desired,p:read_u16(slots[n].id),p:read_u16(slots[n].state)))
                    end
                    pulse(n,"hp",age_css,176,8)
                end
                if age_css==156 then screen:snapshot("air_join_highlight.png") end
                local s,v=sample(side),sample(3-side)
                if p:read_u16(0x010601d0)==2 and owned(s,v) and s.hp==161 and v.hp==161 then
                    match=frame;state("MATCH",s,v);screen:snapshot("air_join_match.png")
                end
            end
            if match then
                local s,v=sample(side),sample(3-side)
                check(owned(s,v) and s.hp>0 and v.hp>0,"joined live identities and health")
                local ma=frame-match
                state("FIELD",s,v)
                if ma>=180 and not jump then
                    if math.abs(s.x-v.x)>63 then
                        local direction=s.x<v.x and "right" or "left"
                        fields[side][direction]:set_value(1);ready=nil
                        print(string.format("MK2_AIR_JOIN_CONTROL frame=%d slot=%d button=%s value=1 writes=0",frame,side,direction))
                    elseif clean(s) and clean(v) then
                        ready=ready or frame
                        if frame-ready>=30 then
                            jump=frame;command=jump+20;state("JUMP",s,v)
                            print(string.format("MK2_AIR_JOIN_COMMAND frame=%d jump=%d side=%d button=block hold=6 gap=%d victim_hp=%d writes=0",command,jump,side,math.abs(s.x-v.x),v.hp))
                        end
                    else ready=nil end
                end
                if jump then
                    pulse(1,"up",frame-jump,0,3);pulse(2,"up",frame-jump,0,3)
                    pulse(side,"block",frame-command,0,6)
                    if frame-jump<=180 then state("STATE",s,v) end
                    if caught and own_recovered and victim_recovered and not complete and clean(s) and clean(v) then
                        complete=true;state("READY",s,v);check(damage==16 and stores==1,"one native sixteen-point throw")
                        screen:snapshot("air_join_ready.png")
                        if followup then
                            follow_epoch=frame+16
                            print(string.format("MK2_AIR_JOIN_FOLLOW_PLAN frame=%d begin=%d side=%d vid=%d walk=0,%d jump=40,3 hp=112,3 block=136,6 settle=160 writes=0",frame,follow_epoch,side,vid,follow_walk))
                        end
                    end
                    for _,offset in ipairs({24,32,40,48,56,64,72,80,96,120}) do
                        if frame-jump==offset then screen:snapshot("air_join_pose_"..offset..".png") end
                    end
                end
                if follow_epoch and frame>=follow_epoch then
                    local fa=frame-follow_epoch
                    for n=1,2 do
                        local me,them=n==side and s or v,n==side and v or s
                        local direction=me.x<them.x and "right" or "left"
                        for _,step in ipairs({{direction,0,follow_walk},{"up",40,3},{"hp",112,3},{"block",136,6}}) do
                            if fa>=step[2] and fa<step[2]+step[3] then
                                fields[n][step[1]]:set_value(1)
                                print(string.format("MK2_AIR_JOIN_FOLLOW_CONTROL frame=%d age=%d slot=%d button=%s value=1 writes=0",frame,fa,n,step[1]))
                            end
                        end
                    end
                    if fa==follow_walk or fa==64 or fa==120 or fa==144 or fa==160 then
                        state("FOLLOW_SAMPLE",s,v);screen:snapshot("air_join_follow_"..fa..".png")
                    end
                    if fa==160 then
                        check(clean(s) and clean(v),"follow-up controls finish with native clean recovery")
                        follow_done=clean(s) and clean(v)
                        print(string.format("MK2_AIR_JOIN_FOLLOW_RESULT frame=%d begin=%d fields=161 pass=%s writes=0",frame,follow_epoch,tostring(follow_done)))
                    end
                end
                if ma==600 then state("FINAL",s,v);screen:snapshot("air_join_final.png");finish();manager.machine:exit() end
            end
            if age>=1800 and not match then check(false,"native join timed out");finish();manager.machine:exit() end
        end,
        finish=finish
    }
end
