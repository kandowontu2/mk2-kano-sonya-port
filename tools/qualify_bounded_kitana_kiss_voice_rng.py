"""Separate original count input from observed native random result."""
import inspect
import qualify_bounded_kitana_kiss_voice_packets as previous

def main():
    source=inspect.getsource(previous.voice_gate)
    before="    assert steps[1]['a0']==steps[2]['a0']=='00000002'"
    assert source.count(before)==1
    source=source.replace(before,"    assert steps[1]['a0']=='00000002'\n    random_value=int(steps[2]['a0'],16);assert random_value in (1,2)")
    source=source.replace('nativeVariantCount=2','nativeVariantCount=2,observedNativeRandomValue=random_value')
    main_source=inspect.getsource(previous.main).replace('audit_bounded_kitana_kiss_voice_packets_checked','audit_bounded_kitana_kiss_voice_rng_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::native_random_result','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
