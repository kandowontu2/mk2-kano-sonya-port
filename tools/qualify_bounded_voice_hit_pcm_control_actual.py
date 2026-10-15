"""Bind exact observed disabled-owner field2593 to unchanged gameplay."""
import inspect
import qualify_bounded_voice_hit_pcm_convergence as original
from qualify_bounded_voice_hit_pcm_native_control import gameplay

def main():
    source=inspect.getsource(original.main)
    before="assert trace.scan(onfolder)['digest']==trace.scan(offolder)['digest']"
    assert source.count(before)==1
    source=source.replace(before,"assert gameplay(onfolder)==gameplay(offolder)\n    assert trace.scan(offolder)['active']=={2593}")
    source=source.replace("'convergence_check.json'","'actual_control_convergence_check.json'")
    source=source.replace('unchangedActualGameplayAndOwnerTrace=True','unchangedActualPhysicalGameplay=True,disabledOwnerSingleObservedField=2593')
    namespace=dict(original.__dict__);namespace.update(gameplay=gameplay,__file__=__file__)
    exec(compile(source,__file__+'::actual_native_control','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
