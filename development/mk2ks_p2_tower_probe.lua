-- Full native P2 tower. Only explicitly labelled HEALTH assistance is allowed;
-- no actor, identity, position, schedule, stage or action writes are made.
if rawget(_G,"MK2_P2_TOWER_ACTIVE") then
    print("MK2_P2_TOWER_REBOOT_GUARD duplicate_callbacks_prevented=true")
    return
end
rawset(_G,"MK2_P2_TOWER_ACTIVE",true)
assert(os.getenv("MK2_TRACE_LADDER")~="1")
assert(os.getenv("MK2_TRACE_POSITION_ASSIST")~="1")
dofile("mk2ks_finish_range_test.lua")

local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local fighter=assert(os.getenv("MK2KS_P2_FIGHTER"))
local identity=assert(({kano=17,sonya=18})[fighter])
local morph=assert(rawget(_G,"MK2_NATIVE_SHANG_OBSERVER"))
local assist=os.getenv("MK2_P2_TOWER_HEALTH_ASSIST")=="1"
local frame,checks,errors,wins,initial_action=0,0,0,0,false
local stage_wins,stage_seen,stage_start={},{},{}
local campaign_order,last_stage,last_state=nil,nil,nil
local health_writes,regen_writes=0,0
local ending_start,completed=nil,false
local picture_reads,text_reads={0,0},{0,0}
local tap_handles,id_taps={},{}
local last_hud=-1000
local fields={}
local high,low=manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields
for _,label in ipairs({"Up","Down","Left","Right","High Punch","High Kick","Block"}) do
    fields[label]=high["P2 "..label]
end
for _,label in ipairs({"Low Punch","Low Kick","Block 2"}) do fields[label]=low["P2 "..label] end
local function valid(a) return a>=0x01000000 and a<0x01100000 end
local function id(a) return valid(a) and p:read_u16(a+0x1f0) or 0xffff end
local function order()
    local table,schedule=p:read_u32(0xff8a11f0),p:read_u32(0x01061b10)
    if table==0xfffa2c00 then
        for n=0,5 do if p:read_u32(table+n*32)==schedule then return n,schedule end end
    end
    return -1,schedule
end
local function error_at(reason)
    errors=errors+1
    if errors<=12 then print(string.format("MK2_P2_TOWER_ERROR frame=%d reason=%s",frame,reason)) end
end
local action=fighter=="kano" and 0xfffaae00 or 0xfffab200
tap_handles[#tap_handles+1]=p:install_read_tap(action,action+15,"P2 tower initial fatality",function(at)
    if at==action and cpu.A8.value==p:read_u32(0x01060df0) and id(cpu.A8.value)==identity then initial_action=true end
end)
tap_handles[#tap_handles+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,"P2 tower native wins",function(at)
    local a1,a2=p:read_u32(0x01060220),p:read_u32(0x01060df0)
    if at~=0xfffef800+identity*32 or id(a2)~=identity or
        p:read_u16(0x01060e50)~=identity or p:read_u16(0x01060dc0)~=1 or
        p:read_u16(0x01060ec0)<=p:read_u16(0x010602f0) or p:read_u16(0x01061b00)~=2 then return end
    wins=wins+1
    local stage,s1=p:read_u16(0x01061b30),p:read_u16(0x010601f0)
    if s1==0 then stage_wins[stage]=(stage_wins[stage] or 0)+1 end
    local n,schedule=order()
    print(string.format("MK2_P2_TOWER_WIN frame=%d stage=%d order=%d schedule=%08X states=%d,1 cpu=%d:%d human=%d:%d actors=%08X,%08X health=%d,%d wins=%d stage_wins=%d",
        frame,stage,n,schedule,s1,p:read_u16(0x01060280),id(a1),identity,id(a2),a1,a2,
        p:read_u16(0x010602f0),p:read_u16(0x01060ec0),wins,stage_wins[stage] or 0))
end)
tap_handles[#tap_handles+1]=p:install_read_tap(0xfffee000,0xfffee000+19*64-1,"P2 tower CPU HUD",function(at)
    if (at-0xfffee000)%64==0 then last_hud=frame end
end)
local pictures=0xff800000+0xf4900*8
for page=0,1 do
    local entry=pictures+(50+(identity-17)*2+page)*32
    tap_handles[#tap_handles+1]=p:install_read_tap(entry,entry+31,"P2 tower own ending picture",function(at,data)
        if at~=entry or (stage_wins[16] or 0)<1 or p:read_u16(0x01061b30)~=16 or
            p:read_u16(0x01060e50)~=identity then return end
        picture_reads[page+1]=picture_reads[page+1]+1
        print(string.format("MK2_P2_TOWER_PICTURE frame=%d page=%d roster=%d entry=%08X value=%04X pc=%08X",
            frame,page+1,p:read_u16(0x01060e50),at,data&0xffff,cpu.PC.value))
    end)
    local table=0xff800000+(page==0 and 0xf4a00 or 0xf4b00)*8
    tap_handles[#tap_handles+1]=p:install_read_tap(table+identity*3*32,table+(identity*3+3)*32-1,
        "P2 tower own story text",function(at,data)
            if (at-table)%32~=0 or (stage_wins[16] or 0)<1 or p:read_u16(0x01061b30)~=16 or
                p:read_u16(0x01060e50)~=identity then return end
            text_reads[page+1]=text_reads[page+1]+1
            print(string.format("MK2_P2_TOWER_TEXT frame=%d page=%d roster=%d entry=%08X value=%04X pc=%08X",
                frame,page+1,p:read_u16(0x01060e50),at,data&0xffff,cpu.PC.value))
        end)
