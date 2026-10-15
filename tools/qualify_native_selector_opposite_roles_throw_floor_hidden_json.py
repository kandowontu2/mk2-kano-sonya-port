"""Publish all internal field/slot keys losslessly as JSON text keys.

All original geometry and27 effective fault checks rerun unchanged. Only the
completed report's tuple-key dictionary is converted after every assertion.
"""
from pathlib import Path
import qualify_native_selector_opposite_roles_throw_floor_hidden_pins as previous

ROOT=previous.ROOT
JSON_FAILURE=previous.OUT/'failure.json'
SCOPE_SOURCE=Path(previous.previous.__file__)
current=previous.previous.current
source=previous.source
source=current.replace(source,
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_pins_checked'",
    "OUT=ROOT/'audit_native_selector_opposite_roles_throw_floor_hidden_json_checked'")
source=current.replace(source,
    'for path in (Path(__file__),Path(previous.__file__),PIN_FAILURE,',
    'for path in (Path(__file__),Path(previous.__file__),JSON_FAILURE,SCOPE_SOURCE,PIN_FAILURE,')
source=current.replace(source,
    "    OUT.mkdir();current.prior.save(OUT/'report.json',value)",
    "    fields=value['wholeNativeBodyROMShadowCase']['state']['floorByDrawingField']\n    value['wholeNativeBodyROMShadowCase']['state']['floorByDrawingField']={f'{f}:{s}':v for (f,s),v in fields.items()}\n    need(len(fields)==len(value['wholeNativeBodyROMShadowCase']['state']['floorByDrawingField']),'Lossless full field/slot JSON publication only after qualification')\n    OUT.mkdir();current.prior.save(OUT/'report.json',value)")
scope=dict(previous.scope,__file__=__file__,previous=previous,JSON_FAILURE=JSON_FAILURE,SCOPE_SOURCE=SCOPE_SOURCE)
exec(compile(source,__file__+'::unchanged_original_geometry_with_lossless_JSON_keys','exec'),scope)
OUT=scope['OUT']
execute=scope['execute']
safe_execute=scope['safe_execute']
