"""Disabled sample ownership appears only at real launch then retires."""
import inspect
import qualify_bounded_voice_hit_pcm_native_control as previous

def main():
    source=inspect.getsource(previous.main)
    before="assert trace.scan(offolder)['active']==set()"
    assert source.count(before)==1
    source=source.replace(before,"assert trace.scan(offolder)['active']=={2592}")
    source=source.replace("'native_control_convergence_check.json'","'disabled_launch_convergence_check.json'")
    source=source.replace('disabledSamplesHaveNoVoiceOwner=True','disabledSamplesOwnerOnlyAtLaunchFrame=2592')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::disabled_launch','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
