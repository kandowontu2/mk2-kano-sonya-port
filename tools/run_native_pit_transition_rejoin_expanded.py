"""Full Pit/rejoin trial with exact expanded observer source, failed inputs frozen.

The first native attempt exited3 during observer source adaptation, before
frame1 or guest transport. Nested source transformers require the complete
declared timing/display text, not wrappers around that text. All original
native model/earned/movie/floor/shadow/rejoin/fault gates remain unchanged.
"""
import json
from pathlib import Path
import run_native_pit_transition_rejoin_source_bound as original

ROOT,need,sha,once=original.ROOT,original.need,original.sha,original.once
FAILED_FOLDER=ROOT/'audit_native_pit_transition_rejoin_source_bound_kano_p1_ram'
FAILED_OUTPUT=ROOT/'audit_native_pit_transition_rejoin_source_bound_kano_p1_checked/report.json'
failed=json.loads(FAILED_OUTPUT.read_text());meta=json.loads((FAILED_FOLDER/'result.json').read_text())
need(not failed['passed']and meta['captureCompleted']and meta['exit_code']==3 and
     meta['ramGuestSHA256']is None and meta['observedRGBFields']==meta['modelExactFields']==0 and
     not meta['modelErrors']and 'whole_source_defined_completed_Pit_scanout:5: assertion failed!'
     in(FAILED_FOLDER/'stderr.log').read_text(),
     'Actual failed native observer startup preserved, no gameplay or guest proof claimed')
need(all(sha(p)==h for p,h in meta['input_hashes'].items()),'All actual failed native inputs unchanged')
source=original.source
source=once(source,"PREFIX='audit_native_pit_transition_rejoin_source_bound'",
                   "PREFIX='audit_native_pit_transition_rejoin_expanded'")
source=once(source,"leaf = f'audit_native_pit_transition_rejoin_source_bound_{fighter}_p{side}'",
                   "leaf = f'audit_native_pit_transition_rejoin_expanded_{fighter}_p{side}'")
old="LUA=tuple(ROOT/('mk2ks_native_pit_rejoin_'+name+'.lua')for name in\n          ('provenance','display','timing_display','scanout_display'))"
new="LUA=(ROOT/'mk2ks_native_pit_rejoin_provenance.lua',)+tuple(ROOT/('mk2ks_native_pit_rejoin_expanded_'+name+'.lua')for name in('display','timing_display','scanout_display'))"
source=once(source,old,new)
source=once(source,"    for p in(*LUA,Path(__file__).resolve(),original_source_path,failure_path):",
    "    for p in(*LUA,Path(__file__).resolve(),original_source_path,failure_path,source_bound_path,failed_native_output,"
    "*(p for p in failed_native_folder.rglob('*')if p.is_file())):")
scope=dict(__name__=__name__,__file__=__file__,original_source_path=original.original_source_path,
           failure_path=original.failure_path,source_bound_path=Path(original.__file__),
           failed_native_folder=FAILED_FOLDER,failed_native_output=FAILED_OUTPUT)
exec(compile(source,__file__+'::entire_original_Pit_trial_exact_expanded_observers_only','exec'),scope)
globals().update({k:v for k,v in scope.items()if not k.startswith('__')})
