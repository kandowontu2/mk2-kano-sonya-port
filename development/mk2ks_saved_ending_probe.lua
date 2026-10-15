-- Replay an uninterrupted Sonya stage-16 save with the same diagnostic fight
-- assistance, then identify the first invalid-code trap in the ending path.
local origin=tonumber(os.getenv("MK2KS_SAVED_GLOBAL_FRAME") or "0")
local frame,program,cpu,fields=0,nil,nil,nil
local last_health_write=85967
local health_writes,regen_writes=0,0
local first_trap=nil
local completed=false
local trap_tap=nil
local scene_tap=nil
local scene_word_tap=nil
local scene_field_tap=nil
local ending_script_tap=nil
local ending_script_write_tap=nil
local ending_coop_tap=nil
local spare_tap=nil
local task_slot_tap=nil
local spare_read_tap=nil
local spare_reads=0
local task_slot_writes={}
local trace_path=os.getenv("MK2KS_SAVED_TRACE_PATH")
local trace_started=false

local function dump_registers(label)
    local regs={}
    for _,bank in ipairs({"A","B"}) do
        for i=0,15 do
            local reg=cpu.state[bank..i]
            if reg then regs[#regs+1]=string.format("%s%d=%08X",bank,i,reg.value) end
        end
    end
    print(string.format("MK2KS_SAVED_ENDING_%s frame=%d global=%d pc=%08X sp=%08X %s",
        label,frame,origin+frame,cpu.state.PC.value,cpu.state.SP.value,
        table.concat(regs," ")))
end

emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"]
        program=cpu.spaces.program
        local port=manager.machine.ioport.ports[":IN0"].fields
        fields={left=port["P1 Left"],right=port["P1 Right"],
            down=port["P1 Down"],hp=port["P1 High Punch"]}
        trap_tap=program:install_read_tap(0xffa1e700,0xffa1e8ff,
            "late-ending bad code",function(offset,data,mask)
                if first_trap then return end
                first_trap=frame
                print(string.format("MK2KS_SAVED_ENDING_TRAP_FETCH frame=%d address=%08X data=%08X",
                    frame,offset,data))
                dump_registers("TRAP")
            end)
        scene_tap=program:install_read_tap(0xff9f88c0,0xff9f88ef,
            "late-ending scene callback",function(offset,data,mask)
                if frame<3000 or frame>3200 then return end
                local task=cpu.state.A13.value
                local scene=program:read_u16(task+0x310)
                local slot=0xff9f7cf0+scene*32
                local record=program:read_u32(slot)
                print(string.format("MK2KS_SAVED_ENDING_SCENE frame=%d pc=%08X task=%08X scene=%04X slot=%08X record=%08X a0=%08X a1=%08X entry0=%08X entry1=%08X entry2=%08X entry3=%08X",
                    frame,cpu.state.PC.value,task,scene,slot,record,
                    cpu.state.A0.value,cpu.state.A1.value,
                    program:read_u32(record),program:read_u32(record+32),
                    program:read_u32(record+64),program:read_u32(record+96)))
            end)
        scene_word_tap=program:install_write_tap(0x0106ad70,0x0106ad7f,
            "late-ending scene index",function(offset,data,mask)
                print(string.format("MK2KS_SAVED_ENDING_SCENE_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X mode=%d a12=%08X a13=%08X b6=%08X",
                    frame,cpu.state.PC.value,offset,data,mask,
                    program:read_u16(0x010601d0),cpu.state.A12.value,
                    cpu.state.A13.value,cpu.state.B6.value))
            end)
        scene_field_tap=program:install_write_tap(0x0106acd0,0x0106acdf,
            "ending scene slot",function(offset,data,mask)
                if frame>=3000 and frame<=3200 then
                    print(string.format("MK2KS_SAVED_ENDING_SCENE_FIELD_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X a12=%08X b6=%08X",
                        frame,cpu.state.PC.value,offset,data,mask,cpu.state.A12.value,cpu.state.B6.value))
                end
            end)
        ending_script_tap=program:install_read_tap(0x0106ad50,0x0106ad5f,
            "ending text script pointer",function(offset,data,mask)
                if frame>=3000 and frame<=3200 then
                    print(string.format("MK2KS_SAVED_ENDING_SCRIPT_READ frame=%d pc=%08X offset=%08X data=%08X mask=%08X",
                        frame,cpu.state.PC.value,offset,data,mask))
                end
            end)
        ending_script_write_tap=program:install_write_tap(0x0106ad50,0x0106ad5f,
            "ending saved callback pointer",function(offset,data,mask)
                if frame<=3200 then
                    print(string.format("MK2KS_SAVED_ENDING_SCRIPT_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X a9=%08X a12=%08X",
                        frame,cpu.state.PC.value,offset,data,mask,cpu.state.A9.value,
                        cpu.state.A12.value))
                end
            end)
        ending_coop_tap=program:install_read_tap(0xffa2ea80,0xffa2eaaf,
            "ending cooperative register restore",function(offset,data,mask)
                if frame>=3000 and frame<=3200 then
                    print(string.format("MK2KS_SAVED_ENDING_COOP frame=%d pc=%08X a8=%08X a12=%08X a1=%08X a5=%08X a9=%08X a10=%08X a11=%08X slot2f0=%08X",
                        frame,cpu.state.PC.value,cpu.state.A8.value,cpu.state.A12.value,
                        cpu.state.A1.value,cpu.state.A5.value,cpu.state.A9.value,
                        cpu.state.A10.value,cpu.state.A11.value,
                        program:read_u32(0x0106ad50)))
                end
            end)
        spare_tap=program:install_write_tap(0x0106acf0,0x0106acff,
            "candidate ending task slot",function(offset,data,mask)
                print(string.format("MK2KS_SAVED_ENDING_SPARE_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X",
                    frame,cpu.state.PC.value,offset,data,mask))
            end)
        task_slot_tap=program:install_write_tap(0x0106ab60,0x0106ad6f,
            "late-ending task field census",function(offset,data,mask)
                local key=string.format("%03X",offset-0x0106aa60)
                local event=task_slot_writes[key]
                if not event then
                    event={count=0,pc=string.format("%08X",cpu.state.PC.value)}
                    task_slot_writes[key]=event
                end
                event.count=event.count+1
            end)
        spare_read_tap=program:install_read_tap(0x0106acd0,0x0106acef,
            "candidate scene-index slot reads",function(offset,data,mask)
                spare_reads=spare_reads+1
                if spare_reads<=12 then
                    local scene=data & 0xffff
                    local slot=0xff9f7cf0+scene*32
                    local record=program:read_u32(slot)
                    print(string.format("MK2KS_SAVED_ENDING_SPARE_READ frame=%d pc=%08X offset=%08X data=%08X slot=%08X record=%08X entries=%08X,%08X,%08X,%08X",
                        frame,cpu.state.PC.value,offset,data,slot,record,
                        program:read_u32(record),program:read_u32(record+32),
                        program:read_u32(record+64),program:read_u32(record+96)))
                end
            end)
    end
    for _,field in pairs(fields) do field:set_value(0) end
    local stage=program:read_u16(0x01061b30)
    local roster=program:read_u16(0x01060280)
    local p1,p2=program:read_u32(0x01060220),program:read_u32(0x01060df0)
    local live=p1>=0x01000000 and p1<0x01100000 and
        p2>=0x01000000 and p2<0x01100000
    local mode=program:read_u16(0x010601d0)
    local hp1,hp2=program:read_u16(0x010602f0),program:read_u16(0x01060ec0)
    if first_trap and os.getenv("MK2KS_SAVED_STOP_ON_TRAP")=="1" then
        manager.machine:exit()
    end
    if not completed and stage==16 and mode==11 and roster~=18 then
        completed=true
        print(string.format("MK2KS_SAVED_ENDING_COMPLETED frame=%d global=%d p1=%d",
            frame,origin+frame,roster))
        if os.getenv("MK2KS_SAVED_STOP_ON_COMPLETE")=="1" then
            manager.machine:exit()
        end
    end
    if trace_path and not trace_started and frame==2750 then
        assert(manager.machine.debugger,"CPU tracing requires -debug")
        manager.machine.debugger.visible_cpu=cpu
        manager.machine.debugger:command("trace "..trace_path..",maincpu")
        manager.machine.debugger.execution_state="run"
        trace_started=true
        print("MK2KS_SAVED_ENDING_TRACE_STARTED frame=2750")
    elseif trace_started and first_trap and frame>first_trap then
        manager.machine.debugger:command("trace off,maincpu")
        trace_started=false
        print(string.format("MK2KS_SAVED_ENDING_TRACE_STOPPED frame=%d",frame))
    end
    if frame==1 or frame%120==0 or first_trap==frame then
        print(string.format("MK2KS_SAVED_ENDING_STATE frame=%d global=%d stage=%d mode=%d roster=%d cpu=%d live=%s hp=%d,%d pc=%08X",
            frame,origin+frame,stage,mode,roster,program:read_u16(0x01060e50),
            tostring(live),hp1,hp2,cpu.state.PC.value))
        if frame==1 or frame%300==0 then
            print(string.format("MK2KS_SAVED_ENDING_INDEX frame=%d value=%04X spare=%04X task_next=%08X",
                frame,program:read_u16(0x0106ad70),program:read_u16(0x0106acf0),
                program:read_u32(0x0106aa60+0x140)))
        end
        if mode==11 and frame%300==0 then manager.machine.video:snapshot() end
    end
    if frame==1 then
        for _,base in ipairs({0xff8446e0,0xff844880}) do
            for address=base,base+0x60,0x10 do
                print(string.format("MK2KS_SAVED_ENDING_ROM_WORD address=%08X word=%04X",
                    address,program:read_u16(address)))
            end
        end
    end
    if stage~=16 or roster~=18 or not live or first_trap then return end
    if hp1>0 and hp1<161 then
        program:write_u16(0x010602f0,161)
        regen_writes=regen_writes+1
    end
    if hp2==161 and origin+frame-last_health_write>250 then
        program:write_u16(0x01060ec0,1)
        health_writes=health_writes+1
        last_health_write=origin+frame
        print(string.format("MK2KS_SAVED_ENDING_HEALTH frame=%d global=%d",
            frame,origin+frame))
    end
    if hp1==0 or hp2==0 then return end
    local x1,x2=program:read_u16(p1+0x90),program:read_u16(p2+0x90)
    if x1>=0x8000 then x1=x1-0x10000 end
    if x2>=0x8000 then x2=x2-0x10000 end
    if math.abs(x1-x2)>85 then fields[x1<x2 and "right" or "left"]:set_value(1)
    else
        fields.down:set_value(1)
        if (origin+frame-1548)%50<4 then fields.hp:set_value(1) end
    end
end)

