-- Observe original MK3 bicycle feedback using the existing real-input capture.
dofile("mk3_bicycle_reference.lua")
local frame,entry,program,cpu=0,nil,nil,nil
local ticks,impacts,shakes,stops,taps={},{},{},{},{}
local start_value
mk3_bicycle_feedback_subscriptions={}
mk3_bicycle_feedback_subscriptions.frame=emu.add_machine_frame_notifier(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        for _,event in ipairs({{0xff9e4da0,"entry"},{0xff9e6040,"tick"},{0xffaa6680,"impact"},
                              {0xffaa2a20,"shake"},{0xff95fe70,"stop"}}) do
            taps[#taps+1]=program:install_read_tap(event[1],event[1]+15,"original bicycle feedback",function()
                if frame<3900 or frame>4200 or cpu.state.A8.value~=program:read_u32(0x010609b0) then return end
                local kind=event[2]
                if kind=="entry" then entry=frame end
                if not entry or (kind=="stop" and cpu.state.A0.value~=0x103) then return end
                if kind=="tick" then ticks[#ticks+1]=frame
                elseif kind=="impact" then impacts[#impacts+1]=frame
                elseif kind=="shake" then
                    shakes[#shakes+1]=frame;start_value=program:read_u16(0x0105d8a0)
                    assert(cpu.state.A11.value==0x30030,"original shake parameters")
                elseif kind=="stop" then stops[#stops+1]=frame end
                print(string.format("MK3_BICYCLE_FEEDBACK_EVENT frame=%d kind=%s A0=%08X A11=%08X screen_y=%04X",
                    frame,kind,cpu.state.A0.value,cpu.state.A11.value,program:read_u16(0x0105d8a0)))
            end)
        end
        taps[#taps+1]=program:install_write_tap(0x0105d8a0,0x0105d8af,"original bicycle shake displacement",function(offset,data)
            if entry and frame<=entry+180 then
                print(string.format("MK3_BICYCLE_FEEDBACK_SCREEN frame=%d value=%04X",frame,data&0xffff))
            end
        end)
    end
end)
mk3_bicycle_feedback_subscriptions.stop=emu.add_machine_stop_notifier(function()
    local mode=os.getenv("MK3_BICYCLE_TARGET") or "near"
    local hit=mode=="near" or mode=="air"
    assert(entry,"original bicycle entry observed")
    assert(#shakes==(hit and 1 or 0) and #stops==(hit and 2 or 0),"shake start replaces prior ID, release stops it")
    assert(#impacts==(hit and math.ceil(#ticks/7) or 0),"one impact per seven paired fields")
    for index,at in ipairs(impacts) do assert(at==ticks[1]+(index-1)*7,"exact original impact cadence") end
    print(string.format("MK3_BICYCLE_FEEDBACK_RESULT pass=true mode=%s ticks=%d impacts=%d shakes=%d stops=%d screen_start=%04X screen_final=%04X",
        mode,#ticks,#impacts,#shakes,#stops,start_value or 0,program:read_u16(0x0105d8a0)))
    for _,tap in ipairs(taps) do tap:remove() end
end)
