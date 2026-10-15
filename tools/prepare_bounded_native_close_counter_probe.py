"""Normal closer approach and released kick pulses; log actual physical ports."""
import prepare_bounded_native_recovery_counterkick_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.prior.ROOT/'audit_bounded_native_close_counter_preparation'
tail=scope['TAIL']
changes={
 'and math.abs(a.x-b.x)<160':'and math.abs(a.x-b.x)<80 and age%8<2',
 'math.abs(a.x-b.x)>70':'math.abs(a.x-b.x)>50',
 "high['P1 High Kick']:set_value(1)":"high['P1 High Kick']:set_value(1);press='highkick'",
 "else manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1) end":"else manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1);press='lowkick' end",
 "bounded_presses=bounded_presses+1;press='lowkick24'":"bounded_presses=bounded_presses+1",
}
for before,after in changes.items():
    assert tail.count(before)==1
    tail=tail.replace(before,after,1)
marker="    print(string.format('MK2_BOUNDED_FIELD"
assert tail.count(marker)==1
tail=tail.replace(marker,"""    print(string.format('MK2_BOUNDED_PHYSICAL frame=%d in0=%04X in2=%04X flags=%04X body=%04X press=%s writes=0',
        selection_frame,manager.machine.ioport.ports[':IN0']:read(),manager.machine.ioport.ports[':IN2']:read(),a.flags,a.body,press))
"""+marker,1)
scope['TAIL']=tail
exec(compile(old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
