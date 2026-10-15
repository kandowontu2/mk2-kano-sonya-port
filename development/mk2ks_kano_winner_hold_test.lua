-- Read-only winner observer, following the ordinary input-driven finish test.
dofile("mk2ks_finish_state_trace.lua")
assert(os.getenv("MK2_TRACE_NATIVE_FINISH") == "kano")
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
local program=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,ordinary,holds,fields,errors=0,0,0,0,0
local tracked,started,last
local expected_victim_pose=tonumber(os.getenv("MK2_TRACE_EXPECT_VICTIM_HELD_POSE") or "",16)
local expected_victim_id=tonumber(os.getenv("MK2_TRACE_EXPECT_VICTIM_ID") or "",16)
local victim_fields,victim_errors=0,0
assert((expected_victim_pose==nil)==(expected_victim_id==nil))
local function valid(pointer) return pointer>=0x01000000 and pointer<0x01100000 end
local tap=program:install_read_tap(0xffa162d0,0xffa162df,"Kano winner hold",function(offset)
    if offset~=0xffa162d0 or frame<600 then return end
    local own,task=cpu.A8.value,cpu.A13.value
    local expected=program:read_u32(side==1 and 0x01060220 or 0x01060df0)
    if own~=expected or not valid(own) or not valid(task) or program:read_u16(own+0x1f0)~=17 then return end
    local child=program:read_u32(task+0x190)
    local pose=program:read_u32(own+0x1d0)
    local child_pose=valid(child) and program:read_u32(child+0x1d0) or 0
    if child_pose==0xfe9b2490 then
        holds=holds+1
        if pose~=0xfe9b2810 then errors=errors+1 end
        tracked={own=own,child=child,victim=program:read_u32(side==1 and 0x01060df0 or 0x01060220)}
        started=frame
    elseif pose==0xff012560 then
        ordinary=ordinary+1
    end
    print(string.format("MK2_KANO_WINNER_JOIN frame=%d side=%d pose=%08X child_pose=%08X ordinary=%d holds=%d errors=%d",
        frame,side,pose,child_pose,ordinary,holds,errors))
end)
emu.register_frame(function()
    frame=frame+1
    if not tracked then return end
    -- 01061B00 is the winner/finish state (1=P1, 2=P2, 3=finish prompt),
    -- despite the older finish trace's historical "mode" label. 010601F0
    -- is P1 participation state, not a winner flag. The native scene changes
    -- during winner/continue processing: bound this observation by the exact
    -- winner actor's published lifetime, not an assumed scene enum.
    local winner=program:read_u16(0x01061b00)
    local scene=program:read_u16(0x010601d0)
    local current=program:read_u32(side==1 and 0x01060220 or 0x01060df0)
    if (winner~=side and winner~=3) or current~=tracked.own or frame-started>600 then
        print(string.format("MK2_KANO_WINNER_HOLD_END frame=%d age=%d winner=%d scene=%d current=%08X original=%08X",
            frame,frame-started,winner,scene,current,tracked.own))
        tracked=nil return
    end
    local own,child=tracked.own,tracked.child
    if program:read_u16(own+0x1f0)~=17 or program:read_u32(child+0x1d0)~=0xfe9b2490 then
        tracked=nil return
    end
    local pose=program:read_u32(own+0x1d0)
    fields=fields+1
    if pose~=0xfe9b2810 then errors=errors+1 end
    if expected_victim_pose then
        victim_fields=victim_fields+1
        local victim=tracked.victim
        local current_victim=program:read_u32(side==1 and 0x01060df0 or 0x01060220)
        local health=program:read_u16(side==1 and 0x01060ec0 or 0x010602f0)
        if not valid(victim) or current_victim~=victim or health~=0 or
            program:read_u32(victim+0x1d0)~=expected_victim_pose or
            program:read_u16(victim+0x1f0)~=expected_victim_id then
            victim_errors=victim_errors+1
        end
    end
    local age=frame-started
    if pose~=last or age%40==0 then
        print(string.format("MK2_KANO_WINNER_HOLD frame=%d age=%d winner=%d scene=%d pose=%08X fields=%d errors=%d",
            frame,age,winner,scene,pose,fields,errors))
        last=pose
    end
    if age==0 or age==40 or age==80 then
        manager.machine.screens[":screen"]:snapshot(string.format("kano_winner_hold_%03d.png",age))
    end
end)
emu.register_stop(function()
    local passed=ordinary>=1 and holds==1 and fields>=80 and errors==0
    print(string.format("MK2_KANO_WINNER_HOLD_RESULT pass=%s side=%d ordinary=%d holds=%d fields=%d errors=%d",
        tostring(passed),side,ordinary,holds,fields,errors))
    if expected_victim_pose then
        print(string.format("MK2_KANO_VICTIM_HOLD_RESULT pass=%s id=%04X expected=%08X fields=%d errors=%d",
            tostring(victim_fields>=80 and victim_errors==0),expected_victim_id,
            expected_victim_pose,victim_fields,victim_errors))
    end
    tap:remove()
end)
