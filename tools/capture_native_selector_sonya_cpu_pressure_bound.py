"""Same full pressure capture; preserve preflight-pinned generated Lua source.

Only loader text boundary corrected before native execution. No prior failed
native run is claimed; the first Python preflight never compiled nested Lua.
"""
from pathlib import Path
import capture_native_selector_sonya_cpu_pressure as original

path=Path(original.__file__)
original_capture_source=path
source=path.read_text()
for before,after in (
    ("BASE=ROOT/'audit_native_selector_sonya_cpu_pressure_ram'",
     "BASE=ROOT/'audit_native_selector_sonya_cpu_pressure_bound_ram'"),
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_capture_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_bound_capture_checked'"),
    ("LUA=ROOT/'mk2ks_native_selector_sonya_cpu_pressure.lua'",
     "LUA=ROOT/'mk2ks_native_selector_sonya_cpu_pressure_bound.lua'"),
    ('Path(__file__),LUA,checkpoint,',
     "Path(__file__),original_capture_source,ROOT/'mk2ks_native_selector_sonya_cpu_pressure.lua',LUA,checkpoint,"),
    ('lua=LUA.read_text()', "lua=(ROOT/'mk2ks_native_selector_sonya_cpu_pressure.lua').read_text()")):
    original.need(source.count(before)==1,'Only explicit Lua loader/source-preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,str(path)+'::whole_original_pressure_capture_with_bound_Lua_loader','exec'))
