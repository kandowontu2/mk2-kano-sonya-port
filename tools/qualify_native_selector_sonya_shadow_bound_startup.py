"""Include independently observed first projectile before first pre-field.

Both prior coverage rejections remain false. No fabricated field at1817.
"""
import inspect
import qualify_native_selector_sonya_shadow_bound_words as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_shadow_bound_startup_checked'


def admissible_entry(r,expected,text):
    if int(r['frame']) in expected:return True
    ledger=previous.previous.prior.capture.choices.native_state
    actual=ledger.rows(text,'MK2_FIRST_PROJECTILE_ENTRY')
    need(int(r['frame'])==1817 and r['kind']=='ring','Only actual opening ring precedes first live pre-field')
    matches=[a for a in actual if a['frame']==r['frame'] and a['kind']==r['kind'] and a['mode']=='2' and
             all(a[k]==r[k] for k in ('actor','main','owner','id','opcode','mask','writes','assistance'))]
    return len(matches)==1


def execute(state):
    base=previous.previous
    scope=previous.functions()
    source=inspect.getsource(base.gate)
    replace=base.prior.phase_source.replace
    source=replace(source,"all(r[k]==posts[key][k] for k in ('actor','main','owner','id','pose','body'))",
        "all(int(r[k],10 if k=='id' else 16)==int(posts[key][k],10 if k=='id' else 16) for k in ('actor','main','owner','id','pose','body'))")
    source=replace(source,"int(r['frame']) in expected,'Real owned native move entry, opcode and drawing context'",
        "admissible_entry(r,expected,text),'Real owned native entry and independently executing opening ring'")
    scope.update(admissible_entry=admissible_entry,OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::whole_draw_coverage_and_actual_startup_entry','exec'),scope)
    source=inspect.getsource(base.execute)
    source=replace(source,'Path(capture.__file__),',
        "Path(capture.__file__),Path(base.__file__),Path(previous.__file__),base.OUT/'failure.json',previous.OUT/'failure.json',")
    scope.update(base=base,previous=previous)
    exec(compile(source,__file__+'::whole_original_native_coverage_and_store_census','exec'),scope)
    return scope['execute'](state)
