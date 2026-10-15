-- Read-only native cache/DMA/palette evidence for complete body and effects.
-- Capture all draws during the releases so foreground overdraw is observable.
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local frame,collecting,taps,active,registers,palettes,ordinal=0,false,{}, {}, {}, {},0
local slots={{actor=0x01060220,main=0x01060260},{actor=0x01060df0,main=0x01060e30}}
local release={}
for _,g in ipairs({0xfe82f400,0xfe82f460,0xfe82f4c0,0xfe82f520,0xfe82f580,0xfe82f5e0,0xfe82f640,0xfe82f6a0,
                  0xfe83dbe0,0xfe83dc40,0xfe83dca0,0xfe83dd00,0xfe83dec0}) do release[g]=true end
local function valid(v)return v>=0x01000000 and v<0x01100000 end
local function signed(v)return v>=0x8000 and v-0x10000 or v end
local function live()
    for _,start in pairs(active) do if frame<=start+65 then return true end end
    return false
end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,"complete native release drawing",function(at,data)
    if collecting then return end
    local reg=(at-0x01a80000)//16;registers[reg]=data&0xffff
    if reg~=1 or (data&0x8000)==0 or not live() then return end
    collecting=true;ordinal=ordinal+1
    local bank=(registers[8] or 0)&0x7f00
    local colors={}
    for i=0,63 do colors[#colors+1]=string.format("%04X",p:read_u16(0x01800000+(bank+i)*16)) end
    local color_words=table.concat(colors,",")
    if palettes[bank]~=color_words then
        palettes[bank]=color_words
        print(string.format("MK2_RENDER_PALETTE frame=%d ordinal=%d bank=%04X colors=%s writes=0",frame,ordinal,bank,color_words))
    end
    print(string.format("MK2_RENDER_DMA frame=%d ordinal=%d pc=%08X graphic=%08X command=%04X x=%d y=%d width=%d height=%d palette=%04X color=%04X scale_x=%04X scale_y=%04X lskip=%04X writes=0",
        frame,ordinal,cpu.PC.value,(registers[2] or 0)|((registers[3] or 0)<<16),data&0xffff,signed(registers[4] or 0),signed(registers[5] or 0),
        registers[6] or 0,registers[7] or 0,registers[8] or 0,registers[9] or 0,registers[10] or 0,registers[11] or 0,registers[0] or 0))
    -- The imported fighter's floor silhouette is projected in the native
    -- video handler after this body copy. Record the actual actor/cache/floor
    -- inputs, so a verifier cannot invent a dark rectangular occlusion.
    local graphic=(registers[2] or 0)|((registers[3] or 0)<<16)
    if graphic>=0x10000000 and graphic<0x1a000000 and (data&0x008f)==0x0082 and
       (registers[7] or 0)>=48 and (registers[7] or 0)<=200 and (registers[6] or 0)<=100 then
        for side,slot in ipairs(slots) do
            local actor,process=p:read_u32(slot.actor),p:read_u32(slot.main)
            if valid(actor) and valid(process) then
                local id,cache=p:read_u16(actor+0x1f0),p:read_u32(actor+0x1a0)
                if (id==17 or id==18) and valid(cache) then
                    for index=0,11 do
                        local entry=cache+index*0x70
                        if p:read_u32(entry)==graphic then
                            print(string.format("MK2_RENDER_SHADOW_SOURCE frame=%d ordinal=%d side=%d actor=%08X process=%08X id=%d index=%d graphic=%08X object_y=%d part_y=%d stage_y=%d floor_y=%d writes=0",
                                frame,ordinal,side,actor,process,id,index,graphic,signed(p:read_u16(actor+0xb0)),signed(p:read_u16(entry+0x60)),
                                signed(p:read_u16(0x0105ecd0)),signed(p:read_u16(process+0x200))))
                            break
                        end
                    end
                end
            end
        end
    end
    collecting=false
end)
emu.register_frame(function()
    collecting=true;frame=frame+1;ordinal=0
    if p:read_u16(0x010601d0)==2 and p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==1 then
        for side,slot in ipairs(slots) do
            local actor,process=p:read_u32(slot.actor),p:read_u32(slot.main)
            if valid(actor) and valid(process) then
                local pose=p:read_u32(actor+0x1d0)
                if release[pose] then
                    if not active[side] or frame>active[side]+65 then active[side]=frame end
                    local list=p:read_u32(actor+0x1a0);local count=0
                    for i=0,15 do
                        local descriptor=p:read_u32(pose+i*32)
                        if descriptor==0 then break end
                        local entry=list+i*0x70;count=count+1
                        print(string.format("MK2_RENDER_BODY_COMPONENT frame=%d side=%d actor=%08X process=%08X pose=%08X index=%d descriptor=%08X graphic=%08X command=%04X width=%d height=%d dx=%d dy=%d writes=0",
                            frame,side,actor,process,pose,i,descriptor,p:read_u32(entry),p:read_u16(entry+0x40),p:read_u16(entry+0x20),p:read_u16(entry+0x30),
                            signed(p:read_u16(entry+0x50)),signed(p:read_u16(entry+0x60))))
                    end
                    print(string.format("MK2_RENDER_BODY frame=%d side=%d actor=%08X process=%08X id=%d pose=%08X components=%d flags=%04X x=%d y=%d writes=0",
                        frame,side,actor,process,p:read_u16(actor+0x1f0),pose,count,p:read_u16(actor+0xf0),signed(p:read_u16(actor+0x90)),signed(p:read_u16(actor+0xb0))))
                end
            end
        end
    end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps) do tap:remove() end end)
dofile("mk2ks_projectile_choreography_probe.lua")
