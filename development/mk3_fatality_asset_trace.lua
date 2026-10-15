-- Diagnostic-only original MK3 finisher capture. Never loaded by mk2ks.
-- Health/position assistance is explicit; the command buttons are inputs.
local fighter = os.getenv("MK3_FATALITY_FIGHTER") or "kano"
assert(fighter == "kano" or fighter == "sonya")
dofile(os.getenv("MK3_FATALITY_SELECTION_SCRIPT") or
    (fighter == "kano" and "mk3_kano_native.lua" or "mk3_sonya_native.lua"))

local frame, round_zeros, finish_frame = 0, 0, nil
local was_alive = false
local health_writes, position_writes = 0, 0
local auto_cheat = os.getenv("MK3_FATALITY_AUTO_CHEAT") == "1"
local input_only = os.getenv("MK3_FATALITY_INPUT_ONLY_APPROACH") == "1"
assert(not input_only or not auto_cheat,"Input validation cannot use automatic fatality cheats")
assert(not input_only or os.getenv("MK3_FATALITY_FORCE_P1_RIGHT")~="1",
       "Input validation cannot force orientation")
local approach_age,command_gap,action_frame,selection_verified
local human_command,held_charge,distance_gate,native_action=false,false,false,false
local cheat_frame = tonumber(os.getenv("MK3_FATALITY_CHEAT_FRAME")) or 3000
local trace_start = tonumber(os.getenv("MK3_FATALITY_TRACE_START") or "2250")
assert(trace_start>=1000)
local cheat_index = tonumber(os.getenv("MK3_FATALITY_CHEAT_INDEX") or "2")
assert(cheat_index==1 or cheat_index==2)
local trace_assets = os.getenv("MK3_FATALITY_ASSET_TRACE") == "1"
local trace_objects = os.getenv("MK3_FATALITY_OBJECT_TRACE") == "1"
local trace_orb = os.getenv("MK3_FATALITY_ORB_TRACE") == "1"
local diagnostic_stage = tonumber(os.getenv("MK3_FATALITY_STAGE") or "")
assert(not diagnostic_stage or diagnostic_stage>=0 and diagnostic_stage<=10)
local space, fields, cpu
local taps, last_pose, last_objects = {}, {}, {}
local victim_palette_seen = false
local delayed_snapshots={}
local victim_geometry_phases={[0xff9b2d10]=0,[0xff9b2db0]=1,[0xff9b2e50]=2,
    [0xff9b2ef0]=3,[0xff9b2f70]=4,[0xff9b2fb0]=5}
local orb_process, orb_entry_count, orb_last_graphic = nil, 0, nil
local function signed(value) return value >= 0x8000 and value - 0x10000 or value end
local function pulse(name, age, first, length)
    if age >= first and age < first + length then fields[name]:set_value(1) end
