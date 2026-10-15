-- Read-only gate observer. Reused harness supplies normal approach/commands
-- and native round damage, never forced positions or actions.
dofile("mk2ks_finish_state_trace.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
local fighter=assert(os.getenv("MK2_TRACE_NATIVE_FINISH"))
local expected=os.getenv("MK2_RANGE_EXPECT") or "activate"
local multiple_finishes=os.getenv("MK2_RANGE_MULTIPLE_FINISHES")=="1"
assert(expected=="activate" or expected=="reject")
local identity=fighter=="kano" and 17 or 18
local action=fighter=="kano" and 0xfffaaE00 or 0xfffab200
local bound=fighter=="kano" and 80 or 128
local own_pointer=side==1 and 0x01060220 or 0x01060df0
local frame,gate_count,action_count,errors,last_gate,first_action=0,0,0,0,nil,nil
local function own_actor()
    local own=p:read_u32(own_pointer)
    return own>=0x01000000 and own<0x01100000 and p:read_u16(own+0x1f0)==identity and own or nil
end
local taps={}
taps[1]=p:install_read_tap(0xff876fa0,0xff876faf,"individual fatality range compare",function(offset)
    if offset~=0xff876fa0 or cpu.A7.value~=action or cpu.A8.value~=own_actor() then return end
    gate_count=gate_count+1
    local distance,limit=cpu.A3.value,cpu.A1.value
    last_gate=frame
    if limit~=bound or (distance<=limit)~=(expected=="activate") then errors=errors+1 end
    print(string.format("MK2_RANGE_GATE frame=%d fighter=%s side=%d actor=%08X action=%08X distance=%d limit=%d expected=%s",
        frame,fighter,side,cpu.A8.value,cpu.A7.value,distance,limit,expected))
end)
taps[2]=p:install_read_tap(action,action+15,"individual fatality range action",function(offset)
    if offset~=action or cpu.A8.value~=own_actor() then return end
    action_count=action_count+1
    first_action=first_action or frame
    if expected~="activate" or not last_gate or frame-last_gate>2 then errors=errors+1 end
    print(string.format("MK2_RANGE_ACTION frame=%d fighter=%s side=%d actor=%08X",frame,fighter,side,cpu.A8.value))
end)
emu.register_frame(function()
    frame=frame+1
    assert(#taps==2,"Keep the code-observer taps owned for the entire run")
    if first_action then
        local age=frame-first_action
        local capture=fighter=="kano" and (age==30 or age==90) or
            fighter=="sonya" and (age>=90 and age<=132 and age%6==0 or age==145)
        if capture then
            manager.machine.screens[":screen"]:snapshot(string.format("range_%s_side%d_action_%03d.png",fighter,side,age))
            print(string.format("MK2_RANGE_RENDER frame=%d action_age=%d",frame,age))
        end
    end
end)
emu.register_stop(function()
    local passed=gate_count>=1 and errors==0 and last_gate and frame-last_gate>=180 and
        ((expected=="activate" and action_count==gate_count and
            (action_count==1 or multiple_finishes and action_count>=1)) or (expected=="reject" and action_count==0))
    print(string.format("MK2_RANGE_RESULT pass=%s fighter=%s side=%d expected=%s gates=%d actions=%d errors=%d observed_after_gate=%d multiple_finishes=%s",
        tostring(not not passed),fighter,side,expected,gate_count,action_count,errors,last_gate and frame-last_gate or -1,
        tostring(multiple_finishes)))
end)
