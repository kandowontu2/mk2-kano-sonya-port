"""Whole preservation routine rebased to the actual second stopped trial."""
import inspect
import seal_stopped_postending_trial as prior
if __name__=='__main__':
    source=inspect.getsource(prior.main)
    for before,after in [("'audit_native_postending_kano_p2_sonya_join'","'audit_native_postending_kano_p2_sonya_reactive'"),
                         ("==53","==30"),("actualLosses=53","actualLosses=30"),("losses=53","losses=30")]:
        prior.need(source.count(before)==1,'Exact actual stopped trial rebase')
        source=source.replace(before,after,1)
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_preservation','exec'),scope)
    scope['main']()
