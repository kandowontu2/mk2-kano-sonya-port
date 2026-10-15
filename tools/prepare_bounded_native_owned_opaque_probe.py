"""Event-time FIFO ownership for every actual sparse opaque body copy."""
from types import FunctionType
import prepare_bounded_native_entrance_dma_probe as old
scope=dict(old.scope)
scope['OUT']=old.scope['ROOT']/'audit_bounded_native_owned_opaque_preparation'
tail=scope['TAIL']
marker='local sole_queue_count=0'
assert tail.count(marker)==1
tail=tail.replace(marker,'local owned_opaque_fifo={}\n'+marker,1)
marker='            sole_queue_count=sole_queue_count+1'
assert tail.count(marker)==1
tail=tail.replace(marker,marker+r'''
            local size,xy,cmd=regs.A9.value,regs.A10.value,(regs.A12.value>>16)&0xffff
            local key=string.format('%d_%08X_%d_%d_%04X_%d_%d',selection_frame,regs.A11.value,
                size&0x3ff,(size>>16)&0x3ff,cmd,xy&0x3ff,(xy>>16)&0x1ff)
            assert(not owned_opaque_fifo[key],'Unique actual publication')
            owned_opaque_fifo[key]={slot=slot,id=s.id,part=(row-cache)//112,actor=s.a,main=s.m,
                pose=selection_p:read_u32(s.a+0x1d0),actor_y=s.y,floor=s.floor,action=s.action}
''',1)
tail+=r'''
local owned_opaque_count=0
local owned_opaque_tap=selection_p:install_write_tap(0x01a80010,0x01a8001f,
    'actual FIFO-owned opaque copies',function(at,data,mask)
    if not first_live or at~=0x01a80010 then return end
    local function reg(n)return selection_p:read_u16(0x01a80000+n*16)end
    local source=reg(2)|(reg(3)<<16);local w,h=reg(6)&0x3ff,reg(7)&0x3ff
    local command=data&0xffff;local x,y=reg(4)&0x3ff,reg(5)&0x1ff
    local key=string.format('%d_%08X_%d_%d_%04X_%d_%d',selection_frame,source,w,h,command,x,y)
    local owner=owned_opaque_fifo[key];if not owner then return end
    local opaque,top,bottom,bits=opaque_bounds(source,w,h,command)
    owned_opaque_count=owned_opaque_count+1
    print(string.format('MK2_BOUNDED_OWNED_OPAQUE frame=%d slot=%d id=%d part=%d actor=%08X main=%08X pose=%08X source=%08X width=%d height=%d command=%04X bank=%04X x=%d y=%d opaque=%d top=%d bottom=%d bits=%d unclipped_opaque_bottom_y=%d actor_y=%d floor=%d action=%04X writes=0',
        selection_frame,owner.slot,owner.id,owner.part,owner.actor,owner.main,owner.pose,source,w,h,command,reg(8)&0x7f00,
        x,y,opaque,top,bottom,bits,(y+bottom)&0x1ff,owner.actor_y,owner.floor,owner.action))
    owned_opaque_fifo[key]=nil
end)
emu.register_stop(function()
    assert(owned_opaque_tap,'Actual opaque observer retained')
    print(string.format('MK2_BOUNDED_OWNED_OPAQUE_TERMINAL copies=%d writes=0',owned_opaque_count))
end)
'''
scope['TAIL']=tail
main=FunctionType(old.scope['main'].__code__,scope)
if __name__=='__main__':main()
