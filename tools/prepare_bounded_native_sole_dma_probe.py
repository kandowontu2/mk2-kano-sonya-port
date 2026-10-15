"""Sparse actual opaque DMA contact coordinates, matched to native caches."""
import prepare_bounded_native_stance_bounds_short_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.prior.ROOT/'audit_bounded_native_sole_dma_preparation'
scope['TAIL']+=r'''
local sole_dma_count=0
local sole_dma_tap=selection_p:install_write_tap(0x01a80010,0x01a8001f,
    'bounded actual opaque body DMA',function(at,data,mask)
    if not first_live or at~=0x01a80010 then return end
    local age=selection_frame-first_live
    if age~=8 and age~=16 and age~=24 and age~=32 then return end
    local command=data&0xffff
    if command&15~=2 then return end
    local function reg(n)return selection_p:read_u16(0x01a80000+n*16)end
    local palette=reg(8);local slot=palette==0x200 and 1 or (palette==0x300 and 2 or nil)
    if not slot then return end
    local s=assert(bounded_actor(slot));local cache=selection_p:read_u32(s.a+0x1a0)
    local source=reg(2)|(reg(3)<<16);local w,h=reg(6)&0x3ff,reg(7)&0x3ff
    local part=nil
    for index=0,11 do
        local row=cache+index*112;local graphic=selection_p:read_u32(row)
        if graphic==0 then break end
        if graphic==source and selection_p:read_u16(row+0x20)==w and selection_p:read_u16(row+0x30)==h then part=index;break end
    end
    if not part then return end
    local opaque,top,bottom,bits=opaque_bounds(source,w,h,command)
    sole_dma_count=sole_dma_count+1
    print(string.format('MK2_BOUNDED_SOLE_DMA frame=%d age=%d slot=%d id=%d part=%d source=%08X command=%04X palette=%04X width=%d height=%d x=%d y=%d opaque=%d top=%d bottom=%d opaque_bottom_y=%d stage_floor=%d actor_y=%d floor=%d action=%04X pc=%08X writes=0',
        selection_frame,age,slot,s.id,part,source,command,palette,w,h,reg(4)&0x3ff,reg(5)&0x1ff,opaque,top,bottom,
        ((reg(5)&0x1ff)+bottom)&0x1ff,selection_p:read_i16(0x0105ecd0),s.y,s.floor,s.action,
        manager.machine.devices[':maincpu'].state.PC.value))
end)
emu.register_stop(function()
    assert(sole_dma_tap,'Native body DMA tap retained')
    print(string.format('MK2_BOUNDED_SOLE_DMA_TERMINAL copies=%d writes=0',sole_dma_count))
end)
'''
exec(compile(old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
