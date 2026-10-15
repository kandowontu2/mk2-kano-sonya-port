"""Exact5929 scene source, restoring the full original5908 execution globals.

Preserve the actual5931 missing-continuous binding failure. No scene, shadow,
font, floor, source or fault predicate changes; use the existing complete
native scene function's original namespace, not the wrapper module globals.
"""
import current_pit_shadow_schedule_contract_v5929 as executed
from current_pit_shadow_schedule_contract_v5929 import *
scope=dict(executed.previous.scene_contract.__globals__,policy=executed.policy,__file__=__file__)
exec(compile(executed.source,__file__+'::exact5929_whole5908_original_globals','exec'),scope)
scene_contract=scope['scene_contract']
need(scene_contract.__code__.co_code==executed.scene_contract.__code__.co_code and
     scope['continuous']is executed.previous.previous.continuous,
     'Byte-identical full scene function with restored exact original continuous-render dependency')
