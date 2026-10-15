-- Read-only first-cyan-field palette/DMA trace, not a rendering workaround.
dofile("mk2ks_p2_campaign_probe.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local screen=manager.machine.screens[":screen"]
local frame,first,entry=0,nil,nil
local palette,draws,registers,taps={},{},{},{}
local function push(items,item,limit)
    items[#items+1]=item
    if #items>limit then table.remove(items,1) end
end
local function active()
    return not first and p:read_u16(0x01061b30)==1 and p:read_u16(0x01060dc0)==1
end
taps[1]=p:install_write_tap(0x01800000,0x0187ffff,"cyan palette provenance",function(at,value,mask)
    if not active() then return end
    push(palette,string.format("MK2_CYAN_PALETTE_WRITE frame=%d address=%08X old=%04X value=%04X mask=%04X pc=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X caller=%08X",
        frame,at,p:read_u16(at),value&0xffff,mask&0xffff,cpu.PC.value,cpu.A0.value,cpu.A1.value,
        cpu.A2.value,cpu.A8.value,cpu.A13.value,p:read_u32(cpu.SP.value)),2048)
end)
taps[2]=p:install_write_tap(0x01a80000,0x01a800ff,"cyan DMA provenance",function(at,value,mask)
    local r=(at-0x01a80000)//16
    registers[r]=((registers[r] or 0)&(~mask))|(value&mask)
    if r==1 and value&0x8000~=0 and active() then
        push(draws,string.format("MK2_CYAN_DMA frame=%d source=%08X xy=%d,%d wh=%d,%d command=%04X palette=%04X color=%04X pc=%08X a8=%08X a13=%08X",
            frame,(registers[2] or 0)|((registers[3] or 0)<<16),registers[4] or 0,registers[5] or 0,
            registers[6] or 0,registers[7] or 0,value&0xffff,registers[8] or 0,registers[9] or 0,
            cpu.PC.value,cpu.A8.value,cpu.A13.value),256)
    end
end)
taps[3]=p:install_read_tap(0xff80c6b0,0xff80c6bf,"cyan palette queue producer",function(at)
    if at~=0xff80c6b0 or not active() then return end
    local source,pen,count=cpu.A0.value,cpu.A1.value&0xffff,cpu.A2.value&0xffff
    if count>256 or source<0x01000000 then
        local stack={}
        for i=0,7 do stack[#stack+1]=string.format("%08X",p:read_u32(cpu.SP.value+i*32)) end
        print(string.format("MK2_CYAN_BAD_ENQUEUE frame=%d source=%08X pen=%04X count=%d pc=%08X a8=%08X a9=%08X a13=%08X stack=%s",
            frame,source,pen,count,cpu.PC.value,cpu.A8.value,cpu.A9.value,cpu.A13.value,table.concat(stack,",")))
    end
end)
taps[4]=p:install_read_tap(0xff80c8a0,0xff80c8af,"cyan palette queue consumer",function(at)
    if at~=0xff80c8a0 or not active() then return end
    local queue=cpu.A0.value
    local source,pen,count=p:read_u32(queue),p:read_u16(queue+32),p:read_u16(queue+48)
    if count>256 or source<0x01000000 then
        print(string.format("MK2_CYAN_BAD_COPY frame=%d queue=%08X source=%08X pen=%04X count=%d",frame,queue,source,pen,count))
    end
end)
emu.register_frame(function()
    frame=frame+1
    assert(#taps==4)
    if active() then
        entry=entry or frame
        local pixels,width=screen:pixels()
        local colors={}
        local matches=0
        for _,point in ipairs({{10,100},{200,100},{390,100},{200,200}}) do
            local value=string.unpack("<I4",pixels,(point[2]*width+point[1])*4+1)&0xffffff
            colors[#colors+1]=string.format("%06X",value)
            if value==0x7bceff then matches=matches+1 end
        end
        if frame%30==0 then
            print(string.format("MK2_CYAN_BEFORE frame=%d mode=%d colors=%s",frame,p:read_u16(0x010601d0),table.concat(colors,",")))
            screen:snapshot(string.format("cyan_before_%05d.png",frame))
        end
        if matches>=3 then
            first=frame
            print(string.format("MK2_CYAN_FIRST frame=%d entry=%d mode=%d colors=%s actors=%08X,%08X flags=%04X,%04X",
                frame,entry,p:read_u16(0x010601d0),table.concat(colors,","),p:read_u32(0x01060220),
                p:read_u32(0x01060df0),p:read_u16(p:read_u32(0x01060220)+0x160),
                p:read_u16(p:read_u32(0x01060df0)+0x160)))
            for _,row in ipairs(palette) do print(row) end
            for _,row in ipairs(draws) do print(row) end
            for pen=0,32767 do
                if p:read_u16(0x01800000+pen*16)&0x7fff==0x3f3f then
                    print(string.format("MK2_CYAN_PEN frame=%d pen=%04X address=%08X",frame,pen,0x01800000+pen*16))
                end
            end
            screen:snapshot("cyan_first.png")
        end
    elseif first and (frame==first+30 or frame==first+120) then
        screen:snapshot(string.format("cyan_after_%03d.png",frame-first))
    end
end)
emu.register_stop(function()
    print(string.format("MK2_CYAN_TRACE_RESULT found=%s first=%s entry=%s writes=0 scope=read_only_render_provenance",
        tostring(first~=nil),tostring(first),tostring(entry)))
end)
