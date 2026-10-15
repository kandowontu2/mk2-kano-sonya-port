"""Exact cue equals actual native base plus random result minus one."""
import inspect
import qualify_bounded_kitana_kiss_voice_packets as previous

def main():
    source=inspect.getsource(previous.voice_gate)
    before="    assert steps[1]['a0']==steps[2]['a0']=='00000002'"
    assert source.count(before)==1
    source=source.replace(before,"    assert steps[1]['a0']=='00000002'\n    random_value=int(steps[2]['a0'],16);assert random_value in (1,2)")
    before="cue=int(steps[3]['a0'],16);assert cue in (base,base+1)"
    assert source.count(before)==1
    source=source.replace(before,"cue=int(steps[3]['a0'],16);assert cue==base+random_value-1")
    source=source.replace('nativeVariantCount=2','nativeVariantCount=2,observedNativeRandomValue=random_value')
    main_source=inspect.getsource(previous.main).replace('audit_bounded_kitana_kiss_voice_packets_checked','audit_bounded_kitana_kiss_voice_choice_checked')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source+'\n'+main_source,__file__+'::exact_native_choice','exec'),namespace)
    namespace['main']()

if __name__=='__main__':main()
