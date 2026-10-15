"""Whole settled-cursor Pit trial; hash non-source artifacts as bytes, not Lua.

Retain actual preboot compressed-log decode failure. All binary evidence
still receives its exact full-byte SHA; only Lua source requires text scanning.
Bound diagnostic exception text so a decoder never prints its entire input.
"""
import json
from pathlib import Path
import run_native_pit_transition_rejoin_settled as original

ROOT,need,sha,once=original.ROOT,original.need,original.sha,original.once
BYTE_FAILURE=ROOT/'audit_native_pit_transition_rejoin_settled_kano_p1_checked/report.json'
failure=json.loads(BYTE_FAILURE.read_text())
need(not failure['passed']and failure['error'].startswith("UnicodeDecodeError('charmap', b")and
     'source_guard'in failure['traceback']and 'read_text'in failure['traceback']and
     not(ROOT/'audit_native_pit_transition_rejoin_settled_kano_p1_ram').exists(),
     'Actual immutable binary-log/source-reader failure occurred before native boot')
source=original.source
source=once(source,"PREFIX='audit_native_pit_transition_rejoin_settled'","PREFIX='audit_native_pit_transition_rejoin_settled_bytes'")
source=once(source,"leaf = f'audit_native_pit_transition_rejoin_settled_{fighter}_p{side}'",
                   "leaf = f'audit_native_pit_transition_rejoin_settled_bytes_{fighter}_p{side}'")
source=once(source,'        text=p.read_text()',"        text=p.read_text()if p.suffix=='.lua'else''")
source=once(source,"    for p in(*LUA,Path(__file__).resolve(),literal_source_path,",
    "    for p in(*LUA,Path(__file__).resolve(),settled_source_path,byte_failure,literal_source_path,")
source=once(source,'report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),',
    "report=dict(passed=False,error=type(error).__name__+': '+str(error)[:4096],traceback=traceback.format_exc(),")
scope=dict(__name__=__name__,__file__=__file__,original_source_path=original.original_source_path,
           failure_path=original.failure_path,source_bound_path=original.source_bound_path,
           failed_native_folder=original.failed_native_folder,failed_native_output=original.failed_native_output,
           expanded_source_path=original.expanded_source_path,literal_failure=original.literal_failure,
           strip_lua_strings=original.strip_lua_strings,settled_source_proof=original.settled_source_proof,
           literal_source_path=original.literal_source_path,race_receipt=original.race_receipt,
           race_output=original.race_output,race_folder=original.race_folder,
           settled_source_path=Path(original.__file__),byte_failure=BYTE_FAILURE)
exec(compile(source,__file__+'::entire_original_Pit_trial_source_scan_only_actual_Lua_and_all_byte_pins','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
