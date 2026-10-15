-- Input-only cannonball/square-wave test after the real restart observer.
-- Read taps observe native code; no game state, position or history writes.
return function(target,side)
    local identity=assert(({kano=17,sonya=18})[target])
    assert(side==1 or side==2)
    local charge_strategy=os.getenv("MK2KS_RESTART_CHARGE_STRATEGY") or "guard"
    assert(charge_strategy=="guard" or charge_strategy=="retreat")
    local spec=target=="kano" and {name="ball",parser=0xffffdb00,action=0xffffde00,attack=0xffffec00,animation=0xff0000e0,state=0x20b} or
        {name="square",parser=0xffffc800,action=0xffffca00,attack=0xffffda00,animation=0xff0203c0,state=0x207}
    local p=manager.machine.devices[":maincpu"].spaces.program
    local cpu=manager.machine.devices[":maincpu"].state
    local screen=manager.machine.screens[":screen"]
    local ownp=side==1 and {actor=0x01060220,process=0x01060260,roster=0x01060280,state=0x010601f0} or
        {actor=0x01060df0,process=0x01060e30,roster=0x01060e50,state=0x01060dc0}
    local other=side==1 and 0x01060df0 or 0x01060220
    local frame,epoch,errors,commands=0,nil,0,0
    local taps,captures,cycles={},{},{}
    local counts={parser=0,action=0,animation=0,attack=0,recovery=0,ready=0}
    local cycle,last_command,charged,released,back,forward=0,nil,nil,nil,nil,nil
    local function valid(v) return v>=0x01000000 and v<0x01100000 end
    local function check(ok,label)
        if not ok then errors=errors+1;if errors<=10 then print("MK2_RESTART_MOBILITY_ERROR "..label) end end
    end
    local function sample()
        local actor,process=p:read_u32(ownp.actor),p:read_u32(ownp.process)
        if not valid(actor) or not valid(process) then return end
        return {actor=actor,process=process,id=p:read_u16(actor+0x1f0),
            action=p:read_u16(process+0x1f0),flags=p:read_u16(process+0x210),body=p:read_u16(actor+0x160),
            y=p:read_u16(actor+0xb0),floor=p:read_u16(process+0x200),
            vx=p:read_u32(actor+0x40),vy=p:read_u32(actor+0x60),trail=p:read_u32(process+0x190)}
    end
    local function owned(s) return s and s.id==identity and p:read_u16(ownp.roster)==identity and p:read_u16(ownp.state)==1 end
    check(p:read_u16(spec.parser)==(target=="kano" and 0x09e0 or 0x09c0) and
        p:read_u16(spec.action)==0x09e1 and p:read_u16(spec.action+16)==spec.state and
        p:read_u16(spec.attack)==(target=="kano" and 57 or 70),"native code/descriptor guards")
    print(string.format("MK2_RESTART_MOBILITY_ROM target=%s side=%d move=%s parser=%08X action=%08X attack=%08X animation=%08X state=%04X writes=0",
        target,side,spec.name,spec.parser,spec.action,spec.attack,spec.animation,spec.state))
    for kind,address in pairs({parser=spec.parser,action=spec.action,animation=spec.animation,attack=spec.attack,recovery=0xff861350}) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"restart owned mobility "..kind,function(at)
            if at~=address or not epoch then return end
            local s=sample()
            if not s or cpu.A8.value~=s.actor then return end
            if kind~="parser" and kind~="action" and (cycle==0 or frame-epoch>600) then return end
            if kind=="recovery" and (not cycles[cycle].attack or cycles[cycle].recovery) then return end
            check(owned(s) and valid(cpu.A13.value),"native owned "..kind)
            if not owned(s) or not valid(cpu.A13.value) then return end
            if kind~="parser" then check(cpu.A13.value==s.process,"main process executes "..kind) end
            if kind=="action" then
                check(last_command and frame-last_command>=1 and frame-last_command<=36,"actual command precedes action")
                cycle=cycle+1;cycles[cycle]={start=frame}
                captures[frame+12]="action_"..cycle.."_12";captures[frame+24]="action_"..cycle.."_24"
            elseif kind=="attack" then cycles[cycle].attack=true
            elseif kind=="animation" then cycles[cycle].animation=true
            elseif kind=="recovery" then cycles[cycle].recovery=frame end
            counts[kind]=counts[kind]+1
            print(string.format("MK2_RESTART_MOBILITY_EVENT frame=%d age=%d kind=%s cycle=%d side=%d id=%d actor=%08X process=%08X a13=%08X pc=%08X entry=%08X count=%d",
                frame,frame-epoch,kind,cycle,side,identity,s.actor,s.process,cpu.A13.value,cpu.PC.value,address,counts[kind]))
        end)
    end
    if target=="kano" then
        taps[#taps+1]=p:install_read_tap(0xffffdb60,0xffffdb6f,"native LK elapsed charge",function(at)
            local s=sample()
            if at~=0xffffdb60 or not epoch or not released or not s or cpu.A8.value~=s.actor then return end
            print(string.format("MK2_RESTART_MOBILITY_ELAPSED frame=%d age=%d side=%d actor=%08X ticks=%d pc=%08X",frame,frame-epoch,side,s.actor,cpu.A1.value,cpu.PC.value))
        end)
    end
    local result={}
    function result.drive(now,match,fields)
        frame=now;epoch=match
        local age=frame-epoch
        local s=sample();check(owned(s),"live mobility actor")
        if not owned(s) then return end
        if captures[frame] then screen:snapshot("restart_mobility_"..captures[frame]..".png") end
        if cycle>0 then
            local c=cycles[cycle]
            if (s.action==spec.state or s.action==0x602) and (frame-c.start)%4==0 then
                print(string.format("MK2_RESTART_MOBILITY_PHYSICS frame=%d age=%d cycle=%d side=%d id=%d actor=%08X action=%04X y=%d floor=%d vx=%08X vy=%08X body=%04X",
                    frame,age,cycle,side,identity,s.actor,s.action,s.y,s.floor,s.vx,s.vy,s.body))
            end
            if not c.ready and age%8==0 then
                print(string.format("MK2_RESTART_MOBILITY_CYCLE_STATE frame=%d age=%d cycle=%d action=%04X y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X",
                    frame,age,cycle,s.action,s.y,s.floor,s.vx,s.vy,s.flags,s.body))
            end
            if c.recovery and not c.ready and c.animation and s.y==s.floor and s.vx==0 and s.vy==0 and
                s.flags&0x1c==0 and s.body&8==0 and s.trail==0 and s.action~=spec.state and s.action~=0x602 then
                c.ready=frame;counts.ready=counts.ready+1
                screen:snapshot("restart_mobility_ready_"..cycle..".png")
                print(string.format("MK2_RESTART_MOBILITY_READY frame=%d age=%d cycle=%d side=%d id=%d actor=%08X process=%08X y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X trail=%08X count=%d writes=0",
                    frame,age,cycle,side,identity,s.actor,s.process,s.y,s.floor,s.vx,s.vy,s.flags,s.body,s.trail,counts.ready))
            end
        end
        if target=="kano" then
            fields.lk:clear_value()
            if not charged then
                charged=frame
                print(string.format("MK2_RESTART_MOBILITY_PRESS frame=%d age=%d side=%d target=kano button=lk writes=0 strategy=%s",frame,age,side,charge_strategy))
            end
            if not released and frame-charged>=81 and s.flags&0x1c==0 and s.y==s.floor and s.vy==0 then
                released=frame;last_command=frame;commands=commands+1
                print(string.format("MK2_RESTART_MOBILITY_RELEASE frame=%d age=%d side=%d target=kano button=lk hold=%d writes=0",frame,age,side,frame-charged))
            end
            if not released then
                fields.lk:set_value(1)
                if charge_strategy=="guard" then fields.block:set_value(1)
                else
                    fields.block:clear_value()
                    local victim=p:read_u32(other)
                    if valid(victim) then fields[p:read_u16(s.actor+0x90)<p:read_u16(victim+0x90) and "left" or "right"]:set_value(1) end
                end
            elseif frame-released<20 then fields.block:clear_value()
            else fields.block:set_value(1) end
        elseif age<340 then
            local phase=age%160
            fields.block:clear_value();if phase>=20 then fields.block:set_value(1) end
            if phase==0 then
                commands=commands+1;last_command=frame
                local victim=p:read_u32(other);check(valid(victim),"square command victim")
                if valid(victim) then
                    forward=p:read_u16(s.actor+0x90)<p:read_u16(victim+0x90) and "right" or "left"
                    back=forward=="right" and "left" or "right"
                    print(string.format("MK2_RESTART_MOBILITY_COMMAND frame=%d age=%d side=%d target=sonya first=%s second=%s button=hp writes=0",frame,age,side,forward,back))
                end
            end
            if forward and phase<3 then fields[forward]:set_value(1) end
            if back and phase>=5 and phase<8 then fields[back]:set_value(1) end
            if phase>=6 and phase<9 then fields.hp:set_value(1) end
        end
    end
    function result.finish()
        check(commands==(target=="kano" and 1 or 3),"complete real commands")
        check(counts.parser>0 and counts.action>0 and counts.animation>0 and counts.attack>0 and counts.recovery>0 and counts.ready>0,"complete owned movement and recovery")
        print(string.format("MK2_RESTART_MOBILITY_RESULT pass=%s target=%s side=%d move=%s commands=%d parsers=%d actions=%d animations=%d attacks=%d recoveries=%d ready=%d errors=%d writes=0",
            tostring(errors==0),target,side,spec.name,commands,counts.parser,counts.action,counts.animation,counts.attack,counts.recovery,counts.ready,errors))
        for _,tap in ipairs(taps) do tap:remove() end
        return errors==0
    end
    return result
end
