"""Actual native round reset plus the complete existing adaptive response gate.

Keep all-mode native HP/reset/store replay and both independent ground/owner
streams. Every walk/jump/punch/recovery/survival criterion is the original
contract, bound to this run's actual post-draw fields and ordinary inputs.
"""
import inspect
import re
import verify_native_kano_laser_cpu_post_ko_ground as ground
import single_continue_controls_v6580 as original_controls

ROOT,need,once=ground.ROOT,ground.need,ground.once


def rows(text,tag):
    prefix='MK2_CPU_ROUND_HEALTH 'if tag=='HEALTH'else'MK2_POST_CTRL_'+tag+' '
    return [dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith(prefix)]


def round_binding():
    source=inspect.getsource(ground.binding)
    source=once(source,'    source=inspect.getsource(prior.check)',
        """    source=inspect.getsource(prior.check)
    source=once(source,"last==restart+60", "last==control_recovery+180")
    source=once(source,"'Exact sixty-field native post-reset observation'", "'Exact observed native control recovery plus180 survival fields'")""")
    source=once(source,'scope=dict(vars(prior))','scope=dict(vars(prior),control_recovery=control_recovery)')
    scope=dict(vars(ground),control_recovery=None)
    exec(compile(source,__file__+'::whole_actual_round_ground_gate_adaptive_terminal','exec'),scope)
    def binding(recover):
        scope['control_recovery']=recover
        return scope['binding']()
    return binding


def check(b,guest,payload,gfx):
    text=b['cpuLog'];result=rows(text,'RESULT')
    need(len(result)==1 and not rows(text,'FAILED'),'One actual adaptive terminal; no post-reset human KO or input timeout')
    recover=int(result[0]['recover']);terminal=int(result[0]['frame'])
    need(recover>0 and terminal==recover+180,'Actual full control recovery and exact survival terminal')
    round_result=round_binding()(recover)(b,guest,payload,gfx)
    fields=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_HPHASE_POST_FIELD ')]
    need(len({(r['frame'],r['slot'])for r in fields})==len(fields),'All actual native post-draw control fields are unique')
    events=dict(reReady=int(result[0]['ready']))
    original_controls.actual_controls(text,events,fields,1,terminal)
    need(events['reReady']==round_result['actualNativeResume'],
         'Adaptive ordinary controls start only at the actual independently proven native round reset')
    return dict(passed=True,round=round_result,actualControls=events,
        wholeOriginalAdaptiveResponseGateRetained=True,postResetWalkJumpPunchRecoveryAnd180SurvivalVerified=True,
        bodyShadowFaultsPending=True,fullPostResetRasterAcceptance=False,fullAudioAcceptance=False,
        allCPUContextsAccepted=False,fullPortAcceptance=False)
