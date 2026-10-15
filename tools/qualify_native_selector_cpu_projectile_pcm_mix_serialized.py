"""Same original full mixed waveform; exact video8-decimal serialization.

Preserve the initial video-vs-full-double matcher rejection. The native video
observer explicitly prints %.8f; sound callbacks retain all64 position bits.
No timing/gain tolerance or waveform fit, and no native replay.
"""
import inspect,json,traceback
import qualify_native_selector_cpu_projectile_pcm_mix as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_mix_serialized_checked'


def execute(state):
    rejected=json.loads((prior.OUT/'failure.json').read_text())
    need(not rejected['passed']and rejected['newNativeGames']==0 and
         'Every source-derived native channel/length/position MK2_MAUDIO_CHANNEL' in rejected['error']and
         "'1818', '0'" in rejected['error'],'Actual original first video serialization rejection preserved')
    scope=dict(vars(prior),OUT=OUT,__file__=__file__)
    source=inspect.getsource(prior.channel_clocks)
    before="need(actual==want,'Every source-derived native channel/length/position "
    after="need(actual[:2]==want[:2]and (r['pos']==format(want[2],'.8f')if video else actual[2]==want[2]),'Every source-derived native channel/length/position "
    need(source.count(before)==1,'Only exact original declared video serialization differs')
    exec(compile(source.replace(before,after,1),__file__+'::whole_source_clocks_exact_video_serialization','exec'),scope)
    exec(compile(inspect.getsource(prior.execute),__file__+'::whole_original_complete_native_mix','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve original successor matcher rejection')
        OUT.mkdir();prior.capture.prior.current.prior.save(OUT/'failure.json',dict(passed=False,goalStatus='active',
            error=repr(error),traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False))
        raise
