-- Actual challenger transition after fresh CPU gameplay; no guest memory writes.
-- Attach the existing complete lifecycle observers BEFORE the joined HUD loads.
return function(target,side,options)
    options=options or {}
    assert(options.driver==nil or options.driver=="mobility_contact" or options.driver=="projectile_contact")
    local identity=assert(({kano=17,sonya=18})[target])
    local move=options.driver=="projectile_contact" and (target=="kano" and "knife" or "ring") or
        options.driver and (target=="kano" and "ball" or "square") or (target=="kano" and "blade" or "bicycle")
    local victim=target=="kano" and "sonya" or "kano"
    local vid=target=="kano" and 18 or 17
    local p=manager.machine.devices[":maincpu"].spaces.program
    local screen=manager.machine.screens[":screen"]
    local slots={{id=0x01060280,state=0x010601f0,actor=0x01060220,main=0x01060260,hp=0x010602f0},
        {id=0x01060e50,state=0x01060dc0,actor=0x01060df0,main=0x01060e30,hp=0x01060ec0}}
    local coords={[17]={0,0},[1]={1,0},[0]={2,0},[2]={3,0},[9]={4,0},[18]={5,0},
        [8]={1,1},[6]={2,1},[4]={3,1},[11]={4,1},[5]={1,2},[3]={2,2},[10]={3,2},[7]={4,2}}
    local frame,begin,css,match,attached,completed=0,nil,nil,nil,nil,nil
    local errors,fields,constructing,controls,routes=0,0,0,{},{}
    local taps={}
    local function check(ok,label)
        if not ok then errors=errors+1;if errors<=20 then print("MK2_JOIN_LIFE_ERROR frame="..frame.." "..label) end end
    end
    local function valid(x) return x>=0x01000000 and x<0x01100000 end
    local function clear()
        for _,slot in ipairs(controls) do for _,field in pairs(slot) do field:set_value(0) end end
    end
    local function pulse(n,key,age,first,hold)
        if age>=first and age<first+(hold or 5) then
            controls[n][key]:set_value(1)
            print(string.format("MK2_JOIN_LIFE_CONTROL frame=%d slot=%d button=%s value=1 writes=0",frame,n,key))
        end
    end
    local function state(tag)
        for n,slot in ipairs(slots) do
            local actor,main=p:read_u32(slot.actor),p:read_u32(slot.main)
            local id=valid(actor) and p:read_u16(actor+0x1f0) or 65535
            print(string.format("MK2_JOIN_LIFE_%s frame=%d age=%d slot=%d actor=%08X main=%08X id=%d roster=%d state=%d hp=%d mode=%d writes=0",
                tag,frame,match and frame-match or 0,n,actor,main,id,p:read_u16(slot.id),p:read_u16(slot.state),p:read_u16(slot.hp),p:read_u16(0x010601d0)))
        end
    end
    local function visible_css()
        local pixels,width=screen:pixels();if width~=400 then return false end
        local yellow=0
        for y=0,24,2 do for x=40,360,2 do
            local c=string.unpack("<I4",pixels,(y*width+x)*4+1)
            if (c>>16)&255>175 and (c>>8)&255>140 and c&255<100 then yellow=yellow+1 end
        end end
        return yellow>=400 and yellow<=430
    end
    local function attach()
        attached=frame
        local names={victim,victim};names[side]=target
        local driver=options.driver and "mk2ks_"..options.driver..".lua" or "mk2ks_"..move.."_lifecycle_test.lua"
        assert(loadfile(driver))({native_join=true,side=side,names=names,
            now=function() return frame end,active=function() return match~=nil end,clear_controls=clear,
            complete=function(now,ok)
                completed=now;check(ok,"actual complete native lifecycle")
                check(constructing==(options.driver and 0 or 1),"expected native round reconstruction fields")
                state("COMPLETE");screen:snapshot("join_life_complete.png")
            end})
        print(string.format("MK2_JOIN_LIFE_ATTACH frame=%d move=%s side=%d target=%s victim=%s writes=0",frame,move,side,target,victim))
    end
    for n,slot in ipairs(slots) do
        taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,"whole joined lifecycle health observer",function(at,data)
            if at~=slot.hp or not match then return end
            local before,after=p:read_u16(slot.hp),data&0xffff;if before==after then return end
            local cpu=manager.machine.devices[":maincpu"].state
            print(string.format("MK2_JOIN_LIFE_HEALTH frame=%d age=%d slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X writes=0",
                frame,frame-match,n,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
        end)
    end
    emu.register_stop(function()
        print(string.format("MK2_JOIN_LIFE_RESULT pass=%s target=%s side=%d victim=%s move=%s begin=%s css=%s attached=%s match=%s complete=%s fields=%d errors=%d writes=0",
            tostring(begin~=nil and css~=nil and attached~=nil and match~=nil and completed~=nil and errors==0),target,side,victim,move,
            tostring(begin),tostring(css),tostring(attached),tostring(match),tostring(completed),fields,errors))
        for _,tap in ipairs(taps) do tap:remove() end
    end)
    return {begin=function(now)
        begin=now;frame=now
        local high,low,system=manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields,manager.machine.ioport.ports[":IN1"].fields
        for n=1,2 do
            local label="P"..n.." "
            controls[n]={up=high[label.."Up"],down=high[label.."Down"],left=high[label.."Left"],right=high[label.."Right"],
                hp=high[label.."High Punch"],hk=high[label.."High Kick"],block=high[label.."Block"],lp=low[label.."Low Punch"],lk=low[label.."Low Kick"],
                coin=system["Coin "..n],start=system[n==1 and "1 Player Start" or "2 Players Start"]}
        end
        print(string.format("MK2_JOIN_LIFE_BEGIN frame=%d target=%s side=%d joining=%d victim=%s move=%s mode=%d p1=%d,%d p2=%d,%d writes=0",frame,target,side,3-side,victim,move,p:read_u16(0x010601d0),p:read_u16(slots[1].state),p:read_u16(slots[1].id),p:read_u16(slots[2].state),p:read_u16(slots[2].id)))
    end,drive=function(now)
        assert(begin);frame=now
        if not match then
            clear();local age=frame-begin
            pulse(3-side,"coin",age,10);pulse(3-side,"coin",age,30);pulse(3-side,"start",age,60)
            if not css and p:read_u16(0x010601d0)==4 and visible_css() then
                css=frame
                for n,slot in ipairs(slots) do
                    local initial=p:read_u16(slot.id);local desired=n==side and identity or vid
                    local from,to=assert(coords[initial]),coords[desired];local route={}
                    for _=1,from[2] do route[#route+1]="up" end
                    local delta=to[1]-from[1];for _=1,math.abs(delta) do route[#route+1]=delta<0 and "left" or "right" end
                    for _=1,to[2] do route[#route+1]="down" end
                    routes[n]=route
                    print(string.format("MK2_JOIN_LIFE_CSS frame=%d slot=%d initial=%d target=%d state=%d route=%s writes=0",frame,n,initial,desired,p:read_u16(slot.state),table.concat(route,",")))
                end
                screen:snapshot("join_life_css.png")
            end
            if css then
                local age_css=frame-css
                for n=1,2 do
                    for index,direction in ipairs(routes[n]) do pulse(n,direction,age_css,56+(index-1)*12) end
                    if age_css==156 then
                        local desired=n==side and identity or vid
                        check(p:read_u16(slots[n].id)==desired,"actual joined highlight slot "..n)
                        print(string.format("MK2_JOIN_LIFE_HIGHLIGHT frame=%d age=%d slot=%d target=%d roster=%d state=%d writes=0",frame,age_css,n,desired,p:read_u16(slots[n].id),p:read_u16(slots[n].state)))
                    end
                    pulse(n,"hp",age_css,176,8)
                end
                if age_css==156 then screen:snapshot("join_life_highlight.png");attach() end
                local both=true
                for n,slot in ipairs(slots) do
                    local actor=p:read_u32(slot.actor);local desired=n==side and identity or vid
                    both=both and valid(actor) and p:read_u16(actor+0x1f0)==desired and p:read_u16(slot.id)==desired and p:read_u16(slot.state)==1 and p:read_u16(slot.hp)==161
                end
                if attached and p:read_u16(0x010601d0)==2 and both then
                    match=frame;state("MATCH");screen:snapshot("join_life_match.png")
                end
            end
            if frame-begin>=1800 then check(false,"actual native join timed out");manager.machine:exit() end
        end
        if match then
            fields=fields+1
            local mode=p:read_u16(0x010601d0)
            local rebuilding=mode==6 and p:read_u32(slots[1].actor)==0 and p:read_u32(slots[2].actor)==0
            if rebuilding then constructing=constructing+1 end
            for n,slot in ipairs(slots) do
                local actor=p:read_u32(slot.actor);local desired=n==side and identity or vid
                check((rebuilding or valid(actor) and p:read_u16(actor+0x1f0)==desired) and valid(p:read_u32(slot.main)) and
                    p:read_u16(slot.id)==desired and p:read_u16(slot.state)==1,"whole joined lifecycle identity/controller "..n)
            end
            state("FIELD")
            if frame-match>=5000 and not completed then check(false,"native lifecycle timed out");manager.machine:exit() end
        end
    end}
end
