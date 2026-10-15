"""P2 observed105-field voice packets; stock timing parity explicitly unproven."""
import inspect
import qualify_bounded_jax_arms_voice_priority as previous

def main():
    gate_source=inspect.getsource(previous.gate)
    assert gate_source.count('104')==3
    gate_source=gate_source.replace('104','105')
    main_source=inspect.getsource(previous.main)
    assert main_source.count('ready+104')==1
    main_source=main_source.replace('ready+104','ready+105')
    before="audit_bounded_jax_arms_voice_priority_p{side}_checked"
    assert main_source.count(before)==1
    main_source=main_source.replace(before,'audit_bounded_p2_jax_arms_voice_observed_checked')
    main_source=main_source.replace('heardAudioAccepted=False,allEffectPacketsVerified=False','heardAudioAccepted=False,stockVoiceTimingParityAccepted=False,allEffectPacketsVerified=False')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate_source+'\n'+main_source,__file__+'::observed_P2_route','exec'),namespace)
    namespace['main'](2)

if __name__=='__main__':main()
