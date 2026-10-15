"""Whole original audio checks, one genuinely observed startup Ring caller."""
import inspect,json
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_audio as rejected

failure=rejected.OUT/'failure.json'
rejected.need(json.loads(failure.read_text())['error']==
    "ValueError('All three actual ring release voice callers own their real18 actor/Main')",
    'Actual unrelated three-Ring inventory assumption rejected; keep full original source and failure')
startup_source=inspect.getsource(rejected.prior.startup.startup_cue)
for before,after in (
    ('len(route)==3','len(route)==1'),
    ('All three actual ring release voice callers own their real18 actor/Main','Whole actual single startup Ring caller owns real18 actor/Main'),
    ('actualRingVoiceCalls=3','actualRingVoiceCalls=1')):
    rejected.need(startup_source.count(before)==1,'Only actual one-Ring entry inventory boundary')
    startup_source=startup_source.replace(before,after,1)
startup_scope=dict(rejected.prior.startup.startup_cue.__globals__)
exec(compile(startup_source,__file__+'::whole_original_single_actual_Ring_cue','exec'),startup_scope)
startup_cue=startup_scope['startup_cue']
source=Path(rejected.__file__).read_text()
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_audio_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_audio_startup_checked'"),
    ('startupRing=prior.startup.startup_cue(text,guest)','startupRing=startup_cue(text,guest)'),
    ('for p in (Path(__file__),parent,Path(compound.__file__),',
     'for p in (Path(__file__),Path(rejected.__file__),failure,parent,Path(compound.__file__),'),
    ('wholeActualAudioWaveformAccepted=True,','wholeActualAudioWaveformAccepted=True,originalThreeRingAssumptionRejectionPreserved=True,')):
    rejected.need(source.count(before)==1,'Only startup evidence inventory and failed-source preservation')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_actual_air_trial_audio_single_Ring_context','exec'))
