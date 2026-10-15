-- Observe the real P2-human/P1-CPU ladder after a two-human match.
-- All selection, combat and finish inputs come from the existing harness.
-- This observer never writes game RAM, positions, identities or schedules.
-- MAME reruns autoboot after a soft reset without retiring frame callbacks.
-- Never install a second input/observer set into the same machine session.
if rawget(_G,"MK2_P2_CAMPAIGN_PROBE_ACTIVE") then
    print("MK2_P2_CAMPAIGN_REBOOT_GUARD duplicate_callbacks_prevented=true")
    return
end
rawset(_G,"MK2_P2_CAMPAIGN_PROBE_ACTIVE",true)
dofile("mk2ks_finish_range_test.lua")

local p = manager.machine.devices[":maincpu"].spaces.program
local cpu = manager.machine.devices[":maincpu"].state
local screen = manager.machine.screens[":screen"]
local fighter = assert(os.getenv("MK2KS_P2_FIGHTER"))
local identity = assert(({kano=17, sonya=18})[fighter])
local frame, first, checks, errors, stage_changes = 0, nil, 0, 0, 0
local last, last_stage, human_wins, own_action = nil, nil, 0, false
local loss_seen,terminal_frame=false,nil
local stop_on_loss=os.getenv("MK2_P2_CAMPAIGN_STOP_ON_LOSS")=="1"
local hud_read = -1000
local strategy = os.getenv("MK2_P2_CAMPAIGN_STRATEGY") or "existing"
assert(strategy == "existing" or strategy == "uppercut" or strategy == "standing_hk" or strategy == "projectile_guard")
local fields = {}
local high,low = manager.machine.ioport.ports[":IN0"].fields,manager.machine.ioport.ports[":IN2"].fields
for _,label in ipairs({"Up","Down","Left","Right","High Punch","High Kick","Block"}) do
    fields[label] = high["P2 "..label]
end
for _,label in ipairs({"Low Punch","Low Kick","Block 2"}) do fields[label] = low["P2 "..label] end
local taps = {}
local function valid(pointer)
    return pointer >= 0x01000000 and pointer < 0x01100000
end
local function actor_id(pointer)
    return valid(pointer) and p:read_u16(pointer+0x1f0) or 0xffff
end
local action = fighter == "kano" and 0xfffaae00 or 0xfffab200
taps[#taps+1] = p:install_read_tap(action, action+15, "P2 campaign initial finish", function(at)
    if at == action and cpu.A8.value == p:read_u32(0x01060df0) and
        actor_id(cpu.A8.value) == identity then own_action = true end
end)
local win_table = 0xfffef800
taps[#taps+1] = p:install_read_tap(win_table, win_table+19*32-1, "P2 campaign winner", function(at)
    local own = p:read_u32(0x01060df0)
    if (at-win_table)%32 == 0 and (at-win_table)//32 == identity and
        actor_id(own) == identity and p:read_u16(0x01060e50) == identity and
        p:read_u16(0x01060dc0) == 1 and p:read_u16(0x010602f0) == 0 and
        p:read_u16(0x01060ec0) > 0 then
        human_wins = human_wins+1
        print(string.format("MK2_P2_CAMPAIGN_WIN frame=%d stage=%d actor=%08X wins=%d states=%d,%d",
            frame,p:read_u16(0x01061b30),own,human_wins,
            p:read_u16(0x010601f0),p:read_u16(0x01060dc0)))
    end
end)
taps[#taps+1] = p:install_read_tap(0xfffee000, 0xfffee000+19*64-1,
    "P1 campaign HUD construction", function(at)
        if (at-0xfffee000)%64 == 0 then hud_read = frame end
    end)