end

emu.register_frame(function()
    frame=frame+1
    assert(#tap_handles==7,"Retain all native code and ending observer handles")
    if frame==1 then
        print(string.format("MK2_P2_TOWER_BOOT fighter=%s assistance=%s identity_writes=0 position_writes=0 stage_writes=0 schedule_writes=0",
            fighter,assist and "health_only" or "none"))
        for n=0,5 do
            local rom_table=p:read_u32(0xff8a11f0)
            local list=p:read_u32(rom_table+n*32)
            local ids={}
            for stage=0,16 do ids[#ids+1]=p:read_u16(list+stage*16) end
            print(string.format("MK2_P2_TOWER_ROM table=%08X order=%d list=%08X ids=%s",rom_table,n,list,table.concat(ids,",")))
        end
    end
    if frame<3000 or completed then return end
    local mode,s1,s2=p:read_u16(0x010601d0),p:read_u16(0x010601f0),p:read_u16(0x01060dc0)
    local stage,native_winner=p:read_u16(0x01061b30),p:read_u16(0x01061b00)
    local n,schedule=order()
    local expected=n>=0 and stage<=16 and p:read_u16(schedule+stage*16) or 0xffff
    local a1,a2=p:read_u32(0x01060220),p:read_u32(0x01060df0)
    local id1,id2=id(a1),id(a2)
    local r1,r2=p:read_u16(0x01060280),p:read_u16(0x01060e50)
    local h1,h2=p:read_u16(0x010602f0),p:read_u16(0x01060ec0)
    local key=string.format("%d:%d:%d:%d:%d:%d:%08X:%08X:%d:%d",mode,s1,s2,stage,r1,r2,a1,a2,id1,id2)
    if key~=last_state or frame%120==0 then
        print(string.format("MK2_P2_TOWER_STATE frame=%d mode=%d states=%d,%d stage=%d order=%d schedule=%08X expected=%d roster=%d,%d actors=%08X:%d,%08X:%d health=%d,%d winner=%d hud_read=%d",
            frame,mode,s1,s2,stage,n,schedule,expected,r1,r2,a1,id1,a2,id2,h1,h2,native_winner,last_hud))
        last_state=key
    end
    -- A boss round win is not yet the ending. Wait for the actual native
    -- post-boss scene, continuing ordinary inputs through any further round.
    if (stage_wins[16] or 0)>=1 and not ending_start and mode==11 and native_winner==2 and
        h1==0 and h2>0 and r2==identity and a1==0 and a2==0 then
        ending_start=frame
        print(string.format("MK2_P2_TOWER_ENDING_START frame=%d fighter=%s roster=%d health=%d,%d winner=%d",
            frame,fighter,r2,h1,h2,native_winner))
    end
    if ending_start then
        local age=frame-ending_start
        if age==0 or age==120 or age==300 or age==600 or age==900 or age==1200 or
            age==1800 or age==2400 or age==3000 or age==3600 or age==4800 or age==6000 then
            screen:snapshot(string.format("p2_ending_%04d.png",age))
            print(string.format("MK2_P2_TOWER_ENDING_STATE frame=%d age=%d mode=%d roster=%d,%d actors=%08X,%08X winner=%d",frame,age,mode,r1,r2,a1,a2,native_winner))
        end
        if age>1200 and mode==11 and r2~=identity then
            completed=true
            print(string.format("MK2_P2_TOWER_COMPLETED frame=%d ending_age=%d mode=%d roster=%d,%d pictures=%d,%d texts=%d,%d",
                frame,age,mode,r1,r2,picture_reads[1],picture_reads[2],text_reads[1],text_reads[2]))
            -- Restart acceptance needs the genuine completed-campaign latch,
            -- but must continue with all tower assistance/input driving stopped.
            if os.getenv("MK2_P2_POST_ENDING_RESTART")~="1" then manager.machine:exit() end
        end
        return
    end
    if initial_action and wins>=2 and s1==0 and s2==1 and mode==2 and
        valid(a1) and valid(a2) and h1>0 and h2>0 then
        checks=checks+1
        if n<0 or stage>16 or r1~=expected or (id1~=expected and not morph.allowed(a1,expected)) or r2~=identity or id2~=identity then
            error_at("live_ownership")
        end
        if campaign_order and n~=campaign_order then error_at("changed_schedule") end
        campaign_order=campaign_order or n
        if not stage_seen[stage] then
            stage_seen[stage]=true;stage_start[stage]=frame
            if last_stage then
                local skipped=stage==last_stage+2 and p:read_u16(schedule+(last_stage+1)*16)==14
                if (stage~=last_stage+1 and not skipped) or (stage_wins[last_stage] or 0)<2 then error_at("stage_advance_without_wins") end
            elseif stage~=0 then error_at("campaign_did_not_start_at_zero") end
            print(string.format("MK2_P2_TOWER_STAGE frame=%d stage=%d order=%d cpu=%d human=%d previous=%s",frame,stage,n,r1,r2,tostring(last_stage)))
            screen:snapshot(string.format("p2_tower_stage_%02d.png",stage))
            last_stage=stage
        end
        if frame==stage_start[stage]+120 then screen:snapshot(string.format("p2_tower_stage_%02d_age120.png",stage)) end
        if checks<=600 or frame%30==0 then
            print(string.format("MK2_P2_TOWER_LIVE frame=%d stage=%d order=%d schedule=%08X cpu=%d:%d human=%d:%d actors=%08X,%08X health=%d,%d flags=%04X,%04X",
                frame,stage,n,schedule,r1,id1,r2,id2,a1,a2,h1,h2,p:read_u16(a1+0x160),p:read_u16(a2+0x160)))
        end
        if not id_taps[a1] then
            id_taps[a1]=p:install_write_tap(a1+0x1f0,a1+0x1ff,"native CPU morph provenance",function(at,data,mask)
                if p:read_u32(0x01060220)~=a1 or p:read_u16(0x01061b30)~=14 or
                    p:read_u16(0x01060280)~=6 then return end
                print(string.format("MK2_P2_TOWER_ID_WRITE frame=%d actor=%08X old=%d new=%d pc=%08X a0=%08X a1=%08X a8=%08X a13=%08X mask=%04X",
                    frame,a1,p:read_u16(a1+0x1f0),data&0xffff,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,mask))
            end)
        end
        if assist and r1==expected and r2==identity and id2==identity and native_winner==0 then
            if h2<161 then
                regen_writes=regen_writes+1
                print(string.format("MK2_P2_TOWER_HEALTH frame=%d side=2 stage=%d old=%d new=161",frame,stage,h2))
                p:write_u16(0x01060ec0,161)
            end
            if h1==161 then
                health_writes=health_writes+1
                print(string.format("MK2_P2_TOWER_HEALTH frame=%d side=1 stage=%d old=161 new=1",frame,stage))
                p:write_u16(0x010602f0,1)
            end
        end
        if native_winner==0 then
            for _,field in pairs(fields) do field:clear_value() end
            local x1,x2=p:read_u16(a1+0x90),p:read_u16(a2+0x90)
            if math.abs(x1-x2)>65 then fields[x2<x1 and "Right" or "Left"]:set_value(1)
            else fields.Down:set_value(1);if frame%22<4 then fields["High Punch"]:set_value(1) end end
        end
    end
end)
emu.register_stop(function()
    local mandatory=true
    for stage=0,16 do
        if stage~=13 and (not stage_seen[stage] or (stage_wins[stage] or 0)<(stage==16 and 1 or 2)) then mandatory=false end
    end
    print(string.format("MK2_P2_TOWER_RESULT pass=%s fighter=%s checks=%d errors=%d wins=%d initial_action=%s complete=%s mandatory=%s health_writes=%d regen_writes=%d assistance=%s pictures=%d,%d texts=%d,%d scope=full_p2_tower_structure_not_unassisted_clear",
        tostring(checks>=500 and errors==0 and initial_action and completed and mandatory and picture_reads[1]>0 and picture_reads[2]>0 and text_reads[1]>0 and text_reads[2]>0),
        fighter,checks,errors,wins,tostring(initial_action),tostring(completed),tostring(mandatory),health_writes,regen_writes,
        assist and "health_only" or "none",picture_reads[1],picture_reads[2],text_reads[1],text_reads[2]))
end)
