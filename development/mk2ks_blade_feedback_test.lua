-- Extend the real-input blade test; never write game memory or render effects.
dofile("mk2ks_blade_test.lua")
local side=tonumber(os.getenv("MK2KS_BLADE_SIDE") or "1")
local mode=os.getenv("MK2KS_BLADE_MODE") or "near"
local hit=mode=="near" or mode=="duck" or mode=="air"
local frame,entry,hurt=0,nil,nil
local cpu,program,taps=nil,nil,{}
local pointers={0x01060220,0x01060df0}
local errors,requests,starts,allocations,insertions,cleanups,palette_checks=0,0,0,0,0,0,0
local objects,sounds={},{}
local checked_recovery=false
local swishes,cuts,grunts,deliveries=0,0,0,{}
local active_sound,pending_delivery
local function check(value,label)
    if not value then errors=errors+1;print("MK2KS_BLADE_FEEDBACK_ERROR "..label) end
end
local function actor(index) return program:read_u32(pointers[index]) end
local function tap(address,label,callback)
    taps[#taps+1]=program:install_read_tap(address,address+15,label,callback)
end
emu.register_frame(function()
    frame=frame+1
    if not program then
        cpu=manager.machine.devices[":maincpu"];program=cpu.spaces.program
        tap(0xfff8cc00,"feedback blade entry",function()
            if frame>900 and cpu.state.A8.value==actor(side) and not entry then entry=frame end
        end)
        tap(0xfff90000,"feedback blade victim",function()
            if entry and frame<=entry+20 then
                check(cpu.state.A8.value==actor(3-side),"reaction belongs to actual victim")
                hurt=frame
            end
        end)
        tap(0xff9a5b00,"blade native blood request",function()
            if not entry or frame>entry+20 then return end
            requests=requests+1
            check(hurt==frame,"blood requested only by actual blade hit")
            check(cpu.state.A0.value==1,"original blood recipe index")
            check(cpu.state.A8.value==actor(3-side),"blood source is actual victim")
            check(program:read_u16(0x01061a60)==0,"normal arcade blood setting enabled")
            print(string.format("MK2KS_BLADE_BLOOD_REQUEST frame=%d type=%d victim=%08X",frame,cpu.state.A0.value,cpu.state.A8.value))
        end)
        tap(0xff9a7f70,"blade native blood task",function()
            if entry and frame<=entry+25 then
                starts=starts+1
                check(cpu.state.A8.value==actor(3-side),"native task inherits actual victim")
            end
        end)
        tap(0xff9aff00,"blade blood allocated",function()
            if not entry or frame>entry+25 then return end
            local object=cpu.state.A8.value
            check(cpu.state.A11.value==actor(3-side),"native blood object source")
            check(program:read_u32(object+0x1a0)==0xffbe9030,"unmodified stock blood frame")
            check(not objects[object],"separate native blood object allocation")
            objects[object]={created=frame,process=cpu.state.A13.value}
            allocations=allocations+1
            print(string.format("MK2KS_BLADE_BLOOD_OBJECT frame=%d object=%08X process=%08X",frame,object,cpu.state.A13.value))
        end)
        tap(0xff83f610,"blade blood inserted",function()
            local object=objects[cpu.state.A8.value]
            if object and not object.inserted then object.inserted=frame;insertions=insertions+1 end
        end)
        tap(0xff9b0e50,"blade blood native cleanup",function()
            local object=objects[cpu.state.A8.value]
            if object and not object.cleaned then object.cleaned=frame;cleanups=cleanups+1 end
        end)
        tap(0xffa12530,"blade sound observation",function()
            if entry and frame>=entry and frame<=entry+50 then
                local command=cpu.state.A0.value
                sounds[#sounds+1]=command
                if command==0xc8 or command==0x44 then
                    active_sound={command=command,frame=frame,actor=cpu.state.A8.value}
                    if command==0xc8 then
                        swishes=swishes+1
                        check(frame==entry and cpu.state.A8.value==actor(side),"one own entry-field weapon swish")
                    else
                        cuts=cuts+1
                        check(frame==hurt and cpu.state.A8.value==actor(3-side),"cut belongs to actual contact and victim")
                    end
                else active_sound=nil end
                print(string.format("MK2KS_BLADE_SOUND frame=%d command=%04X actor=%08X",frame,cpu.state.A0.value,cpu.state.A8.value))
            end
        end)
        for _,address in ipairs({0xffa11fd0,0xffa11ee0}) do
            tap(address,"blade native victim grunt",function()
                if hurt==frame and cpu.state.A8.value==actor(3-side) then
                    grunts=grunts+1
                    check(address==(mode=="air" and 0xffa11ee0 or 0xffa11fd0),"native ground/air hurt-grunt category")
                end
            end)
        end
        tap(0xffa13ba0,"blade native DCS delivery",function()
            if not active_sound or active_sound.frame~=frame then return end
            local command=active_sound.command
            local base=program:read_u16(0xffa0ef20+command*32+16)
            local code=cpu.state.A3.value&0xffff
            check(code>=base and code<=base+2,"native sound record and channel selected")
            pending_delivery={command=command,frame=frame,code=code,bytes={}}
            deliveries[#deliveries+1]=pending_delivery
            active_sound=nil
        end)
        taps[#taps+1]=program:install_write_tap(0x01d01030,0x01d0103f,"observe blade DCS command bytes",function(offset,data,mask)
            if pending_delivery and pending_delivery.frame==frame and #pending_delivery.bytes<2 then
                pending_delivery.bytes[#pending_delivery.bytes+1]=data&0xff
            end
        end)
    end
    if not entry then return end
    if hurt and frame==hurt+5 then
        local visible={}
        local cursor,count=program:read_u32(0x0105d480),0
        while cursor~=0 and count<1024 do visible[cursor]=true;cursor=program:read_u32(cursor);count=count+1 end
        check(count<1024,"native display list terminates")
        local source=0xffaf2a40
        local colors=program:read_u16(source)
        check(colors==15,"original palette has fifteen entries including transparent zero")
        for object,data in pairs(objects) do
            check(visible[object],"blood object in real display list")
            local palette=program:read_u16(object+0x140)&0x7f00
            for color=1,colors-1 do
                check((program:read_u16(0x01800000+(palette+color)*16)&0x7fff)==
                    (program:read_u16(source+16+color*16)&0x7fff),"native blood palette color "..color)
                palette_checks=palette_checks+1
            end
        end
        manager.machine.video:snapshot()
    end
    if hurt and (frame==hurt+1 or frame==hurt+12 or frame==hurt+30) then manager.machine.video:snapshot() end
    if frame==entry+180 then
        checked_recovery=true
        local cursor,count=program:read_u32(0x0105d480),0
        while cursor~=0 and count<1024 do
            check(not objects[cursor],"blood object removed from recovered display list")
            cursor=program:read_u32(cursor);count=count+1
        end
        check(count<1024,"recovered display list terminates")
        for _,data in pairs(objects) do check(data.cleaned and data.cleaned<frame,"native blood cleanup completed") end
    end
end)
emu.register_stop(function()
    check(entry and checked_recovery,"completed blade and recovery observation")
    check(requests==(hit and 1 or 0) and starts==(hit and 1 or 0),"one native recipe on hit, none on block/miss")
    check(allocations==(hit and 8 or 0) and insertions==allocations,"six particles and two splashes, all inserted")
    check(cleanups==allocations,"all blood objects use native cleanup")
    check(palette_checks==(hit and 112 or 0),"all native blood palette colors verified")
    check(swishes==1 and cuts==(hit and 1 or 0),"native swish always; cutting sound only on hit")
    check(grunts==(hit and 1 or 0),"one native victim grunt at contact")
    check(#deliveries==(hit and 2 or 1),"weapon sounds delivered to native DCS device")
    for _,delivery in ipairs(deliveries) do
        check(#delivery.bytes==2 and delivery.bytes[1]==delivery.code>>8 and delivery.bytes[2]==(delivery.code&255),
            "both bytes of native DCS sound command transmitted")
    end
    print(string.format("MK2KS_BLADE_FEEDBACK_RESULT pass=%s mode=%s side=%d requests=%d starts=%d allocations=%d insertions=%d cleanups=%d palette_checks=%d swishes=%d cuts=%d grunts=%d deliveries=%d sounds=%d errors=%d",
        tostring(errors==0),mode,side,requests,starts,allocations,insertions,cleanups,palette_checks,swishes,cuts,grunts,#deliveries,#sounds,errors))
    for _,handle in ipairs(taps) do handle:remove() end
end)
