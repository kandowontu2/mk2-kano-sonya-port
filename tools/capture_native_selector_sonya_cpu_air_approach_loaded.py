"""Preserve terminal30960 loader failure; correct defining Lua source boundary."""
import json
from pathlib import Path
import capture_native_selector_sonya_cpu_air_approach as source_capture
import capture_native_selector_sonya_cpu_air_approach_bound as prior_bound
import capture_native_selector_sonya_cpu_air_approach_ready as failed_native

first_failure=source_capture.OUT/'failure.json'
second_failure=prior_bound.OUT/'failure.json'
native_failure=failed_native.OUT/'failure.json'
proof=json.loads(native_failure.read_text())
source_capture.need(not proof['passed'] and proof['nativeExit']==3 and
                    proof['actualNativeIdentity']['ProcessId']==30960 and
                    failed_native.NATIVE_HANDLES[failed_native.KEY]['process'].poll()==3 and
                    proof['actualDenseDisplayCallbacks']==0,
                    'Actual loader failure terminal3 with no gameplay captures, never timeout restart')
failed_folder=failed_native.RAM_CASES[failed_native.KEY][0]
source_capture.need('assertion failed!' in (failed_folder/'stderr.log').read_text(),
                    'Real failed defining-source string lookup preserved')
source=Path(source_capture.__file__).read_text()
for before,after in (
    ('inspect.getsource(previous.prepare)','inspect.getsource(previous.original.prepare)'),
    ("BASE=ROOT/'audit_native_selector_sonya_cpu_air_approach_ram'",
     "BASE=ROOT/'audit_native_selector_sonya_cpu_air_approach_loaded_ram'"),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_capture_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_approach_loaded_capture_checked'"),
    ("LUA=ROOT/'mk2ks_native_selector_sonya_cpu_air_approach.lua'",
     "LUA=ROOT/'mk2ks_native_selector_sonya_cpu_air_approach_loaded.lua'"),
    ('for p in (Path(__file__),LUA,Path(snapshot.__file__),',
     "for p in (Path(__file__),Path(source_capture.__file__),Path(prior_bound.__file__),Path(failed_native.__file__),first_failure,second_failure,native_failure,*(p for p in failed_folder.rglob('*') if p.is_file()),ROOT/'mk2ks_native_selector_sonya_cpu_air_approach.lua',LUA,Path(snapshot.__file__),"),
    ("lua.count(\"io.open('mk2ks_native_selector_sonya_cpu_pressure_bound.lua','rb')\")==1 and\n         'walk_periodic_jump' in lua",
     "lua.count(\"io.open('mk2ks_native_selector_sonya_cpu_air_approach.lua','rb')\")==1 and\n         'actual_defining_source' in lua")):
    source_capture.need(source.count(before)==1, 'Only exact defining Lua source/failure-preservation boundaries')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_air_trial_correct_native_loader_no_state_assistance','exec'))
