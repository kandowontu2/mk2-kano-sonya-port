"""Exact identified third failed controller: preserve intentional cancellation."""
import inspect
import stop_native_reactive_postending_trial as prior
if __name__=='__main__':
    source=inspect.getsource(prior.main)
    for before,after in [('174412','58332'),('125744','171568'),
                         ('Subzero-only approach/jump-kick physical policy','Subzero-only guarded approach physical policy')]:
        prior.need(source.count(before)==1,'Exact known native identity rebase')
        source=source.replace(before,after,1)
    scope=dict(vars(prior),OUT=prior.ROOT/'audit_native_postending_kano_p2_sonya_defensive',__file__=__file__)
    exec(compile(source,__file__+'::actual_third_native_stop','exec'),scope)
    scope['main']()
