"""Distinct normal Low Kick rhythm, retaining corrected passive observers."""
import prepare_bounded_native_uppercut_retained_tap_probe as old
scope=dict(old.scope)
scope['OUT']=old.prior.ROOT/'audit_bounded_native_lowkick24_preparation'
tail=scope['TAIL']
changes={
 "math.abs(a.x-b.x)<120 and age%36<4":"math.abs(a.x-b.x)<110 and age%24<4",
 "high['P1 Down']:set_value(1);high['P1 High Punch']:set_value(1)":"manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1)",
 "press='down_highpunch'":"press='lowkick24'",
 "math.abs(a.x-b.x)>50":"math.abs(a.x-b.x)>70",
}
for before,after in changes.items():
    assert tail.count(before)==1
    tail=tail.replace(before,after,1)
scope['TAIL']=tail
source=old.previous.source
marker="    prepared = prefix+TAIL"
assert source.count(marker)==1
source=source.replace(marker,"""    boundary="high['P1 Down'],high['P1 Block']}"
    assert prefix.count(boundary)==1
    prefix=prefix.replace(boundary,"high['P1 Down'],high['P1 Block'],manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']}",1)
    prepared = prefix+TAIL""",1)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
