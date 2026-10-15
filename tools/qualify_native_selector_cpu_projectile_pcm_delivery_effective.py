"""Whole original delivery gate with two effective counterexamples.

Native first port byte FF01 and DSP read 0001 were mistakenly reused as
corruptions. Preserve both failures, all positive rules and all other faults.
"""
import inspect
from pathlib import Path
import qualify_native_selector_cpu_projectile_pcm_delivery as original
import qualify_native_selector_cpu_projectile_pcm_delivery_byte as byte_trial

OUT = original.ROOT / 'audit_native_selector_cpu_projectile_pcm_delivery_effective_checked'
scope = dict(vars(original), __file__=__file__, OUT=OUT)
source = inspect.getsource(original.execute)
for before, after in (
    ("alter('MK2_MAUDIO_SOUND','word','FF01',pc='FFA13C90',frame=1837)",
     "alter('MK2_MAUDIO_SOUND','word','FF03',pc='FFA13C90',frame=1837)"),
    ("alter('MK2_MAUDIO_DELIVERY','word','0001',dsp_pc='03A1')",
     "alter('MK2_MAUDIO_DELIVERY','word','0003',dsp_pc='03A1')"),
    ('for p in(Path(__file__),Path(prior.__file__)',
     "for p in(Path(__file__),Path(delivery_original.__file__),delivery_original.OUT/'failure.json',Path(byte_trial.__file__),byte_trial.OUT/'failure.json',Path(prior.__file__)")):
    original.need(source.count(before) == 1, 'Exactly specified original counterexample/pin correction')
    source = source.replace(before, after, 1)
scope.update(delivery_original=original, byte_trial=byte_trial)
exec(compile(source, __file__ + '::entire_delivery_effective_counterexamples', 'exec'), scope)
exec(compile(inspect.getsource(original.safe_execute), __file__ + '::original_failure_handler', 'exec'), scope)
execute = scope['execute']
safe_execute = scope['safe_execute']
