"""Retain native absolute DAC ordinals in an explicitly scoped RAM interval."""
import inspect, json
from pathlib import Path
import qualify_challenger_retained_precombat as original
import qualify_kano_launch_audio_v6656 as dacmodel
ROOT, need, sha = original.ROOT, original.need, original.sha


def dac_models(count, first_index):
    source = inspect.getsource(dacmodel.host.models.original_dac.dac_gate)
    need(source.count('len(chunks)==len(headers)==len(pcm_headers)==685') == 1 and source.count("r['index']==str(i+1)") == 1, 'Entire original DAC gate; only duration and absolute ordinal origin differ')
    source = source.replace('len(chunks)==len(headers)==len(pcm_headers)==685', 'len(chunks)==len(headers)==len(pcm_headers)==count').replace("r['index']==str(i+1)", "r['index']==str(i+first_index)")
    scope = dict(vars(dacmodel.host.models.original_dac), count=count, first_index=first_index)
    exec(compile(source, __file__+'::whole_native_DAC_absolute_ordinals', 'exec'), scope)
    exec(compile(inspect.getsource(dacmodel.host.models.original_dac.dac_faults), __file__+'::whole_actual_DAC_faults', 'exec'), scope)
    return scope['dac_gate'], scope['dac_faults']


def qualify(c):
    failure = ROOT/'audit_challenger_precombat_DAC_ordinal_rejection'
    need(not failure.exists(), 'Fresh original executed ordinal rejection')
    failure.mkdir()
    (failure/'failure.json').write_text(json.dumps(dict(passed=False, nativeGameFailure=False,
        nativeTerminal=c['terminal'], error='Complete actual native DAC callback/ring/cursor/PCM association',
        cause='Original gate required scoped first absolute DAC ordinal1348 to equal1; the complete waveform and both-slot ownership already passed.',
        inputHashes={str(Path(original.__file__)): sha(original.__file__)}, newNativeBoots=0), indent=2)+'\n')
    source = inspect.getsource(original.qualify)
    before = "original.prior.mirror.qualifier.source_audio.dac_models(len(scoped['pcmHeaders']))"
    need(source.count(before) == 1, 'Complete same-terminal qualifier, no dropped positive contract')
    source = source.replace(before, "dac_models(len(scoped['pcmHeaders']), int(scoped['dacHeaders'][0]['index']))")
    source = source.replace('Path(__file__), Path(original.__file__),', 'Path(__file__), Path(adapter.__file__), Path(original.__file__),')
    scope = dict(vars(original), __file__=__file__, adapter=original, dac_models=dac_models)
    exec(compile(source, __file__+'::whole_original_scoped_qualification', 'exec'), scope)
    return scope['qualify'](c)
