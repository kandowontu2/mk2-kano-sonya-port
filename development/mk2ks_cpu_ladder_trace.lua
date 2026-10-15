-- Observe native one-player opponent selection and AI. Optional diagnostic
-- ID injection is one RAM write before opponent construction, never a port fix.
dofile("mk2ks_selector_exit_test.lua")
local frame,program,cpu=0,nil,nil
local last_roster,last_actor,last_action=nil,nil,nil
local changes,ai_actions,write_events=0,0,0
local seen={}
local tap
local diagnostic_id=tonumber(os.getenv("MK2KS_DIAGNOSTIC_CPU_ID") or "")
-- Diagnostic-only injection can also exercise MKII's three hidden fighter
-- IDs. The game payload and its ordinary ladder remain untouched.
assert(not diagnostic_id or diagnostic_id==8 or diagnostic_id==14 or diagnostic_id==15 or
    diagnostic_id==16 or diagnostic_id==17 or diagnostic_id==18)
local diagnostic_written,diagnostic_injection_stage=false,nil
local diagnostic_ladder_index=tonumber(os.getenv("MK2KS_DIAGNOSTIC_LADDER_INDEX") or "")
assert(not diagnostic_ladder_index or diagnostic_ladder_index>=0 and diagnostic_ladder_index<=16)
local diagnostic_ladder_written=false
local diagnostic_all_stages=os.getenv("MK2KS_DIAGNOSTIC_ALL_STAGES")=="1"
assert(not diagnostic_all_stages or not diagnostic_ladder_index)
local diagnostic_cpu_health=tonumber(os.getenv("MK2KS_DIAGNOSTIC_CPU_HEALTH") or "")
assert(not diagnostic_cpu_health or (diagnostic_ladder_index or diagnostic_all_stages) and
    diagnostic_cpu_health>=1 and diagnostic_cpu_health<=160)
local diagnostic_health_writes,last_diagnostic_health_frame=0,-1000
local diagnostic_p1_regen=os.getenv("MK2KS_DIAGNOSTIC_P1_REGEN")=="1"
local diagnostic_p1_regen_writes=0
local special_tap,special_reads=nil,0
local ai_owned_action_taps,ai_owned_action_counts={}, {[17]=0,[18]=0}
local ai_variety_counts={knife=0,ball=0,blade=0,ring=0,square=0,bicycle=0,leg=0,choke=0}
local ai_router_entries=0
local ai_owned_capture_frames={}
local ai_close_tap,ai_close_other_tap,ai_close_counts,ai_close_events=nil,nil,{},0
local ai_close_capture_frames,ai_close_near_entries,ai_close_last_capture={},0,-1000
local progress_tap,progress_wins,progress_initial=nil,0,false
local progress_stage_wins,progress_stage1_seen={},false
local progress_ids={kano=17,sonya=18,liu_kang=1}
local progress_fighter=assert(progress_ids[os.getenv("MK2KS_TEST_FIGHTER")],
    "Choose a supported ladder probe fighter")
