"""Distinct genuine continuous Block; all native choices and tower stay native.

The original test released Block while waiting for paired victim recovery.
This successor changes physical input only. Whole original health/state/RNG
contracts bind the actual tower proven against all six native ROM lists; no
old trajectory or original rejected result is relabeled as accepted.
"""
import inspect,json,struct
from pathlib import Path
import capture_native_selector_cpu_sonya_startup_guard as original

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_native_selector_cpu_sonya_continuous_guard_ram'
OUT=ROOT/'audit_native_selector_cpu_sonya_continuous_guard_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_sonya_continuous_guard.lua'
KEY='cpu_sonya_p2_continuous_guard_boot606_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None


def bind(function,schedule):
    source=inspect.getsource(function)
    need(source.count('0xfffa3180')==1,'Only independently proven native tower context differs')
    source=source.replace('0xfffa3180','schedule')
    scope=dict(function.__globals__,schedule=schedule)
    exec(compile(source,__file__+'::whole_original_native_tower_'+function.__name__,'exec'),scope)
    return scope[function.__name__]


def whole_sonya(text,guest):
    model=original.sonya
    cold=model.pair.rows_prefix(text,'MK2_P2CPU_COLD_LIVE ')
    need(len(cold)==1 and (cold[0]['human_id'],cold[0]['cpu_id'],cold[0]['stage'])==(18,18,0),
         'Actual naturally selected true Sonya mirror, not supplied CPU identity')
    tables=model.pair.rows(text,'ROM');expected=model.pair.expected_orders()
    table=struct.unpack_from('<I',guest,(0xff8a11f0-0xff800000)//8)[0]
    need(len(tables)==6 and table==0xfffa2c00 and [r['order']for r in tables]==list(range(6)),
         'Whole six native ROM ladder lists and independent guest table pointer')
    for i,row in enumerate(tables):
        pointer=struct.unpack_from('<I',guest,(table+i*32-0xff800000)//8)[0]
        ids=struct.unpack_from('<17H',guest,(pointer-0xff800000)//8)
        need(row['table']==table and row['list']==pointer==0xfffa3000+i*0x180 and
             tuple(map(int,row['ids'].split(',')))==ids==expected[i]and
             row['writes']==0 and row['assistance']=='none','Whole native ladder inventory unchanged')
    schedule=cold[0]['schedule'];orders=[r['order']for r in tables if r['list']==schedule]
    need(len(orders)==1 and expected[orders[0]][0]==18,'Actual source-owned Sonya first opponent')
    hp,by=bind(model.stream.health_ledger,schedule)(text,guest,'sonya')
    states=model.stream.state_ledgers(text,guest,'sonya',by)
    choices=bind(model.choice_gate,schedule)(model.choice_rows(text),guest)
    selected=model.pair.rows_prefix(text,'MK2_P2CPU_SELECT_RESULT ')
    need(len(selected)==1 and selected[0]['human']=='sonya'and
         selected[0]['human_id']==selected[0]['initial_cpu']==18 and
         selected[0]['checks']==50 and selected[0]['errors']==0,
         'Whole original natural selection-to-match contract, no character proxy')
    inputs=model.pair.rows(text,'CONTINUOUS_GUARD_INPUT')
    fields=model.pair.rows(text,'FIELD')
    need([r['frame']for r in inputs]==[r['frame']for r in fields]and inputs and
         all(r['policy']=='continuous_guard'and r['buttons']=='Block'and r['writes']==0 and
             r['assistance']=='none'and (r['actor'],r['main'],r['hp'])==(f['vactor'],f['vmain'],f['vhp'])
             for r,f in zip(inputs,fields)),
         'Every actual live callback receives physical Block from one controller, including paired recovery')
    return dict(passed=True,actualNativeTower=orders[0],wholeNativeHealthLedger=hp,
        wholeNativeStateLedger=states,nativeChoices=choices,continuousPhysicalGuardFields=len(inputs),
        wholeMovePhaseAcceptancePending=True,blockedRingAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not BASE.exists()and not OUT.exists()and
         not original.prior.prior.current.prior.identity.census(),
         'Fresh distinct continuous physical input strategy; no pending game or timeout replay')
    source=inspect.getsource(original.execute)
    before="""    source=prior.current.replace(source,'scope.update(KEY=KEY,normalize=normalize)',
        'scope.update(KEY=KEY,normalize=normalize,whole_sonya=whole_sonya)')
"""
    source=original.prior.prior.current.replace(source,before,'')
    marker="    source=prior.current.replace(source,\"victim='kano'\", \"victim='sonya'\")"
    timing="""    source=prior.current.replace(source,"MK2KS_TEST_BOOT_FRAME='605'", "MK2KS_TEST_BOOT_FRAME='606'")
    source=prior.current.replace(source,"MK2KS_CPU_PAIR_CONFIRM_AGE='265'", "MK2KS_CPU_PAIR_CONFIRM_AGE='264')
"""
    source=original.prior.prior.current.replace(source,marker,marker+'\n'+timing)
    marker='    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,'
    source=original.prior.prior.current.replace(source,marker,
        "    sonya_lua += [ROOT/name for name in('mk2ks_native_selector_cpu_sonya_base_expanded.lua','mk2ks_native_selector_cpu_sonya_guard_bound.lua','mk2ks_native_selector_cpu_sonya_startup_guard.lua','mk2ks_native_selector_cpu_sonya_startup_guard_bound.lua')]\n"+marker)
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        whole_sonya=whole_sonya,__file__=__file__)
    exec(compile(source,__file__+'::whole_original_transport_continuous_physical_guard','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    return report
