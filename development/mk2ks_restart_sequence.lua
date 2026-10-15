-- Ordinary-input blade/bicycle observation in an actual post-ending match.
-- All memory access is read-only; the native game owns action/effect/recovery.
return function(target,side)
    local id=assert(({kano=17,sonya=18})[target])
    assert(side==1 or side==2)
    local first_age=tonumber(os.getenv("MK2KS_RESTART_SEQUENCE_FIRST_COMMAND_AGE") or "0")
    assert(first_age and first_age>=0 and first_age<=140 and first_age%1==0)
    local spec=target=="kano" and {name="blade",parser=0xfff8c800,action=0xfff8cc00,
        intro=0xfff8e800,attack=0xfff8e400,effect=0xfff8d800,step=0xfff8e000,state=0x117} or
        {name="bicycle",parser=0xfff9a000,action=0xfff9a400,intro=0xfff9e800,
        loop=0xfff9eb00,attack=0xfff9ee00,state=0x204}
    local p=manager.machine.devices[":maincpu"].spaces.program
    local cpu=manager.machine.devices[":maincpu"].state
    local screen=manager.machine.screens[":screen"]
    local ptrs={
        {actor=0x01060220,process=0x01060260,roster=0x01060280,state=0x010601f0},
        {actor=0x01060df0,process=0x01060e30,roster=0x01060e50,state=0x01060dc0}}
    local own,other=ptrs[side],ptrs[3-side]
    local frame,epoch,cycle,commands,errors=0,nil,0,0,0
    local taps,cycles,captures={},{},{}
    local counts={parser=0,action=0,intro=0,loop=0,attack=0,effect=0,step=0,recovery=0,ready=0}
    local last_command,forward,back=nil,nil,nil
    local function valid(v) return v>=0x01000000 and v<0x01100000 end
    local function check(ok,label)
        if not ok then errors=errors+1;if errors<=10 then print("MK2_RESTART_SEQUENCE_ERROR "..label) end end
    end
    local function signed(v) return v>=0x8000 and v-0x10000 or v end
    local function sample()
        local actor,process=p:read_u32(own.actor),p:read_u32(own.process)
        local victim,vproc=p:read_u32(other.actor),p:read_u32(other.process)
        if not valid(actor) or not valid(process) or not valid(victim) or not valid(vproc) then return end
        return {actor=actor,process=process,id=p:read_u16(actor+0x1f0),action=p:read_u16(process+0x1f0),
            y=signed(p:read_u16(actor+0xb0)),floor=signed(p:read_u16(process+0x200)),
            vx=p:read_u32(actor+0x40),vy=p:read_u32(actor+0x60),flags=p:read_u16(process+0x210),
            body=p:read_u16(actor+0x160),trail=p:read_u32(process+0x190),
            victim=victim,vproc=vproc,vid=p:read_u16(victim+0x1f0),vaction=p:read_u16(vproc+0x1f0)}
    end
    local function owned(s) return s and s.id==id and p:read_u16(own.roster)==id and p:read_u16(own.state)==1 end
    check(p:read_u16(spec.parser)==0x09e0 and p:read_u16(spec.action)==0x09e1 and
        p:read_u16(spec.action+16)==spec.state and p:read_u32(spec.intro)==6 and
        p:read_u16(spec.attack)==(target=="kano" and 109 or 54),"native parser/action/script/descriptor guards")
    print(string.format("MK2_RESTART_SEQUENCE_ROM target=%s side=%d move=%s parser=%08X action=%08X intro=%08X attack=%08X state=%04X writes=0",
        target,side,spec.name,spec.parser,spec.action,spec.intro,spec.attack,spec.state))
    print(string.format("MK2_RESTART_SEQUENCE_PLAN first=%d interval=180 commands=3 writes=0",first_age))
    local entries={parser=spec.parser,action=spec.action,intro=spec.intro,attack=spec.attack,recovery=0xff861350}
    if target=="kano" then entries.effect=spec.effect;entries.step=spec.step else entries.loop=spec.loop end
    for kind,address in pairs(entries) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"post-restart owned sequence "..kind,function(at)
            if at~=address or not epoch or frame-epoch>600 then return end
            local s=sample()
            if not s or cpu.A8.value~=s.actor then return end
            if kind~="parser" and kind~="action" and (cycle==0 or cycles[cycle].ready) then return end
            if kind=="recovery" and (not cycles[cycle].attack or cycles[cycle].recovery) then return end
            check(owned(s) and valid(cpu.A13.value),"native owned "..kind)
            if not owned(s) or not valid(cpu.A13.value) then return end
            if kind~="parser" then check(cpu.A13.value==s.process,"main process executes "..kind) end
            if kind=="action" then
                check(last_command and frame-last_command>=1 and frame-last_command<=36,"real command before action")
                cycle=cycle+1;cycles[cycle]={start=frame}
                for _,offset in ipairs({4,12,24}) do captures[frame+offset]="action_"..cycle.."_"..offset end
            elseif kind=="attack" then cycles[cycle].attack=frame
            elseif kind=="recovery" then cycles[cycle].recovery=frame end
            counts[kind]=counts[kind]+1
            print(string.format("MK2_RESTART_SEQUENCE_EVENT frame=%d age=%d kind=%s cycle=%d side=%d id=%d actor=%08X process=%08X a13=%08X pc=%08X entry=%08X count=%d",
                frame,frame-epoch,kind,cycle,side,id,s.actor,s.process,cpu.A13.value,cpu.PC.value,address,counts[kind]))
        end)
    end
    local module={}
    function module.drive(now,match,fields)
        frame=now;epoch=match
        local age=frame-epoch
        local s=sample();check(owned(s),"live owned sequence actor")
        if not owned(s) then return end
        if captures[frame] then screen:snapshot("restart_sequence_"..captures[frame]..".png") end
        if cycle>0 and not cycles[cycle].ready then
            local c=cycles[cycle]
            if age%4==0 then
                print(string.format("MK2_RESTART_SEQUENCE_STATE frame=%d age=%d cycle=%d side=%d id=%d actor=%08X process=%08X action=%04X y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X trail=%08X victim=%08X vid=%d vprocess=%08X vaction=%04X",
                    frame,age,cycle,side,id,s.actor,s.process,s.action,s.y,s.floor,s.vx,s.vy,s.flags,s.body,s.trail,s.victim,s.vid,s.vproc,s.vaction))
            end
            if c.recovery and s.y==s.floor and s.vx==0 and s.vy==0 and s.flags&0x1c==0 and s.body&8==0 and s.trail==0 and
                s.action~=spec.state and s.action~=0x618 and s.action~=0x611 and s.action~=0x214 then
                c.ready=frame;counts.ready=counts.ready+1
                screen:snapshot("restart_sequence_ready_"..cycle..".png")
                print(string.format("MK2_RESTART_SEQUENCE_READY frame=%d age=%d cycle=%d side=%d id=%d actor=%08X process=%08X y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X trail=%08X count=%d writes=0",
                    frame,age,cycle,side,id,s.actor,s.process,s.y,s.floor,s.vx,s.vy,s.flags,s.body,s.trail,counts.ready))
            end
        end
        local relative=age-first_age
        if relative<0 then fields.block:set_value(1)
        elseif relative<390 then
            local phase=relative%180
            fields.block:clear_value();if phase>=24 then fields.block:set_value(1) end
            if phase==0 then
                commands=commands+1;last_command=frame
                forward=p:read_u16(s.actor+0x90)<p:read_u16(s.victim+0x90) and "right" or "left"
                back=forward=="right" and "left" or "right"
                print(string.format("MK2_RESTART_SEQUENCE_COMMAND frame=%d age=%d side=%d target=%s move=%s forward=%s back=%s button=%s writes=0",
                    frame,age,side,target,spec.name,forward,back,target=="kano" and "hp" or "hk"))
            end
            if target=="kano" then
                if phase<3 then fields.down:set_value(1) end
                if phase>=5 and phase<8 then fields[forward]:set_value(1) end
                if phase>=6 and phase<9 then fields.hp:set_value(1) end
            else
                if phase<3 or (phase>=6 and phase<9) then fields[back]:set_value(1) end
                if phase>=12 and phase<15 then fields.down:set_value(1) end
                if phase>=13 and phase<16 then fields.hk:set_value(1) end
            end
        end
    end
    function module.finish()
        check(commands==3,"three real input command attempts")
        check(counts.parser>0 and counts.action>0 and counts.intro>0 and counts.attack>0 and counts.recovery>0 and counts.ready>0 and
            (target=="kano" and counts.effect>0 and counts.step>0 or target=="sonya" and counts.loop>0),"complete owned sequence pipeline")
        print(string.format("MK2_RESTART_SEQUENCE_RESULT pass=%s target=%s side=%d move=%s commands=%d parsers=%d actions=%d intros=%d loops=%d attacks=%d effects=%d steps=%d recoveries=%d ready=%d errors=%d writes=0",
            tostring(errors==0),target,side,spec.name,commands,counts.parser,counts.action,counts.intro,counts.loop,counts.attack,counts.effect,counts.step,counts.recovery,counts.ready,errors))
        for _,tap in ipairs(taps) do tap:remove() end
        return errors==0
    end
    return module
end
