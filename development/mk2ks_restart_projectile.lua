-- Opt-in ordinary-input test. Observe the actual owned native pipeline,
-- never write actor/health/action/history/position/stage memory.
return function(target,side)
    local ids={kano=17,sonya=18}
    local identity=assert(ids[target])
    assert(side==1 or side==2)
    local first_age=tonumber(os.getenv("MK2KS_RESTART_FIRST_COMMAND_AGE") or "0")
    assert(first_age and first_age>=0 and first_age<=140 and first_age%1==0)
    local p=manager.machine.devices[":maincpu"].spaces.program
    local cpu=manager.machine.devices[":maincpu"].state
    local screen=manager.machine.screens[":screen"]
    local human=side==1 and {actor=0x01060220,roster=0x01060280,state=0x010601f0,process=0x01060260} or
        {actor=0x01060df0,roster=0x01060e50,state=0x01060dc0,process=0x01060e30}
    local other=side==1 and 0x01060df0 or 0x01060220
    local parser=target=="kano" and 0xffffac00 or 0xffffae00
    local action=target=="kano" and 0xffffb000 or 0xffffb400
    local animation=(target=="kano" and 0xff000000 or 0xff020000)+39*32
    local frame,epoch,errors,commands=0,nil,0,0
    local counts={parser=0,action=0,animation=0}
    local taps,captures={},{}
    local last_command,last_action,direction=nil,nil,nil
    local flags_observed=false
    local function valid(a) return a>=0x01000000 and a<0x01100000 end
    local function check(value,label)
        if not value then errors=errors+1;if errors<=10 then print("MK2_RESTART_PROJECTILE_ERROR "..label) end end
    end
    local first,mask=p:read_u16(parser),p:read_u16(parser+16)
    local opcode=p:read_u16(action)
    check(first==0x09c0 and mask==(target=="kano" and 0x63 or 0x72) and opcode==0x574a,"native code guard")
    print(string.format("MK2_RESTART_PROJECTILE_ROM target=%s side=%d parser=%08X first=%04X mask=%04X action=%08X opcode=%04X animation=%08X writes=0",
        target,side,parser,first,mask,action,opcode,animation))
    print(string.format("MK2_RESTART_PROJECTILE_PLAN first=%d interval=160 commands=3 writes=0",first_age))
    for kind,address in pairs({parser=parser,action=action,animation=animation}) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"post-restart owned "..kind,function(at)
            if at~=address or not epoch then return end
            local own=p:read_u32(human.actor)
            if not valid(own) or cpu.A8.value~=own then return end
            if kind=="animation" and (not last_action or frame-last_action>40) then return end
            local process=p:read_u32(human.process)
            local owned=p:read_u16(own+0x1f0)==identity and p:read_u16(human.roster)==identity and
                p:read_u16(human.state)==1 and valid(process) and valid(cpu.A13.value)
            check(owned,"native "..kind.." human ownership")
            if not owned then return end
            if kind=="action" then
                check(last_command and frame-last_command>=6 and frame-last_command<=36,"action follows actual command")
                last_action=frame
                if counts.action==0 then captures[frame+8]="08";captures[frame+16]="16" end
            end
            counts[kind]=counts[kind]+1
            print(string.format("MK2_RESTART_PROJECTILE_EVENT frame=%d age=%d kind=%s side=%d id=%d actor=%08X process=%08X a13=%08X pc=%08X entry=%08X count=%d",
                frame,frame-epoch,kind,side,identity,own,process,cpu.A13.value,cpu.PC.value,address,counts[kind]))
        end)
    end
    for _,address in ipairs({0xff8775d0,0xff877420,0xff8771f0,0xff877270,0xff8772f0}) do
        taps[#taps+1]=p:install_read_tap(address,address+15,"ordinary projectile gate diagnostic",function(at)
            if at~=address or not epoch or not last_command or frame-last_command>36 then return end
            local own=p:read_u32(human.actor)
            if not valid(own) or cpu.A8.value~=own then return end
            local process=p:read_u32(human.process)
            print(string.format("MK2_PROJECTILE_GATE frame=%d age=%d at=%08X a0=%08X a1=%08X a4=%08X a7=%08X a13=%08X pc=%08X action=%04X process_flags=%04X vy=%08X",
                frame,frame-epoch,address,cpu.A0.value,cpu.A1.value,cpu.A4.value,cpu.A7.value,cpu.A13.value,cpu.PC.value,
                valid(process) and p:read_u16(process+0x1f0) or 0xffff,
                valid(process) and p:read_u16(process+0x210) or 0xffff,p:read_u32(own+0x60)))
        end)
    end
    local result={}
    function result.drive(now,match,fields)
        frame=now;epoch=match
        if not flags_observed then
            local own,process=p:read_u32(human.actor),p:read_u32(human.process)
            if valid(own) and valid(process) then
                flags_observed=true
                print(string.format("MK2_PROJECTILE_INITIAL_STATE frame=%d side=%d id=%d actor=%08X process=%08X flags=%04X action=%04X writes=0",
                    frame,side,identity,own,process,p:read_u16(process+0x210),p:read_u16(process+0x1f0)))
                -- Observe the GAME's writes, never return a replacement value.
                taps[#taps+1]=p:install_write_tap(process+0x210,process+0x21f,"native human action flag lifecycle",function(at,data,mask)
                    if at~=process+0x210 or frame-epoch>600 then return end
                    local before=p:read_u16(at)
                    local after=((before&(~mask))|(data&mask))&0xffff
                    if before==after then return end
                    print(string.format("MK2_PROJECTILE_NATIVE_FLAGS frame=%d age=%d side=%d actor=%08X process=%08X pc=%08X before=%04X after=%04X mask=%04X action=%04X writer=native_game",
                        frame,frame-epoch,side,own,process,cpu.PC.value,before,after,mask&0xffff,p:read_u16(process+0x1f0)))
                end)
            end
        end
        if captures[frame] then screen:snapshot("restart_projectile_"..captures[frame]..".png") end
        local age=frame-epoch
        -- Start as soon as the actual live match is observed, before the CPU
        -- closes into repeated hit/block reactions (P2 can be struck by age 29).
        -- Later attempts still exercise normal gating under live CPU pressure.
        if age<first_age or age>=first_age+340 then return end
        local phase=(age-first_age)%160
        fields.block:clear_value()
        if phase>=20 then fields.block:set_value(1) end
        if phase==0 then
            commands=commands+1;last_command=frame
            local own,victim=p:read_u32(human.actor),p:read_u32(other)
            check(valid(own) and valid(victim),"actual command actors")
            if valid(own) and valid(victim) then
                local forward=p:read_u16(own+0x90)<p:read_u16(victim+0x90) and "right" or "left"
                direction=target=="sonya" and forward or (forward=="right" and "left" or "right")
                print(string.format("MK2_RESTART_PROJECTILE_COMMAND frame=%d age=%d side=%d target=%s direction=%s button=%s writes=0",
                    frame,age,side,target,direction,target=="kano" and "hp" or "lp"))
            end
        end
        if phase<3 then fields.down:set_value(1) end
        -- Ordinary Down, neutral, then horizontal + punch, within the native
        -- 36-field history window. The game's action-ready gate stays intact.
        if direction and phase>=10 and phase<14 then fields[direction]:set_value(1) end
        if phase>=12 and phase<16 then fields[target=="kano" and "hp" or "lp"]:set_value(1) end
        if phase==12 then
            local own,process=p:read_u32(human.actor),p:read_u32(human.process)
            if valid(own) and valid(process) then
                print(string.format("MK2_PROJECTILE_COMMAND_STATE frame=%d age=%d action=%04X y=%d floor=%d flags=%04X input=%04X process_flags=%04X vy=%08X",
                    frame,age,p:read_u16(process+0x1f0),p:read_u16(own+0xb0),p:read_u16(process+0x200),p:read_u16(own+0x160),p:read_u16(0x01600000),
                    p:read_u16(process+0x210),p:read_u32(own+0x60)))
            end
        end
    end
    function result.finish()
        check(epoch and commands==3 and counts.parser>0 and counts.action>0 and counts.animation>0,"complete actual native pipeline")
        print(string.format("MK2_RESTART_PROJECTILE_RESULT pass=%s target=%s side=%d commands=%d parsers=%d actions=%d animations=%d errors=%d writes=0",
            tostring(errors==0),target,side,commands,counts.parser,counts.action,counts.animation,errors))
        for _,tap in ipairs(taps) do tap:remove() end
        return errors==0
    end
    return result
end
