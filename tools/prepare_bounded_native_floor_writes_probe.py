"""Observe actual physical Main floor writes, including natural KO reaction."""
import prepare_bounded_native_close_counter_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.old.prior.ROOT/'audit_bounded_native_floor_writes_preparation'
scope['TAIL']+=r'''
local floor_taps,floor_mains={},{}
emu.register_frame(function()
    if not first_live then return end
    for slot=1,2 do
        local s=bounded_actor(slot)
        if s and floor_mains[slot]~=s.m then
            if floor_taps[slot] then floor_taps[slot]:remove() end
            floor_mains[slot]=s.m
            local address=s.m+0x200
            floor_taps[slot]=selection_p:install_write_tap(address,address+15,
                'actual native physical floor '..slot,function(at,data,mask)
                local current=bounded_actor(slot)
                if not current then return end
                local regs=manager.machine.devices[':maincpu'].state
                print(string.format('MK2_BOUNDED_FLOOR_WRITE frame=%d seconds=%.12f slot=%d main=%08X actor=%08X id=%d hp=%d action=%04X stage_floor=%d y=%d before=%d data=%04X mask=%04X pc=%08X a0=%08X a13=%08X op0=%04X op1=%04X writes=0',
                    selection_frame,emu.time(),slot,current.m,current.a,current.id,current.hp,current.action,
                    selection_p:read_i16(0x0105ecd0),current.y,selection_p:read_i16(address),data&0xffff,mask&0xffff,
                    regs.PC.value,regs.A0.value,regs.A13.value,
                    selection_p:read_u16(regs.PC.value-32),selection_p:read_u16(regs.PC.value-16)))
            end)
        end
    end
end)
emu.register_stop(function()
    assert(floor_taps[1] and floor_taps[2],'Both physical floor observers bound')
    print('MK2_BOUNDED_FLOOR_TERMINAL retained=2 writes=0')
end)
'''
exec(compile(old.old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