emu.register_stop(function()
    print(string.format("MK2KS_SAVED_ENDING_RESULT frames=%d trap=%s completed=%s health_writes=%d regen_writes=%d last_stage=%d",
        frame,tostring(first_trap),tostring(completed),health_writes,regen_writes,
        program and program:read_u16(0x01061b30) or 0xffff))
    if trap_tap then trap_tap:remove() end
    if scene_tap then scene_tap:remove() end
    if scene_word_tap then scene_word_tap:remove() end
    if scene_field_tap then scene_field_tap:remove() end
    if ending_script_tap then ending_script_tap:remove() end
    if ending_script_write_tap then ending_script_write_tap:remove() end
    if ending_coop_tap then ending_coop_tap:remove() end
    if spare_tap then spare_tap:remove() end
    if task_slot_tap then task_slot_tap:remove() end
    if spare_read_tap then spare_read_tap:remove() end
    print(string.format("MK2KS_SAVED_ENDING_SPARE_READ_RESULT reads=%d",spare_reads))
    local keys={}
    for key in pairs(task_slot_writes) do keys[#keys+1]=key end
    table.sort(keys)
    for _,key in ipairs(keys) do
        print(string.format("MK2KS_SAVED_ENDING_TASK_SLOT offset=%s count=%d first_pc=%s",
            key,task_slot_writes[key].count,task_slot_writes[key].pc))
    end
end)
