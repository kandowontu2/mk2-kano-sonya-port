"""Confirmed natural P1 Sonya/P2 CPU Sonya route with complete repeated recovery.

Five observation-only transformations of the full original1438 controller:
completion accounting and event-based exit. ALL physical inputs unchanged.
The original1463 repeated-pair contract is rebound to actual physical slots.
"""
import code
import gzip
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_cpu_leg_repeat as previous

prior,base=previous.prior,previous.base
ROOT,need,sha,once=previous.ROOT,previous.need,previous.sha,previous.once
BASE=ROOT/'audit_native_kano_laser_cpu_leg_repeat_p2_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_leg_repeat_p2_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_leg_repeat_p2_initializer_source'
GUARD=ROOT/'audit_native_kano_laser_cpu_leg_repeat_p2_source'
LUA=ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua'
KEY='leg_cpu_sonya_p2_human_sonya_p1'
RAM_CASES={}
COMPLETED=[]


def repeat_expected():
    source=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()
    for before,after in (
        ('local frame,cycle,complete=0,0,nil','local frame,cycle,complete=0,0,nil\nlocal complete_count,last_complete=0,nil'),
        ("state('COMPLETE',s,v);complete=frame","state('COMPLETE',s,v);complete=frame\n            complete_count=complete_count+1;last_complete=frame"),
        ('local deadline=follow_regain and math.max(complete,follow_regain)+30 or complete+180\n        if frame>=deadline then manager.machine:exit()end','if complete_count>=2 and frame>=last_complete+30 then manager.machine:exit()end'),
        ('schema=8 cycles=%d complete=%d follow_regain=%d','schema=9 cycles=%d complete_count=%d complete=%d follow_regain=%d'),
        ('cycle,complete or -1,follow_regain or -1','cycle,complete_count,complete or -1,follow_regain or -1')):
        source=once(source,before,after)
    return source


def wrapper_expected():
    source=(ROOT/'mk2ks_cpu_choke_shadow_v5328.lua').read_text()
    source=once(source,"local move,side,attempt,air='choke',2,1,false","local move,side,attempt,air='leg',2,1,false")
    source=once(source,"local expected={human=='kano'and 17 or 18,17}","local expected={human=='kano'and 17 or 18,18}")
    root=LUA.read_text()
    marker="once('local count\\ndriver,count=driver:gsub',[["
    at=root.index(marker)+len(marker);end=root.index(']])',at)
    return once(source,'local count\ndriver,count=driver:gsub',root[at:end])


def qualify():
    source=inspect.getsource(prior.qualify)
    source=once(source,"ROOT/'mk2ks_native_kano_laser_cpu_choke_parse.lua'","ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2_parse.lua'")
    source=once(source,"original=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()","original=repeat_expected()")
    source=once(source,"expanded['wrapper']==(ROOT/'mk2ks_cpu_choke_shadow_v5328.lua').read_text()","expanded['wrapper']==wrapper_expected()")
    scope=dict(vars(prior),GUARD=GUARD,LUA=LUA,__file__=__file__,wrapper_expected=wrapper_expected,repeat_expected=repeat_expected)
    exec(compile(source,__file__+'::whole_native_compiled_five_observation_changes_six_RAM_sinks','exec'),scope)
    return scope['qualify']()


def physical_bindings(guest):
    source=inspect.getsource(previous.physical_bindings)
    source=once(source,'scope=dict(vars(repeated),CURRENT_GUEST=guest)',
                'scope=dict(vars(repeated),CURRENT_GUEST=guest,CPU_SLOT=2,HUMAN_SLOT=1,PHYSICAL_ROLE={1:2,2:1})')
    before="for function in (repeated._verify_log,repeated.verify_log):\n        exec(compile(inspect.getsource(function),__file__+'::entire_original_repeated_pair_contract','exec'),scope)"
    after="""for function in (repeated.verify_repeated_stream,repeated._verify_log,repeated.verify_log):
        observed_source=inspect.getsource(function)
        if function is repeated._verify_log:
            need(observed_source.count('MK2_P1CPU_')==4,'All four real cold physical prefixes')
            observed_source=observed_source.replace('MK2_P1CPU_','MK2_P2CPU_')
            need(observed_source.count('0x01060ea0')==2,'Both actual physical victim velocity checks')
            observed_source=observed_source.replace('0x01060ea0','0x010602d0')
        exec(compile(observed_source,__file__+'::entire_original_repeated_pair_contract_physical_P2_CPU','exec'),scope)"""
    source=once(source,before,after)
    for line in (
        '    source=once(source,"((1,\'vhp\'),(2,\'hp\'))","((1,\'hp\'),(2,\'vhp\'))")\n',
        '    source=once(source,"(h[\'cpu_slot\'],h[\'human_slot\'])==(2,1)","(h[\'cpu_slot\'],h[\'human_slot\'])==(1,2)")\n',
        '    source=once(source,"prefix=\'v\'if slot==1 else\'\'","prefix=\'v\'if slot==2 else\'\'")\n'):
        source=once(source,line,'')
    source=once(source,"physical_source=(ROOT/'mk2ks_cpu_recovery_probe_v1459.lua').read_text()","physical_source=repeat_expected()")
    source=once(source,"(r['cpu_slot'],r['human_slot'])==(1,2)","(r['cpu_slot'],r['human_slot'])==(2,1)")
    scope=dict(vars(previous),__file__=__file__,repeat_expected=repeat_expected)
    # repeat_expected is used by the source-generated whole-health checker too.
    source=once(source,'health_scope=dict(complete_health.whole_health.__globals__,repeated=repeated,re=re)',
                'health_scope=dict(complete_health.whole_health.__globals__,repeated=repeated,re=re,repeat_expected=repeat_expected)')
    exec(compile(source,__file__+'::whole_current_repeated_physical_health_factory_P2_CPU','exec'),scope)
    return scope['physical_bindings'](guest)


