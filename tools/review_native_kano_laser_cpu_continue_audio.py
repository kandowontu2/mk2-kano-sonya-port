"""Same complete CPU mirror proof against the corrected first-loss carrier."""
import inspect
from pathlib import Path
import review_native_kano_laser_cpu_audio as prior


def review(capture):
    source=inspect.getsource(prior.review)
    old="audit_native_kano_laser_cpu_audio_review"
    prior.need(source.count(old)==1,'Exact fresh corrected-fixture report target')
    source=source.replace(old,'audit_native_kano_laser_cpu_continue_audio_review')
    scope=dict(vars(prior),__file__=str(Path(__file__).resolve()))
    exec(compile(source,__file__+'::same_native_CPU_mirror_acceptance','exec'),scope)
    return scope['review'](capture)
