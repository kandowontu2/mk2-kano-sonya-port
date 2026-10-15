-- Real close-move inputs after an actual ending/restart. No memory writes.
-- Native execution owns catch, paired animation, health, fling and recovery.
return function(target,side)
    local identity=assert(({kano=17,sonya=18})[target])
    assert(side==1 or side==2)
    local first=tonumber(os.getenv("MK2KS_RESTART_PAIR_FIRST_COMMAND_AGE") or "60")
    assert(first and first>=0 and first<=140 and first%1==0)
    local spec=target=="kano" and {name="choke",parser=0xfff91000,action=0xfff91400,
        intro=0xfff94000,attack=0xfff94800,release=0xfff93800,pulse=0xfff93400,
        state=0x111,vstate=0x112,total=32,steps=22,calls=4} or
        {name="leg",parser=0xfff80000,action=0xfff80800,intro=0xfff83000,
        attack=0xfff83800,release=0xfff82200,state=0x110,vstate=0x111,total=35,steps=5,calls=1}
    local p=manager.machine.devices[":maincpu"].spaces.program
    local cpu=manager.machine.devices[":maincpu"].state
    local screen=manager.machine.screens[":screen"]
    local players={
        {actor=0x01060220,process=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
        {actor=0x01060df0,process=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
    local own,other=players[side],players[3-side]
    local frame,epoch,cycle,commands,errors=0,nil,0,0,0
    local taps,cycles,captures={},{},{}
    local command,forward,last_try,complete=nil,nil,-1000,false
    local counts={parser=0,action=0,intro=0,attack=0,step=0,pulse=0,damage=0,
        release=0,fling=0,velocity=0,own_recovery=0,victim_recovery=0,health=0,ready=0,miss=0}
    local function valid(v) return v>=0x01000000 and v<0x01100000 end
    local function signed(v) return v>=0x8000 and v-0x10000 or v end
    local function check(ok,label)
        if not ok then errors=errors+1;if errors<=20 then print("MK2_RESTART_PAIR_ERROR "..label) end end
    end
    local function sample(slot)
        local actor,process=p:read_u32(slot.actor),p:read_u32(slot.process)
        if not valid(actor) or not valid(process) then return end
        return {actor=actor,process=process,id=p:read_u16(actor+0x1f0),
            action=p:read_u16(process+0x1f0),x=signed(p:read_u16(actor+0x90)),y=signed(p:read_u16(actor+0xb0)),
            floor=signed(p:read_u16(process+0x200)),vx=p:read_u32(actor+0x40),vy=p:read_u32(actor+0x60),
            flags=p:read_u16(process+0x210),body=p:read_u16(actor+0x160),trail=p:read_u32(process+0x190),
            pose=p:read_u32(actor+0x1d0),health=p:read_u16(slot.hp)}
    end
    local function owned(s,v)
        return s and v and s.id==identity and p:read_u16(own.roster)==identity and p:read_u16(own.state)==1 and
            p:read_u16(other.state)==0 and p:read_u16(other.roster)==v.id
    end
    local function grounded(s)
        return s.y==s.floor and s.vx==0 and s.vy==0 and s.flags&0x1c==0 and s.body&8==0 and s.trail==0
    end
    local function command_ready(s)
        local vx=s.vx>=0x80000000 and s.vx-0x100000000 or s.vx
        return s.y==s.floor and s.vy==0 and math.abs(vx)<=0x28000 and s.flags&0x1c==0 and s.body&8==0 and s.trail==0
    end
    local function victim_ready(v)
        -- The original CPU can walk immediately after FF861350. A real
        -- cleared/grounded walking state is recovery, not a leftover fling.
        local vx=v.vx>=0x80000000 and v.vx-0x100000000 or v.vx
        return v.y==v.floor and v.vy==0 and v.flags&0x1c==0 and v.body&8==0 and v.trail==0 and
            (v.vx==0 or (v.action==0x303 and math.abs(vx)<=0x30000))
    end
    local function state(tag,s,v,extra)
        print(string.format("MK2_RESTART_PAIR_%s frame=%d age=%d cycle=%d side=%d id=%d actor=%08X process=%08X action=%04X x=%d y=%d floor=%d vx=%08X vy=%08X flags=%04X body=%04X trail=%08X pose=%08X health=%d victim=%08X vid=%d vprocess=%08X vaction=%04X vxpos=%d vypos=%d vfloor=%d vvx=%08X vvy=%08X vflags=%04X vbody=%04X vtrail=%08X vpose=%08X vhealth=%d suppression=%d left=%d right=%d %s",
            tag,frame,frame-epoch,cycle,side,identity,s.actor,s.process,s.action,s.x,s.y,s.floor,s.vx,s.vy,s.flags,s.body,s.trail,s.pose,s.health,
            v.actor,v.id,v.process,v.action,v.x,v.y,v.floor,v.vx,v.vy,v.flags,v.body,v.trail,v.pose,v.health,p:read_u16(0x010619d0),
            signed(p:read_u16(0x0105ecf0))+0x3a,signed(p:read_u16(0x0105ed00))+0x15f,extra or "writes=0"))
    end
    local function event(kind,address,s,v,value)
        counts[kind]=counts[kind]+1
        print(string.format("MK2_RESTART_PAIR_EVENT frame=%d age=%d cycle=%d kind=%s side=%d id=%d actor=%08X process=%08X victim=%08X vid=%d vprocess=%08X a8=%08X a13=%08X pc=%08X entry=%08X value=%08X a0=%08X a1=%08X a2=%08X a3=%08X count=%d",
            frame,frame-epoch,cycle,kind,side,identity,s.actor,s.process,v.actor,v.id,v.process,cpu.A8.value,cpu.A13.value,cpu.PC.value,address,value or 0,
            cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,counts[kind]))
    end
    check(p:read_u16(spec.parser)==0x09e0 and p:read_u16(spec.action)==0x09e1 and
        p:read_u16(spec.action+16)==spec.state and p:read_u16(spec.attack)==(target=="kano" and 101 or 115) and
        p:read_u16(spec.release)==0x09e0 and p:read_u16(spec.release+16)==0x506 and
        p:read_u32(spec.intro)==(target=="kano" and 0xfe830420 or 3),"native code/descriptor guards")
    local descriptor={};for n=0,8 do descriptor[#descriptor+1]=p:read_u16(spec.attack+n*16) end
    print(string.format("MK2_RESTART_PAIR_ROM target=%s side=%d move=%s parser=%08X action=%08X intro=%08X attack=%08X release=%08X state=%04X victim_state=%04X damage=%d descriptor=%s writes=0",
        target,side,spec.name,spec.parser,spec.action,spec.intro,spec.attack,spec.release,spec.state,spec.vstate,spec.total,table.concat(descriptor,",")))
    print(string.format("MK2_RESTART_PAIR_PLAN first=%d gap=104 attempts=4 latest=400 cooldown=90 approach=walk_continuous command=grounded_walk_or_idle writes=0",first))
    -- Observe the original parser helpers, not a synthesized input history.
    -- Their actual register arguments show why a real command was rejected.
    for _,address in ipairs({0xff877d80,0xff877450,0xff8771f0,0xff8772f0,0xff877300}) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"native close command gate",function(at)
            if at~=address or not epoch or not command or frame-command>36 or frame-epoch>600 then return end
            local s,v=sample(own),sample(other)
            if not owned(s,v) or cpu.A8.value~=s.actor then return end
            print(string.format("MK2_RESTART_PAIR_GATE frame=%d age=%d side=%d id=%d actor=%08X process=%08X at=%08X a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a7=%08X a13=%08X pc=%08X flags=%04X action=%04X vy=%08X writes=0",
                frame,frame-epoch,side,identity,s.actor,s.process,address,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A4.value,cpu.A7.value,cpu.A13.value,cpu.PC.value,s.flags,s.action,s.vy))
        end)
    end
    local entries={parser=spec.parser,action=spec.action,intro=spec.intro,attack=spec.attack,step=0xfff89400,
        release=spec.release,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,recovery=0xff861350}
    if spec.pulse then entries.pulse=spec.pulse end
    for entry_kind,address in pairs(entries) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"post-restart native pair "..entry_kind,function(at)
            -- Classification belongs to this invocation, not the callback's
            -- persistent loop upvalue: both main processes use this entry.
            local kind=entry_kind
            if at~=address or not epoch or frame-epoch>600 then return end
            local s,v=sample(own),sample(other)
            if not owned(s,v) then return end
            local c=cycles[cycle]
            if kind=="parser" or kind=="action" then
                if cpu.A8.value~=s.actor then return end
                check(valid(cpu.A13.value),"owned parser process")
                if kind=="action" then
                    check(command and frame-command>=1 and frame-command<=36,"actual command before action")
                    check(cpu.A13.value==s.process,"actual own main action process")
                    cycle=cycle+1;c={start=frame,actor=s.actor,process=s.process,victim=v.actor,vprocess=v.process,
                        vid=v.id,steps={},damage=0,stores=0,calls=0,pulses=0,vhealth=v.health,health=s.health,
                        direction=forward=="right" and 1 or -1};cycles[cycle]=c
                    for _,offset in ipairs({4,12,24}) do captures[frame+offset]="action_"..cycle.."_"..offset end
                end
            else
                if not c or c.closed then return end
                check(s.actor==c.actor and s.process==c.process and v.actor==c.victim and v.process==c.vprocess and v.id==c.vid,"stable paired owners")
                if kind=="intro" or kind=="attack" or kind=="step" then
                    if cpu.A8.value~=s.actor then return end
                    check(cpu.A13.value==s.process,"own main executes choreography")
                    if kind=="attack" then c.attack=c.attack or frame end
                    if kind=="step" then
                        if s.action~=spec.state then return end
                        local group=p:read_u32(cpu.A9.value)
                        if group==0 then return end
                        c.steps[#c.steps+1]=frame;c.paired=c.paired or frame
                        captures[frame+1]="step_"..cycle.."_"..#c.steps
                        event(kind,address,s,v,group);return
                    end
                elseif kind=="recovery" then
                    if cpu.A8.value==s.actor and cpu.A13.value==s.process and not c.own_recovery then
                        kind="own_recovery";c.own_recovery=frame
                    elseif cpu.A8.value==v.actor and cpu.A13.value==v.process and c.release and not c.victim_recovery then
                        kind="victim_recovery";c.victim_recovery=frame
                    else return end
                else
                    if not c.paired or cpu.A8.value~=v.actor then return end
                    check(cpu.A13.value==s.process or cpu.A13.value==v.process,"actual victim damage/release context")
                    if kind=="pulse" then c.pulses=c.pulses+1
                    elseif kind=="damage" then
                        if target=="sonya" and not c.release then return end
                        c.calls=c.calls+1;event(kind,address,s,v,cpu.A10.value);return
                    elseif kind=="release" then
                        check(not c.release and cpu.A13.value==v.process,"one actual victim release process")
                        c.release=frame;captures[frame+1]="release_"..cycle
                    elseif kind=="fling" or kind=="velocity" then
                        if not c.release or frame-c.release>1 then return end
                    end
                end
            end
            event(kind,address,s,v)
        end)
    end
    taps[#taps+1]=p:install_write_tap(other.hp,other.hp+15,"observe native paired victim health",function(at,data)
        local c=cycles[cycle]
        if at~=other.hp or not epoch or not c or not c.paired or c.closed or frame-epoch>600 then return end
        local before,after=p:read_u16(other.hp),data&0xffff
        if before==after then return end
        local s,v=sample(own),sample(other)
        check(owned(s,v) and v.actor==c.victim,"native victim health ownership")
        c.damage=c.damage+before-after;c.stores=c.stores+1;counts.health=counts.health+1
        print(string.format("MK2_RESTART_PAIR_HEALTH frame=%d age=%d cycle=%d side=%d id=%d actor=%08X process=%08X victim=%08X vid=%d vprocess=%08X before=%d after=%d a8=%08X a13=%08X pc=%08X count=%d observer_writes=0",
            frame,frame-epoch,cycle,side,identity,s.actor,s.process,v.actor,v.id,v.process,before,after,cpu.A8.value,cpu.A13.value,cpu.PC.value,counts.health))
    end)
    local module={}
    function module.drive(now,match,fields)
        frame=now;epoch=match
        local age=frame-epoch
        for _,key in ipairs({"left","right","up","down","hp","lp","hk","lk","block"}) do fields[key]:set_value(0) end
        local s,v=sample(own),sample(other);check(owned(s,v),"live actual human/CPU owners")
        if not owned(s,v) then return end
        if not complete and (not cycles[cycle] or cycles[cycle].closed) then state("APPROACH",s,v) end
        if captures[frame] then screen:snapshot("restart_pair_"..captures[frame]..".png") end
        local c=cycles[cycle]
        if c and not c.closed then
            state("STATE",s,v)
            if c.own_recovery and grounded(s) then
                if not c.paired then
                    c.closed=true;counts.miss=counts.miss+1
                    state("MISS",s,v,"count="..counts.miss.." writes=0")
                elseif c.release and c.victim_recovery and victim_ready(v) and v.action~=spec.vstate and s.action~=spec.state then
                    check(#c.steps==spec.steps and c.calls==spec.calls and c.stores==spec.calls and c.damage==spec.total and
                        c.vhealth-v.health==spec.total and (target=="sonya" or c.pulses==4),"complete native paired choreography/damage")
                    c.closed=true;c.ready=frame;complete=true;counts.ready=counts.ready+1
                    state("READY",s,v,"damage="..c.damage.." stores="..c.stores.." steps="..#c.steps.." count="..counts.ready.." writes=0")
                    screen:snapshot("restart_pair_ready_"..cycle..".png")
                end
            end
        end
        if complete then fields.block:set_value(1);return end
        if command and frame-command<16 then
            local phase=frame-command
            if target=="kano" then
                if phase<3 then fields.down:set_value(1) end
                if phase>=3 and phase<6 then fields[forward]:set_value(1) end
                if phase>=4 and phase<7 then fields.lp:set_value(1) end
            else
                if phase<7 then fields.down:set_value(1) end
                if phase>=3 and phase<7 then fields.lp:set_value(1);fields.block:set_value(1) end
            end
            return
        end
        if c and not c.closed then
            if c.own_recovery then fields.block:set_value(1) end
            return
        end
        if age>400 or commands>=4 or s.y~=s.floor or s.vy~=0 or s.flags&0x1c~=0 or s.body&8~=0 or s.trail~=0 then
            fields.block:set_value(1);return
        end
        local gap=math.abs(s.x-v.x)
        if age>=first and command_ready(s) and gap<=104 and v.y==v.floor and v.vy==0 and frame-last_try>=90 then
            commands=commands+1;command=frame;last_try=frame
            forward=s.x<v.x and "right" or "left"
            state("COMMAND",s,v,string.format("attempt=%d target=%s move=%s forward=%s gap=%d button=%s writes=0",
                commands,target,spec.name,forward,gap,target=="kano" and "lp" or "lp_block"))
            fields.down:set_value(1)
        elseif gap>104 then
            fields[s.x<v.x and "right" or "left"]:set_value(1)
        -- In range, release walking naturally before testing the zero-velocity
        -- command gate. Guarding here continually re-entered the block parser.
        end
    end
    function module.finish()
        check(commands>=1 and commands<=4 and complete and counts.ready>=1,"complete native paired action after restart")
        print(string.format("MK2_RESTART_PAIR_RESULT pass=%s target=%s side=%d move=%s commands=%d parsers=%d actions=%d intros=%d attacks=%d steps=%d pulses=%d damage_calls=%d releases=%d flings=%d velocities=%d own_recoveries=%d victim_recoveries=%d health_stores=%d ready=%d misses=%d errors=%d writes=0",
            tostring(errors==0),target,side,spec.name,commands,counts.parser,counts.action,counts.intro,counts.attack,counts.step,counts.pulse,counts.damage,
            counts.release,counts.fling,counts.velocity,counts.own_recovery,counts.victim_recovery,counts.health,counts.ready,counts.miss,errors))
        for _,tap in ipairs(taps) do tap:remove() end
        return errors==0
    end
    return module
end