end
emu.register_frame(function()
    frame = frame + 1
    if frame == 1 then
        cpu = manager.machine.devices[":maincpu"]
        space = cpu.spaces.program
        if input_only and os.getenv("MK3_FATALITY_INPUT_GATE_TRACE")=="1" then
            for _,address in ipairs({0xff982880,0xff992cf0,0xff992d50,0xff993160,0xff9987e0,0xff9b12e0}) do
                taps[#taps+1]=space:install_read_tap(address,address+15,"original skeleton input gate",function(offset)
                    if offset~=address or not finish_frame or frame-finish_frame>200 then return end
                    if cpu.state.A8.value==space:read_u32(0x010609b0) then
                        if address==0xff982880 and cpu.state.A11.value==0xff986380 then human_command=true end
                        if address==0xff992d50 and cpu.state.A1.value>=64 then held_charge=true end
                        local gap=math.abs(space:read_u16(space:read_u32(0x010609b0)+0x90)-
                            space:read_u16(space:read_u32(0x01061560)+0x90))
                        if address==0xff993160 and gap>=32 and gap<=80 then distance_gate=true end
                        if address==0xff9b12e0 then native_action=true end
                    end
                    print(string.format("MK3_FATALITY_INPUT_GATE frame=%d age=%d at=%08X a0=%08X a1=%08X a5=%08X a6=%08X a8=%08X a11=%08X x=%d,%d",
                        frame,frame-finish_frame,address,cpu.state.A0.value,cpu.state.A1.value,
                        cpu.state.A5.value,cpu.state.A6.value,cpu.state.A8.value,cpu.state.A11.value,
                        space:read_u16(space:read_u32(0x010609b0)+0x90),space:read_u16(space:read_u32(0x01061560)+0x90)))
                end)
            end
        end
        if trace_orb and fighter=="sonya" then
            for _,address in ipairs({0xff9af630,0xff9af7a0,0xff9af930,
                0xff9afbb0,0xff9afdc0,0xff9b0100}) do
                taps[#taps+1]=space:install_read_tap(address,address+15,
                    "original Sonya kiss projectile",function(offset)
                        if offset~=address or not finish_frame or frame-finish_frame>245 or
                            orb_entry_count>=35 then return end
                        orb_entry_count=orb_entry_count+1
                        if address==0xff9af930 then orb_process=cpu.state.A8.value end
                        print(string.format("MK3_FATALITY_ORB_CODE age=%d at=%08X pc=%08X a8=%08X a9=%08X a10=%08X a13=%08X",
                            frame-finish_frame,address,cpu.state.PC.value,cpu.state.A8.value,
                            cpu.state.A9.value,cpu.state.A10.value,cpu.state.A13.value))
                    end)
            end
        end
        local high, low = manager.machine.ioport.ports[":IN0"].fields,
            manager.machine.ioport.ports[":IN1"].fields
        fields = {hp=high["P1 High Punch"],lp=low["P1 Low Punch"],
            hk=high["P1 High Kick"],lk=low["P1 Low Kick"],
            block=high["P1 Block"],run=low["P1 Run"],
            left=high["P1 Left"],right=high["P1 Right"],
            up=high["P1 Up"],down=high["P1 Down"]}
        if trace_assets then
            for _,root in ipairs({{0xff823ca0,0xff8244bf,"main"},
                                  {0xff8244c0,0xff824cdf,"special"}}) do
                taps[#taps+1]=space:install_read_tap(root[1],root[2],
                    "original fatality animation root",function(offset)
                        if not finish_frame or frame-finish_frame>300 or offset%32~=0 then return end
                        local side=cpu.state.A8.value==space:read_u32(0x010609b0) and 1 or
                            cpu.state.A8.value==space:read_u32(0x01061560) and 2 or 0
                        if side==0 then return end
                        print(string.format("MK3_FATALITY_ANIM_ROOT fighter=%s frame=%d age=%d side=%d table=%s index=%d",
                            fighter,frame,frame-finish_frame,side,root[3],(offset-root[1])//32))
                    end)
            end
        end
    end
    if diagnostic_stage and frame>=1720 and frame<=3100 then
        space:write_u8(0x01062210,diagnostic_stage)
        if frame==1720 then
            print(string.format("MK3_FATALITY_STAGE_ASSIST stage=%d",diagnostic_stage))
        end
    end
    if frame < trace_start then return end
    if frame == cheat_frame and auto_cheat then
        local api=assert(emu.plugin and emu.plugin.cheat,"MK3 cheat plugin was not loaded")
        local selected
        for index,name in pairs(api.list()) do
            if name=="Select Perm Fatality Type" then selected=api.get(index);break end
        end
        assert(selected,"MK3 automatic fatality cheat was not loaded")
        selected.set_index(cheat_index) -- XML item two is Automatic Fatality (value 1).
        print("MK3_FATALITY_AUTO_CHEAT enabled at frame="..frame.." value="..tostring(selected.get_value()))
    end
    for _,field in pairs(fields) do field:clear_value() end
    local p1,p2 = space:read_u32(0x010609b0),space:read_u32(0x01061560)
    if p1 < 0x01000000 or p1 >= 0x01400000 or
        p2 < 0x01000000 or p2 >= 0x01400000 then return end
    local hp1,hp2=space:read_u16(0x01060a40),space:read_u16(0x010615f0)
    if input_only and not selection_verified then
        print(string.format("MK3_FATALITY_SELECTION frame=%d ids=%d,%d own=%08X victim=%08X",
            frame,space:read_u16(p1+0x1f0),space:read_u16(p2+0x1f0),p1,p2))
        -- Human P1 ownership is proved by the native command record/timer
        -- gate below, not by assuming the meaning of unfamiliar globals.
        manager.machine.video:snapshot()
        local own_id=fighter=="kano" and 0 or 1
        local victim_id=fighter=="kano" and 1 or 0
        if space:read_u16(p1+0x1f0)~=own_id or space:read_u16(p2+0x1f0)~=victim_id then
            manager.machine:exit()
            error("Input reference selection must match the requested attacker")
        end
        selection_verified=true
    end
    local x1,x2=signed(space:read_u16(p1+0x90)),signed(space:read_u16(p2+0x90))
    if hp2 > 0 and hp2 <= 166 then was_alive = true end
    if was_alive and hp2 == 0 then
        round_zeros = round_zeros + 1
        was_alive = false
        print(string.format("MK3_FATALITY_ROUND_ZERO frame=%d count=%d x=%d,%d",frame,round_zeros,x1,x2))
        if round_zeros == 2 then finish_frame = frame end
    end
    if finish_frame then
        local age=frame-finish_frame
        if input_only and age==0 then
            print(string.format("MK3_FATALITY_FINISH_OWNERS frame=%d own=%08X victim=%08X",frame,p1,p2))
        end
        if age==0 and fighter=="kano" and
            os.getenv("MK3_FATALITY_FORCE_P1_RIGHT")=="1" then
            space:write_u16(p1+0x90,x2+125)
            position_writes=position_writes+1
            print(string.format("MK3_FATALITY_ORIENTATION_ASSIST frame=%d p1=%d p2=%d",
                frame,x2+125,x2))
        end
        if trace_orb and fighter=="sonya" and orb_process and
            age>=172 and age<=231 then
            local graphic=space:read_u32(orb_process+0x1a0)
            if graphic~=orb_last_graphic then
                local bank=space:read_u16(orb_process+0x140)&0x7f00
                local colors={}
                for index=0,31 do colors[#colors+1]=string.format("%04X",
                    space:read_u16(0x01880000+(bank+index)*0x10)) end
                print(string.format("MK3_FATALITY_ORB_FRAME age=%d object=%08X x=%d y=%d graphic=%08X pose=%08X bank=%04X size=%d,%d gfx=%08X colors=%s",
                    age,orb_process,signed(space:read_u16(orb_process+0x90)),
                    signed(space:read_u16(orb_process+0xb0)),graphic,
                    space:read_u32(orb_process+0x1d0),bank,
                    space:read_u16(graphic),space:read_u16(graphic+0x10),
                    space:read_u32(graphic+0x80),table.concat(colors,",")))
                orb_last_graphic=graphic
            end
        end
        if trace_orb and fighter=="sonya" and
            (age==200 or age==208 or age==216 or age==224 or age==232 or age==240) then
            if orb_process and orb_process>=0x01000000 and orb_process<0x01100000 then
                print(string.format("MK3_FATALITY_ORB_PROCESS age=%d base=%08X x=%d y=%d pose=%08X graphic=%08X vx=%08X vy=%08X",
                    age,orb_process,signed(space:read_u16(orb_process+0x90)),
                    signed(space:read_u16(orb_process+0xb0)),space:read_u32(orb_process+0x1d0),
                    space:read_u32(orb_process+0x1a0),space:read_u32(orb_process+0x40),
                    space:read_u32(orb_process+0x60)))
            end
            local count=0
            for base=0x01020000,0x01060000,0x10 do
                if base~=p1 and base~=p2 then
                    local pose=space:read_u32(base+0x1d0)
                    if pose>=0xff800000 and pose<0xffe00000 then
                        local id=space:read_u16(base+0x1f0)
                        local x=signed(space:read_u16(base+0x90))
                        local y=signed(space:read_u16(base+0xb0))
                        if id<0x1000 and x>=100 and x<2000 and y>=-100 and y<1000 then
                            count=count+1
                            if count<=160 then
                                print(string.format("MK3_FATALITY_ORB_CANDIDATE age=%d base=%08X id=%04X pose=%08X x=%d y=%d palette=%08X next=%08X",
                                    age,base,id,pose,x,y,space:read_u32(base+0x1a0),space:read_u32(base)))
                            end
                        end
                    end
                end
            end
            print(string.format("MK3_FATALITY_ORB_SCAN age=%d candidates=%d",age,count))
        end
        if input_only and delayed_snapshots[frame] then
            manager.machine.screens[":screen"]:snapshot(string.format("native_contact_phase_%02d.png",delayed_snapshots[frame]))
            delayed_snapshots[frame]=nil
        end
        if trace_assets and age<=(input_only and 450 or 300) then
            for side,actor in ipairs({p1,p2}) do
                local pose=space:read_u32(actor+0x1d0)
                if pose~=last_pose[side] then
                    print(string.format("MK3_FATALITY_POSE fighter=%s frame=%d age=%d side=%d id=%d pose=%08X x=%d y=%d",
                        fighter,frame,age,side,space:read_u16(actor+0x1f0),pose,
                        signed(space:read_u16(actor+0x90)),signed(space:read_u16(actor+0xb0))))
                    if fighter=="kano" and side==2 and not victim_palette_seen and
                        pose>=0xff9b0000 and pose<0xff9c0000 then
                        local bank=space:read_u16(actor+0x140)&0x7f00
                        local colors={}
                        for index=0,63 do colors[#colors+1]=string.format("%04X",
                            space:read_u16(0x01880000+(bank+index)*0x10)) end
                        print(string.format("MK3_FATALITY_VICTIM_COLORS age=%d id=%d pose=%08X bank=%04X colors=%s",
                            age,space:read_u16(actor+0x1f0),pose,bank,table.concat(colors,",")))
                        victim_palette_seen=true
                    end
                    if fighter=="kano" and side==2 and pose==0xff9b29b0 then
                        local bank=space:read_u16(actor+0x140)&0x7f00
                        local colors={}
                        for index=0,31 do colors[#colors+1]=string.format("%04X",
                            space:read_u16(0x01880000+(bank+index)*0x10)) end
                        print(string.format("MK3_FATALITY_KANO_VICTIM_COLORS age=%d bank=%04X colors=%s",
                            age,bank,table.concat(colors,",")))
                    end
                    if side==1 and ((fighter=="kano" and pose>=0xff9b24f0 and pose<=0xff9b2810) or
                       (fighter=="sonya" and pose>=0xff8402c0 and pose<=0xff8407a0)) then
                        action_frame=action_frame or frame
                    end
                    if fighter=="kano" and side==2 and pose==0xff9b3110 then
                        local bank=space:read_u16(actor+0x140)&0x7f00
                        local colors={}
                        for index=0,63 do colors[#colors+1]=string.format("%04X",
                            space:read_u16(0x01880000+(bank+index)*0x10)) end
                        print(string.format("MK3_FATALITY_JAX_VICTIM_COLORS age=%d bank=%04X colors=%s",
                            age,bank,table.concat(colors,",")))
                    end
                    last_pose[side]=pose
                    if input_only and side==2 and victim_geometry_phases[pose]~=nil then
                        delayed_snapshots[frame+3]=victim_geometry_phases[pose]
                    end
                end
            end
        end
        if trace_objects and age<=(input_only and 450 or 360) and (input_only or age%4==0) then
            -- MK3's attached/projectile sprites use the same object layout as
            -- actors. Observe additional live composite-group pointers rather
            -- than inferring fire/skeleton art from the two fighter poses.
            for base=0x01020000,0x01060000,0x10 do
                if base~=p1 and base~=p2 then
                    local pose=space:read_u32(base+0x1d0)
                    if pose>=0xff800000 and pose<0xffe00000 and pose%16==0 then
                        local first=space:read_u32(pose)
                        local width=space:read_u16(pose)
                        local height=space:read_u16(pose+0x10)
                        local single=width>0 and width<=200 and height>0 and height<=200 and
                            space:read_u32(pose+0x40)<0x0a000000
                        local group=first>=0xff800000 and first<0xfff00000
                        local id=space:read_u16(base+0x1f0)
                        local x=signed(space:read_u16(base+0x90))
                        local y=signed(space:read_u16(base+0xb0))
                        if (group or single) and
                            id<0x1000 and x>=100 and x<2000 and y>=-100 and y<1000 and
                            last_objects[base]~=pose then
                            print(string.format("MK3_FATALITY_OBJECT fighter=%s frame=%d age=%d base=%08X id=%04X pose=%08X kind=%s first=%08X x=%d y=%d palette=%08X source=%08X frame_palette=%08X",
                                fighter,frame,age,base,id,pose,group and "group" or "frame",first,x,y,
                                space:read_u32(base+0x1a0),group and space:read_u32(first+0x80) or 0,
                                group and space:read_u32(first+0xe0) or 0))
                            if group and pose>=0xff9b22d0 and pose<=0xff9b2490 then
                                local bank=space:read_u16(base+0x140)&0x7f00
                                local sample={}
                                for index=0,31 do sample[#sample+1]=string.format("%04X",
                                    space:read_u16(0x01880000+(bank+index)*0x10)) end
                                print(string.format("MK3_FATALITY_SKELETON_COLORS age=%d pose=%08X bank=%04X colors=%s",
                                    age,pose,bank,table.concat(sample,",")))
                            end
                            if group and pose>=0xff9b0ae0 and pose<=0xff9b0f20 then
                                local bank=space:read_u16(base+0x140)&0x7f00
                                local sample={}
                                for index=0,15 do sample[#sample+1]=string.format("%04X",
                                    space:read_u16(0x01880000+(bank+index)*0x10)) end
                                print(string.format("MK3_FATALITY_EFFECT_COLORS age=%d pose=%08X bank=%04X first16=%s",
                                    age,pose,bank,table.concat(sample,",")))
                            end
                            if trace_objects and pose == 0xff9b0ae0 then
                                local palette = space:read_u16(base+0x140)&0x7f00
                                local colors = {}
                                for index=0,63 do
                                    colors[#colors+1] = string.format("%04X",space:read_u16(0x01880000+(palette+index)*0x10))
                                end
                                print(string.format("MK3_FATALITY_PALETTE frame=%d bank=%04X p1bank=%04X p2bank=%04X colors=%s",
                                    frame,palette,space:read_u16(p1+0x140)&0x7f00,
                                    space:read_u16(p2+0x140)&0x7f00,
                                    table.concat(colors,",")))
                                local nonzero, first = 0, {}
                                for at=0,0x7ffff,0x10 do
                                    local value=space:read_u16(0x01880000+at)
                                    if value~=0 then
                                        nonzero=nonzero+1
                                        if #first<40 then first[#first+1]=string.format("%05X:%04X",at,value) end
                                    end
                                end
                                print(string.format("MK3_FATALITY_PALETTE_SCAN nonzero=%d first=%s",
                                    nonzero,table.concat(first,",")))
                            end
                            last_objects[base]=pose
                        end
                    end
                end
            end
        end
        local forward=x1<x2 and "right" or "left"
        local back=forward=="right" and "left" or "right"
        if fighter=="kano" and not input_only and (age==60 or age==94) then
            space:write_u16(p1+0x90,x2+(x1<x2 and -25 or 25))
            position_writes=position_writes+1
            print(string.format("MK3_FATALITY_CLOSE_ASSIST frame=%d old=%d target=%d",frame,x1,x2))
        end
        if input_only and not approach_age and age>=35 and math.abs(x1-x2)<=65 then
            approach_age=age
            command_gap=math.abs(x1-x2)
            print(string.format("MK3_FATALITY_INPUT_APPROACH frame=%d age=%d gap=%d",frame,age,command_gap))
        end
        -- Release the walking direction before the command's first Forward.
        -- Continuing the same held direction creates no new history edge.
        local command_age=input_only and (approach_age and age-approach_age or -1) or age
        if auto_cheat then
            -- Let the original MK3 program choose the action; this is an
            -- asset-discovery diagnostic, not input validation.
        elseif fighter=="kano" then
            if input_only then
                -- Skeleton pull, not the LP/Block/Block/HK eye-laser command.
                -- Hold LP during recovery/movement, F,D,D,F, then release it.
                -- Establish Block before charging LP, and never walk with a
                -- held LP that can turn into a normal punch at close range.
                if approach_age and command_age<90 then fields.block:set_value(1) end
                if command_age>=10 and command_age<90 then fields.lp:set_value(1) end
                if not approach_age and age>=35 then fields[forward]:set_value(1) end
                pulse(forward,command_age,50,4)
                pulse("down",command_age,60,4)
                pulse("down",command_age,70,4)
                pulse(forward,command_age,80,4)
            else
                pulse("lp",age,65,4)
                pulse("block",age,75,4)
                pulse("block",age,85,4)
                pulse("hk",age,95,4)
            end
        else
            if input_only and not approach_age then fields[forward]:set_value(1) end
            pulse(back,command_age,65,4)
            pulse(forward,command_age,75,4)
            pulse("down",command_age,85,4)
            pulse("down",command_age,95,4)
            pulse("run",command_age,105,4)
        end
        if age % 20 == 0 and age <= 360 then
            print(string.format("MK3_FATALITY_FINISH frame=%d age=%d hp=%d,%d x=%d,%d",
                frame,age,hp1,hp2,x1,x2))
            if input_only then
                print(string.format("MK3_FATALITY_INPUT_STATE age=%d in0=%04X in1=%04X timer=%d lp_stamp=%d finish=%d history=%08X",
                    age,manager.machine.ioport.ports[":IN0"]:read(),
                    manager.machine.ioport.ports[":IN1"]:read(),space:read_u16(0x0105d800),
                    space:read_u16(0x01062430),space:read_u16(0x01062250),space:read_u32(0x01060d50)))
            end
            manager.machine.video:snapshot()
        end
        if age > 400 then manager.machine:exit() end
        return
    end
    if hp2 > 1 and hp2 <= 166 then
        space:write_u16(0x010615f0,1)
        health_writes=health_writes+1
    end
    if hp1 > 0 and hp1 < 166 then
        space:write_u16(0x01060a40,166)
        health_writes=health_writes+1
    end
    if hp2 > 0 and hp2 <= 166 then
        if not input_only and math.abs(x1-x2)>65 and frame % 30 == 0 then
            space:write_u16(p1+0x90,x2+(x1<x2 and -45 or 45))
            position_writes=position_writes+1
        end
        if input_only and math.abs(x1-x2)>65 then
            fields[x1<x2 and "right" or "left"]:set_value(1)
        else
            -- Standing HK avoids a direction-history special move that can
            -- push the final-round victim far away before the charge window.
            if frame % 30 < 4 then fields.hk:set_value(1) end
        end
    end
    if frame % 300 == 0 then
        print(string.format("MK3_FATALITY_STATE frame=%d p1=%d p2=%d hp=%d,%d zeros=%d health_writes=%d position_writes=%d",
            frame,space:read_u16(p1+0x1f0),space:read_u16(p2+0x1f0),hp1,hp2,
            round_zeros,health_writes,position_writes))
        manager.machine.video:snapshot()
    end
end)
emu.register_stop(function()
    if not input_only then return end
    local passed=selection_verified and human_command and held_charge and distance_gate and native_action and
        action_frame~=nil and command_gap~=nil and position_writes==0 and not auto_cheat
    print(string.format("MK3_FATALITY_INPUT_OWNERSHIP human_command=%s held_charge=%s distance_gate=%s native_action=%s",
        tostring(human_command),tostring(held_charge),tostring(distance_gate),tostring(native_action)))
    print(string.format("MK3_FATALITY_INPUT_RESULT pass=%s fighter=%s round_health_writes=%d position_writes=%d auto_cheat=%s action_frame=%s command_gap=%s",
        tostring(passed),fighter,health_writes,position_writes,tostring(auto_cheat),tostring(action_frame),tostring(command_gap)))
end)
