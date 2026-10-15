"""Counter with normal High Kick during approach and native recovery action."""
import prepare_bounded_native_counterkick_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.prior.ROOT/'audit_bounded_native_recovery_counterkick_preparation'
tail=scope['TAIL']
before='b.action==0x0207 or b.action==0x0204'
assert tail.count(before)==2
tail=tail.replace(before,before+' or b.action==0x0304')
scope['TAIL']=tail
exec(compile(old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
