"""Retain full delivery qualification; correct a no-op counterexample.

The original first high-byte store is FF01. Its intended corruption was also
FF01, so the original checker correctly rejected the test itself. Change that
counterexample to FF03, not the native capture or acceptance rules.
"""
import inspect
from pathlib import Path
import qualify_native_selector_cpu_projectile_pcm_delivery as prior

OUT = prior.ROOT / 'audit_native_selector_cpu_projectile_pcm_delivery_byte_checked'
scope = dict(vars(prior), __file__=__file__, OUT=OUT)
source = inspect.getsource(prior.execute)
old = "alter('MK2_MAUDIO_SOUND','word','FF01',pc='FFA13C90',frame=1837)"
prior.need(source.count(old) == 1, 'Exactly the original no-op port-byte fault')
source = source.replace(old, old.replace("'FF01'", "'FF03'"), 1)
old_pins = 'for p in(Path(__file__),Path(prior.__file__)'
prior.need(source.count(old_pins) == 1, 'Preserve original executed-source pin inventory')
source = source.replace(old_pins,
    "for p in(Path(__file__),Path(delivery_original.__file__),delivery_original.OUT/'failure.json',Path(prior.__file__)", 1)
scope['delivery_original'] = prior
exec(compile(source, __file__ + '::whole_delivery_with_effective_byte_fault', 'exec'), scope)
exec(compile(inspect.getsource(prior.safe_execute), __file__ + '::preserved_failure_handler', 'exec'), scope)
execute = scope['execute']
safe_execute = scope['safe_execute']
