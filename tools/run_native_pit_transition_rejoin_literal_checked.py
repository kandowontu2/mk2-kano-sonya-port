"""Whole Pit continuation: distinguish quoted substitutions from executed Lua.

Keep original expanded-source rejection frozen. The rejected snapshot token
is the quoted OLD replacement key, not a callable disk sink. Require exact
full reference-source transformations before checking actual Lua tokens.
"""
import json
import re
from pathlib import Path
import run_native_pit_transition_rejoin_expanded as original

ROOT,need,sha,once=original.ROOT,original.need,original.sha,original.once
LITERAL_FAILURE=ROOT/'audit_native_pit_transition_rejoin_expanded_kano_p1_checked/report.json'
failure=json.loads(LITERAL_FAILURE.read_text())
need(not failure['passed']and failure['error']=="ValueError('Only passive observer targets change, no guest/register/raw-file writes')"and
     not(ROOT/'audit_native_pit_transition_rejoin_expanded_kano_p1_ram').exists(),
     'Exact immutable quoted-old-key rejection before native boot')


def strip_lua_strings(text):
    return re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"",'quoted_literal',text)


def exact_expanded_source():
    display=(ROOT/'mk2ks_native_tomb_rejoin_display.lua').read_text()
    display=once(display,"local f=assert(io.open('mk2ks_native_tomb_display_v2062.lua','rb'))",
        "local f=assert(io.open('mk2ks_native_pit_display_v2092.lua','rb'))")
    display=once(display,"once(\"dofile('mk2ks_stage_branch_provenance_v1722.lua')\",\"dofile('mk2ks_native_tomb_rejoin_provenance.lua')\")",
        "once(\"dofile('mk2ks_native_stage_performer_v806.lua')\",\"dofile('mk2ks_native_pit_rejoin_provenance.lua')\")")
    display=once(display,"once('\\nend\\n-- END v2062 full-render read-only observer','\\n'..post..'\\nend\\n-- END v2062 full-render read-only observer')",
        "once('\\nend\\n-- END v2092 full-render read-only observer','\\n'..post..'\\nend\\n-- END v2092 full-render read-only observer')")
    display=once(display,'MK2_CURRENT_TOMB_RENDER_DEADLINE','MK2_CURRENT_PIT_RENDER_DEADLINE')
    timing=(ROOT/'mk2ks_native_tomb_rejoin_timing_display.lua').read_text()
    timing=once(timing,"io.open('mk2ks_native_tomb_rejoin_display.lua','rb')",
                       "io.open('mk2ks_native_pit_rejoin_expanded_display.lua','rb')")
    timing=once(timing,"once(\"dofile('mk2ks_native_tomb_rejoin_provenance.lua')\",\"dofile('mk2ks_native_tomb_rejoin_guarded_provenance.lua')\")",
        "assert(source:find(\"dofile('mk2ks_native_pit_rejoin_provenance.lua')\",1,true))")
    scanout=(ROOT/'mk2ks_native_tomb_rejoin_scanout_display.lua').read_text()
    scanout=once(scanout,"io.open('mk2ks_native_tomb_rejoin_timing_display.lua','rb')",
                        "io.open('mk2ks_native_pit_rejoin_expanded_timing_display.lua','rb')")
    for name,expected in(('display',display),('timing_display',timing),('scanout_display',scanout)):
        need((ROOT/('mk2ks_native_pit_rejoin_expanded_'+name+'.lua')).read_text()==expected,
             'Entire original passive transport/timing/register source, only exact declared Pit targets '+name)
    # Every actual original Pit disk sink is replaced exactly once in the
    # generated body. Its later transport contains no disk snapshot call.
    body=(ROOT/'mk2ks_native_pit_display_v2092.lua').read_text()
    for old,new in(("dofile('mk2ks_native_stage_performer_v806.lua')","dofile('mk2ks_native_pit_rejoin_provenance.lua')"),
                    ("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)'),
                    ('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')):
        body=once(body,old,new)
    need(not re.search(r':write_u\d+|\.value\s*=(?!=)|load_?state|snapshot\(|io\.open',strip_lua_strings(body)),
         'Actual whole generated Pit observer has no guest/register/raw-file writes')


source=original.source
source=once(source,"PREFIX='audit_native_pit_transition_rejoin_expanded'","PREFIX='audit_native_pit_transition_rejoin_literal_checked'")
source=once(source,"leaf = f'audit_native_pit_transition_rejoin_expanded_{fighter}_p{side}'",
                   "leaf = f'audit_native_pit_transition_rejoin_literal_checked_{fighter}_p{side}'")
source=once(source,"    pins={}","    exact_expanded_source()\n    pins={}")
source=once(source,"load_?state|snapshot\\(',text)","load_?state|snapshot\\(',strip_lua_strings(text))")
source=once(source,"    for p in(*LUA,Path(__file__).resolve(),original_source_path,failure_path,source_bound_path,failed_native_output,",
    "    for p in(*LUA,Path(__file__).resolve(),expanded_source_path,literal_failure,original_source_path,failure_path,source_bound_path,failed_native_output,")
scope=dict(__name__=__name__,__file__=__file__,original_source_path=original.original_source_path,
           failure_path=original.failure_path,source_bound_path=original.source_bound_path,
           failed_native_folder=original.failed_native_folder,failed_native_output=original.failed_native_output,
           expanded_source_path=Path(original.__file__),literal_failure=LITERAL_FAILURE,
           strip_lua_strings=strip_lua_strings,exact_expanded_source=exact_expanded_source)
exec(compile(source,__file__+'::whole_Pit_trial_exact_reference_source_and_actual_Lua_tokens','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
