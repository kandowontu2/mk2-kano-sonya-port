"""Distinct physical boot608; current PCM under the actual natural CPU roster.

Keep failed boot607 mirror-only observation and all current cold/transport/
PID/source rules. Unchanged mirror state checker remains separately reported;
a naturally different CPU is not waived into mirror gameplay acceptance.
"""
import inspect,json
from pathlib import Path
import capture_native_selector_cpu_projectile_pcm as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_projectile_pcm_natural_ram'
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_natural_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_projectile_pcm_natural.lua'
KEY='cpu_kano_p2_projectile_pcm_natural_boot608_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={}
SCOPE=None


def observe_original_state_contract(b,guest,player):
    checker=prior.physical.allocation.phase.model
    try:return checker.verify(b,guest)
    except(AssertionError,ValueError,KeyError,IndexError)as error:
        selected=checker.original.pair.rows_prefix(b,'MK2_P2CPU_SELECT_RESULT ')
        cold=checker.original.pair.rows_prefix(b,'MK2_P2CPU_COLD_LIVE ')
        need(len(selected)==len(cold)==1 and selected[0]['human_id']==cold[0]['human_id']==17 and
             selected[0]['checks']==50 and selected[0]['errors']==0,
             'Real human Kano selection retained; natural CPU identity not prescribed')
        return dict(passed=False,originalFullMirrorContractFailure=repr(error),
            actualSelection=selected[0],actualColdLive=cold[0],
            fullStockOpponentStateHealthAcceptance=False,fullPortAcceptance=False)


def prepare():
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,
        __file__=__file__,observe_original_state_contract=observe_original_state_contract)
    exec(compile(inspect.getsource(prior.decode_audio),__file__+'::whole_original_audio_transport','exec'),scope)
    source=inspect.getsource(prior.functions)
    need(source.count("MK2KS_TEST_BOOT_FRAME='607'")==1,'One distinct physical boot608 route')
    source=source.replace("MK2KS_TEST_BOOT_FRAME='607'","MK2KS_TEST_BOOT_FRAME='608'",1)
    exec(compile(source,__file__+'::whole_original_collector_natural_opponent','exec'),scope)
    source=inspect.getsource(prior.execute)
    before="sources=[LUA,ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',"
    need(source.count(before)==1,'Pin entire original failed observer unchanged')
    source=source.replace(before,"sources=[LUA,ROOT/'mk2ks_native_selector_cpu_projectile_pcm.lua',ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',",1)
    before='full_state=physical.allocation.phase.model.verify'
    need(source.count(before)==1,'Report unchanged mirror checker separately; do not waive into gameplay acceptance')
    source=source.replace(before,'full_state=lambda text,guest:observe_original_state_contract(text,guest,\'kano\')',1)
    before="PCMSourceWaveformAcceptance=False,PCMArtisticAcceptance=False,fullPortAcceptance=False,"
    need(source.count(before)==1,'Explicitly preserve original gameplay-contract outcome')
    source=source.replace(before,"PCMSourceWaveformAcceptance=False,PCMArtisticAcceptance=False,fullPortAcceptance=False,\n        originalNativeStateContract=report['sourceBoundBodyShadowSemantics'],",1)
    exec(compile(source,__file__+'::whole_current_natural_CPU_PCM_capture','exec'),scope)
    return scope


def execute(state,preflight=False):
    global SCOPE
    failed=prior.BASE/prior.KEY/'result.json'
    receipt=json.loads(failed.read_text());held=prior.NATIVE_HANDLES[prior.KEY]
    need(not receipt['passed']and receipt['nativeExit']==held['process'].poll()==0 and
         held['identity']==receipt['nativeTerminal']['actualWindowsIdentity']and held['process'].pid==46008 and
         not prior.AUDIO[prior.KEY]['pcmChunks']and not prior.AUDIO[prior.KEY]['dacChunks'],
         'Original mirror-only origin failed with zero PCM; exact terminal game retained, not restarted')
    SCOPE=prepare()
    return SCOPE['execute'](state,preflight)
