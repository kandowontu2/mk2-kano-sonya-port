-- Observe native impact delivery and camera-task lifetime; never alter game state.
local driver=os.getenv("MK2KS_BICYCLE_FEEDBACK_DRIVER") or "single"
local scripts={single="mk2ks_bicycle_test.lua",rounds="mk2ks_bicycle_lifecycle_test.lua",interrupt="mk2ks_bicycle_interrupt_test.lua"}
dofile(assert(scripts[driver]))
local side=tonumber(os.getenv("MK2KS_BICYCLE_SIDE") or "1")
local frame,program,cpu,current=0,nil,nil,nil
local pointers={0x01060220,0x01060df0}
local taps,actions={},{}
local active_impact,pending_delivery,pending_camera
local grounded_camera
local errors=0
local function check(value,label)
    if not value then errors=errors+1;if errors<=40 then print("MK2KS_BICYCLE_FEEDBACK_ERROR "..label) end end
end
local function own() return program:read_u32(pointers[side]) end
local function caller_between(first,last)
    local caller=program:read_u32(cpu.state.SP.value)
    return caller>=first and caller<last
end
local function tap(address,label,callback)
    taps[#taps+1]=program:install_read_tap(address,address+15,label,callback)
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        tap(0xfff9a400,"feedback bicycle entry",function()
            if frame<900 or cpu.state.A8.value~=own() then return end
            current={entry=frame,ticks={},impacts={},deliveries={},starts={},stops={},steps={},camera_writes=0,
                camera_base=grounded_camera,camera_entry=program:read_u32(0x0105d130)}
            actions[#actions+1]=current
        end)
        tap(0xfff9d000,"feedback bicycle paired tick",function()
            if current and cpu.state.A8.value==own() then current.ticks[#current.ticks+1]=frame end
        end)
        tap(0xffa11ea0,"native paired bicycle impact",function()
            if not caller_between(0xfff9d000,0xfff9d800) then return end
            check(current and cpu.state.A8.value==own(),"impact belongs to actual bicycling Sonya")
            if not current then return end
            active_impact={frame=frame}
            current.impacts[#current.impacts+1]=active_impact
            print("MK2KS_BICYCLE_FEEDBACK_IMPACT frame="..frame)
        end)
        tap(0xffa12530,"bicycle impact sound selection",function()
            if not active_impact or active_impact.frame~=frame then return end
            local command=cpu.state.A0.value
            check(command==0x14 or command==0x15,"native hard-hit effect, not a fighter voice")
            check(cpu.state.A8.value==own(),"sound actor remains actual Sonya")
            active_impact.command=command
        end)
        tap(0xffa13ba0,"bicycle impact DCS delivery",function()
            if not active_impact or active_impact.frame~=frame or not active_impact.command then return end
            local base=program:read_u16(0xffa0ef20+active_impact.command*32+16)
            local code=cpu.state.A3.value&0xffff
            check(code>=base and code<=base+2,"native effect record/channel selected")
            pending_delivery={frame=frame,code=code,bytes={}}
            current.deliveries[#current.deliveries+1]=pending_delivery
            active_impact=nil
        end)
        taps[#taps+1]=program:install_write_tap(0x01d01030,0x01d0103f,"bicycle DCS hardware bytes",function(offset,data)
            if pending_delivery and pending_delivery.frame==frame and #pending_delivery.bytes<2 then
                pending_delivery.bytes[#pending_delivery.bytes+1]=data&255
            end
        end)
        tap(0xff9e1290,"bicycle native camera shake",function()
            if not caller_between(0xfff9a400,0xfff9d000) then return end
            check(current and cpu.state.A8.value==own(),"camera effect belongs to actual bicycle")
            if not current then return end
            check(cpu.state.A11.value==0x30030,"original three-pixel, 48 half-cycle shake recipe")
            current.starts[#current.starts+1]=frame
            print("MK2KS_BICYCLE_FEEDBACK_SHAKE frame="..frame)
        end)
        tap(0xff840020,"native bicycle shake task removal",function()
            if not current or cpu.state.A0.value~=0x103 or cpu.state.A8.value~=own() then return end
            -- FF9E1290 creates through FF840070; that helper, not the shake
            -- wrapper itself, calls the native replacement/removal routine.
            local creating=current.starts[#current.starts]==frame and caller_between(0xff840070,0xff8400d0)
            if not caller_between(0xfff9a400,0xfff9d000) and not creating then return end
            current.stops[#current.stops+1]=frame
            print("MK2KS_BICYCLE_FEEDBACK_STOP frame="..frame)
        end)
        tap(0xff9e1390,"native bicycle camera step",function()
            if not current or #current.starts==0 or cpu.state.A8.value~=own() then return end
            local amount=cpu.state.A11.value
            current.steps[#current.steps+1]={frame=frame,amount=amount}
            pending_camera={frame=frame,value=(program:read_u32(0x0105d130)-amount)&0xffffffff}
        end)
        taps[#taps+1]=program:install_write_tap(0x0105d130,0x0105d14f,"native camera displacement",function(offset,data,mask)
            if pending_camera and pending_camera.frame==frame and cpu.state.PC.value>=0xff9e13d0 and cpu.state.PC.value<=0xff9e1400 then
                local expected=(pending_camera.value>>(offset-0x0105d130))&0xffff
                check((data&mask)==(expected&mask),"camera task writes the actual three-pixel displacement")
                current.camera_writes=current.camera_writes+1
            end
        end)
        tap(0xfff9e000,"feedback bicycle victim release",function()
            if current and cpu.state.A8.value==program:read_u32(pointers[3-side]) then current.release=frame end
        end)
    end
    if frame>1200 then
        local grounded=true
        for index,pointer in ipairs(pointers) do
            local actor=program:read_u32(pointer)
            local process=program:read_u32(index==1 and 0x01060260 or 0x01060e30)
            grounded=grounded and actor~=0 and process~=0 and
                program:read_u16(actor+0xb0)==program:read_u16(process+0x200) and
                program:read_u32(actor+0x60)==0 and program:read_u32(actor+0x20)==0
        end
        if grounded then grounded_camera=program:read_u32(0x0105d130) end
    end
    if current and frame==current.entry+220 then
        current.recovered=true
        local recovered_camera=program:read_u32(0x0105d130)
        check(current.camera_base~=nil and recovered_camera==current.camera_base,"native camera returns to its grounded baseline")
        print(string.format("MK2KS_BICYCLE_FEEDBACK_CAMERA entry=%08X grounded=%08X recovered=%08X",
            current.camera_entry,current.camera_base or 0,recovered_camera))
    end
end)
emu.register_stop(function()
    local total_ticks,total_impacts,total_deliveries,total_steps=0,0,0,0
    for _,action in ipairs(actions) do
        local paired=#action.ticks>0
        local expected=math.ceil(#action.ticks/7)
        check(action.recovered,"feedback observed through full recovery")
        check(#action.impacts==expected and #action.deliveries==expected,"exact paired impact and DCS-delivery count")
        check(#action.starts==(paired and 1 or 0) and #action.stops==(paired and 2 or 0),"native camera task created/replaced then stopped only on a hit")
        for index,impact in ipairs(action.impacts) do
            check(impact.frame==action.ticks[1]+(index-1)*7,"original first-field and seven-field impact cadence")
        end
        for _,delivery in ipairs(action.deliveries) do
            check(#delivery.bytes==2 and delivery.bytes[1]==delivery.code>>8 and delivery.bytes[2]==(delivery.code&255),"both actual DCS command bytes transmitted")
        end
        if paired then
            -- The owner stops the camera on its final paired tick. Native
            -- task ordering runs P1's victim handoff one field later; P2's
            -- victim runs in the same field. Neither may keep the shake alive.
            check(action.stops[2]==action.ticks[#action.ticks],"camera task removed on final paired field")
            check(action.release and action.stops[2] and action.release>=action.stops[2] and
                action.release<=action.stops[2]+1,"victim release follows native same/next-field task ordering")
            check(#action.steps>=math.floor(#action.ticks/3) and #action.steps<=math.ceil(#action.ticks/3)+1,"bounded native camera-step count")
            check(action.camera_writes==#action.steps*2,"both words of every native camera displacement observed")
        else check(#action.steps==0 and action.camera_writes==0,"no paired shake on miss/block/interrupted startup") end
        for index,step in ipairs(action.steps) do
            check(step.amount==(index%2==1 and 3 or 0xfffffffd),"alternating three-pixel camera amplitude")
            if index>1 then check(step.frame-action.steps[index-1].frame==3,"original three-field camera cadence") end
            check(action.stops[2] and step.frame<=action.stops[2],"no lingering camera task after owner stops it")
        end
        total_ticks=total_ticks+#action.ticks;total_impacts=total_impacts+#action.impacts
        total_deliveries=total_deliveries+#action.deliveries;total_steps=total_steps+#action.steps
    end
    print(string.format("MK2KS_BICYCLE_FEEDBACK_RESULT pass=%s driver=%s side=%d actions=%d ticks=%d impacts=%d deliveries=%d camera_steps=%d errors=%d",
        tostring(errors==0),driver,side,#actions,total_ticks,total_impacts,total_deliveries,total_steps,errors))
    for _,handle in ipairs(taps) do handle:remove() end
end)
