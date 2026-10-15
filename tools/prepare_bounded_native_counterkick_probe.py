"""Ordinary reactive High Kick, with passive exact health-write provenance."""
import prepare_bounded_native_lowkick24_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.prior.ROOT/'audit_bounded_native_counterkick_preparation'
tail=scope['TAIL']
before='if math.abs(a.x-b.x)<110 and age%24<4 then'
after='if ((b.action==0x0207 or b.action==0x0204) and math.abs(a.x-b.x)<160) or (math.abs(a.x-b.x)<110 and age%24<4) then'
assert tail.count(before)==1;tail=tail.replace(before,after,1)
before="manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1)"
after="""if b.action==0x0207 or b.action==0x0204 then
                high['P1 High Kick']:set_value(1)
            else manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1) end"""
assert tail.count(before)==1;tail=tail.replace(before,after,1)
tail+=r'''
local counter_health_taps={}
for slot,address in ipairs({0x010602f0,0x01060ec0}) do
    counter_health_taps[slot]=selection_p:install_write_tap(address,address+15,
        'bounded native health provenance '..slot,function(at,data,mask)
        print(string.format('MK2_BOUNDED_HEALTH_WRITE frame=%d seconds=%.12f slot=%d address=%08X before=%d data=%04X mask=%04X pc=%08X writes=0',
            selection_frame,emu.time(),slot,at,selection_p:read_u16(address),data&0xffff,mask&0xffff,
            manager.machine.devices[':maincpu'].state.PC.value))
    end)
end
emu.register_stop(function()
    assert(#counter_health_taps==2,'Both actual health taps retained')
    print('MK2_BOUNDED_HEALTH_TAPS_TERMINAL retained=2 writes=0')
end)
'''
scope['TAIL']=tail
source=old.source
before="high['P1 Down'],high['P1 Block'],manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']}"
assert source.count(before)==1
source=source.replace(before,"high['P1 Down'],high['P1 Block'],high['P1 High Kick'],manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']}",1)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
