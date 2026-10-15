"""All four current Pit19 sound/owner contexts, without replacing baseline.

Run only after each original capture interpreter releases its full bound RAM.
Every original per-case waveform, source, fault, queue and retirement check is
retained. Earlier three-owner matrix stays required, unchanged and correctly
limited. Wider suppression/stock/mirror/stage/port acceptance stays false.
"""
import inspect
import json
from pathlib import Path
import check_native_current_pit_19_audio_matrix as original
import run_native_current_cross_pit_19_audio as host


def run():
    prior_path=original.OUT/'report.json'
    prior=original.read(prior_path)
    original.need(prior['passed'] and prior['directOwnedAudioContexts']==3 and
                  not prior['allFourDirectOwnerRNGContextsAccepted'] and
                  all(original.sha(p)==h for p,h in prior['inputHashes'].items()),
                  'Actual four waveform/three owned predecessor remains frozen at its scope')
    body=inspect.getsource(original.run)
    body=host.once(body,"has_owners=(fighter,side)!=('kano',1)","has_owners=True")
    body=host.once(body,'Three actual directly observed own cinematic actors',
                   'All four actual directly observed own cinematic actors')
    body=host.once(body,"    bind(scope['inputHashes'])",
        "    bind(scope['inputHashes'])\n    bind(prior['inputHashes'])\n    bind({str(prior_path):sha(prior_path)})")
    for before,after in (('directOwnedAudioContexts=3','directOwnedAudioContexts=4'),
                         ('allFourDirectOwnerRNGContextsAccepted=False','allFourDirectOwnerRNGContextsAccepted=True'),
                         ('actualDirectOwnerFaults=66','actualDirectOwnerFaults=88'),
                         ('actualObservedQueueRNGFaults=108','actualObservedQueueRNGFaults=144')):
        body=host.once(body,before,after)
    scope=dict(vars(original),__file__=__file__,prior=prior,prior_path=prior_path,
               OUT=original.ROOT/'audit_native_current_pit_19_four_owned_audio_checked')
    exec(compile(body,__file__+'::entire_four_current_owned_sound_matrix','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v for k,v in result.items()if k not in
        ('inputHashes','originalNaturalIntegrationRequirements','originalRemainingWorkGroups')},indent=2))
