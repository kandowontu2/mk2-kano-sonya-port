"""Preserve actual host-name collision; retain entire native eligibility model.

The clip module's eight scalar checks use a dict named clip. Executing that
original source in a shared host namespace replaced the module handle used by
the new independent eligibility helper. Explicit module alias only; no native
or geometry/coverage/fault assertion changes and no new game.
"""
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_round_shadow_eligibility as eligibility

eligibility_source=Path(eligibility.__file__)
eligibility_failure=eligibility.OUT/'failure.json'
need=eligibility.need
need(json.loads(eligibility_failure.read_text())['error']==
     'AttributeError("\'dict\' object has no attribute \'mechanics\'")',
     'Actual host namespace collision rejection preserved')
source=eligibility_source.read_text()
for before,after in (
    ('import qualify_native_selector_sonya_cpu_pressure_round_shadow_clip as clip',
     'import qualify_native_selector_sonya_cpu_pressure_round_shadow_clip as clip\nclip_module=clip'),
    ('clip.mechanics.capture.base.choices.native_state.original.pair',
     'clip_module.mechanics.capture.base.choices.native_state.original.pair'),
    ('audit_native_selector_sonya_cpu_pressure_round_shadow_eligibility_checked',
     'audit_native_selector_sonya_cpu_pressure_round_shadow_bound_checked'),
    ('Path(__file__),clip_source,clip_failure,original_source,original_failure,ops,parent,Path(disasm.__file__),',
     'Path(__file__),eligibility_source,eligibility_failure,clip_source,clip_failure,original_source,original_failure,ops,parent,Path(disasm.__file__),')):
    expected=2 if before.startswith('clip.mechanics.')else 1
    need(source.count(before)==expected,'Only exact independent helper module-alias/source preservation boundary')
    source=source.replace(before,after)
exec(compile(source,str(eligibility_source)+'::whole_original_model_explicit_clip_module_handle','exec'))