local progress_check_frame=tonumber(os.getenv("MK2KS_PROGRESS_CHECK_FRAME") or "3800")
local second_progress_check_frame=tonumber(os.getenv("MK2KS_SECOND_PROGRESS_CHECK_FRAME") or "5900")
local multi_min_stage=tonumber(os.getenv("MK2KS_ASSERT_MULTI_PROGRESS_MIN_STAGE") or "")
local multi_check_frame=tonumber(os.getenv("MK2KS_MULTI_CHECK_FRAME") or "")
local multi_snap_stage=tonumber(os.getenv("MK2KS_MULTI_SNAP_MIN_STAGE") or "")
local multi_last_stage,multi_transition_frame=nil,nil
local multi_stage_errors,multi_identity_checks,multi_identity_errors=0,0,0
local multi_campaign_ended=false
local multi_campaign_completed=false
local camera_tap,camera_writes=nil,0
local palette_tap,palette_trace_count=nil,0
local freeze_code_tap,freeze_code_reads=nil,0
local kano_ai_tap,kano_ai_reads=nil,0
local ai_trace_start=tonumber(os.getenv("MK2KS_AI_TRACE_START") or "")
local ai_trace_end=tonumber(os.getenv("MK2KS_AI_TRACE_END") or "")
local reset_trace_start=tonumber(os.getenv("MK2KS_RESET_TRACE_START") or "")
local reset_trace_end=tonumber(os.getenv("MK2KS_RESET_TRACE_END") or "")
local reset_trace_stage=tonumber(os.getenv("MK2KS_RESET_TRACE_STAGE") or "")
local reset_trace_stage_age=tonumber(os.getenv("MK2KS_RESET_TRACE_STAGE_AGE") or "2100")
local cpu_trace_stage=tonumber(os.getenv("MK2KS_CPU_TRACE_STAGE") or "")
local cpu_trace_age=tonumber(os.getenv("MK2KS_CPU_TRACE_AGE") or "1400")
local cpu_trace_path=os.getenv("MK2KS_CPU_TRACE_PATH")
local cpu_trace_started=false
local ending_trace_all=os.getenv("MK2KS_ENDING_TRACE_ALL")=="1"
local ending_start=nil
local ending_stack_trace=os.getenv("MK2KS_ENDING_STACK_TRACE")=="1"
local ending_stack_tap,ending_coop_tap,ending_stack_writes=nil,nil,0
local save_stage=tonumber(os.getenv("MK2KS_SAVE_STAGE") or "")
local save_state_path=os.getenv("MK2KS_SAVE_STATE_PATH")
assert(not save_stage or save_state_path and save_state_path~="")
local save_requested=false
local ladder_dma_tap,ladder_dma_regs,ladder_dma_seen=nil,{},{}
local stage_palette_tap,stage_palette_reads=nil,0
local watchdog_tap,watchdog_stage_writes,last_watchdog_stage_frame=nil,0,nil
local stage_visual_snapshots=os.getenv("MK2KS_STAGE_VISUAL_SNAPSHOTS")=="1"
local stage_visual_seen={}
local stage_visual_ready={}
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"]
        program=cpu.spaces.program
        tap=program:install_write_tap(0x01060e50,0x01060e5f,"one-player opponent selection",function(offset,data,mask)
            if frame<900 or write_events>=32 then return end
            write_events=write_events+1
            print(string.format("MK2KS_CPU_ROSTER_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X",
                frame,cpu.state.PC.value,offset,data,mask))
        end)
        if ending_stack_trace then
            ending_stack_tap=program:install_write_tap(0x01060000,0x010bffff,
                "ending task and stack writes",function(offset,data,mask)
                    local pc=cpu.state.PC.value
                    if ending_stack_writes>=40 or
                        (pc~=0xff844710 and pc~=0xff904910) or
                        program:read_u16(0x01061b30)~=16 then return end
                    ending_stack_writes=ending_stack_writes+1
                    print(string.format("MK2KS_ENDING_STACK_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X a12=%08X a13=%08X b6=%08X",
                        frame,pc,offset,data,mask,cpu.state.A12.value,
                        cpu.state.A13.value,cpu.state.B6.value))
                end)
            ending_coop_tap=program:install_read_tap(0xffa2ea80,0xffa2eaaf,
                "ending cooperative restore",function(offset,data,mask)
                    if program:read_u16(0x01061b30)~=16 then return end
                    local pc=cpu.state.PC.value
                    if pc==0xffa2ea90 or pc==0xffa2eab0 then
                        print(string.format("MK2KS_ENDING_COOP frame=%d pc=%08X a8=%08X a1=%08X a12=%08X slot2f0=%08X",
                            frame,pc,cpu.state.A8.value,cpu.state.A1.value,
                            cpu.state.A12.value,program:read_u32(0x0106ad50)))
                    end
                end)
        end
        special_tap=program:install_read_tap(0xfffa26c0,0xfffa26ff,"added CPU specials",function(offset,data,mask)
            special_reads=special_reads+1
            if special_reads<=50 then
                print(string.format("MK2KS_CPU_SPECIAL frame=%d pc=%08X address=%08X value=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X",
                    frame,cpu.state.PC.value,offset,data,cpu.state.A0.value,cpu.state.A1.value,
                    cpu.state.A2.value,cpu.state.A8.value,cpu.state.A13.value))
            end
        end)
        if os.getenv("MK2KS_TRACE_CPU_OWNED_SPECIALS") == "1" then
            for id,address in pairs({[17]=0xffffb000,[18]=0xffffb400}) do
                ai_owned_action_taps[#ai_owned_action_taps+1]=program:install_read_tap(
                    address,address+15,"CPU-owned special action",function(offset,data,mask)
                        if offset~=address then return end
                        local owner=program:read_u32(cpu.state.A13.value+0xc0)
                        local opponent=program:read_u32(0x01060df0)
                        if owner~=opponent or owner<0x01000000 or owner>=0x01100000 or
                            program:read_u16(owner+0x1f0)~=id then return end
                        ai_owned_action_counts[id]=ai_owned_action_counts[id]+1
                        if ai_owned_action_counts[id]<=6 then
                            ai_owned_capture_frames[frame+12]=id
                            ai_owned_capture_frames[frame+24]=id
                        end
                        if ai_owned_action_counts[id]<=20 then
                            print(string.format("MK2KS_CPU_OWNED_SPECIAL frame=%d id=%d entry=%08X owner=%08X stage=%d",
                                frame,id,address,owner,program:read_u16(0x01061b30)))
                        end
                    end)
            end
        end
        if os.getenv("MK2KS_TRACE_AI_VARIETY") == "1" then
            ai_owned_action_taps[#ai_owned_action_taps+1]=program:install_read_tap(
                0xfffbc000,0xfffbc20f,"CPU move router context",function(offset,data,mask)
                    if offset~=0xfffbc000 and offset~=0xfffbc200 then return end
                    local task=cpu.state.A13.value
                    if task<0x01000000 or task>=0x01100000 then return end
                    local owner=program:read_u32(task+0xc0)
                    local player=program:read_u32(0x01060220)
                    if owner<0x01000000 or owner>=0x01100000 or
                        player<0x01000000 or player>=0x01100000 then return end
                    ai_router_entries=ai_router_entries+1
                    if ai_router_entries<=24 then
                        print(string.format("MK2KS_CPU_ROUTER_CONTEXT frame=%d id=%d gap=%d owner_x=%d player_x=%d a0=%08X a1=%08X a2=%08X a3=%08X a4=%08X a10=%08X",
                            frame,program:read_u16(owner+0x1f0),
                            math.abs(program:read_u16(owner+0x90)-program:read_u16(player+0x90)),
                            program:read_u16(owner+0x90),program:read_u16(player+0x90),
                            cpu.state.A0.value,cpu.state.A1.value,cpu.state.A2.value,
                            cpu.state.A3.value,cpu.state.A4.value,cpu.state.A10.value))
                    end
                end)
            for _,spec in ipairs({
                {id=17,move="knife",address=0xffffb000},
                {id=17,move="ball",address=0xffffde00},
                {id=17,move="blade",address=0xfff8cc00},
                {id=18,move="ring",address=0xffffb400},
                {id=18,move="square",address=0xffffca00},
                {id=18,move="bicycle",address=0xfff9a400},
                {id=18,move="leg",address=0xfff80800},
                {id=17,move="choke",address=0xfff91400}
            }) do
                ai_owned_action_taps[#ai_owned_action_taps+1]=program:install_read_tap(
                    spec.address,spec.address+15,"CPU move variety",function(offset,data,mask)
                        if offset~=spec.address then return end
                        local task=cpu.state.A13.value
                        if task<0x01000000 or task>=0x01100000 then return end
                        local owner=program:read_u32(task+0xc0)
                        local opponent=program:read_u32(0x01060df0)
                        if owner~=opponent or owner<0x01000000 or owner>=0x01100000 or
                            program:read_u16(owner+0x1f0)~=spec.id then return end
                        ai_variety_counts[spec.move]=ai_variety_counts[spec.move]+1
                        if ai_variety_counts[spec.move]<=6 then
                            ai_owned_capture_frames[frame+12]=spec.id
                            ai_owned_capture_frames[frame+24]=spec.id
                        end
                        if ai_variety_counts[spec.move]<=20 then
                            print(string.format("MK2KS_CPU_VARIETY_ENTRY frame=%d id=%d move=%s action=%08X owner=%08X stage=%d",
                                frame,spec.id,spec.move,spec.address,owner,program:read_u16(0x01061b30)))
                        end
                    end)
            end
        end
        if os.getenv("MK2KS_TRACE_AI_CLOSE") == "1" then
            -- Read-only address census of the stock AI decision region. A
            -- CPU-owned task and the true opponent pointer are required;
            -- compare near and distant executions before choosing a hook.
            local function close_census(offset,data,mask)
                    if frame<1500 or frame>7200 then return end
                    local task=cpu.state.A13.value
                    if task<0x01000000 or task>=0x01100000 then return end
                    local owner=program:read_u32(task+0xc0)
                    local opponent=program:read_u32(0x01060df0)
                    local player=program:read_u32(0x01060220)
                    if owner~=opponent or owner<0x01000000 or owner>=0x01100000 or
                        player<0x01000000 or player>=0x01100000 then return end
                    local gap=math.abs(program:read_u16(owner+0x90)-program:read_u16(player+0x90))
                    local zone=gap<=90 and 1 or gap>=140 and 2 or 0
                    if zone==0 then return end
                    local count=ai_close_counts[offset]
                    if not count then count={0,0}; ai_close_counts[offset]=count end
                    count[zone]=count[zone]+1
                    if ai_close_events<36 and (offset==0xff9b8740 or
                        offset==0xff9b8ed0 or offset==0xff9b90b0 or
                        offset==0xff9b9240 or offset==0xff9b55f0 or
                        offset==0xff9b71a0) then
                        ai_close_events=ai_close_events+1
                        print(string.format("MK2KS_AI_CLOSE_EVENT frame=%d pc=%08X gap=%d id=%d task_action=%04X owner_action=%04X player_y=%d owner_y=%d a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a9=%08X",
                            frame,offset,gap,program:read_u16(owner+0x1f0),
                            program:read_u16(task+0x1f0),program:read_u16(owner+0x1d0),
                            program:read_u16(player+0xb0),program:read_u16(owner+0xb0),
                            cpu.state.A8.value,cpu.state.A13.value,cpu.state.A0.value,
                            cpu.state.A1.value,cpu.state.A2.value,cpu.state.A9.value))
                    end
                    if (offset==0xff9b8740 or offset==0xff9b55f0 or
                        offset==0xff9b71a0) and zone==1 and
                        os.getenv("MK2KS_AI_CLOSE_SNAPSHOT")=="1" and
                        ai_close_near_entries<4 and frame-ai_close_last_capture>=30 then
                        ai_close_near_entries=ai_close_near_entries+1
                        ai_close_last_capture=frame
                        ai_close_capture_frames[frame+6]=true
                        ai_close_capture_frames[frame+18]=true
                    end
            end
            ai_close_tap=program:install_read_tap(0xff9b7e00,0xff9b935f,
                "stock CPU distance decision census",close_census)
            if os.getenv("MK2KS_TRACE_AI_CLOSE_WIDE")=="1" then
                ai_close_other_tap=program:install_read_tap(0xff9b0000,0xff9b7dff,
                    "stock CPU broad decision census",close_census)
            end
        end
        if os.getenv("MK2KS_TRACE_AI_KANO") == "1" then
            kano_ai_tap=program:install_read_tap(0xffffb000,0xffffb0ff,
                "CPU Kano special action",function(offset,data,mask)
                    if (not ai_trace_start or frame>=ai_trace_start) and
                        (not ai_trace_end or frame<=ai_trace_end) and kano_ai_reads<80 then
                        kano_ai_reads=kano_ai_reads+1
                        print(string.format("MK2KS_AI_KANO_CODE frame=%d pc=%08X offset=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X",
                            frame,cpu.state.PC.value,offset,cpu.state.A0.value,cpu.state.A1.value,
                            cpu.state.A2.value,cpu.state.A8.value,cpu.state.A13.value))
                    end
                end)
        end
        if os.getenv("MK2KS_TRACE_PALETTE_WRITES") == "1" then
            palette_tap=program:install_write_tap(0x01800000,0x0187ffff,
                "freeze palette writer",function(offset,data,mask)
                    if frame>=4800 and frame<=4840 and palette_trace_count<100 then
                        palette_trace_count=palette_trace_count+1
                        print(string.format("MK2KS_PALETTE_WRITE frame=%d pc=%08X offset=%08X data=%08X mask=%08X a0=%08X a1=%08X a2=%08X a5=%08X a8=%08X",
                            frame,cpu.state.PC.value,offset,data,mask,cpu.state.A0.value,
                            cpu.state.A1.value,cpu.state.A2.value,cpu.state.A5.value,cpu.state.A8.value))
                    end
                end)
        end
        if os.getenv("MK2KS_TRACE_FREEZE_CODE") == "1" then
            freeze_code_tap=program:install_read_tap(0xff80c700,0xff80c75f,
                "imported palette setup",function(offset,data,mask)
                    if frame>=4800 and frame<=4830 and freeze_code_reads<80 then
                        freeze_code_reads=freeze_code_reads+1
                        print(string.format("MK2KS_FREEZE_CODE frame=%d pc=%08X offset=%08X a0=%08X a1=%08X a2=%08X a5=%08X a8=%08X",
                            frame,cpu.state.PC.value,offset,cpu.state.A0.value,cpu.state.A1.value,
                            cpu.state.A2.value,cpu.state.A5.value,cpu.state.A8.value))
                    end
                end)
        end
        if reset_trace_stage then
            stage_palette_tap=program:install_read_tap(0xff80c700,0xff80c9ff,
                "stage-relative palette copy trace",function(offset,data,mask)
                    if program:read_u16(0x01061b30)==reset_trace_stage and
                        stage_palette_reads<120 then
                        stage_palette_reads=stage_palette_reads+1
                        print(string.format("MK2KS_STAGE_PALETTE_READ frame=%d pc=%08X offset=%08X a0=%08X a1=%08X a2=%08X a5=%08X a8=%08X",
                            frame,cpu.state.PC.value,offset,cpu.state.A0.value,cpu.state.A1.value,
                            cpu.state.A2.value,cpu.state.A5.value,cpu.state.A8.value))
                    end
                end)
            watchdog_tap=program:install_write_tap(0x01d81060,0x01d8107f,
                "stage watchdog kicks",function(offset,data,mask)
                    if program:read_u16(0x01061b30)==reset_trace_stage then
                        watchdog_stage_writes=watchdog_stage_writes+1
                        last_watchdog_stage_frame=frame
                    end
                end)
        end
        if os.getenv("MK2KS_ASSERT_WIN_PROGRESS") == "1" or
            os.getenv("MK2KS_ASSERT_SECOND_WIN_PROGRESS") == "1" or multi_min_stage then
            local win_table=0xff800000+0xfdf00*8
            progress_tap=program:install_read_tap(win_table,win_table+19*32-1,
                "input-driven ladder progress",function(offset,data,mask)
                    if (offset-win_table)%32==0 and (offset-win_table)//32==progress_fighter then
                        local stage=program:read_u16(0x01061b30)
                        local opponent=program:read_u16(0x01060e50)
                        local schedule=program:read_u32(0x01061b10)
                        if stage<=16 and schedule>=0xff800000 and
                            opponent==program:read_u16(schedule+stage*16) then
                            progress_stage_wins[stage]=(progress_stage_wins[stage] or 0)+1
                            if stage==0 then progress_wins=progress_wins+1 end
                        end
                    end
                end)
        end
        if os.getenv("MK2KS_CPU_TRACE_CAMERA") == "1" then
            camera_tap=program:install_write_tap(0x0105d120,0x0105d13f,"ladder camera",function(offset,data,mask)
                if frame>=1100 and frame<=1550 and cpu.state.PC.value~=0xff804e10 then
                    camera_writes=camera_writes+1
                    if camera_writes<=120 then
                        print(string.format("MK2KS_CPU_CAMERA frame=%d pc=%08X offset=%08X data=%08X mask=%08X",
                            frame,cpu.state.PC.value,offset,data,mask))
                    end
                end
            end)
        end
        if os.getenv("MK2KS_CPU_TRACE_LADDER_DMA") == "1" then
            ladder_dma_tap=program:install_write_tap(0x01a80000,0x01a800ff,"ladder DMA",function(offset,data,mask)
                local reg=(offset-0x01a80000)//16
                ladder_dma_regs[reg]=((ladder_dma_regs[reg] or 0)&(~mask))|(data&mask)
                if reg==1 and (data&0x8000)~=0 and frame>=1110 and frame<=1510 then
                    local x,y,w,h=ladder_dma_regs[4] or 0,ladder_dma_regs[5] or 0,
                        ladder_dma_regs[6] or 0,ladder_dma_regs[7] or 0
                    if w>=80 and h>=40 then
                        local source=(ladder_dma_regs[2] or 0)|((ladder_dma_regs[3] or 0)<<16)
                        local key=string.format("%08X:%d:%d:%d:%d",source,x,y,w,h)
                        if not ladder_dma_seen[key] then
                            ladder_dma_seen[key]=true
                            print(string.format("MK2KS_LADDER_DMA frame=%d source=%08X xy=%d,%d wh=%d,%d command=%04X palette=%04X pc=%08X",
                                frame,source,x,y,w,h,data,ladder_dma_regs[8] or 0,cpu.state.PC.value))
                        end
                    end
                end
            end)
        end
    end
    if frame<900 then return end
    if ai_close_capture_frames[frame] then
        print(string.format("MK2KS_AI_CLOSE_SNAPSHOT frame=%d",frame))
        manager.machine.screens[":screen"]:snapshot(string.format("close_%04d.png",frame))
    end
    if ai_owned_capture_frames[frame] then
        print(string.format("MK2KS_CPU_OWNED_SPECIAL_SNAPSHOT frame=%d id=%d",
            frame,ai_owned_capture_frames[frame]))
        manager.machine.video:snapshot()
    end
    if diagnostic_ladder_index and not diagnostic_ladder_written and frame==1100 then
        print(string.format("MK2KS_CPU_DIAGNOSTIC_LADDER_WRITE frame=%d old=%d requested=%d",
            frame,program:read_u16(0x01061b30),diagnostic_ladder_index))
        program:write_u16(0x01061b30,diagnostic_ladder_index)
        diagnostic_ladder_written=true
    end
    if stage_visual_snapshots and frame>=1450 then
        local stage=program:read_u16(0x01061b30)
        local arena=program:read_u16(0x01061ac0)
        local p1=program:read_u32(0x01060220)
        local p2=program:read_u32(0x01060df0)
        local pixels,width=manager.machine.screens[":screen"]:pixels()
        local hud=string.unpack("<I4",pixels,(30*width+80)*4+1)&0xffffff
        local visible_hud=((hud>>8)&0xff)>=180 and ((hud>>16)&0xff)<80 and (hud&0xff)<80
        if stage<16 and visible_hud and not stage_visual_seen[stage] and
            p1>=0x01000000 and p1<0x01100000 and
            p2>=0x01000000 and p2<0x01100000 and
            program:read_u16(p1+0x1f0)==progress_ids[os.getenv("MK2KS_TEST_FIGHTER")] and
            program:read_u16(p2+0x1f0)==program:read_u16(0x01060e50) then
            stage_visual_ready[stage]=stage_visual_ready[stage] or frame
            if frame-stage_visual_ready[stage]>=90 then
                stage_visual_seen[stage]=true
                print(string.format("MK2KS_STAGE_VISUAL frame=%d stage=%d arena=%d p1=%d p2=%d",
                    frame,stage,arena,program:read_u16(p1+0x1f0),program:read_u16(p2+0x1f0)))
                manager.machine.screens[":screen"]:snapshot(string.format("stage_visual_%02d.png",stage))
            end
        end
    end
    if frame==1100 and os.getenv("MK2KS_ASSERT_LADDER_ROSTER") == "1" then
        local pointer_table=program:read_u32(0xff8a11f0)
        assert(pointer_table==0xfffa2c00,"Native ladder pointer table was not installed")
        local chosen=program:read_u32(0x01061b10)
        local chosen_valid=false
        for order=0,5 do
            local schedule=program:read_u32(pointer_table+order*32)
            if schedule==chosen then chosen_valid=true end
            local seen={}
            for i=0,16 do
                local id=program:read_u16(schedule+i*16)
                assert(id<=14 or id==17 or id==18,"Unexpected ladder fighter ID")
                assert(not seen[id],"Duplicate fighter in native ladder order")
                seen[id]=true
            end
            for id=0,14 do assert(seen[id],"Missing stock ladder fighter") end
            assert(seen[17] and seen[18],"Missing Kano or Sonya in ladder order")
            assert(program:read_u16(schedule+17*16)==0xffff,"Missing ladder terminator")
            assert(program:read_u16(schedule+13*16)==14 and
                program:read_u16(schedule+14*16)==6 and
                program:read_u16(schedule+15*16)==12 and
                program:read_u16(schedule+16*16)==13,"Native ladder boss tail changed")
        end
        assert(chosen_valid,"Game did not choose one of the six native orders")
        local previous=program:read_u16(0xfffa3a00)
        assert(previous==940,"Unexpected tower bottom")
        for i=1,15 do
            local y=program:read_u16(0xfffa3a00+i*16)
            assert(previous-y>=50 and previous-y<=51,"Tower portrait frames overlap or drift")
            previous=y
        end
        assert(previous==186 and program:read_u16(0xfffa3a00+16*16)==128,"Tower top changed")
        assert(program:read_u16(0xfffa3c00)==784 and
            program:read_u16(0xfffa3c00+16*16)==4,"Tower scroll endpoints changed")
        print("MK2KS_LADDER_TABLE_RESULT pass=true orders=6 fighters=17 portrait_slots=16")
    end
    if os.getenv("MK2KS_CPU_LADDER_SNAP") == "1" and
        (frame==1180 or frame==1240 or frame==1300 or frame==1360 or frame==1420 or
         frame==1450 or frame==1470 or frame==1490 or frame==1510 or
         frame==1530 or frame==1550 or frame==1570 or frame==1590) then
        print(string.format("MK2KS_CPU_LADDER_SNAP frame=%d",frame))
        manager.machine.video:snapshot()
    end
    if os.getenv("MK2KS_CPU_STAGE7_LADDER_SNAP") == "1" and
        frame>=37800 and frame<=38200 and frame%40==0 then
        print(string.format("MK2KS_CPU_STAGE7_LADDER_SNAP frame=%d",frame))
        manager.machine.video:snapshot()
    end
    if os.getenv("MK2KS_CPU_PROGRESS_SNAP") == "1" and
        (frame==3372 or frame==3400 or frame==3450 or frame==3500 or
         frame==3550 or frame==3580 or frame==3600) then
        print(string.format("MK2KS_CPU_PROGRESS_SNAP frame=%d index=%d p1=%d p2=%d",frame,
            program:read_u16(0x01061b30),program:read_u16(0x01060280),
            program:read_u16(0x01060e50)))
        manager.machine.video:snapshot()
    end
    if os.getenv("MK2KS_CPU_SECOND_PROGRESS_SNAP") == "1" and
        (frame==5472 or frame==5500 or frame==5550 or frame==5600 or
         frame==5650 or frame==5680 or frame==5700) then
        print(string.format("MK2KS_CPU_SECOND_PROGRESS_SNAP frame=%d index=%d p1=%d p2=%d",frame,
            program:read_u16(0x01061b30),program:read_u16(0x01060280),
            program:read_u16(0x01060e50)))
        manager.machine.video:snapshot()
    end
    if frame==1100 or frame==1111 then
        local schedule=program:read_u32(0x01061b10)
        local ids={}
        if schedule>=0xff800000 then
            for i=0,17 do ids[#ids+1]=string.format("%04X",program:read_u16(schedule+i*16)) end
        end
        print(string.format("MK2KS_CPU_SCHEDULE frame=%d address=%08X index=%d ids=%s",
            frame,schedule,program:read_u16(0x01061b30),table.concat(ids,",")))
    end
    if frame==1100 and os.getenv("MK2KS_DUMP_AI_CODE") == "1" then
        for index=0,32 do
            print(string.format("MK2KS_AI_POINTER index=%d address=%08X value=%08X",
                index,0xff9b76d0+index*32,program:read_u32(0xff9b76d0+index*32)))
        end
        for base=0xff9b7600,0xff9b77f0,0x10 do
            print(string.format("MK2KS_AI_ROM %08X %04X %04X %04X %04X %04X %04X %04X %04X",
                base,program:read_u16(base),program:read_u16(base+0x10),
                program:read_u16(base+0x20),program:read_u16(base+0x30),
                program:read_u16(base+0x40),program:read_u16(base+0x50),
                program:read_u16(base+0x60),program:read_u16(base+0x70)))
        end
        for base=0xffa1e7c0,0xffa1e850,0x10 do
            print(string.format("MK2KS_TRAP_ROM %08X %04X %04X %04X %04X %04X %04X %04X %04X",
                base,program:read_u16(base),program:read_u16(base+0x10),
                program:read_u16(base+0x20),program:read_u16(base+0x30),
                program:read_u16(base+0x40),program:read_u16(base+0x50),
                program:read_u16(base+0x60),program:read_u16(base+0x70)))
        end
    end
    local roster=program:read_u16(0x01060e50)
    if diagnostic_id and not diagnostic_written and frame>1000 and roster<=11 and
        program:read_u16(0x01060280)>=17 then
        print(string.format("MK2KS_CPU_DIAGNOSTIC_WRITE frame=%d native_choice=%d requested=%d",
            frame,roster,diagnostic_id))
        program:write_u16(0x01060e50,diagnostic_id)
        roster=program:read_u16(0x01060e50)
        diagnostic_written=true
        diagnostic_injection_stage=program:read_u16(0x01061b30)
    end
    local actor=program:read_u32(0x01060df0)
    local valid=actor>=0x01000000 and actor<0x01100000
    local id=valid and program:read_u16(actor+0x1f0) or 0xffff
    local stage=program:read_u16(0x01061b30)
    if ending_trace_all and not ending_start and stage==16 and roster==13 and
        program:read_u16(0x01060ec0)==0 and
        program:read_u16(0x01060280)==progress_fighter and
        (progress_stage_wins[16] or 0)>=1 then
        ending_start=frame
        print(string.format("MK2KS_FULL_ENDING_START frame=%d",frame))
    end
    if ending_start then
        local age=frame-ending_start
        if age==0 or age==120 or age==300 or age==600 or age==900 or
            age==1200 or age==1800 or age==2400 or age==3000 or age==3600 or
            age==4800 or age==6000 then
            print(string.format("MK2KS_FULL_ENDING_STATE frame=%d age=%d pc=%08X mode=%d p1=%d cpu=%d actor=%08X hp=%d,%d stage=%d",
                frame,age,cpu.state.PC.value,program:read_u16(0x010601d0),
                program:read_u16(0x01060280),roster,actor,
                program:read_u16(0x010602f0),program:read_u16(0x01060ec0),stage))
            manager.machine.video:snapshot()
        end
    end
    if cpu_trace_stage and cpu_trace_path and not cpu_trace_started and
        stage==cpu_trace_stage and multi_last_stage==cpu_trace_stage and
        multi_transition_frame and
        frame-multi_transition_frame>=cpu_trace_age then
        assert(manager.machine.debugger,"CPU tracing requires -debug")
        manager.machine.debugger.visible_cpu=cpu
        manager.machine.debugger:command("trace "..cpu_trace_path..",maincpu")
        manager.machine.debugger.execution_state="run"
        cpu_trace_started=true
        print(string.format("MK2KS_CPU_TRACE_STARTED frame=%d stage=%d age=%d",
            frame,stage,frame-multi_transition_frame))
    elseif cpu_trace_started and stage~=cpu_trace_stage then
        manager.machine.debugger:command("trace off,maincpu")
        cpu_trace_started=false
        cpu_trace_stage=nil
        print(string.format("MK2KS_CPU_TRACE_STOPPED frame=%d stage=%d",frame,stage))
    end
    local save_age=multi_transition_frame and frame-multi_transition_frame or
        (diagnostic_ladder_index==stage and frame-1100 or -1)
    if save_stage and not save_requested and stage==save_stage and valid and
        save_age>=350 and
        program:read_u16(0x01060280)==progress_fighter then
        save_requested=true
        manager.machine:save(save_state_path)
        print(string.format("MK2KS_SAVE_REQUEST frame=%d stage=%d path=%s",frame,stage,save_state_path))
    end
    -- The top-level scene word is not a reliable active-fight gate on this
    -- build. Require the chosen native fighter and live actors/health below;
    -- stop assistance once the campaign observer reports a loss or ending.
    local diagnostic_stage=(diagnostic_all_stages and stage<=16 or stage==diagnostic_ladder_index) and
        program:read_u16(0x01060280)==progress_fighter and not multi_campaign_ended
    if diagnostic_p1_regen and diagnostic_stage and valid then
        local p1=program:read_u32(0x01060220)
        local health=program:read_u16(0x010602f0)
        if p1>=0x01000000 and p1<0x01100000 and health>0 and health<161 then
            program:write_u16(0x010602f0,161)
            diagnostic_p1_regen_writes=diagnostic_p1_regen_writes+1
            if diagnostic_p1_regen_writes<=3 or os.getenv("MK2KS_TRACE_ALL_REGEN")=="1" then
                print(string.format("MK2KS_DIAGNOSTIC_P1_REGEN frame=%d old=%d",frame,health))
            end
        end
    end
    if diagnostic_cpu_health and diagnostic_stage and valid and frame>1400 and
        program:read_u16(0x010602f0)>0 and
        program:read_u16(0x01060ec0)==161 and
        frame-last_diagnostic_health_frame>250 then
        print(string.format("MK2KS_DIAGNOSTIC_HEALTH_WRITE frame=%d stage=%d cpu=%d old=161 new=%d",
            frame,stage,id,diagnostic_cpu_health))
        program:write_u16(0x01060ec0,diagnostic_cpu_health)
        diagnostic_health_writes=diagnostic_health_writes+1
        last_diagnostic_health_frame=frame
    end
    if ai_trace_start and ai_trace_end and frame>=ai_trace_start and frame<=ai_trace_end then
        print(string.format("MK2KS_AI_TRACE frame=%d pc=%08X sp=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X p1=%08X p2=%08X cpu_id=%d mode=%d hp=%d,%d",
            frame,cpu.state.PC.value,cpu.state.SP.value,cpu.state.A0.value,cpu.state.A1.value,
            cpu.state.A2.value,cpu.state.A8.value,cpu.state.A13.value,
            program:read_u32(0x01060220),actor,id,program:read_u16(0x010601d0),
            program:read_u16(0x010602f0),program:read_u16(0x01060ec0)))
        if frame==ai_trace_start or frame==ai_trace_end or frame%30==0 then
            manager.machine.video:snapshot()
        end
    end
    if (multi_min_stage or multi_snap_stage) and frame>=1100 and not multi_campaign_ended then
        local stage=program:read_u16(0x01061b30)
        local schedule=program:read_u32(0x01061b10)
        local player=program:read_u16(0x01060280)
        -- A stage-zero timeout loss can enter GAME OVER directly, without
        -- first advancing the ladder index. Do not grade the following stock
        -- attract demonstration as the selected fighter's campaign.
        if stage<16 and player==progress_fighter and
            multi_identity_checks>1000 and
            program:read_u16(0x010601d0)==11 and
            program:read_u32(0x01060220)==0 and
            program:read_u32(0x01060df0)==0 then
            multi_campaign_ended=true
            print(string.format("MK2KS_MULTI_GAME_OVER frame=%d stage=%d wins=%d",
                frame,stage,progress_stage_wins[stage] or 0))
            return
        end
        if multi_last_stage==16 and player~=progress_fighter and
            (progress_stage_wins[16] or 0)>=1 and
            program:read_u16(0x010601d0)==11 then
            multi_campaign_ended=true
            multi_campaign_completed=true
            print(string.format("MK2KS_MULTI_CAMPAIGN_COMPLETED frame=%d p1=%d wins=%d",
                frame,player,progress_stage_wins[16] or 0))
            if os.getenv("MK2KS_STOP_ON_CAMPAIGN_COMPLETE")=="1" then
                manager.machine:exit()
            end
            return
        end
        if multi_last_stage and multi_last_stage>=1 and stage==0 and
            player~=progress_fighter and (progress_stage_wins[multi_last_stage] or 0)<2 then
            multi_campaign_ended=true
            print(string.format("MK2KS_MULTI_CAMPAIGN_ENDED frame=%d last_stage=%d wins=%d p1=%d",
                frame,multi_last_stage,progress_stage_wins[multi_last_stage] or 0,player))
            return
        end
        if multi_last_stage==nil then
            multi_last_stage=stage
        elseif stage~=multi_last_stage then
            local skipped_hidden=stage==multi_last_stage+2 and schedule>=0xff800000 and
                program:read_u16(schedule+(multi_last_stage+1)*16)==14
            if (stage~=multi_last_stage+1 and not skipped_hidden) or
                (progress_stage_wins[multi_last_stage] or 0)<2 then
                multi_stage_errors=multi_stage_errors+1
            end
            local expected=diagnostic_written and stage==diagnostic_injection_stage and diagnostic_id or
                (stage<=16 and program:read_u16(schedule+stage*16) or 0xffff)
            print(string.format("MK2KS_MULTI_STAGE frame=%d old=%d new=%d wins=%d cpu=%d expected=%d",
                frame,multi_last_stage,stage,progress_stage_wins[multi_last_stage] or 0,
                roster,expected))
            multi_last_stage=stage
            multi_transition_frame=frame
        end
        if multi_snap_stage and stage>=multi_snap_stage and multi_transition_frame and
            (frame==multi_transition_frame or frame==multi_transition_frame+30 or
             frame==multi_transition_frame+80 or frame==multi_transition_frame+130 or
             frame==multi_transition_frame+180 or frame==multi_transition_frame+220) then
            print(string.format("MK2KS_MULTI_SNAP frame=%d stage=%d age=%d",frame,stage,
                frame-multi_transition_frame))
            manager.machine.video:snapshot()
        end
        local p1=program:read_u32(0x01060220)
        if multi_min_stage and stage<=16 and schedule>=0xff800000 and
            p1>=0x01000000 and p1<0x01100000 and valid and
            (not multi_transition_frame or frame-multi_transition_frame>3) and
            program:read_u16(0x010602f0)>0 and program:read_u16(0x01060ec0)>0 then
            multi_identity_checks=multi_identity_checks+1
            local shang_morph=stage==14 and roster==6 and id<=11
            local expected=diagnostic_written and stage==diagnostic_injection_stage and diagnostic_id or
                program:read_u16(schedule+stage*16)
            if program:read_u16(0x01060280)~=progress_fighter or
                program:read_u16(p1+0x1f0)~=progress_fighter or
                roster~=expected or
                (id~=roster and not shang_morph) then
                multi_identity_errors=multi_identity_errors+1
                if multi_identity_errors<=4 then
                    print(string.format("MK2KS_MULTI_ID_ERROR frame=%d stage=%d p1=%d p1actor=%d cpu=%d cpuactor=%d expected=%d",
                        frame,stage,program:read_u16(0x01060280),program:read_u16(p1+0x1f0),
                        roster,id,expected))
                end
            end
        end
        if multi_min_stage and multi_check_frame and frame==multi_check_frame then
            local p1valid=p1>=0x01000000 and p1<0x01100000
            local complete=true
            for prior=0,multi_min_stage-1 do
                if progress_stage_wins[prior]~=2 then complete=false end
            end
            local passed=complete and multi_stage_errors==0 and multi_identity_errors==0 and
                multi_identity_checks>1000 and stage>=multi_min_stage and
                p1valid and valid and program:read_u16(p1+0x1f0)==progress_fighter and
                roster==program:read_u16(schedule+stage*16) and id==roster and
                not diagnostic_written and not diagnostic_ladder_written
            local wins={}
            for prior=0,multi_min_stage-1 do wins[#wins+1]=progress_stage_wins[prior] or 0 end
            print(string.format("MK2KS_MULTI_PROGRESS_RESULT pass=%s frame=%d stage=%d wins=%s identity_checks=%d identity_errors=%d stage_errors=%d p1=%d p1actor=%d cpu=%d cpuactor=%d diagnostic=%s,%s",
                tostring(passed),frame,stage,table.concat(wins,","),multi_identity_checks,
                multi_identity_errors,multi_stage_errors,program:read_u16(0x01060280),
                p1valid and program:read_u16(p1+0x1f0) or 0xffff,roster,id,
                tostring(diagnostic_written),tostring(diagnostic_ladder_written)))
            assert(passed,"Multi-match native ladder progression failed")
        end
    end
    if reset_trace_start and reset_trace_end and frame>=reset_trace_start and
        frame<=reset_trace_end then
        print(string.format("MK2KS_RESET_TRACE frame=%d pc=%08X sp=%08X a0=%08X a1=%08X a2=%08X a5=%08X a8=%08X mode=%04X p1state=%04X winner=%04X index=%d p1ptr=%08X p2ptr=%08X p1=%d p2=%d hp=%d,%d",
            frame,cpu.state.PC.value,cpu.state.SP.value,cpu.state.A0.value,cpu.state.A1.value,
            cpu.state.A2.value,cpu.state.A5.value,cpu.state.A8.value,
            program:read_u16(0x010601d0),program:read_u16(0x010601f0),
            program:read_u16(0x01061b00),program:read_u16(0x01061b30),
            program:read_u32(0x01060220),actor,program:read_u16(0x01060280),roster,
            program:read_u16(0x010602f0),program:read_u16(0x01060ec0)))
        if frame==reset_trace_start or frame==reset_trace_end or frame%20==0 then
            manager.machine.video:snapshot()
        end
    end
    if reset_trace_stage and program:read_u16(0x01061b30)==reset_trace_stage and
        multi_transition_frame and frame-multi_transition_frame<=reset_trace_stage_age then
        print(string.format("MK2KS_STAGE_RESET_TRACE frame=%d age=%d pc=%08X sp=%08X a0=%08X a1=%08X a2=%08X a5=%08X a8=%08X mode=%04X p1state=%04X winner=%04X index=%d p1ptr=%08X p2ptr=%08X p1=%d p2=%d hp=%d,%d",
            frame,frame-multi_transition_frame,cpu.state.PC.value,cpu.state.SP.value,
            cpu.state.A0.value,cpu.state.A1.value,cpu.state.A2.value,cpu.state.A5.value,cpu.state.A8.value,
            program:read_u16(0x010601d0),program:read_u16(0x010601f0),program:read_u16(0x01061b00),
            program:read_u16(0x01061b30),program:read_u32(0x01060220),actor,
            program:read_u16(0x01060280),roster,program:read_u16(0x010602f0),program:read_u16(0x01060ec0)))
        if frame%20==0 then manager.machine.video:snapshot() end
    end
    if os.getenv("MK2KS_ENDING_SNAP")=="1" and frame>=3300 and frame<=7500 and
        frame%300==0 then
        print(string.format("MK2KS_ENDING_SNAP frame=%d stage=%d p1=%d cpu=%d mode=%d",
            frame,program:read_u16(0x01061b30),program:read_u16(0x01060280),roster,
            program:read_u16(0x010601d0)))
        manager.machine.video:snapshot()
    end
    if valid and id==18 and roster==18 and program:read_u16(0x01061b30)==0 and
        program:read_u16(0x01060280)==progress_fighter then progress_initial=true end
    if valid and id==8 and roster==8 and program:read_u16(0x01061b30)==1 and
        program:read_u16(0x01060280)==progress_fighter then progress_stage1_seen=true end
    if os.getenv("MK2KS_ASSERT_WIN_PROGRESS") == "1" and frame==progress_check_frame then
        local schedule=program:read_u32(0x01061b10)
        local p1=program:read_u32(0x01060220)
        local p1valid=p1>=0x01000000 and p1<0x01100000
        local passed=not diagnostic_written and not diagnostic_ladder_written and
            progress_initial and progress_wins==2 and
            program:read_u16(schedule)==18 and program:read_u16(schedule+16)==8 and
            program:read_u16(0x01061b30)==1 and program:read_u16(0x01060280)==progress_fighter and
            roster==8 and id==8 and p1valid and program:read_u16(p1+0x1f0)==progress_fighter
        print(string.format("MK2KS_WIN_PROGRESS_RESULT pass=%s frame=%d wins=%d initial=%s index=%d p1=%d p1actor=%d cpu=%d cpuactor=%d diagnostic=%s,%s",
            tostring(passed),frame,progress_wins,tostring(progress_initial),program:read_u16(0x01061b30),
            program:read_u16(0x01060280),p1valid and program:read_u16(p1+0x1f0) or 0xffff,
            roster,id,tostring(diagnostic_written),tostring(diagnostic_ladder_written)))
        assert(passed,"Input-driven native ladder transition failed")
    end
    if os.getenv("MK2KS_ASSERT_SECOND_WIN_PROGRESS") == "1" and frame==second_progress_check_frame then
        local schedule=program:read_u32(0x01061b10)
        local p1=program:read_u32(0x01060220)
        local p1valid=p1>=0x01000000 and p1<0x01100000
        local passed=not diagnostic_written and not diagnostic_ladder_written and
            progress_initial and progress_stage1_seen and
            progress_stage_wins[0]==2 and progress_stage_wins[1]==2 and
            program:read_u16(schedule)==18 and program:read_u16(schedule+16)==8 and
            program:read_u16(schedule+32)==2 and program:read_u16(0x01061b30)==2 and
            program:read_u16(0x01060280)==progress_fighter and roster==2 and id==2 and
            p1valid and program:read_u16(p1+0x1f0)==progress_fighter
        print(string.format("MK2KS_SECOND_WIN_PROGRESS_RESULT pass=%s frame=%d wins=%d,%d index=%d p1=%d p1actor=%d cpu=%d cpuactor=%d diagnostic=%s,%s",
            tostring(passed),frame,progress_stage_wins[0] or 0,progress_stage_wins[1] or 0,
            program:read_u16(0x01061b30),program:read_u16(0x01060280),
            p1valid and program:read_u16(p1+0x1f0) or 0xffff,
            roster,id,tostring(diagnostic_written),tostring(diagnostic_ladder_written)))
        assert(passed,"Second input-driven native ladder transition failed")
    end
    if os.getenv("MK2KS_TRACE_P1_LIFECYCLE") == "1" and
        (frame==3300 or frame==3369 or frame==3370 or frame==3371 or frame==3372 or
         frame==3400 or frame==3500 or frame==3589 or frame==3600 or frame==3700) then
        local p1=program:read_u32(0x01060220)
        local p1valid=p1>=0x01000000 and p1<0x01100000
        print(string.format("MK2KS_P1_LIFECYCLE frame=%d roster=%d pointer=%08X actor_id=%d fixed_id=%d cpu_id=%d index=%d",
            frame,program:read_u16(0x01060280),p1,p1valid and program:read_u16(p1+0x1f0) or 0xffff,
            program:read_u16(0x01035080),id,program:read_u16(0x01061b30)))
    end
    local process=program:read_u32(0x01060e30)
    local action=valid and process>=0x01000000 and process<0x01100000 and program:read_u16(process+0x1f0) or 0xffff
    if os.getenv("MK2KS_CPU_TRACE_TAIL") == "1" and frame>=4045 and frame<=4377 then
        print(string.format("MK2KS_CPU_TAIL frame=%d pc=%08X sp=%08X a13=%08X actor=%08X action=%04X hp=%d,%d",
            frame,cpu.state.PC.value,cpu.state.SP.value,cpu.state.A13.value,
            actor,action,program:read_u16(0x010602f0),program:read_u16(0x01060ec0)))
        if cpu.state.PC.value>=0xffa1e700 and cpu.state.PC.value<=0xffa1e880 then
            local regs={}
            for i=0,15 do
                local reg=cpu.state["A"..i]
                if reg then regs[#regs+1]=string.format("A%d=%08X",i,reg.value) end
            end
            print("MK2KS_CPU_TRAP_REGS frame="..frame.." "..table.concat(regs," "))
        end
    end
    if roster~=last_roster or id~=last_actor or action~=last_action and frame%10==0 then
        print(string.format("MK2KS_CPU_STATE frame=%d roster=%d actor_id=%d action=%04X hp=%d,%d p1=%d",
            frame,roster,id,action,program:read_u16(0x010602f0),program:read_u16(0x01060ec0),
            program:read_u16(0x01060280)))
    end
    if valid and id==roster and frame>1200 and action~=last_action and action~=0x0303 then ai_actions=ai_actions+1 end
    if valid and id==roster and roster<19 then seen[roster]=true end
    if roster~=last_roster then changes=changes+1 end
    last_roster,last_actor,last_action=roster,id,action
end)
emu.register_stop(function()
    if multi_min_stage then
        local wins={}
        for stage=0,16 do
            if progress_stage_wins[stage] then
                wins[#wins+1]=string.format("%d:%d",stage,progress_stage_wins[stage])
            end
        end
        print(string.format("MK2KS_MULTI_FINAL frame=%d last_stage=%s wins=%s identity_checks=%d identity_errors=%d stage_errors=%d ended=%s completed=%s diagnostic=%s,%s",
            frame,tostring(multi_last_stage),table.concat(wins,","),multi_identity_checks,
            multi_identity_errors,multi_stage_errors,tostring(multi_campaign_ended),
            tostring(multi_campaign_completed),tostring(diagnostic_written),
            tostring(diagnostic_ladder_written)))
    end
    local opponents={}
    for id in pairs(seen) do opponents[#opponents+1]=id end
    table.sort(opponents)
    print(string.format("MK2KS_CPU_LADDER_RESULT frames=%d changes=%d ai_actions=%d writes=%d opponent_ids=%s",
        frame,changes,ai_actions,write_events,table.concat(opponents,",")))
    print(string.format("MK2KS_CPU_DIAGNOSTIC_RESULT requested=%s injected=%s",
        tostring(diagnostic_id),tostring(diagnostic_written)))
    print(string.format("MK2KS_CPU_DIAGNOSTIC_LADDER_RESULT requested=%s injected=%s",
        tostring(diagnostic_ladder_index),tostring(diagnostic_ladder_written)))
    print(string.format("MK2KS_CPU_DIAGNOSTIC_HEALTH_RESULT requested=%s all_stages=%s writes=%d",
        tostring(diagnostic_cpu_health),tostring(diagnostic_all_stages),diagnostic_health_writes))
    print(string.format("MK2KS_CPU_DIAGNOSTIC_P1_REGEN_RESULT enabled=%s writes=%d",
        tostring(diagnostic_p1_regen),diagnostic_p1_regen_writes))
    print(string.format("MK2KS_CPU_SPECIAL_RESULT reads=%d",special_reads))
    if os.getenv("MK2KS_TRACE_CPU_OWNED_SPECIALS") == "1" then
        print(string.format("MK2KS_CPU_OWNED_SPECIAL_RESULT kano=%d sonya=%d",
            ai_owned_action_counts[17],ai_owned_action_counts[18]))
    end
    if os.getenv("MK2KS_TRACE_AI_VARIETY") == "1" then
        print(string.format("MK2KS_CPU_VARIETY_RESULT knife=%d ball=%d blade=%d ring=%d square=%d bicycle=%d leg=%d choke=%d",
            ai_variety_counts.knife,ai_variety_counts.ball,ai_variety_counts.blade,
            ai_variety_counts.ring,ai_variety_counts.square,ai_variety_counts.bicycle,
            ai_variety_counts.leg,ai_variety_counts.choke))
    end
    if ai_close_tap then
        local entries={}
        for address,count in pairs(ai_close_counts) do
            entries[#entries+1]={address=address,near=count[1],far=count[2]}
        end
        table.sort(entries,function(a,b)
            if a.near~=b.near then return a.near>b.near end
            return a.address<b.address
        end)
        print(string.format("MK2KS_AI_CLOSE_CENSUS unique=%d",#entries))
        for i=1,math.min(#entries,200) do
            local entry=entries[i]
            print(string.format("MK2KS_AI_CLOSE_ADDRESS address=%08X near=%d far=%d",
                entry.address,entry.near,entry.far))
        end
        local distinctive=0
        for _,entry in ipairs(entries) do
            if entry.near>=2 and entry.far==0 and distinctive<100 then
                distinctive=distinctive+1
                print(string.format("MK2KS_AI_CLOSE_NEAR_ONLY address=%08X near=%d",
                    entry.address,entry.near))
            end
        end
    end
    if reset_trace_stage then
        print(string.format("MK2KS_STAGE_WATCHDOG_RESULT stage=%d writes=%d last_frame=%s",
            reset_trace_stage,watchdog_stage_writes,tostring(last_watchdog_stage_frame)))
    end
    if tap then tap:remove() end
    if special_tap then special_tap:remove() end
    if ai_close_tap then ai_close_tap:remove() end
    if ai_close_other_tap then ai_close_other_tap:remove() end
    for _,owned_tap in ipairs(ai_owned_action_taps) do owned_tap:remove() end
    if progress_tap then progress_tap:remove() end
    if camera_tap then camera_tap:remove() end
    if palette_tap then palette_tap:remove() end
    if stage_palette_tap then stage_palette_tap:remove() end
    if watchdog_tap then watchdog_tap:remove() end
    if freeze_code_tap then freeze_code_tap:remove() end
    if kano_ai_tap then kano_ai_tap:remove() end
    if ladder_dma_tap then ladder_dma_tap:remove() end
    if ending_stack_tap then ending_stack_tap:remove() end
    if ending_coop_tap then ending_coop_tap:remove() end
end)
