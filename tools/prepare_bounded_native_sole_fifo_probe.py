"""Observe actual FIFO publication; later cache snapshots may be another pose."""
from types import FunctionType
import prepare_bounded_native_sole_unmatched_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.old.old.old.prior.ROOT/'audit_bounded_native_sole_fifo_preparation'
scope['TAIL']+=r'''
local sole_queue_count=0
local sole_queue_tap=selection_p:install_read_tap(0xff804410,0xff80441f,
    'actual sparse physical body FIFO',function(at)
    local regs=manager.machine.devices[':maincpu'].state
    if not first_live or at~=0xff804410 or regs.PC.value~=0xff804420 then return end
    local age=selection_frame-first_live
    if age~=8 and age~=16 and age~=24 and age~=32 and age~=80 and age~=96 and age~=112 then return end
    for slot=1,2 do
        local s=bounded_actor(slot)
        if s and s.a==regs.A0.value then
            local cache=selection_p:read_u32(s.a+0x1a0);local row=regs.A3.value-112
            assert(row>=cache and row<cache+12*112 and (row-cache)%112==0)
            sole_queue_count=sole_queue_count+1
            print(string.format('MK2_BOUNDED_SOLE_FIFO frame=%d seconds=%.12f slot=%d id=%d actor=%08X main=%08X pose=%08X part=%d source=%08X size=%08X xy=%08X command=%08X palette=%08X pc=%08X writes=0',
                selection_frame,emu.time(),slot,s.id,s.a,s.m,selection_p:read_u32(s.a+0x1d0),(row-cache)//112,
                regs.A11.value,regs.A9.value,regs.A10.value,regs.A12.value,regs.A6.value,regs.PC.value))
        end
    end
end)
emu.register_stop(function()
    assert(sole_queue_tap,'Actual FIFO tap retained')
    print(string.format('MK2_BOUNDED_SOLE_FIFO_TERMINAL entries=%d writes=0',sole_queue_count))
end)
'''
main=FunctionType(old.scope['main'].__code__,scope)
if __name__=='__main__':main()