emu.register_frame(function()
    frame = frame+1
    assert(#taps == 3, "Retain all campaign observer handles")
    if frame == 1 then
        local rom_table = p:read_u32(0xff8a11f0)
        for order=0,5 do
            local list=p:read_u32(rom_table+order*32)
            local ids={}
            for index=0,16 do ids[#ids+1]=p:read_u16(list+index*16) end
            print(string.format("MK2_P2_CAMPAIGN_ROM table=%08X order=%d list=%08X ids=%s",rom_table,order,list,table.concat(ids,",")))
        end
    end
    if frame < 3000 then return end
    local mode, s1, s2 = p:read_u16(0x010601d0), p:read_u16(0x010601f0), p:read_u16(0x01060dc0)
    local stage = p:read_u16(0x01061b30)
    local table, schedule = p:read_u32(0xff8a11f0), p:read_u32(0x01061b10)
    local order = -1
    if table == 0xfffa2c00 then
        for i=0,5 do if p:read_u32(table+i*32) == schedule then order=i end end
    end
    local expected = order >= 0 and stage <= 16 and p:read_u16(schedule+stage*16) or 0xffff
    local a1,a2 = p:read_u32(0x01060220),p:read_u32(0x01060df0)
    local id1,id2 = actor_id(a1),actor_id(a2)
    local r1,r2 = p:read_u16(0x01060280),p:read_u16(0x01060e50)
    local h1,h2 = p:read_u16(0x010602f0),p:read_u16(0x01060ec0)
    local flags1,flags2 = valid(a1) and p:read_u16(a1+0x160) or 0, valid(a2) and p:read_u16(a2+0x160) or 0
    if own_action and checks>=500 and s1==0 and s2==2 and mode==3 and
        p:read_u16(0x01061b00)==1 and h1>0 and h2==0 and
        order>=0 and id1==expected and r1==expected and id2==identity and r2==identity then
        loss_seen=true
    end
    if loss_seen and not terminal_frame and mode==11 and s1==0 and s2==0 and
        p:read_u16(0x01061b00)==1 and h2==0 and a1==0 and a2==0 then
        terminal_frame=frame
        print(string.format("MK2_P2_CAMPAIGN_TERMINAL frame=%d stage=%d outcome=loss mode=%d states=%d,%d actors=%08X,%08X",
            frame,stage,mode,s1,s2,a1,a2))
        screen:snapshot("p2_campaign_game_over.png")
    end
    if stop_on_loss and terminal_frame and frame==terminal_frame+30 then manager.machine:exit() end
    local key=string.format("%d:%d:%d:%d:%d:%d:%08X:%08X",mode,s1,s2,stage,r1,r2,a1,a2)
    if key ~= last or frame%120 == 0 then
        print(string.format("MK2_P2_CAMPAIGN_STATE frame=%d mode=%d states=%d,%d stage=%d order=%d schedule=%08X expected=%d roster=%d,%d actors=%08X:%d,%08X:%d health=%d,%d winner=%d hud_read=%d",
            frame,mode,s1,s2,stage,order,schedule,expected,r1,r2,a1,id1,a2,id2,h1,h2,
            p:read_u16(0x01061b00),hud_read))
        last=key
    end
    -- Restrict identity grading to the actual published, live P2 campaign.
    -- The CPU must come from a validated ROM schedule, not a hard-coded ID.
    if own_action and human_wins >= 2 and s1 == 0 and s2 == 1 and
        (mode == 2 or mode == 7) and valid(a1) and valid(a2) and h1>0 and h2>0 then
        first=first or frame
        checks=checks+1
        local passed=order>=0 and stage<=16 and r1==expected and id1==expected and
            r2==identity and id2==identity
        if not passed then
            errors=errors+1
            if errors<=3 then print(string.format("MK2_P2_CAMPAIGN_ERROR frame=%d cpu=%d:%d expected=%d human=%d:%d identity=%d",
                frame,r1,id1,expected,r2,id2,identity)) end
        end
        if checks<=600 or frame%30==0 then
            print(string.format("MK2_P2_CAMPAIGN_LIVE frame=%d mode=%d states=%d,%d stage=%d order=%d schedule=%08X cpu=%d:%d human=%d:%d flags=%04X,%04X health=%d,%d",
                frame,mode,s1,s2,stage,order,schedule,r1,id1,r2,id2,flags1,flags2,h1,h2))
        end
        if last_stage and stage~=last_stage then stage_changes=stage_changes+1 end
        if not last_stage or stage~=last_stage then
            screen:snapshot(string.format("p2_campaign_stage_%02d.png",stage))
        end
        last_stage=stage
        if frame==first+120 or frame==first+600 then
            screen:snapshot(string.format("p2_campaign_age_%04d.png",frame-first))
        end
        if strategy ~= "existing" and mode == 2 and p:read_u16(0x01061b00) == 0 then
            -- Ordinary P2 input only: reach true close range rather than
            -- repeating an out-of-range uppercut at the old 85-unit threshold.
            for _,field in pairs(fields) do field:clear_value() end
            local x1,x2=p:read_u16(a1+0x90),p:read_u16(a2+0x90)
            local gap=math.abs(x1-x2)
            local reach=strategy=="standing_hk" and 90 or 65
            if strategy=="projectile_guard" and gap>110 then
                local phase=frame%55
                local forward=x2<x1 and "Right" or "Left"
                local direction=fighter=="sonya" and forward or (forward=="Right" and "Left" or "Right")
                if phase<3 then fields.Down:set_value(1) end
                if phase>=5 and phase<8 then fields[direction]:set_value(1) end
                if phase>=6 and phase<9 then fields[fighter=="sonya" and "Low Punch" or "High Punch"]:set_value(1) end
                if phase>=10 then fields.Block:set_value(1) end
            elseif strategy=="projectile_guard" then
                fields.Down:set_value(1)
                if frame%34<4 then fields["High Punch"]:set_value(1)
                else fields.Block:set_value(1) end
            elseif gap>reach then
                fields[x2<x1 and "Right" or "Left"]:set_value(1)
            elseif strategy=="standing_hk" then
                if frame%22<4 then fields["High Kick"]:set_value(1) end
            else
                fields.Down:set_value(1)
                if frame%22<4 then fields["High Punch"]:set_value(1) end
            end
        end
    end
end)
emu.register_stop(function()
    print(string.format("MK2_P2_CAMPAIGN_RESULT pass=%s fighter=%s checks=%d errors=%d first=%s stage_changes=%d last_stage=%s wins=%d initial_action=%s assistance=none scope=published_p2_campaign_identity",
        tostring(checks>=500 and errors==0 and human_wins>=2 and own_action),fighter,checks,errors,
        tostring(first),stage_changes,tostring(last_stage),human_wins,tostring(own_action)))
    print(string.format("MK2_P2_CAMPAIGN_SESSION loss_seen=%s terminal=%s stop_on_loss=%s",
        tostring(loss_seen),tostring(terminal_frame),tostring(stop_on_loss)))
end)
