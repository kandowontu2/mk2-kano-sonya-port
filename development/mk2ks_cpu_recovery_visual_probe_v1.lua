-- Read-only display provenance for the natural CPU recovery fixture.
-- Keep the existing input-only scenario unchanged; observe native cached parts
-- and take callback snapshots separately from instruction-time snapshots.
dofile('mk2ks_cpu_recovery_probe_v5.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame=0
local dma={}
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'visual DMA provenance',function(at,data,mask)
    dma[at]=data&0xffff
    if at~=0x01a80010 or data&0x8000==0 or frame<1928 or frame>1991 then return end
    local source=(dma[0x01a80020]or 0)|((dma[0x01a80030]or 0)<<16)
    if source<0x10000000 or source>=0x1a000000 or data&0xf==8 then return end
    print(string.format('MK2_VISUAL_DMA frame=%d source=%08X command=%04X x=%d y=%d width=%d height=%d palette=%04X pc=%08X a8=%08X a13=%08X writes=0',
        frame,source,data&0xffff,dma[0x01a80040]or 0,dma[0x01a80050]or 0,dma[0x01a80060]or 0,dma[0x01a80070]or 0,dma[0x01a80080]or 0,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
emu.register_frame(function()
    frame=frame+1
    if frame<1928 or frame>1991 then return end
    for side,field in ipairs({0x01060220,0x01060df0})do
        local a=p:read_u32(field)
        local m=p:read_u32(field+0x40)
        if valid(a)and valid(m)then
            local list=p:read_u32(a+0x1a0)
            print(string.format('MK2_VISUAL_ACTOR frame=%d side=%d actor=%08X main=%08X pose=%08X list=%08X action=%d x=%d y=%d facing=%04X palette=%04X body=%04X writes=0',frame,side,a,m,p:read_u32(a+0x1d0),list,p:read_u16(m+0x1f0),p:read_i16(a+0x90),p:read_i16(a+0xb0),p:read_u16(a+0xf0),p:read_u16(a+0x140),p:read_u16(a+0x160)))
            if valid(list)then for part=0,7 do
                local at=list+part*0x70
                local source=p:read_u32(at)
                if source==0 then break end
                print(string.format('MK2_VISUAL_PART frame=%d side=%d part=%d source=%08X width=%d height=%d command=%04X dx=%d dy=%d writes=0',frame,side,part,source,p:read_u16(at+0x20),p:read_u16(at+0x30),p:read_u16(at+0x40),p:read_i16(at+0x50),p:read_i16(at+0x60)))
            end end
        end
    end
    if frame==1932 or frame==1962 or frame==1963 or frame==1970 or frame==1990 then
        manager.machine.screens[':screen']:snapshot(string.format('callback_%d.png',frame))
    end
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
