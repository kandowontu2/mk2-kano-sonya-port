"""Reuse verified independent current models; prepare a new physical-input case."""
import inspect
import json
from pathlib import Path
from types import FunctionType,SimpleNamespace
import capture_native_selector_sonya_cpu_air_approach as air
import run_prepared_native_selector_lowkick_after_host_exit as run_source
import verify_native_source_sync as sync

ROOT=sync.ROOT
OUT=ROOT/'audit_native_selector_fresh_highkick_owners_preflight'
BASE=ROOT/'audit_native_selector_fresh_highkick_owners_ram'
LUA=ROOT/'mk2ks_native_selector_sonya_cpu_highkick_owners.lua'
KEY='actual_Kano_walk_highkick_natural_Sonya_CPU_saved_owners'
RAM_CASES,NATIVE_HANDLES,COMPLETED,AUDIO={}, {}, [], {}
DISPLAY=dict(buffers=air.snapshot.RAMBuffers(),headers={},gfx={},rgb={},rgbHeaders={})
STATE,SCOPE={},None


def prepare(previous):
    global STATE,SCOPE
    sync.need(not OUT.exists() and not BASE.exists(),'Fresh genuinely distinct case')
    sync.need(sync.verify()['passed'] and not air.previous.base.choices.current.prior.identity.census(),
              'Whole current sources unchanged; no live native game')
    proof=json.loads((ROOT/'audit_native_selector_fresh_lowkick_renderer_faults_checked/report.json').read_text())
    sync.need(proof['passed'] and all(sync.sha(p)==h for p,h in proof['inputHashes'].items()),
              'Earlier whole actual recording accepted and unchanged, not replayed')
    STATE=dict(previous.STATE)
    f=air.snapshot.transport.normalize
    normalize=FunctionType(f.__code__,dict(f.__globals__,DISPLAY=DISPLAY),f.__name__,f.__defaults__)
    source=inspect.getsource(air.prepare)
    sync.need(source.count('inspect.getsource(previous.prepare)')==1,'Retrieve exact original defining factory')
    source=source.replace('inspect.getsource(previous.prepare)','inspect.getsource(previous.original.prepare)',1)
    namespace=dict(vars(air),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
                   NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
                   DISPLAY=DISPLAY,normalize=normalize,__file__=__file__)
    exec(compile(source,__file__+'::original_whole_collector_distinct_buttons','exec'),namespace)
    SCOPE=namespace['prepare'](STATE)
    input_source=(ROOT/'mame-mkp/src/mame/midway/midtunit.cpp').read_text()
    sync.need('PORT_NAME("P1 High Kick")' in input_source and "fields['P1 High Kick']:set_value(1)" in LUA.read_text(),
              'Actual compiled High Kick input field, one physical controller')
    pins=dict(STATE['pins'])
    for p in (Path(__file__),LUA,Path(air.__file__),Path(run_source.__file__)):
        pins[str(p.resolve())]=sync.sha(p)
    STATE['pins']=pins
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(dict(passed=True,preflightOnly=True,
        sourceModelsReusedFromActualQualifiedCase=True,inputHashes=pins,nativeRuntimeAccepted=False,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0),indent=2)+'\n')
    return SimpleNamespace(STATE=STATE,SCOPE=SCOPE,OUT=OUT,BASE=BASE,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,DISPLAY=DISPLAY)


def run(prepared):
    source=inspect.getsource(run_source.execute)
    source=source.replace('LOWKICK_INPUT','HIGHKICK_INPUT').replace('LOWKICK_BIND','HIGHKICK_BIND')
    source=source.replace('fresh_actual_IN2_lowkick_saved_owners','fresh_actual_IN0_highkick_saved_owners')
    scope=dict(vars(run_source),OUT=ROOT/'audit_native_selector_fresh_highkick_owners_capture_checked',__file__=__file__)
    exec(compile(source,__file__+'::original_whole_capture_distinct_physical_highkick','exec'),scope)
    exec(compile(inspect.getsource(run_source.safe_execute),__file__+'::preserve_actual_highkick_failure','exec'),scope)
    return scope['safe_execute'](prepared)
