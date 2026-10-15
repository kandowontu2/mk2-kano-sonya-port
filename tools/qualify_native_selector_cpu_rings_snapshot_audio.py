"""Same new three-shot capture, whole original startup-to-terminal sound model.

Original route/source/DCS/clock/waveform/DAC/ROM equations and all30 faults
retained. Only actual new recorder namespace, terminal PID and current full
state/health receipt differ. No old PCM, clock or outcome substituted.
"""
import inspect
import json
import traceback
import qualify_native_selector_cpu_startup_ring_audio as original
import capture_native_selector_cpu_rings_snapshot_ram as capture
import qualify_native_selector_cpu_rings_snapshot_transport as transport

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_cpu_rings_snapshot_audio_checked'


def execute(state):
    from types import SimpleNamespace
    recorder=SimpleNamespace(**dict(vars(capture),OUT=transport.OUT))
    source=inspect.getsource(original.execute)
    for before,after in (
        ('(46264,38752,1791748793.1740513)','(16764,38752,1791765504.9070606)'),
        ("receipt['originalNativeStateContract']","receipt['wholeNativeStateHealth']"),
        ('for p in (Path(__file__).resolve(),Path(model.__file__).resolve(),',
         'for p in (Path(__file__).resolve(),Path(original_source).resolve(),Path(capture_source).resolve(),Path(model.__file__).resolve(),')):
        need(source.count(before)==1,'Only original actual capture/source provenance boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(original),OUT=OUT,__file__=__file__,capture=recorder,
               original_source=original.__file__,capture_source=capture.__file__)
    exec(compile(source,__file__+'::whole_original_three_release_cues_full_PCM_DCS_ROM','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual three-shot audio qualification failure')
        OUT.mkdir();original.dac_model.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False))
        raise