def bindings(guest,human):
    physical=physical_bindings(guest)
    scope=dict(vars(prior.cpu_body),cpu=SimpleNamespace(original=previous.repeated,verify_log=physical))
    source=inspect.getsource(prior.cpu_body.bindings)
    source=once(source,"ids={2:17,1:cpu.original.HUMANS[b[\"human\"]]}","ids={2:18,1:cpu.original.HUMANS[b[\"human\"]]}")
    exec(compile(source,__file__+'::whole_original_body_shadow_CPU_Sonya_P2','exec'),scope)
    _,original=scope['bindings'](human)
    return lambda b,g,p,gfx:original(dict(b,human=human),g,p,gfx)


def run():
    global guest,gfx,gfx32,payload,native,pins,check
    failure=ROOT/'audit_native_kano_laser_cpu_leg_repeat_ram/leg_cpu_sonya_p1_human_kano_p2/result.json'
    report=json.loads(failure.read_text())
    need(not report['passed'] and report['nativeExit']==0 and not report['nativeTerminal']['hostDecodeErrors'],
         'Preserved first natural trial terminal, not replayed as a CPU Sonya success')
    with gzip.open(failure.parent/'run.log.gz','rt')as file:text=file.read()
    cold=previous.repeated.rows_prefix(text,'MK2_P1CPU_COLD_LIVE ')
    need(len(cold)==1 and cold[0]['cpu_id']==3 and not previous.repeated.rows(text,'ENTRY'),
         'Actual first naturally selected Baraka, no signature grab invented')
    source=inspect.getsource(previous.run)
    source=once(source,"MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_PAIR_APPROACH='guard_until_close'",
                "MK2KS_TEST_FIGHTER='sonya',MK2KS_TEST_BOOT_FRAME='606',MK2KS_CPU_PAIR_APPROACH='original'")
    source=once(source,"key='leg_cpu_sonya_p1_human_kano_p2'","key='leg_cpu_sonya_p2_human_sonya_p1'")
    source=once(source,"human='kano',cpuLog=text","human='sonya',cpuLog=text")
    source=once(source,'"victim=\'kano\'"','"victim=\'sonya\'"')
    source=once(source,"check=bindings(guest,'kano')","check=bindings(guest,'sonya')")
    source=once(source,"r=scope['capture']('leg',1,guest,gfx,gfx32,payload,native,check,decode,pins)",
                "r=scope['capture']('leg',2,guest,gfx,gfx32,payload,native,check,decode,pins)")
    source=once(source,'physicalCPUSlot=1,physicalHumanSlot=2','physicalCPUSlot=2,physicalHumanSlot=1')
    source=once(source,"pins=dict(build['input_hashes']);pins.update(guard['inputHashes'])",
                "pins=dict(build['input_hashes']);pins.update(guard['inputHashes']);pins[str(Path(previous_file).resolve())]=sha(previous_file);pins[str(prior_failure.resolve())]=sha(prior_failure)")
    scope=dict(vars(previous),BASE=BASE,OUT=OUT,INIT=INIT,GUARD=GUARD,LUA=LUA,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED,
               qualify=qualify,bindings=bindings,__file__=__file__,previous_file=previous.__file__,prior_failure=failure)
    exec(compile(source,__file__+'::whole_current_capture_confirmed_original_P2_CPU_route','exec'),scope)
    try:scope['run']()
    finally:
        for name in ('guest','gfx','gfx32','payload','native','pins','check'):
            if name in scope:globals()[name]=scope[name]


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual successor failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual P2 CPU Sonya repeated trial in RAM; no terminal replay.',
                 local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
