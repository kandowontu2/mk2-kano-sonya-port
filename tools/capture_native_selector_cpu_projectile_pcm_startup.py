"""Distinct real guard-from-start policy; observe either native startup cue.

Keep original complete cold windows, terminal-first exact identities, every
PCM/DAC/ROM block and full original state contract (separately if rejected).
Neither the CPU roster nor its move or RNG is supplied. No raw media files.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_projectile_pcm_natural as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_projectile_pcm_startup_ram'
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_startup_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_projectile_pcm_startup.lua'
KEY='cpu_kano_p2_startup_pcm_boot608_confirm264_guard_wait'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={}
SCOPE=None

def prepare():
    original=prior.prior
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        __file__=__file__,observe_original_state_contract=prior.observe_original_state_contract)
    exec(compile(inspect.getsource(original.decode_audio),__file__+'::whole_original_audio_transport','exec'),scope)
    source=inspect.getsource(original.functions)
    for before,after in (("MK2KS_TEST_BOOT_FRAME='607'","MK2KS_TEST_BOOT_FRAME='608'"),
        ("MK2KS_CPU_PAIR_APPROACH='original'","MK2KS_CPU_PAIR_APPROACH='guard_wait'")):
        need(source.count(before)==1,'Exactly declared distinct physical input strategy')
        source=source.replace(before,after,1)
    exec(compile(source,__file__+'::whole_original_collector_guard_from_start','exec'),scope)
    source=inspect.getsource(original.execute)
    before="sources=[LUA,ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',"
    after="sources=[LUA,ROOT/'mk2ks_native_selector_cpu_projectile_pcm_startup_base.lua',ROOT/'mk2ks_native_selector_cpu_projectile_pcm_natural.lua',ROOT/'mk2ks_native_selector_cpu_projectile_pcm.lua',ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',"
    need(source.count(before)==1,'Every loaded nested observer is explicitly pinned')
    source=source.replace(before,after,1)
    before='full_state=physical.allocation.phase.model.verify'
    need(source.count(before)==1,'Preserve actual whole original mirror-contract outcome separately')
    source=source.replace(before,"full_state=lambda text,guest:observe_original_state_contract(text,guest,'kano')",1)
    before='PCMSourceWaveformAcceptance=False,PCMArtisticAcceptance=False,fullPortAcceptance=False,'
    need(source.count(before)==1,'Transport is not full waveform/move/port acceptance')
    source=source.replace(before,"PCMSourceWaveformAcceptance=False,PCMArtisticAcceptance=False,fullPortAcceptance=False,\n        originalNativeStateContract=report['sourceBoundBodyShadowSemantics'],",1)
    exec(compile(source,__file__+'::whole_current_startup_PCM_capture','exec'),scope)
    return scope

def execute(state,preflight=False):
    global SCOPE
    path=ROOT/'audit_native_selector_cpu_projectile_pcm_checkpoint_checked/report.json'
    proof=json.loads(path.read_text())
    need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()), 'Previous full finite PCM/source/delivery and original14 requirements intact')
    need(prior.NATIVE_HANDLES[prior.KEY]['process'].poll()==0 and prior.NATIVE_HANDLES[prior.KEY]['process'].pid==47172,
         'Previous audio game really terminal; distinct physical guard policy is not a timeout replay')
    SCOPE=prepare()
    return SCOPE['execute'](state,preflight)
