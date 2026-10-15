"""One-field tagged-body inventory without palette or late-cache filtering."""
from types import FunctionType
import prepare_bounded_native_sole_fifo_probe as old
scope=dict(old.scope)
scope['OUT']=old.scope['ROOT']/'audit_bounded_native_entrance_dma_preparation'
scope['TAIL']+=r'''
local entrance_copies=0
local entrance_tap=selection_p:install_write_tap(0x01a80010,0x01a8001f,
    'unfiltered tagged entrance body commands',function(at,data,mask)
    if not first_live or selection_frame-first_live~=8 or at~=0x01a80010 then return end
    local function reg(n)return selection_p:read_u16(0x01a80000+n*16)end
    local source=reg(2)|(reg(3)<<16)
    if source<0x10000000 or source>=0x1a000000 then return end
    local command=data&0xffff;if command&15~=2 then return end
    entrance_copies=entrance_copies+1;assert(entrance_copies<=16)
    print(string.format('MK2_BOUNDED_ENTRANCE_DMA frame=%d source=%08X width=%d height=%d x=%d y=%d command=%04X raw_palette=%04X bank=%04X pc=%08X writes=0',
        selection_frame,source,reg(6)&0x3ff,reg(7)&0x3ff,reg(4)&0x3ff,reg(5)&0x1ff,command,reg(8),reg(8)&0x7f00,
        manager.machine.devices[':maincpu'].state.PC.value))
end)
emu.register_stop(function()
    assert(entrance_tap,'Unfiltered entrance observer retained')
    print(string.format('MK2_BOUNDED_ENTRANCE_TERMINAL copies=%d writes=0',entrance_copies))
end)
'''
main=FunctionType(old.scope['main'].__code__,scope)
if __name__=='__main__':main()
