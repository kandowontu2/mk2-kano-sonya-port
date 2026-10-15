"""Compare equal-width native words numerically; bind intra-field action stores.

Original rejection for 4-vs-8-digit equal body words remains immutable.
"""
import inspect
import qualify_native_selector_sonya_shadow_bound_coverage as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_shadow_bound_words_checked'


def action_values(text,frame,before):
    rows=previous.prior.phase_source.bicycle.state.original.flag_rows(text)
    actual=[r for r in rows if r['slot']==2 and r['kind']=='action' and r['frame']==frame]
    values={before}
    for r in actual:
        need(r['actor']==r['a8']==0x010350a0 and r['main']==r['a13']==0x0106bf30 and r['id']==18,
             'Actual intra-field action store ownership')
        values.update((r['before'],r['after']))
    return values


def functions():
    replace=previous.prior.phase_source.replace
    source=inspect.getsource(previous.gate)
    source=replace(source,"all(r[k]==posts[key][k] for k in ('actor','main','owner','id','pose','body'))",
        "all(int(r[k],10 if k=='id' else 16)==int(posts[key][k],10 if k=='id' else 16) for k in ('actor','main','owner','id','pose','body'))")
    scope=dict(vars(previous),action_values=action_values,__file__=__file__,OUT=OUT)
    exec(compile(source,__file__+'::equal_native_words_not_hex_padding','exec'),scope)
    source=inspect.getsource(previous.horizontal)
    source=replace(source,"r['action']==('0303' if f==3191 else '0204' if f<3211 else '0611')",
        "int(r['action'],16) in action_values(text,f,by[f]['action'])")
    exec(compile(source,__file__+'::actual_intra_field_action_chronology','exec'),scope)
    source=inspect.getsource(previous.execute)
    source=replace(source,'Path(capture.__file__),','Path(capture.__file__),Path(previous.__file__),previous.OUT/\'failure.json\',')
    scope['previous']=previous
    exec(compile(source,__file__+'::whole_original_drawing_store_census','exec'),scope)
    return scope


def execute(state):return functions()['execute'](state)
