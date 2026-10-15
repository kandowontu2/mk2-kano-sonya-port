"""Native new_launch clears pointers before start; derive last generated cache."""
import json
from decimal import Decimal
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_audio_startup as rejected

failure=rejected.OUT/'failure.json';waveform_failure=rejected.OUT/'waveform.json'
rejected.need(json.loads(failure.read_text())['error']==
    "ValueError('Whole actual mixed PCM with real three-kick cry replacement source exact')" and
    json.loads(waveform_failure.read_text())['differentChannelSamples']==320,
    'Keep actual320-sample premature flush/replacement source-model rejection')


def channel_cutoff(event,events,headers):
    original=rejected.compound.original
    next_events=[e for e in events if e['channel']==event['channel'] and e['start']>event['start']]
    if not next_events:return 10**30
    following=min(next_events,key=lambda e:e['start'])
    if event['start']+len(event['sample'])<=following['start']:return following['start']
    rejected.need(event['channel']==13 and event['marker']['frame']=='2731' and following['marker']['frame']=='2806',
                  'This actual overlapping source is the second CPU cry, not an arbitrary cropped clip')
    main=next(e for e in events if e['channel']==12 and e['marker']['frame']==event['marker']['frame'])
    next_main=next(e for e in events if e['channel']==12 and e['marker']['frame']==following['marker']['frame'])
    onset=int(Decimal(main['marker']['seconds'])*original.ATTO)
    stop=int(Decimal(next_main['marker']['seconds'])*original.ATTO);period=original.ATTO//60
    tick=(stop-onset-1)//period;previous=onset+tick*period
    earlier=[int(Decimal(h['seconds'])*original.ATTO) for h in headers if int(Decimal(h['seconds'])*original.ATTO)<stop]
    rejected.need(earlier and previous<stop and original.sample_clock(str(Decimal(previous)/original.ATTO),True)-main['start']>=len(main['sample']),
                  'Main has reached EOF; original && actually queries auxiliary at the last60Hz tick')
    last_update=max(max(earlier),previous)
    cutoff=original.sample_clock(str(Decimal(last_update)/original.ATTO),True)
    rejected.need(event['start']<cutoff<following['start'],'Native stop-without-update preserves only already-generated cry cache')
    return cutoff


source=Path(rejected.rejected.__file__).read_text()
# Retain the one-Ring constructor and both actual failed models unchanged.
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_audio_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_audio_stop_checked'"),
    ('startupRing=prior.startup.startup_cue(text,guest)','startupRing=startup_cue(text,guest)'),
    ("next_start=min((e['start'] for e in events if e['channel']==event['channel'] and e['start']>event['start']),default=10**30)",
     'next_start=channel_cutoff(event,events,headers)'),
    ('scope=dict(vars(compound),__file__=__file__)',
     'scope=dict(vars(compound),__file__=__file__,channel_cutoff=channel_cutoff)'),
    ('for p in (Path(__file__),parent,Path(compound.__file__),',
     'for p in (Path(__file__),Path(rejected.__file__),Path(rejected.rejected.__file__),rejected.failure,failure,waveform_failure,parent,Path(compound.__file__),'),
    ("sameChannelReplacementSource='samples_device::start: stream->update(), replace source, pos=0'",
     "sameChannelReplacementSource='native new_launch -> stop both without update; preserve previous PCM/60Hz generated cache; start new source at native port clock'"),
    ('wholeActualAudioWaveformAccepted=True,',
     'wholeActualAudioWaveformAccepted=True,originalThreeRingAssumptionRejectionPreserved=True,originalFlushBeforeNativeStopRejectionPreserved=True,')):
    rejected.need(source.count(before)==1,'Only source-exact stop/cache chronology and immutable failure preservation')
    source=source.replace(before,after,1)
startup_cue=rejected.startup_cue
exec(compile(source,__file__+'::whole_source_native_new_launch_stop_cache','exec'))
