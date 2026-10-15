"""Correct actual terminal47272 Lua find/assert multi-return, retain both failures."""
import json
from pathlib import Path
import capture_native_selector_sonya_cpu_air_approach as source_capture
import capture_native_selector_sonya_cpu_air_approach_bound as prior_bound
import capture_native_selector_sonya_cpu_air_approach_ready as first_native
import capture_native_selector_sonya_cpu_air_approach_loaded as second_native

first_failure=source_capture.OUT/'failure.json'
second_failure=prior_bound.OUT/'failure.json'
native_failures=[m.OUT/'failure.json' for m in (first_native,second_native)]
failed_files=[]
for module,pid in ((first_native,30960),(second_native,47272)):
    failure=json.loads((module.OUT/'failure.json').read_text())
    source_capture.need(not failure['passed'] and failure['nativeExit']==3 and
        failure['actualNativeIdentity']['ProcessId']==pid and
        module.NATIVE_HANDLES[module.KEY]['process'].poll()==3 and failure['actualDenseDisplayCallbacks']==0,
        'Both original actual loader failures terminal, no observation-timeout substitution')
    folder=module.RAM_CASES[module.KEY][0]
    failed_files.extend(p for p in folder.rglob('*') if p.is_file())
source_capture.need("local 'last'" in (second_native.RAM_CASES[second_native.KEY][0]/'stderr.log').read_text(),
                    'Actual find/assert multi-return failure recorded')
source=Path(source_capture.__file__).read_text()
for before,after in (
    ('inspect.getsource(previous.prepare)','inspect.getsource(previous.original.prepare)'),
    ("BASE=ROOT/'audit_native_selector_sonya_cpu_air_approach_ram'",
     "BASE=ROOT/'audit_native_selector_sonya_cpu_air_approach_checked_ram'"),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_capture_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_checked_capture_checked'"),
    ("LUA=ROOT/'mk2ks_native_selector_sonya_cpu_air_approach.lua'",
     "LUA=ROOT/'mk2ks_native_selector_sonya_cpu_air_approach_checked.lua'"),
    ('for p in (Path(__file__),LUA,Path(snapshot.__file__),',
     "for p in (Path(__file__),Path(source_capture.__file__),Path(prior_bound.__file__),Path(first_native.__file__),Path(second_native.__file__),first_failure,second_failure,*native_failures,*failed_files,ROOT/'mk2ks_native_selector_sonya_cpu_air_approach.lua',ROOT/'mk2ks_native_selector_sonya_cpu_air_approach_loaded.lua',LUA,Path(snapshot.__file__),"),
    ("lua.count(\"io.open('mk2ks_native_selector_sonya_cpu_pressure_bound.lua','rb')\")==1 and\n         'walk_periodic_jump' in lua",
     "lua.count(\"io.open('mk2ks_native_selector_sonya_cpu_air_approach_loaded.lua','rb')\")==1 and\n         'two_real_find_results' in lua")):
    source_capture.need(source.count(before)==1, 'Only exact loader/failure-preservation boundaries')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_air_trial_actual_find_return_binding','exec'))
