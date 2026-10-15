"""Repair only the source-pin name collision after positive geometry/faults.

The previous JSON parent shadowed a module alias during final inventory
construction. Preserve that rejection and rerun all original positive/faults.
"""
from pathlib import Path
import qualify_native_selector_opposite_roles_throw_floor_hidden_scope as previous

ROOT=previous.ROOT
PIN_FAILURE=previous.OUT/'failure.json'
WORDS_SOURCE=Path(previous.hidden_parent.parent.__file__)
source=previous.source
source=previous.current.replace(source,
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_scope_checked'",
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_pins_checked'")
source=previous.current.replace(source,'Path(parent.__file__)','WORDS_SOURCE')
source=previous.current.replace(source,
    'for path in (Path(__file__),Path(hidden_parent.__file__),SCOPE_FAILURE,',
    'for path in (Path(__file__),Path(previous.__file__),PIN_FAILURE,Path(hidden_parent.__file__),SCOPE_FAILURE,')
scope=dict(previous.scope,__file__=__file__,previous=previous,PIN_FAILURE=PIN_FAILURE,WORDS_SOURCE=WORDS_SOURCE)
exec(compile(source,__file__+'::unchanged_original_geometry_and_faults_source_pin_only','exec'),scope)
OUT=scope['OUT']
execute=scope['execute']
safe_execute=scope['safe_execute']
