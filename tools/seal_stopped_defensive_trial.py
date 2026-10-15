"""Preserve the third unsuccessful physical-controller campaign trial."""
import inspect
import seal_stopped_postending_trial as prior

if __name__=='__main__':
    source=inspect.getsource(prior.main)
    for before,after in [("'audit_native_postending_kano_p2_sonya_join'","'audit_native_postending_kano_p2_sonya_defensive'"),
                         ('==53','==63'),('actualLosses=53','actualLosses=63'),('losses=53','losses=63')]:
        prior.need(source.count(before)==1,'Exact actual stopped defensive trial rebase')
        source=source.replace(before,after,1)
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_preservation','exec'),scope)
    scope['main']()
