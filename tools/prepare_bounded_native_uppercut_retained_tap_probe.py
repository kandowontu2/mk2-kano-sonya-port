"""Keep passive tap handle reachable for the entire native run.

Executed predecessors remain unchanged. This is preparation, not a fix claim.
"""
import prepare_bounded_native_uppercut_owners_bound_probe as previous
prior=previous.prior
scope=dict(previous.scope)
scope['OUT']=prior.ROOT/'audit_bounded_native_uppercut_retained_tap_preparation'
scope['TAIL']=prior.TAIL+r'''
-- A registered closure retains the actual tap userdata beyond chunk return.
emu.register_stop(function()
    assert(bounded_sound_tap,'Actual passive sound tap retained through stop')
    print('MK2_BOUNDED_TAP_TERMINAL retained=1 writes=0')
end)
'''
exec(compile(previous.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
