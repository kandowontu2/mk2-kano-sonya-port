"""Same original game; distinguish native fighter type79 from child type81.

The first check incorrectly required the projectile object's type on its
parent fighter. Preserve that rejection. Keep all other entry, original
knife, source-owned pool, first-callback and complete state/HP/RNG rules.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_native_selector_cpu_first_round_knife as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_first_round_knife_type_checked'


def prepare():
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    source=inspect.getsource(prior.first_entry)
    before="observed['type']=='81'"
    need(source.count(before)==1,'Only initial parent fighter type differs from its allocated projectile child')
    source=source.replace(before,"observed['type']=='79'and observed['process_slot']=='2'",1)
    exec(compile(source,__file__+'::whole_initial_native_fighter_not_child_type','exec'),scope)
    for function in(prior.whole_knife,prior.bindings):
        exec(compile(inspect.getsource(function),__file__+'::whole_original_'+function.__name__,'exec'),scope)
    source=inspect.getsource(prior.execute)
    marker="        ('initial_entry_roster',change('MK2_STARTUP_PROJECTILE_EVENT','roster','1,17',kind='knife')),"
    need(source.count(marker)==1,'Add two actual native fighter-type/physical-role faults')
    source=source.replace(marker,marker+"\n        ('initial_parent_is_not_projectile',change('MK2_STARTUP_PROJECTILE_EVENT','type','81',kind='knife')),\n        ('initial_parent_is_not_human_slot',change('MK2_STARTUP_PROJECTILE_EVENT','process_slot','1',kind='knife')),",1)
    source=source.replace('/26 faults','/28 faults')
    exec(compile(source,__file__+'::whole_original_first_round_gate_real_parent_type','exec'),scope)
    return scope


def safe_execute(state):
    try:
        failure=json.loads((prior.OUT/'failure.json').read_text())
        need(not failure['passed']and failure['newNativeGames']==0 and
             failure['error']=="ValueError('Actual executing first-round parent/Main/type/roster/role and first independent physical callbacks')",
             'Exact original matcher rejection remains unchanged, not a game failure or native replay')
        return prepare()['execute'](state)
    except Exception as error:
        need(not OUT.exists(),'Preserve same-game successor rejection')
        OUT.mkdir();prior.capture.prior.prior.current.prior.save(OUT/'failure.json',dict(passed=False,
            error=repr(error),traceback=traceback.format_exc(),newNativeGames=0,goalStatus='active',fullPortAcceptance=False))
        raise
