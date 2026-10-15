"""Distinct genuine Sonya guard-from-start; whole latest transport/state proof.

Original complete native1800-field HP/state and Sonya RNG/source rules, no
prescribed CPU choice, fake child, proxy or state writes. Actual ring/child
and visual/audio acceptance are separate from capture/state acceptance.
"""
import inspect,json,re,sys
from pathlib import Path
import capture_native_selector_cpu_guard_shadow as prior
import verify_current_existing_cpu_leg_choices_v6274 as sonya

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_sonya_startup_guard_ram'
OUT=ROOT/'audit_native_selector_cpu_sonya_startup_guard_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_sonya_startup_guard.lua'
KEY='cpu_sonya_p2_guard_from_start_confirm265'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None
normalize=prior.normalize
key_selftest=prior.key_selftest


def whole_sonya(text,guest):
    hp,by=sonya.stream.health_ledger(text,guest,'sonya')
    states=sonya.stream.state_ledgers(text,guest,'sonya',by)
    choices=sonya.choice_gate(sonya.choice_rows(text),guest)
    selected=sonya.pair.rows_prefix(text,'MK2_P2CPU_SELECT_RESULT ')
    need(len(selected)==1 and selected[0]['human']=='sonya'and
         selected[0]['human_id']==selected[0]['initial_cpu']==18 and
         selected[0]['checks']==50 and selected[0]['errors']==0,
         'True natural Sonya selection and CPU, no host-supplied opponent')
    return dict(passed=True,wholeNativeHealthLedger=hp,wholeNativeStateLedger=states,
        nativeChoices=choices,wholeMovePhaseAcceptancePending=True,fullPortAcceptance=False)


def execute(state):
    parent=ROOT/'audit_native_selector_cpu_startup_guard_checkpoint_checked/report.json'
    proof=json.loads(parent.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Previous finite blocked-Kano checkpoint and full original goal unchanged')
    source=inspect.getsource(prior.execute)
    boundary="    boundary=\"    scope.update(KEY=KEY,normalize=normalize)\""
    added="""    source=prior.current.replace(source,"MK2KS_CPU_PAIR_APPROACH='guard_until_close'", "MK2KS_CPU_PAIR_APPROACH='guard_wait'")
    source=prior.current.replace(source,"MK2KS_TEST_FIGHTER='kano'", "MK2KS_TEST_FIGHTER='sonya'")
    source=prior.current.replace(source,"victim='kano'", "victim='sonya'")
    source=prior.current.replace(source,'sources=[LUA,', "sources=[LUA,*SONYA_LUA,")
    source=prior.current.replace(source,'scope.update(KEY=KEY,normalize=normalize)',
        'scope.update(KEY=KEY,normalize=normalize,whole_sonya=whole_sonya)')
"""
    source=prior.prior.current.replace(source,boundary,added+boundary)
    source=prior.prior.current.replace(source,'full_phase=allocation.phase.model.verify',
        'full_phase=whole_sonya')
    boundary="    exec(compile(source,__file__+'::whole_prior_collector_distinct_guard_route_callback_keys','exec'),scope)"
    source=prior.prior.current.replace(source,boundary,
        '    scope.update(whole_sonya=whole_sonya,SONYA_LUA=SONYA_LUA)\n'+boundary)
    sonya_lua=[ROOT/name for name in('mk2ks_native_selector_cpu_sonya_extended_ram.lua',
        'mk2ks_native_selector_cpu_sonya_allocation.lua','mk2ks_native_selector_cpu_sonya_base.lua',
        'mk2ks_native_selector_cpu_sonya_guard.lua','mk2ks_native_selector_cpu_guard_shadow.lua',
        'mk2ks_native_selector_cpu_startup_guard.lua','mk2ks_physical_p2_cpu_ring_trace_v2013.lua')]
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        whole_sonya=whole_sonya,SONYA_LUA=sonya_lua,
        prior=prior.prior,__file__=__file__)
    exec(compile(source,__file__+'::whole_callback_collector_actual_Sonya_controller_and_ledgers','exec'),scope)
    # The nested entire original collector must receive these two explicit host bindings.
    original_execute=scope['execute']
    original_execute.__globals__['whole_sonya']=whole_sonya
    original_execute.__globals__['SONYA_LUA']=sonya_lua
    report=original_execute(state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
