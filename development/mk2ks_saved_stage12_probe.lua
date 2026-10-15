-- Read a MAME state from the late native ladder, replay normal P1 inputs,
-- and label the health assistance separately from gameplay code.
local origin=tonumber(os.getenv("MK2KS_SAVED_GLOBAL_FRAME") or "0")
local frame,program,fields=0,nil,nil
local resets,health_writes,regen_writes=0,0,0
local last_health_write=-1000
local last_stage=nil
local trace_path=os.getenv("MK2KS_SAVED_TRACE_PATH")
local trace_started=false
local roster_tap,copy_tap,copy_count=nil,nil,0

emu.register_frame(function()
    frame=frame+1
    if not program then
        program=manager.machine.devices[":maincpu"].spaces.program
        local high=manager.machine.ioport.ports[":IN0"].fields
        fields={left=high["P1 Left"],right=high["P1 Right"],
            down=high["P1 Down"],hp=high["P1 High Punch"]}
        local cpu=manager.machine.devices[":maincpu"]
        roster_tap=program:install_write_tap(0x01060e50,0x01060e5f,
            "saved-stage roster clobber",function(offset,data,mask)
                print(string.format("MK2KS_SAVED_ROSTER_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X a0=%08X a1=%08X a5=%08X a8=%08X a9=%08X a13=%08X",
                    frame,cpu.state.PC.value,offset,data,mask,cpu.state.A0.value,
                    cpu.state.A1.value,cpu.state.A5.value,cpu.state.A8.value,
                    cpu.state.A9.value,cpu.state.A13.value))
            end)
        copy_tap=program:install_read_tap(0xff838790,0xff83879f,
            "saved-stage animation-copy entry",function(offset,data,mask)
                if frame<17 or copy_count>=30 then return end
                copy_count=copy_count+1
                print(string.format("MK2KS_SAVED_COPY_ENTRY frame=%d pc=%08X a0=%08X a1=%08X a8=%08X a9=%08X a13=%08X actor=%d root=%08X",
                    frame,cpu.state.PC.value,cpu.state.A0.value,cpu.state.A1.value,
                    cpu.state.A8.value,cpu.state.A9.value,cpu.state.A13.value,
                    program:read_u16(cpu.state.A8.value+0x1f0),
                    program:read_u32(cpu.state.A8.value+0x1d0)))
            end)
    end
    for _,field in pairs(fields) do field:set_value(0) end
    local stage=program:read_u16(0x01061b30)
    local roster=program:read_u16(0x01060280)
    local p1=program:read_u32(0x01060220)
    local p2=program:read_u32(0x01060df0)
    local live=p1>=0x01000000 and p1<0x01100000 and
        p2>=0x01000000 and p2<0x01100000
    if trace_path and not trace_started and frame==17 then
        local debugger=manager.machine.debugger
        assert(debugger,"CPU tracing requires -debug")
        debugger.visible_cpu=manager.machine.devices[":maincpu"]
        debugger:command("trace "..trace_path..",maincpu")
        debugger.execution_state="run"
        trace_started=true
        print("MK2KS_SAVED_TRACE_STARTED frame=17")
    end
    if last_stage==12 and stage~=12 then
        resets=resets+1
        if trace_started then manager.machine.debugger:command("trace off,maincpu") end
        print(string.format("MK2KS_SAVED_STAGE_EXIT frame=%d old=12 new=%d roster=%d",frame,stage,roster))
    end
    last_stage=stage
    if frame==5 or frame%60==0 then
        local pc=manager.machine.devices[":maincpu"].state.PC.value
        print(string.format("MK2KS_SAVED_STAGE_STATE frame=%d stage=%d roster=%d cpu=%d live=%s hp=%d,%d pc=%08X",
            frame,stage,roster,program:read_u16(0x01060e50),tostring(live),
            program:read_u16(0x010602f0),program:read_u16(0x01060ec0),pc))
    end
    if frame==5 then
        for id=0,18 do
            print(string.format("MK2KS_SAVED_REACTION_PARAM id=%d value=%04X",
                id,program:read_u16(0xff892d60+id*16)))
        end
    end
    if stage~=12 or (roster~=17 and roster~=18) or not live then return end
    local health=program:read_u16(0x010602f0)
    if health>0 and health<161 then
        program:write_u16(0x010602f0,161)
        regen_writes=regen_writes+1
    end
    if program:read_u16(0x01060ec0)==161 and frame-last_health_write>250 then
        program:write_u16(0x01060ec0,1)
        health_writes=health_writes+1
        last_health_write=frame
    end
    local x1,x2=program:read_u16(p1+0x90),program:read_u16(p2+0x90)
    if x1>=0x8000 then x1=x1-0x10000 end
    if x2>=0x8000 then x2=x2-0x10000 end
    if math.abs(x1-x2)>85 then
        fields[x1<x2 and "right" or "left"]:set_value(1)
    else
        fields.down:set_value(1)
        local phase=(origin+frame-1548)%50
        if phase<4 then fields.hp:set_value(1) end
    end
end)

emu.register_stop(function()
    print(string.format("MK2KS_SAVED_STAGE_RESULT frames=%d resets=%d health_writes=%d regen_writes=%d last_stage=%s",
        frame,resets,health_writes,regen_writes,tostring(last_stage)))
    if roster_tap then roster_tap:remove() end
    if copy_tap then copy_tap:remove() end
end)
