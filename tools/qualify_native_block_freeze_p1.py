"""Whole finite original gate for seven P1 cases, stronger palette/state faults."""
import inspect
import qualify_native_block_freeze_observed as prior

def qualify(captures):
    source=inspect.getsource(prior.qualify)
    changes=[
        ("'audit_native_block_freeze_observed_checked'","'audit_native_block_freeze_p1_checked'"),
        ("('own_hp','160'),('y','-999'),('age','999')",
         "('own_hp','160'),('y','-999'),('age','999'),('bank','FFFF'),('action','0700' if policy=='none' else '0401')"),
        ('len(checks)==6 and len(faults)==108','len(checks)==7 and len(faults)==140'),
        ('six-case guard/recovery','seven-case opposite-slot guard/recovery'),
        ('nativeGames=6,nativeFields=4206','nativeGames=7,nativeFields=4907'),
        ('Dead Pool two-human P2 cases only','Dead Pool two-human P1 cases only'),
        ('nativeFields=4206,effectiveFaults=len(faults)','nativeFields=4907,effectiveFaults=len(faults)'),
    ]
    for before,after in changes:
        prior.need(source.count(before)==1,'Exact whole original P1 gate adaptation: '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_gate_plus_palette_state_faults','exec'),scope)
    return scope['qualify'](captures)
